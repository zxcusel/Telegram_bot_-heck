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
from handlers.clock import ensure_pinned

router = Router()

# ── Дизайн-токены ──────────────────────────────────────────────────────────────
PM = ParseMode.HTML
DIV = "━━━━━━━━━━━━━━━━━━━━"
BULLET = "▫️"
WELCOME_TITLE = "🤖 <b>FIRE-BOT</b>"
WELCOME_TAG = "Генератор чеков · Расписание · Автоматизация"


def _start_kb(user_id: int) -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text="▶️ Начать", callback_data="start:begin")],
        [InlineKeyboardButton(text="🤖 Автоматизация", callback_data="auto:open")],
        # [InlineKeyboardButton(text="🎲 Массовая генерация", callback_data="start:bulk_gen")],
        [InlineKeyboardButton(text="⚙️ Настройки", callback_data="start:settings")],
        [InlineKeyboardButton(text="📖 Инструкция", callback_data="ins:main")],
    ]
    if is_admin(user_id):
        buttons.append([InlineKeyboardButton(text="👨‍💼 Админ-панель", callback_data="start:admin")])
    else:
        # Тикеты — только для пользователей (админы управляют через админ-панель)
        buttons.insert(2, [InlineKeyboardButton(text="🎫 Поддержка", callback_data="tkt:menu")])
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
        f"{BULLET} <b>Поддержка</b> — обратиться в поддержку\n"
        f"{BULLET} <b>Настройки</b> — параметры генерации\n"
        f"{BULLET} <b>Инструкция</b> — описание всех разделов бота\n"
        f"{DIV}\n"
        f"<i>Выберите действие:</i>"
    )




# ── /start ───────────────────────────────────────────────────────────────────

async def _try_delete(bot, chat_id: int, message_id: int) -> None:
    """Delete a single message silently. Telegram may refuse (e.g. >48h,
    или у бота нет права на удаление в этом чате) — это нормально."""
    if not message_id:
        return
    for attempt in range(3):
        try:
            await bot.delete_message(chat_id=chat_id, message_id=message_id)
            return
        except Exception:
            await asyncio.sleep(0.2 * (attempt + 1))


async def _wipe_chat_up_to(bot, chat_id: int, up_to_id: int) -> None:
    """Удаляет сообщения в диапазоне [1..up_to_id] батчами по 100 через
    deleteMessages. Telegram возвращает частичный успех, если в батче есть
    сообщения старше 48ч или без права на удаление — невалидные просто
    игнорируются, остальные удаляются. Так очистка 300+ сообщений
    происходит почти мгновенно, без визуального 'удаляет по одному'."""
    if up_to_id < 1:
        return
    BATCH = 100
    start = 1
    while start <= up_to_id:
        end = min(start + BATCH - 1, up_to_id)
        ids = list(range(start, end + 1))
        try:
            await bot.delete_messages(chat_id=chat_id, message_ids=ids)
        except Exception:
            for mid in ids:
                try:
                    await bot.delete_message(chat_id=chat_id, message_id=mid)
                except Exception:
                    pass
                await asyncio.sleep(0.04)
        await asyncio.sleep(0.25)
        start = end + 1


async def _bg_wipe(bot, chat_id: int, up_to_id: int) -> None:
    """Запускает очистку в фоне. Welcome уже отправлен — пользователь
    не ждёт. Любая ошибка глохнет, чтобы фоновая задача не упала."""
    try:
        await _wipe_chat_up_to(bot, chat_id, up_to_id)
    except Exception:
        pass


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    log.start(message.from_user.id, message.from_user.username)
    chat_id = message.chat.id
    bot = message.bot
    user_id = message.from_user.id
    cmd_mid = message.message_id
    # Сразу удаляем команду /start и показываем welcome —
    # пользователь мгновенно видит главное меню.
    await _try_delete(bot, chat_id, cmd_mid)
    await bot.send_message(
        chat_id=chat_id,
        text=_welcome_text(),
        reply_markup=_start_kb(user_id),
        parse_mode=PM,
    )
    # Закреплённое сообщение с часами (Москва / Боливия / Парагвай).
    # Если оно уже есть — обновится; если нет — отправится и запинится.
    asyncio.create_task(ensure_pinned(bot, chat_id))
    # Остальную историю чистим в фоне, чтобы не висеть на длинном
    # цикле удаления (особенно если в чате много сообщений).
    # Диапазон ниже cmd_mid безопасен — /start был последним входящим.
    asyncio.create_task(_bg_wipe(bot, chat_id, cmd_mid - 1))


# ── Очистка чата ─────────────────────────────────────────────────────────────

@router.callback_query(F.data == "start:clear")
async def cb_start_clear(call: CallbackQuery, state: FSMContext):
    await state.clear()
    chat_id = call.message.chat.id
    log.clear_chat(call.from_user.id, call.from_user.username)
    try: await call.answer()
    except Exception: pass
    top_id = call.message.message_id - 1
    # Удаляем само сообщение с кнопкой "Очистить чат" и сразу
    # показываем welcome, дальше — фон.
    await _try_delete(call.bot, chat_id, call.message.message_id)
    await call.bot.send_message(
        chat_id=chat_id,
        text=_welcome_text(),
        reply_markup=_start_kb(call.from_user.id),
        parse_mode=PM,
    )
    # Закреплённое сообщение с часами.
    asyncio.create_task(ensure_pinned(call.bot, chat_id))
    asyncio.create_task(_bg_wipe(call.bot, chat_id, top_id))


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
