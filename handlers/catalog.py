"""Навигация по каталогу с геолокацией. Дизайн обновлён."""
from aiogram import Router, F
from aiogram.enums import ParseMode
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramBadRequest
import asyncio

from data.db import get_role_string, get_geos, is_admin
from data.config import GEO_CATALOG, GEO_LABELS
from handlers.admin import show_admin_panel
from keyboards.inline import geo_menu, main_menu, sections_menu, items_menu, geo_menu_for
from utils.logger import log

router = Router()

# ── Дизайн-токены ──────────────────────────────────────────────────────────────
PM = ParseMode.HTML
DIV = "━━━━━━━━━━━━━━━━━━━━"
BULLET = "▫️"
WELCOME_TITLE = "🤖 <b>BCKPS F-BOT</b>"
WELCOME_TAG = "Генератор чеков · Расписание · Автоматизация"


def _start_kb(user_id: int) -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text="▶️ Начать", callback_data="start:begin")],
        [InlineKeyboardButton(text="🤖 Автоматизация", callback_data="auto:open")],
        # [InlineKeyboardButton(text="🎲 Массовая генерация", callback_data="start:bulk_gen")],
        [InlineKeyboardButton(text="⚙️ Настройки", callback_data="start:settings")],
    ]
    if is_admin(user_id):
        buttons.append([InlineKeyboardButton(text="👨‍💼 Админ-панель", callback_data="start:admin")])
    buttons.append([InlineKeyboardButton(text="🗑 Очистить чат", callback_data="start:clear")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def _welcome_text() -> str:
    return (
        f"{WELCOME_TITLE}\n"
        f"{DIV}\n"
        f"👋 <b>Добро пожаловать!</b>\n"
        f"<i>{WELCOME_TAG}</i>\n\n"
        f"{BULLET} <b>Начать</b> — выбрать гео и сгенерировать чек\n"
        f"{BULLET} <b>Автоматизация</b> — запуск по расписанию\n"
        f"{BULLET} <b>Настройки</b> — параметры генерации\n"
        f"{DIV}\n"
        f"<i>Выберите действие:</i>"
    )




# ── /start ───────────────────────────────────────────────────────────────────

@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    log.start(message.from_user.id, message.from_user.username)
    await message.answer(_welcome_text(), reply_markup=_start_kb(message.from_user.id), parse_mode=PM)


# ── Очистка чата ─────────────────────────────────────────────────────────────

@router.callback_query(F.data == "start:clear")
async def cb_start_clear(call: CallbackQuery, state: FSMContext):
    await state.clear()
    chat_id = call.message.chat.id
    log.clear_chat(call.from_user.id, call.from_user.username)
    try: await call.answer()
    except Exception: pass
    new_msg = await call.bot.send_message(
        chat_id=chat_id, text=_welcome_text(),
        reply_markup=_start_kb(call.from_user.id),
        parse_mode=PM,
    )
    start_id = new_msg.message_id - 1
    # Чистим весь чат: идём от самого нового сообщения к самому старому.
    # Лимит Telegram — удаление сообщений старше 48 часов ботом запрещено,
    # поэтому по одной штуке с паузой и глушим исключения.
    if start_id < 1:
        ids: list[int] = []
    else:
        ids = list(range(start_id, 0, -1))
    # Чтобы не словить flood limit от Telegram, удаляем по 100 штук
    # через delete_messages (одна операция), с микропаузой между батчами.
    for i in range(0, len(ids), 100):
        batch = ids[i:i + 100]
        try:
            await call.bot.delete_messages(chat_id=chat_id, message_ids=batch)
        except Exception:
            # Если пачка целиком не удаляется (например, из-за старых сообщений),
            # пробуем по одному — те, что старше 48 часов, просто пропускаются.
            for m_id in batch:
                try:
                    await call.bot.delete_message(chat_id=chat_id, message_id=m_id)
                except Exception:
                    pass
                await asyncio.sleep(0.04)
        await asyncio.sleep(0.05)


# ── Начать → выбор гео ───────────────────────────────────────────────────────

@router.callback_query(F.data == "start:begin")
async def cb_start_begin(call: CallbackQuery, state: FSMContext):
    try: await call.answer()
    except Exception: pass
    await state.clear()
    role = get_role_string(call.from_user.id)
    kb   = geo_menu_for(call.from_user.id, role)
    await _safe_edit(
        call,
        f"🌍 <b>Выбор региона</b>\n"
        f"{DIV}\n"
        f"{BULLET} Выберите <b>гео</b>, под которым будут создаваться чеки:",
        kb,
    )


@router.callback_query(F.data == "start:admin")
async def cb_start_admin(call: CallbackQuery, state: FSMContext):
    if not is_admin(call.from_user.id):
        await call.answer("⛔ Нет доступа", show_alert=True); return
    try: await call.answer()
    except Exception: pass
    log.admin_panel(call.from_user.id, call.from_user.username)
    await show_admin_panel(call, state)


# ── Выбор гео → меню категорий ───────────────────────────────────────────────

@router.callback_query(F.data.startswith("geo:"))
async def cb_geo(call: CallbackQuery, state: FSMContext):
    geo = call.data.split(":")[1]
    if geo not in GEO_CATALOG:
        await call.answer("⛔ Неизвестный регион", show_alert=True); return
    # Проверяем доступ к гео
    if not is_admin(call.from_user.id) and geo not in get_geos(call.from_user.id):
        await call.answer("⛔ Нет доступа к этому региону", show_alert=True); return

    try: await call.answer()
    except Exception: pass
    await state.clear()
    await state.update_data(current_geo=geo)
    role = get_role_string(call.from_user.id)
    geo_label = GEO_CATALOG[geo]["label"]
    log.open_category(call.from_user.id, geo, call.from_user.username)
    await _safe_edit(
        call,
        f"📍 <b>{geo_label}</b>\n"
        f"{DIV}\n"
        f"📂 <b>Выберите категорию:</b>",
        main_menu(role, geo),
    )


# ── Выбор категории → разделы ─────────────────────────────────────────────────

@router.callback_query(F.data.startswith("line:"))
async def cb_line(call: CallbackQuery, state: FSMContext):
    try: await call.answer()
    except Exception: pass
    await state.clear()
    parts    = call.data.split(":")   # line:geo:line_key
    geo      = parts[1]
    line_key = parts[2]
    await state.update_data(current_geo=geo, last_line=line_key, last_section=None)
    log.open_section(call.from_user.id, line_key, call.from_user.username)
    await _safe_edit(
        call,
        f"📂 <b>Выберите раздел:</b>\n"
        f"{DIV}\n"
        f"<i>В каждом разделе — набор шаблонов.</i>",
        sections_menu(geo, line_key),
    )


# ── Выбор раздела → шаблоны ──────────────────────────────────────────────────

@router.callback_query(F.data.startswith("section:"))
async def cb_section(call: CallbackQuery, state: FSMContext):
    try: await call.answer()
    except Exception: pass
    await state.clear()
    _, geo, line_key, sec_key = call.data.split(":")
    await state.update_data(current_geo=geo, last_line=line_key, last_section=sec_key)
    await _safe_edit(
        call,
        f"📄 <b>Выберите шаблон:</b>\n"
        f"{DIV}\n"
        f"<i>Нажмите на нужный шаблон для генерации чека.</i>",
        items_menu(geo, line_key, sec_key),
    )


# ── Кнопки Назад ─────────────────────────────────────────────────────────────

@router.callback_query(F.data.startswith("back:"))
async def cb_back(call: CallbackQuery, state: FSMContext):
    try: await call.answer()
    except Exception: pass
    parts = call.data.split(":")
    dest  = parts[1]

    if dest == "welcome":
        await _safe_edit(call, _welcome_text(), _start_kb(call.from_user.id))

    elif dest == "geo":
        # Назад к выбору гео
        role = get_role_string(call.from_user.id)
        await _safe_edit(
            call,
            f"🌍 <b>Выбор региона</b>\n{DIV}\n{BULLET} Выберите <b>гео</b>:",
            geo_menu_for(call.from_user.id, role),
        )

    elif dest == "geo_menu":
        # Назад в меню категорий конкретного гео
        geo  = parts[2]
        role = get_role_string(call.from_user.id)
        geo_label = GEO_CATALOG[geo]["label"]
        await _safe_edit(
            call,
            f"📍 <b>{geo_label}</b>\n{DIV}\n📂 <b>Выберите категорию:</b>",
            main_menu(role, geo),
        )

    elif dest == "geo_section":
        # Назад в разделы
        geo      = parts[2]
        line_key = parts[3]
        await _safe_edit(
            call,
            f"📂 <b>Выберите раздел:</b>\n{DIV}\n<i>В каждом разделе — набор шаблонов.</i>",
            sections_menu(geo, line_key),
        )

    elif dest == "main":
        # Из рендера — обратно к выбору гео
        data = await state.get_data()
        geo  = data.get("current_geo")
        await state.clear()
        if geo:
            role = get_role_string(call.from_user.id)
            geo_label = GEO_CATALOG[geo]["label"]
            await call.message.answer(
                f"📍 <b>{geo_label}</b>\n{DIV}\n📂 <b>Выберите категорию:</b>",
                reply_markup=main_menu(role, geo),
                parse_mode=PM,
            )
        else:
            role = get_role_string(call.from_user.id)
            await call.message.answer(
                f"🌍 <b>Выбор региона</b>\n{DIV}\n{BULLET} Выберите <b>гео</b>:",
                reply_markup=geo_menu_for(call.from_user.id, role),
                parse_mode=PM,
            )


@router.callback_query(F.data == "noop")
async def cb_noop(call: CallbackQuery):
    await call.answer(
        "⛔ В этом разделе пока нет доступных шаблонов или нет доступа к выбранному региону.",
        show_alert=True
    )


# ── Helper ────────────────────────────────────────────────────────────────────

async def _safe_edit(call: CallbackQuery, text: str, kb):
    if call.message.photo:
        await call.message.answer(text, reply_markup=kb, parse_mode=PM)
    else:
        try:
            await call.message.edit_text(text, reply_markup=kb, parse_mode=PM)
        except TelegramBadRequest:
            await call.message.answer(text, reply_markup=kb, parse_mode=PM)
