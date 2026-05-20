"""Админ-панель."""
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.exceptions import TelegramBadRequest

from utils.logger import log
from data.db import (
    is_admin, add_admin, remove_admin, add_role, remove_role, clear_roles,
    get_roles, get_geos, add_geo, remove_geo, clear_geos,
    get_all_admins, get_all_users_all, get_username, upsert_user,
)

router = Router()


class AdminStates(StatesGroup):
    wait_target_id = State()
    managing_roles = State()
    wait_new_admin = State()
    wait_broadcast_text_all = State()
    wait_broadcast_id_indiv = State()
    wait_broadcast_text_indiv = State()


# ── keyboards ─────────────────────────────────────────────────────────────────

def _admin_main_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎭 Выдать роль пользователю", callback_data="admin:set_role")],
        [InlineKeyboardButton(text="📋 Список пользователей",      callback_data="admin:user_list")],
        [InlineKeyboardButton(text="📢 Отправить сообщение",      callback_data="admin:broadcast_menu")],
        [InlineKeyboardButton(text="🔙 Назад",                     callback_data="admin:exit")],
    ])

def _broadcast_menu_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📢 Всем пользователям", callback_data="admin:broadcast_all")],
        [InlineKeyboardButton(text="👤 Индивидуально (по ID)", callback_data="admin:broadcast_indiv")],
        [InlineKeyboardButton(text="🔙 Назад", callback_data="admin:back_main")]
    ])


# Карта гео-кодов → отображаемые названия
_GEO_LABELS: dict[str, str] = {
    "bo": "🇧🇴 Bolivia",
    "pe": "🇵🇪 Peru",
    "uy": "🇺🇾 Uruguay",
    "py": "🇵🇾 Paraguay",
}


def _roles_kb(target_id: int, roles: list[str]) -> InlineKeyboardMarkup:
    fd_icon  = "✅" if "fd" in roles else "🚫"
    rd_icon  = "✅" if "rd" in roles else "🚫"
    cr_icon  = "✅" if "cr" in roles else "🚫"
    ow_icon  = "👑" if is_admin(target_id) else "🚫"
    ow_label = f"{ow_icon} Администратор"
    ow_cb    = f"admin:demote:{target_id}" if is_admin(target_id) else f"admin:promote:{target_id}"
    geos     = get_geos(target_id)
    bo_icon  = "✅" if "bo" in geos else "🚫"
    pe_icon  = "✅" if "pe" in geos else "🚫"
    uy_icon  = "✅" if "uy" in geos else "🚫"
    py_icon  = "✅" if "py" in geos else "🚫"
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=f"{fd_icon} FD",            callback_data=f"admin:toggle:fd:{target_id}")],
        [InlineKeyboardButton(text=f"{rd_icon} RD",            callback_data=f"admin:toggle:rd:{target_id}")],
        [InlineKeyboardButton(text=f"{cr_icon} Контентщик",    callback_data=f"admin:toggle:cr:{target_id}")],
        [InlineKeyboardButton(text=f"{bo_icon} 🇧🇴 Bolivia",  callback_data=f"admin:geo:bo:{target_id}")],
        [InlineKeyboardButton(text=f"{pe_icon} 🇵🇪 Peru",     callback_data=f"admin:geo:pe:{target_id}")],
        [InlineKeyboardButton(text=f"{uy_icon} 🇺🇾 Uruguay",  callback_data=f"admin:geo:uy:{target_id}")],
        [InlineKeyboardButton(text=f"{py_icon} 🇵🇾 Paraguay", callback_data=f"admin:geo:py:{target_id}")],
        [InlineKeyboardButton(text=ow_label,                    callback_data=ow_cb)],
        [InlineKeyboardButton(text="🗑 Очистить всё",          callback_data=f"admin:clear:{target_id}")],
        [InlineKeyboardButton(text="🔙 Назад",                 callback_data="admin:back_main")],
    ])


def _back_to_main_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔙 Назад", callback_data="admin:back_main")]
    ])


