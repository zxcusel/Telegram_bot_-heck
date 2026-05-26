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
from keyboards.inline import geo_menu, main_menu, sections_menu, items_menu, geo_menu_for
from utils.logger import log

router = Router()


def _start_kb(user_id: int) -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text="▶️ Начать", callback_data="start:begin")],
        [InlineKeyboardButton(text="⚙️ Настройки", callback_data="start:settings")],
    ]
    if is_admin(user_id):
        buttons.append([InlineKeyboardButton(text="👨‍💼 Админ-панель", callback_data="start:admin")])
    buttons.append([InlineKeyboardButton(text="🗑 Очистить чат", callback_data="start:clear")])
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
    log.clear_chat(call.from_user.id, call.from_user.username)
    try: await call.answer()
    except Exception: pass
    new_msg = await call.bot.send_message(
        chat_id=chat_id, text="👋 Добро пожаловать!",
        reply_markup=_start_kb(call.from_user.id)
    )
    start_id = new_msg.message_id - 1
    # Ограничиваемся 500 сообщениями, чтобы не ловить 429 Too Many Requests от Telegram
    # и не пытаться удалять сообщения старше 48 часов, которые Telegram всё равно не позволит удалить.
    ids = list(range(start_id, max(start_id - 500, 0), -1))
    for i in range(0, len(ids), 100):
        batch = ids[i:i+100]
        try:
            await call.bot.delete_messages(chat_id=chat_id, message_ids=batch)
        except Exception:
            # Если пачка не удалилась целиком (например, из-за слишком старых сообщений),
            # удаляем по одному с микро-паузой
            for m_id in batch:
                try:
                    await call.bot.delete_message(chat_id=chat_id, message_id=m_id)
                except Exception:
                    pass
                await asyncio.sleep(0.01)


# ── Начать → выбор гео ───────────────────────────────────────────────────────

@router.callback_query(F.data == "start:begin")
async def cb_start_begin(call: CallbackQuery, state: FSMContext):
    await state.clear()
    role = get_role(call.from_user.id)
    kb   = geo_menu_for(call.from_user.id, role)
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
    await state.clear()
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
    await state.clear()
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
    await state.clear()
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
        await _safe_edit(call, "🌍 Выберите регион:", geo_menu_for(call.from_user.id, role))

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
        await state.clear()
        if geo:
            role = get_role(call.from_user.id)
            geo_label = GEO_CATALOG[geo]["label"]
            await call.message.answer(
                f"{geo_label}\n📂 Выберите категорию:", reply_markup=main_menu(role, geo)
            )
        else:
            role = get_role(call.from_user.id)
            await call.message.answer(
                "🌍 Выберите регион:", reply_markup=geo_menu_for(call.from_user.id, role)
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
