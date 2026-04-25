"""Навигация по каталогу с геолокацией."""
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramBadRequest
import asyncio

from data.db import get_role, get_geos, is_admin
from data.config import GEO_CATALOG, GEO_LABELS
from handlers.admin import show_admin_panel
from keyboards.inline import geo_menu, main_menu, sections_menu, items_menu
from utils.logger import log

router = Router()


def _start_kb(user_id: int) -> InlineKeyboardMarkup:
    buttons = [[InlineKeyboardButton(text="▶️ Начать", callback_data="start:begin")]]
    if is_admin(user_id):
        buttons.append([InlineKeyboardButton(text="👨‍💼 Админ-панель", callback_data="start:admin")])
    buttons.append([InlineKeyboardButton(text="🗑 Очистить чат", callback_data="start:clear")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def _geo_menu_for(user_id: int, role: str | None) -> InlineKeyboardMarkup:
    """Меню гео — только те регионы к которым у пользователя есть доступ."""
    if is_admin(user_id):
        allowed_geos = list(GEO_CATALOG.keys())
    else:
        allowed_geos = get_geos(user_id)
    buttons = [
        [InlineKeyboardButton(
            text=GEO_CATALOG[gk]["label"],
            callback_data=f"geo:{gk}"
        )]
        for gk in allowed_geos if gk in GEO_CATALOG
    ]
    if not buttons:
        buttons.append([InlineKeyboardButton(text="⛔ Нет доступа к регионам", callback_data="noop")])
    buttons.append([InlineKeyboardButton(text="🔙 Назад", callback_data="back:welcome")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


# ── /start ───────────────────────────────────────────────────────────────────

@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    log.start(message.from_user.id, message.from_user.username)
    await message.answer("👋 Добро пожаловать!", reply_markup=_start_kb(message.from_user.id))


# ── Очистка чата ─────────────────────────────────────────────────────────────

@router.callback_query(F.data == "start:clear")
async def cb_start_clear(call: CallbackQuery, state: FSMContext):
    await state.clear()
    chat_id = call.message.chat.id
    cur_id  = call.message.message_id
    log.clear_chat(call.from_user.id, call.from_user.username)
    try: await call.answer()
    except Exception: pass
    new_msg = await call.bot.send_message(
        chat_id=chat_id, text="👋 Добро пожаловать!",
        reply_markup=_start_kb(call.from_user.id)
    )
    ids = list(range(cur_id, max(cur_id - 10000, 0), -1))
    for i in range(0, len(ids), 100):
        batch = ids[i:i+100]
        try: await call.bot.delete_messages(chat_id=chat_id, message_ids=batch)
        except Exception:
            await asyncio.gather(*[call.bot.delete_message(chat_id, m) for m in batch],
                                 return_exceptions=True)


# ── Начать → выбор гео ───────────────────────────────────────────────────────

@router.callback_query(F.data == "start:begin")
async def cb_start_begin(call: CallbackQuery, state: FSMContext):
    role = get_role(call.from_user.id)
    kb   = _geo_menu_for(call.from_user.id, role)
    await _safe_edit(call, "🌍 Выберите регион:", kb)
    await call.answer()


@router.callback_query(F.data == "start:admin")
async def cb_start_admin(call: CallbackQuery, state: FSMContext):
    if not is_admin(call.from_user.id):
        await call.answer("⛔ Нет доступа", show_alert=True); return
    log.admin_panel(call.from_user.id, call.from_user.username)
    await show_admin_panel(call, state)
    await call.answer()


# ── Выбор гео → меню категорий ───────────────────────────────────────────────

@router.callback_query(F.data.startswith("geo:"))
async def cb_geo(call: CallbackQuery, state: FSMContext):
    geo = call.data.split(":")[1]
    if geo not in GEO_CATALOG:
        await call.answer("⛔ Неизвестный регион", show_alert=True); return
    # Проверяем доступ к гео
    if not is_admin(call.from_user.id) and geo not in get_geos(call.from_user.id):
        await call.answer("⛔ Нет доступа к этому региону", show_alert=True); return

    await state.update_data(current_geo=geo)
    role = get_role(call.from_user.id)
    geo_label = GEO_CATALOG[geo]["label"]
    log.open_category(call.from_user.id, geo, call.from_user.username)
    await _safe_edit(call, f"{geo_label}\n📂 Выберите категорию:", main_menu(role, geo))
    await call.answer()


# ── Выбор категории → разделы ─────────────────────────────────────────────────

@router.callback_query(F.data.startswith("line:"))
async def cb_line(call: CallbackQuery, state: FSMContext):
    parts    = call.data.split(":")   # line:geo:line_key
    geo      = parts[1]
    line_key = parts[2]
    await state.update_data(current_geo=geo, last_line=line_key, last_section=None)
    log.open_section(call.from_user.id, line_key, call.from_user.username)
    await _safe_edit(call, "📂 Выберите раздел:", sections_menu(geo, line_key))
    await call.answer()


# ── Выбор раздела → шаблоны ──────────────────────────────────────────────────

@router.callback_query(F.data.startswith("section:"))
async def cb_section(call: CallbackQuery, state: FSMContext):
    _, geo, line_key, sec_key = call.data.split(":")
    await state.update_data(current_geo=geo, last_line=line_key, last_section=sec_key)
    await _safe_edit(call, "📄 Выберите шаблон:", items_menu(geo, line_key, sec_key))
    await call.answer()


# ── Кнопки Назад ─────────────────────────────────────────────────────────────

@router.callback_query(F.data.startswith("back:"))
async def cb_back(call: CallbackQuery, state: FSMContext):
    parts = call.data.split(":")
    dest  = parts[1]

    if dest == "welcome":
        await _safe_edit(call, "👋 Добро пожаловать!", _start_kb(call.from_user.id))

    elif dest == "geo":
        # Назад к выбору гео
        role = get_role(call.from_user.id)
        await _safe_edit(call, "🌍 Выберите регион:", _geo_menu_for(call.from_user.id, role))

    elif dest == "geo_menu":
        # Назад в меню категорий конкретного гео
        geo  = parts[2]
        role = get_role(call.from_user.id)
        geo_label = GEO_CATALOG[geo]["label"]
        await _safe_edit(call, f"{geo_label}\n📂 Выберите категорию:", main_menu(role, geo))

    elif dest == "geo_section":
        # Назад в разделы
        geo      = parts[2]
        line_key = parts[3]
        await _safe_edit(call, "📂 Выберите раздел:", sections_menu(geo, line_key))

    elif dest == "main":
        # Из рендера — обратно к выбору гео
        data = await state.get_data()
        geo  = data.get("current_geo")
        if geo:
            role = get_role(call.from_user.id)
            geo_label = GEO_CATALOG[geo]["label"]
            await call.message.answer(
                f"{geo_label}\n📂 Выберите категорию:", reply_markup=main_menu(role, geo)
            )
        else:
            role = get_role(call.from_user.id)
            await call.message.answer(
                "🌍 Выберите регион:", reply_markup=_geo_menu_for(call.from_user.id, role)
            )

    await call.answer()


@router.callback_query(F.data == "noop")
async def cb_noop(call: CallbackQuery):
    await call.answer(
        "⛔ В этом разделе пока нет доступных шаблонов или нет доступа к выбранному региону.",
        show_alert=True
    )


# ── Helper ────────────────────────────────────────────────────────────────────

async def _safe_edit(call: CallbackQuery, text: str, kb):
    if call.message.photo:
        await call.message.answer(text, reply_markup=kb)
    else:
        try:
            await call.message.edit_text(text, reply_markup=kb)
        except TelegramBadRequest:
            await call.message.answer(text, reply_markup=kb)