# ── helpers ───────────────────────────────────────────────────────────────────

def _roles_text(roles: list[str]) -> str:
    return ", ".join(r.upper() for r in roles) if roles else "нет"


def _role_info_text(target_id: int, roles: list[str], extra: str = "") -> str:
    uname    = get_username(target_id) or "none"
    ow_str   = "👑 Администратор" if is_admin(target_id) else "🚫 Не администратор"
    geos     = get_geos(target_id)
    geo_str  = ", ".join(_GEO_LABELS.get(g, g.upper()) for g in geos) or "нет"
    text     = (
        f"👤 <code>{target_id} - @{uname}</code>\n"
        f"Роли: <b>{_roles_text(roles)}</b>  |  {ow_str}\n"
        f"Регионы: <b>{geo_str}</b>\n"
    )
    if extra:
        text += f"✅ {extra}\n"
    text += "\nНажмите чтобы изменить:"
    return text


async def _safe_edit(msg: Message, text: str, kb=None):
    try:
        await msg.edit_text(text, parse_mode="HTML", reply_markup=kb)
    except TelegramBadRequest:
        await msg.answer(text, parse_mode="HTML", reply_markup=kb)


async def _try_delete(msg: Message):
    try:
        await msg.delete()
    except TelegramBadRequest:
        pass


async def _fetch_and_save(bot, user_id: int) -> str | None:
    try:
        chat = await bot.get_chat(user_id)
        upsert_user(user_id, chat.username, chat.first_name)
        return chat.username
    except Exception:
        return get_username(user_id)


async def _admin_list_lines(bot) -> str:
    lines = []
    for uid in get_all_admins():
        uname = await _fetch_and_save(bot, uid)
        lines.append(f"👑 {uid} - @{uname}" if uname else f"👑 {uid} - @none")
    return "\n".join(lines) if lines else "Список пуст"


# ── entry point ───────────────────────────────────────────────────────────────

async def show_admin_panel(event, state: FSMContext):
    await state.clear()
    text = "👨‍💼 <b>Админ-панель</b>\n\nВыберите действие:"
    kb   = _admin_main_kb()
    if isinstance(event, Message):
        await event.answer(text, parse_mode="HTML", reply_markup=kb)
    else:
        await _safe_edit(event.message, text, kb)


# ── navigation ────────────────────────────────────────────────────────────────

@router.callback_query(F.data == "admin:back_main")
async def cb_back_main(call: CallbackQuery, state: FSMContext):
    if not is_admin(call.from_user.id):
        await call.answer("⛔ Нет доступа", show_alert=True); return
    await state.clear()
    await _safe_edit(call.message, "👨‍💼 <b>Админ-панель</b>\n\nВыберите действие:", _admin_main_kb())
    await call.answer()


@router.callback_query(F.data == "admin:exit")
async def cb_exit(call: CallbackQuery, state: FSMContext):
    await state.clear()
    from handlers.catalog import _start_kb
    await _safe_edit(call.message, "👋 Добро пожаловать!", _start_kb(call.from_user.id))
    await call.answer()


# ── выдача ролей ──────────────────────────────────────────────────────────────

@router.callback_query(F.data == "admin:set_role")
async def cb_set_role_start(call: CallbackQuery, state: FSMContext):
    if not is_admin(call.from_user.id):
        await call.answer("⛔ Нет доступа", show_alert=True); return
    await _safe_edit(call.message, "🆔 Введите Telegram ID пользователя:", _back_to_main_kb())
    await state.set_state(AdminStates.wait_target_id)
    await state.update_data(prompt_msg_id=call.message.message_id)
    await call.answer()


@router.message(AdminStates.wait_target_id)
async def process_target_id(message: Message, state: FSMContext):
    if not is_admin(message.from_user.id): return
    data = await state.get_data()
    prompt_msg_id = data.get("prompt_msg_id")
    await _try_delete(message)

    if not message.text or not message.text.strip().lstrip("-").isdigit():
        try:
            await message.bot.edit_message_text(
                chat_id=message.chat.id, message_id=prompt_msg_id,
                text="❌ Некорректный ID. Введите числовой Telegram ID:",
                reply_markup=_back_to_main_kb()
            )
        except TelegramBadRequest:
            pass
        return

    target_id = int(message.text.strip())
    await _fetch_and_save(message.bot, target_id)
    roles = get_roles(target_id)

    try:
        await message.bot.edit_message_text(
            chat_id=message.chat.id, message_id=prompt_msg_id,
            text=_role_info_text(target_id, roles),
            parse_mode="HTML",
            reply_markup=_roles_kb(target_id, roles)
        )
    except TelegramBadRequest:
        await message.answer(_role_info_text(target_id, roles), parse_mode="HTML",
                             reply_markup=_roles_kb(target_id, roles))
    await state.set_state(AdminStates.managing_roles)
    await state.update_data(target_id=target_id)


@router.callback_query(F.data.startswith("admin:toggle:"))
async def cb_toggle_role(call: CallbackQuery, state: FSMContext):
    if not is_admin(call.from_user.id):
        await call.answer("⛔ Нет доступа", show_alert=True); return
    parts     = call.data.split(":")
    role      = parts[2]
    target_id = int(parts[3])
    roles = get_roles(target_id)
    if role in roles:
        remove_role(target_id, role)
        action = f"убрана <b>{role.upper()}</b>"
        log.role_changed(call.from_user.id, target_id, role, "remove", call.from_user.username)
    else:
        add_role(target_id, role)
        action = f"выдана <b>{role.upper()}</b>"
        log.role_changed(call.from_user.id, target_id, role, "add", call.from_user.username)
    roles = get_roles(target_id)
    await _safe_edit(call.message, _role_info_text(target_id, roles, action), _roles_kb(target_id, roles))
    await call.answer()


@router.callback_query(F.data.startswith("admin:geo:"))
async def cb_toggle_geo(call: CallbackQuery, state: FSMContext):
    if not is_admin(call.from_user.id):
        await call.answer("⛔ Нет доступа", show_alert=True); return
    parts     = call.data.split(":")   # admin:geo:bo:12345
    geo       = parts[2]
    target_id = int(parts[3])
    geos = get_geos(target_id)
    geo_label = _GEO_LABELS.get(geo, geo.upper())
    if geo in geos:
        remove_geo(target_id, geo)
        action = f"регион {geo_label} убран 🚫"
    else:
        add_geo(target_id, geo)
        action = f"регион {geo_label} выдан ✅"
    roles = get_roles(target_id)
    await _safe_edit(call.message, _role_info_text(target_id, roles, action),
                     _roles_kb(target_id, roles))
    await call.answer()


@router.callback_query(F.data.startswith("admin:clear:"))
async def cb_clear_roles(call: CallbackQuery, state: FSMContext):
    if not is_admin(call.from_user.id):
        await call.answer("⛔ Нет доступа", show_alert=True); return
    target_id = int(call.data.split(":")[2])
    clear_roles(target_id)
    clear_geos(target_id)
    log.roles_cleared(call.from_user.id, target_id, call.from_user.username)
    roles = get_roles(target_id)
    await _safe_edit(call.message, _role_info_text(target_id, roles, "роли и регионы очищены 🗑"),
                     _roles_kb(target_id, roles))
    await call.answer()


@router.callback_query(F.data.startswith("admin:demote:"))
async def cb_demote_admin(call: CallbackQuery, state: FSMContext):
    if not is_admin(call.from_user.id):
        await call.answer("⛔ Нет доступа", show_alert=True); return
    target_id = int(call.data.split(":")[2])
    if target_id == call.from_user.id:
        await call.answer("⛔ Нельзя снять себя.", show_alert=True); return
    remove_admin(target_id)
    log.admin_demoted(call.from_user.id, target_id, call.from_user.username)
    roles = get_roles(target_id)
    await _safe_edit(call.message, _role_info_text(target_id, roles, "администратор снят 🚫"),
                     _roles_kb(target_id, roles))
    await call.answer()


@router.callback_query(F.data.startswith("admin:promote:"))
async def cb_promote_admin(call: CallbackQuery, state: FSMContext):
    if not is_admin(call.from_user.id):
        await call.answer("⛔ Нет доступа", show_alert=True); return
    target_id = int(call.data.split(":")[2])
    await _fetch_and_save(call.bot, target_id)
    add_admin(target_id)
    log.admin_promoted(call.from_user.id, target_id, call.from_user.username)
    roles = get_roles(target_id)
    await _safe_edit(call.message, _role_info_text(target_id, roles, "назначен администратором 👑"),
                     _roles_kb(target_id, roles))
    await call.answer()


# ── список пользователей ──────────────────────────────────────────────────────

@router.callback_query(F.data == "admin:user_list")
async def cb_user_list(call: CallbackQuery, state: FSMContext):
    if not is_admin(call.from_user.id):
        await call.answer("⛔ Нет доступа", show_alert=True); return

    users = get_all_users_all()
    if not users:
        text = "📋 <b>Список пользователей</b>\n\nПользователей нет."
    else:
        lines = []
        for uid in users:
            # Подтягиваем актуальный username через Telegram API
            uname = await _fetch_and_save(call.bot, uid) or "none"
            roles  = get_roles(uid)
            fd_str = "FD✅" if "fd" in roles else "FD🚫"
            rd_str = "RD✅" if "rd" in roles else "RD🚫"
            cr_str = "CR✅" if "cr" in roles else "CR🚫"
            icon   = "👑" if is_admin(uid) else "👤"
            geos   = get_geos(uid)
            bo_str = "BO✅" if "bo" in geos else "BO🚫"
            pe_str = "PE✅" if "pe" in geos else "PE🚫"
            uy_str = "UY✅" if "uy" in geos else "UY🚫"
            py_str = "PY✅" if "py" in geos else "PY🚫"
            lines.append(f"{icon} {uid} - @{uname} : {fd_str}, {rd_str}, {cr_str} | {bo_str}, {pe_str}, {uy_str}, {py_str}")
        text = "📋 <b>Список пользователей</b>\n\n" + "\n".join(lines)

    await _safe_edit(call.message, text, _back_to_main_kb())
    await call.answer()


# ── Рассылка сообщений ────────────────────────────────────────────────────────

@router.callback_query(F.data == "admin:broadcast_menu")
async def cb_broadcast_menu(call: CallbackQuery, state: FSMContext):
    if not is_admin(call.from_user.id): return
    await _safe_edit(call.message, "📢 Выберите тип рассылки:", _broadcast_menu_kb())
    await call.answer()

@router.callback_query(F.data == "admin:broadcast_all")
async def cb_broadcast_all(call: CallbackQuery, state: FSMContext):
    if not is_admin(call.from_user.id): return
    await _safe_edit(call.message, "⌨️ Введите сообщение для рассылки ВСЕМ пользователям:\n\n(или нажмите Назад)", _back_to_main_kb())
    await state.set_state(AdminStates.wait_broadcast_text_all)
    await state.update_data(prompt_msg_id=call.message.message_id)
    await call.answer()

@router.message(AdminStates.wait_broadcast_text_all)
async def process_broadcast_all(message: Message, state: FSMContext):
    if not is_admin(message.from_user.id): return
    data = await state.get_data()
    await _try_delete(message)
    users = get_all_users_all()
    success = 0
    for uid in users:
        try:
            await message.bot.send_message(uid, message.text, parse_mode=None)
            success += 1
        except Exception:
            pass
    log.broadcast(message.from_user.id, message.text, f"all, sent: {success}", message.from_user.username)
    text = f"✅ Сообщение отправлено {success} пользователям.\n\n👨‍💼 <b>Админ-панель</b>"
    
    try:
        await message.bot.edit_message_text(chat_id=message.chat.id, message_id=data.get("prompt_msg_id"), text=text, parse_mode="HTML", reply_markup=_admin_main_kb())
    except Exception:
        await message.answer(text, parse_mode="HTML", reply_markup=_admin_main_kb())
    await state.clear()


async def _build_users_kb(bot, users: list[int], page: int = 0) -> InlineKeyboardMarkup:
    start_idx = page * 10
    end_idx = start_idx + 10
    page_users = users[start_idx:end_idx]
    
    buttons = []
    for uid in page_users:
        uname = await _fetch_and_save(bot, uid) or "none"
        buttons.append([InlineKeyboardButton(text=f"👤 {uid} - @{uname}", callback_data=f"admin:bc_to:{uid}")])
        
    nav_row = []
    if page > 0:
        nav_row.append(InlineKeyboardButton(text="◀️", callback_data=f"admin:bc_page:{page-1}"))
    if end_idx < len(users):
        nav_row.append(InlineKeyboardButton(text="▶️", callback_data=f"admin:bc_page:{page+1}"))
        
    if nav_row:
        buttons.append(nav_row)
        
    buttons.append([InlineKeyboardButton(text="🔙 Назад", callback_data="admin:broadcast_menu")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)

@router.callback_query(F.data == "admin:broadcast_indiv")
async def cb_broadcast_indiv(call: CallbackQuery, state: FSMContext):
    if not is_admin(call.from_user.id): return
    users = get_all_users_all()
    if not users:
        await call.answer("Нет пользователей", show_alert=True)
        return
    kb = await _build_users_kb(call.bot, users, page=0)
    await _safe_edit(call.message, "👤 Выберите пользователя для отправки сообщения:", kb)
    await call.answer()

@router.callback_query(F.data.startswith("admin:bc_page:"))
async def cb_broadcast_indiv_page(call: CallbackQuery, state: FSMContext):
    if not is_admin(call.from_user.id): return
    page = int(call.data.split(":")[2])
    users = get_all_users_all()
    kb = await _build_users_kb(call.bot, users, page)
    await _safe_edit(call.message, "👤 Выберите пользователя для отправки сообщения:", kb)
    await call.answer()

@router.callback_query(F.data.startswith("admin:bc_to:"))
async def cb_broadcast_indiv_target(call: CallbackQuery, state: FSMContext):
    if not is_admin(call.from_user.id): return
    target_id = int(call.data.split(":")[2])
    await state.update_data(target_id=target_id, prompt_msg_id=call.message.message_id)
    
    uname = await _fetch_and_save(call.bot, target_id) or "none"
    await _safe_edit(call.message, f"⌨️ Введите сообщение для пользователя {target_id} (@{uname}):", _back_to_main_kb())
    await state.set_state(AdminStates.wait_broadcast_text_indiv)
    await call.answer()


@router.message(AdminStates.wait_broadcast_text_indiv)
async def process_broadcast_text_indiv(message: Message, state: FSMContext):
    if not is_admin(message.from_user.id): return
    data = await state.get_data()
    await _try_delete(message)
    target_id = data.get("target_id")
    try:
        await message.bot.send_message(target_id, message.text, parse_mode=None)
        text = f"✅ Сообщение отправлено пользователю {target_id}.\n\n👨‍💼 <b>Админ-панель</b>"
        log.broadcast(message.from_user.id, message.text, f"indiv: {target_id}", message.from_user.username)
    except Exception as e:
        text = f"❌ Ошибка отправки пользователю {target_id}: {e}\n\n👨‍💼 <b>Админ-панель</b>"
        
    try:
        await message.bot.edit_message_text(chat_id=message.chat.id, message_id=data.get("prompt_msg_id"), text=text, parse_mode="HTML", reply_markup=_admin_main_kb())
    except Exception:
        await message.answer(text, parse_mode="HTML", reply_markup=_admin_main_kb())
    await state.clear()
