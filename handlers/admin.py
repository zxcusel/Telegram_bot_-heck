"""Админ-панель."""
from aiogram import Router
from aiogram import F
from aiogram.enums import ParseMode
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.exceptions import TelegramBadRequest

from utils.logger import log
from data.db import (
    is_admin, add_admin, remove_admin, add_role, remove_role, clear_roles,
    get_roles, get_geos, add_geo, remove_geo, clear_geos,
    get_all_admins, get_all_users_all, get_username, upsert_user,
    is_banned, ban_user, unban_user, get_banned_users,
    _conn,
)

router = Router()

# ── Дизайн-токены ──────────────────────────────────────────────────────────────
PM = ParseMode.HTML
DIV = "━━━━━━━━━━━━━━━━━━━━"
BULLET = "▫️"

USERS_PER_PAGE = 8

ROLE_LABELS: dict[str, str] = {
    "fd": "FD",
    "rd": "RD",
    "cr": "Контентщик",
}
GEO_LABELS: dict[str, str] = {
    "bo": "🇧🇴 Bolivia",
    "pe": "🇵🇪 Peru",
    "uy": "🇺🇾 Uruguay",
    "py": "🇵🇾 Paraguay",
    "ma": "🇲🇦 Morocco",
}


class AdminStates(StatesGroup):
    wait_target_id = State()
    managing_roles = State()
    wait_new_admin = State()
    wait_broadcast_text_all = State()
    wait_broadcast_id_indiv = State()
    wait_broadcast_text_indiv = State()
    wait_broadcast_text_picked = State()


# ── keyboards ─────────────────────────────────────────────────────────────────

def _admin_main_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="👥 Управление ролями", callback_data="admin:manage_users:0")],
        [InlineKeyboardButton(text="🎭 Выдать роль по ID", callback_data="admin:set_role")],
        [InlineKeyboardButton(text="🎫 Тикеты",            callback_data="tkt:admin_menu")],
        [InlineKeyboardButton(text="🚫 Забанить",          callback_data="admin:ban_menu")],
        [InlineKeyboardButton(text="⛔️ ЧС",                  callback_data="admin:blacklist_menu")],
        [InlineKeyboardButton(text="📢 Отправить сообщение", callback_data="admin:broadcast_menu")],
        [InlineKeyboardButton(text="🔙 Назад",              callback_data="admin:exit")],
    ])


def _broadcast_menu_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📢 Всем пользователям", callback_data="admin:broadcast_all")],
        [InlineKeyboardButton(text="👤 Индивидуально (по ID)", callback_data="admin:broadcast_indiv")],
        [InlineKeyboardButton(text="📋 Выбрать из списка", callback_data="admin:broadcast_pick:0")],
        [InlineKeyboardButton(text="🔙 Назад", callback_data="admin:back_main")]
    ])



# ── broadcast: pick users from list ──────────────────────────────────────────
# Per-admin in-memory storage: {admin_id: set[user_id]}.
# Чистится при «🗑 Сбросить выбор» и после отправки.
_BC_PICK: dict[int, set[int]] = {}


def _bc_pick_get(admin_id: int) -> set[int]:
    s = _BC_PICK.get(admin_id)
    if s is None:
        s = set()
        _BC_PICK[admin_id] = s
    return s


def _bc_pick_all_users() -> list[int]:
    # Все пользователи из БД, кроме забаненных.
    return [u for u in get_all_users_all() if not is_banned(u)]


def _build_broadcast_pick_kb(users: list[int], page: int, selected: set[int]) -> InlineKeyboardMarkup:
    total = len(users)
    total_pages = max(1, (total + USERS_PER_PAGE - 1) // USERS_PER_PAGE)
    page = max(0, min(page, total_pages - 1))
    start = page * USERS_PER_PAGE
    chunk = users[start:start + USERS_PER_PAGE]

    rows: list[list[InlineKeyboardButton]] = []
    for uid in chunk:
        mark = "✅" if uid in selected else "⬜️"
        label = f"{mark} {uid} · {_short_name(uid)}"[:64]
        rows.append([InlineKeyboardButton(text=label, callback_data=f"admin:bcast_toggle:{uid}:{page}")])

    nav: list[InlineKeyboardButton] = []
    if page > 0:
        nav.append(InlineKeyboardButton(text="◀", callback_data=f"admin:broadcast_pick:{page - 1}"))
    nav.append(InlineKeyboardButton(text=f"{page + 1}/{total_pages}", callback_data="noop"))
    if page < total_pages - 1:
        nav.append(InlineKeyboardButton(text="▶", callback_data=f"admin:broadcast_pick:{page + 1}"))
    rows.append(nav)

    rows.append([
        InlineKeyboardButton(text="☑ Все на стр.", callback_data=f"admin:bcast_page_all:{page}"),
        InlineKeyboardButton(text="☐ Снять всех",   callback_data=f"admin:bcast_page_none:{page}"),
    ])
    rows.append([
        InlineKeyboardButton(text=f"🚀 Отправить ({len(selected)})", callback_data="admin:bcast_done"),
        InlineKeyboardButton(text="🗑 Сбросить выбор",                callback_data="admin:bcast_reset"),
    ])
    rows.append([InlineKeyboardButton(text="🔙 Назад", callback_data="admin:broadcast_menu")])
    return InlineKeyboardMarkup(inline_keyboard=rows)
def _back_to_main_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔙 Назад", callback_data="admin:back_main")]
    ])


def _user_card_kb(target_id: int) -> InlineKeyboardMarkup:
    roles = get_roles(target_id)
    geos = get_geos(target_id)
    admin_flag = is_admin(target_id)
    banned = is_banned(target_id)

    def icon(on: bool) -> str:
        return "✅" if on else "🚫"

    ow_label = "👑 Снять админа" if admin_flag else "👑 Выдать админа"
    ow_cb = f"admin:demote:{target_id}" if admin_flag else f"admin:promote:{target_id}"

    ban_label = "✅ Разбанить" if banned else "🚫 Забанить"
    ban_cb = f"admin:toggle_ban:{target_id}:{0 if banned else 1}"

    rows = [
        [
            InlineKeyboardButton(text=f"{icon('fd' in roles)} FD",          callback_data=f"admin:toggle:fd:{target_id}"),
            InlineKeyboardButton(text=f"{icon('rd' in roles)} RD",          callback_data=f"admin:toggle:rd:{target_id}"),
            InlineKeyboardButton(text=f"{icon('cr' in roles)} Контентщик",  callback_data=f"admin:toggle:cr:{target_id}"),
        ],
        [
            InlineKeyboardButton(text=f"{icon('bo' in geos)} 🇧🇴 BO",  callback_data=f"admin:geo:bo:{target_id}"),
            InlineKeyboardButton(text=f"{icon('pe' in geos)} 🇵🇪 PE",  callback_data=f"admin:geo:pe:{target_id}"),
            InlineKeyboardButton(text=f"{icon('uy' in geos)} 🇺🇾 UY",  callback_data=f"admin:geo:uy:{target_id}"),
        ],
        [
            InlineKeyboardButton(text=f"{icon('py' in geos)} 🇵🇾 PY",  callback_data=f"admin:geo:py:{target_id}"),
            InlineKeyboardButton(text=f"{icon('ma' in geos)} 🇲🇦 MA",  callback_data=f"admin:geo:ma:{target_id}"),
            InlineKeyboardButton(text="🗑 Сброс прав",                  callback_data=f"admin:clear:{target_id}"),
        ],
        [InlineKeyboardButton(text=ow_label, callback_data=ow_cb)],
        [InlineKeyboardButton(text=ban_label, callback_data=ban_cb)],
        [InlineKeyboardButton(text="🔙 К списку", callback_data="admin:manage_users:0")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=rows)


# ── helpers ───────────────────────────────────────────────────────────────────

def _first_name(uid: int) -> str | None:
    with _conn() as con:
        row = con.execute("SELECT first_name FROM users WHERE user_id = ?", (uid,)).fetchone()
    return row["first_name"] if row else None


def _short_name(uid: int) -> str:
    name = _first_name(uid) or ""
    uname = get_username(uid) or ""
    if name and uname:
        return f"{name} (@{uname})"
    if name:
        return name
    if uname:
        return f"@{uname}"
    return f"id{uid}"


def _user_row_icons(uid: int) -> str:
    parts = []
    if is_admin(uid):
        parts.append("👑")
    roles = get_roles(uid)
    if "fd" in roles:
        parts.append("FD")
    if "rd" in roles:
        parts.append("RD")
    if "cr" in roles:
        parts.append("CR")
    if get_geos(uid):
        parts.append(f"{len(get_geos(uid))}🗺")
    if is_banned(uid):
        parts.append("⛔️")
    return " ".join(parts) if parts else "—"


def _user_card_text(uid: int) -> str:
    name = _first_name(uid) or "—"
    uname = get_username(uid) or "—"
    roles = get_roles(uid)
    geos = get_geos(uid)
    admin_flag = is_admin(uid)
    banned = is_banned(uid)

    roles_str = ", ".join(ROLE_LABELS[r] for r in roles) if roles else "нет"
    geos_str = ", ".join(GEO_LABELS[g] for g in geos) if geos else "нет"
    ow_str = "👑 Админ" if admin_flag else "обычный"
    ban_str = "⛔️ Забанен" if banned else "✅ Активен"

    return (
        f"👤 <b>{name}</b>\n"
        f"🆔 <code>{uid}</code>  ·  @{uname}\n"
        f"{DIV}\n"
        f"Статус: {ban_str}\n"
        f"Доступ: {ow_str}\n"
        f"Роли: <b>{roles_str}</b>\n"
        f"Регионы: <b>{geos_str}</b>\n"
        f"{DIV}\n"
        f"Нажмите кнопку, чтобы изменить:"
    )


def _edit_or_answer(call: CallbackQuery, text: str, kb: InlineKeyboardMarkup):
    try:
        return call.message.edit_text(text, parse_mode=PM, reply_markup=kb)
    except TelegramBadRequest:
        return call.message.answer(text, parse_mode=PM, reply_markup=kb)


def _build_users_kb(users: list[int], page: int) -> InlineKeyboardMarkup:
    total = len(users)
    total_pages = max(1, (total + USERS_PER_PAGE - 1) // USERS_PER_PAGE)
    page = max(0, min(page, total_pages - 1))
    start = page * USERS_PER_PAGE
    chunk = users[start:start + USERS_PER_PAGE]

    rows: list[list[InlineKeyboardButton]] = []
    for uid in chunk:
        icon = _user_row_icons(uid)
        label = f"{uid} · {icon}\n{_short_name(uid)}"[:64]
        rows.append([InlineKeyboardButton(text=label, callback_data=f"admin:user_card:{uid}")])

    nav: list[InlineKeyboardButton] = []
    if page > 0:
        nav.append(InlineKeyboardButton(text="◀️", callback_data=f"admin:manage_users:{page - 1}"))
    nav.append(InlineKeyboardButton(text=f"{page + 1}/{total_pages}", callback_data="noop"))
    if page < total_pages - 1:
        nav.append(InlineKeyboardButton(text="▶️", callback_data=f"admin:manage_users:{page + 1}"))
    rows.append(nav)
    rows.append([InlineKeyboardButton(text="🔙 Назад", callback_data="admin:back_main")])
    return InlineKeyboardMarkup(inline_keyboard=rows)


# ── admin entry ───────────────────────────────────────────────────────────────

async def admin_entry(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer(
        f"⚙️ <b>Админ-панель</b>\n{DIV}\nВыберите действие:",
        parse_mode=PM,
        reply_markup=_admin_main_kb(),
    )


# Алиас для совместимости с handlers/catalog.py (start:admin -> show_admin_panel)
async def show_admin_panel(call: CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    text = f"�️ <b>Админ-панель</b>\n{DIV}\nВыберите действие:"
    try:
        await call.message.edit_text(text, parse_mode=PM, reply_markup=_admin_main_kb())
    except TelegramBadRequest:
        await call.message.answer(text, parse_mode=PM, reply_markup=_admin_main_kb())
    try:
        await call.answer()
    except Exception:
        pass


# ── manage users (paginated list → user card) ─────────────────────────────────

async def cb_manage_users(call: CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    page = 0
    try:
        page = int(call.data.split(":")[-1])
    except (ValueError, IndexError):
        page = 0

    users = [u for u in get_all_users_all() if not is_banned(u)]
    if not users:
        return await _edit_or_answer(
            call,
            "👥 <b>Управление ролями</b>\n\nПока нет пользователей.",
            _back_to_main_kb(),
        )

    total = len(users)
    total_pages = max(1, (total + USERS_PER_PAGE - 1) // USERS_PER_PAGE)
    page = max(0, min(page, total_pages - 1))
    start = page * USERS_PER_PAGE
    end = start + USERS_PER_PAGE

    text = (
        f"👥 <b>Управление ролями</b>\n"
        f"{DIV}\n"
        f"Всего: <b>{total}</b>  ·  страница <b>{page + 1}/{total_pages}</b>\n"
        f"Показываю: <b>{start + 1}–{min(end, total)}</b>\n"
        f"{DIV}\n"
        f"👑 — админ   FD/RD/CR — роли   N🗺 — кол-во регионов   ⛔️ — бан\n"
        f"Выберите пользователя:"
    )
    await _edit_or_answer(call, text, _build_users_kb(users, page))


async def cb_user_card(call: CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    try:
        uid = int(call.data.split(":")[-1])
    except (ValueError, IndexError):
        return await call.answer("❌ Ошибка ID", show_alert=True)

    text = _user_card_text(uid)
    await _edit_or_answer(call, text, _user_card_kb(uid))


# ── existing set_role FSM (kept) ──────────────────────────────────────────────

async def cb_set_role_start(call: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(AdminStates.wait_target_id)
    await _edit_or_answer(
        call,
        "🎭 <b>Выдать роль по ID</b>\n\nВведите <code>user_id</code> пользователя:",
        InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🔙 Назад", callback_data="admin:back_main")]
        ]),
    )


async def process_target_id(message: Message, state: FSMContext) -> None:
    raw = (message.text or "").strip()
    if not raw.isdigit():
        await message.answer("❌ ID должен быть числом. Введите ещё раз:")
        return
    uid = int(raw)
    await state.clear()
    await message.answer(
        _user_card_text(uid),
        parse_mode=PM,
        reply_markup=_user_card_kb(uid),
    )


# ── role toggles (reused for both FSM and card) ──────────────────────────────

async def cb_toggle_role(call: CallbackQuery) -> None:
    parts = call.data.split(":")
    # admin:toggle:{role}:{id}
    if len(parts) < 4:
        return await call.answer("❌ Ошибка")
    role = parts[2]
    try:
        uid = int(parts[3])
    except ValueError:
        return await call.answer("❌ Ошибка ID")

    if role not in ("fd", "rd", "cr"):
        return await call.answer("❌ Неизвестная роль")

    roles = get_roles(uid)
    if role in roles:
        remove_role(uid, role)
        await call.answer(f"➖ {ROLE_LABELS[role]} снята")
    else:
        add_role(uid, role)
        await call.answer(f"➕ {ROLE_LABELS[role]} выдана")

    await cb_user_card(call, None)  # type: ignore[arg-type]


async def cb_toggle_geo(call: CallbackQuery) -> None:
    parts = call.data.split(":")
    # admin:geo:{code}:{id}
    if len(parts) < 4:
        return await call.answer("❌ Ошибка")
    geo = parts[2]
    try:
        uid = int(parts[3])
    except ValueError:
        return await call.answer("❌ Ошибка ID")

    if geo not in GEO_LABELS:
        return await call.answer("❌ Неизвестный регион")

    geos = get_geos(uid)
    if geo in geos:
        remove_geo(uid, geo)
        await call.answer(f"➖ {GEO_LABELS[geo]} снят")
    else:
        add_geo(uid, geo)
        await call.answer(f"➕ {GEO_LABELS[geo]} добавлен")

    await cb_user_card(call, None)  # type: ignore[arg-type]


async def cb_clear_roles(call: CallbackQuery) -> None:
    try:
        uid = int(call.data.split(":")[-1])
    except (ValueError, IndexError):
        return await call.answer("❌ Ошибка ID")

    clear_roles(uid)
    clear_geos(uid)
    await call.answer("🗑 Все права и регионы сброшены")
    await cb_user_card(call, None)  # type: ignore[arg-type]


async def cb_promote_admin(call: CallbackQuery) -> None:
    try:
        uid = int(call.data.split(":")[-1])
    except (ValueError, IndexError):
        return await call.answer("❌ Ошибка ID")
    add_admin(uid)
    await call.answer("👑 Админ выдан")
    await cb_user_card(call, None)  # type: ignore[arg-type]


async def cb_demote_admin(call: CallbackQuery) -> None:
    try:
        uid = int(call.data.split(":")[-1])
    except (ValueError, IndexError):
        return await call.answer("❌ Ошибка ID")
    remove_admin(uid)
    await call.answer("👑 Админ снят")
    await cb_user_card(call, None)  # type: ignore[arg-type]


# ── ban / blacklist menus (kept, but also reflect in card) ───────────────────

async def cb_toggle_ban(call: CallbackQuery) -> None:
    parts = call.data.split(":")
    # admin:toggle_ban:{id}:{0|1}
    if len(parts) < 4:
        return await call.answer("❌ Ошибка")
    try:
        uid = int(parts[2])
        flag = int(parts[3])
    except ValueError:
        return await call.answer("❌ Ошибка ID")
    if flag == 1:
        ban_user(uid)
        await call.answer("🚫 Забанен")
    else:
        unban_user(uid)
        await call.answer("✅ Разбанен")
    await cb_user_card(call, None)  # type: ignore[arg-type]


async def cb_ban_menu(call: CallbackQuery) -> None:
    users = [u for u in get_all_users_all() if not is_banned(u)]
    if not users:
        await _edit_or_answer(
            call,
            "🚫 <b>Забанить</b>\n\nНет доступных пользователей.",
            _back_to_main_kb(),
        )
        return
    rows: list[list[InlineKeyboardButton]] = []
    for uid in users:
        rows.append([
            InlineKeyboardButton(
                text=f"{uid} · {_short_name(uid)} · 🚫",
                callback_data=f"admin:toggle_ban:{uid}:1",
            )
        ])
    rows.append([InlineKeyboardButton(text="🔙 Назад", callback_data="admin:back_main")])
    await _edit_or_answer(
        call,
        "🚫 <b>Забанить</b>\n\nВыберите пользователя:",
        InlineKeyboardMarkup(inline_keyboard=rows),
    )


async def cb_blacklist_menu(call: CallbackQuery) -> None:
    banned = get_banned_users()
    if not banned:
        await _edit_or_answer(
            call,
            "⛔️ <b>Чёрный список</b>\n\nПусто.",
            _back_to_main_kb(),
        )
        return
    rows: list[list[InlineKeyboardButton]] = []
    for uid in banned:
        rows.append([
            InlineKeyboardButton(
                text=f"{uid} · {_short_name(uid)} · ✅ разбанить",
                callback_data=f"admin:toggle_ban:{uid}:0",
            )
        ])
    rows.append([InlineKeyboardButton(text="🔙 Назад", callback_data="admin:back_main")])
    await _edit_or_answer(
        call,
        "⛔️ <b>Чёрный список</b>\n\nВыберите пользователя для разбана:",
        InlineKeyboardMarkup(inline_keyboard=rows),
    )


# ── broadcast menu (kept) ─────────────────────────────────────────────────────

async def cb_broadcast_menu(call: CallbackQuery) -> None:
    await _edit_or_answer(
        call,
        "📢 <b>Рассылка</b>\n\nВыберите режим:",
        _broadcast_menu_kb(),
    )


async def cb_broadcast_all(call: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(AdminStates.wait_broadcast_text_all)
    await _edit_or_answer(
        call,
        "📢 Введите текст для рассылки всем пользователям:",
        InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🔙 Отмена", callback_data="admin:broadcast_menu")]
        ]),
    )


async def cb_broadcast_indiv(call: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(AdminStates.wait_broadcast_id_indiv)
    await _edit_or_answer(
        call,
        "👤 Введите <code>user_id</code> получателя:",
        InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🔙 Отмена", callback_data="admin:broadcast_menu")]
        ]),
    )


async def process_broadcast_text_all(message: Message, state: FSMContext) -> None:
    text = message.text or ""
    users = get_all_users_all()
    sent = 0
    for uid in users:
        try:
            await message.bot.send_message(uid, text)
            sent += 1
        except Exception:
            continue
    await state.clear()
    await message.answer(
        f"📢 Рассылка завершена.\nДоставлено: <b>{sent}/{len(users)}</b>",
        reply_markup=_admin_main_kb(),
    )


async def process_broadcast_id_indiv(message: Message, state: FSMContext) -> None:
    raw = (message.text or "").strip()
    if not raw.isdigit():
        await message.answer("❌ ID должен быть числом.")
        return
    uid = int(raw)
    await state.update_data(target_id=uid)
    await state.set_state(AdminStates.wait_broadcast_text_indiv)
    await message.answer(
        f"👤 Получатель: <code>{uid}</code>\nВведите текст сообщения:",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🔙 Отмена", callback_data="admin:broadcast_menu")]
        ]),
    )


async def process_broadcast_text_indiv(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    uid = data.get("target_id")
    text = message.text or ""
    if not uid:
        await state.clear()
        return await message.answer("❌ Ошибка состояния.")
    try:
        await message.bot.send_message(int(uid), text)
        await message.answer(f"✅ Отправлено <code>{uid}</code>")
    except Exception as e:
        await message.answer(f"❌ Не удалось: <code>{e}</code>")
    await state.clear()
    await message.answer("📢 Готово", reply_markup=_admin_main_kb())


# ── broadcast: pick users from list ───────────────────────────────────────────

async def cb_broadcast_pick(call: CallbackQuery, state: FSMContext) -> None:
    """Показывает первую страницу списка пользователей с чекбоксами."""
    aid = call.from_user.id
    _BC_PICK.pop(aid, None)  # сбрасываем предыдущий выбор при входе
    users = _bc_pick_all_users()
    await _edit_or_answer(
        call,
        f"📋 <b>Выбор пользователей для рассылки</b>\n{DIV}\nНажмите на пользователя, чтобы добавить/убрать из выборки. Нажмите 🚀 для отправки.\n\nВсего доступно: <b>{len(users)}</b>",
        _build_broadcast_pick_kb(users, 0, _bc_pick_get(aid)),
    )


async def cb_broadcast_pick_page(call: CallbackQuery, state: FSMContext) -> None:
    """Переключение страницы."""
    aid = call.from_user.id
    page = int((call.data or "").split(":")[-1] or 0)
    users = _bc_pick_all_users()
    await _edit_or_answer(
        call,
        f"📋 <b>Выбор пользователей для рассылки</b>\n{DIV}\nНажмите на пользователя, чтобы добавить/убрать из выборки. Нажмите 🚀 для отправки.\n\nВсего доступно: <b>{len(users)}</b>",
        _build_broadcast_pick_kb(users, page, _bc_pick_get(aid)),
    )


async def cb_bcast_toggle(call: CallbackQuery, state: FSMContext) -> None:
    """Тоггл одного пользователя. data = 'admin:bcast_toggle:UID:PAGE'."""
    aid = call.from_user.id
    parts = (call.data or "").split(":")
    try:
        uid = int(parts[2]); page = int(parts[3])
    except (IndexError, ValueError):
        return await call.answer("⚠️ Ошибка данных", show_alert=True)
    sel = _bc_pick_get(aid)
    if uid in sel:
        sel.discard(uid)
    else:
        sel.add(uid)
    users = _bc_pick_all_users()
    await _edit_or_answer(
        call,
        f"📋 <b>Выбор пользователей для рассылки</b>\n{DIV}\nНажмите на пользователя, чтобы добавить/убрать из выборки. Нажмите 🚀 для отправки.\n\nВсего доступно: <b>{len(users)}</b>",
        _build_broadcast_pick_kb(users, page, sel),
    )


async def cb_bcast_page_all(call: CallbackQuery, state: FSMContext) -> None:
    """Выбрать всех пользователей на текущей странице."""
    aid = call.from_user.id
    page = int((call.data or "").split(":")[-1] or 0)
    users = _bc_pick_all_users()
    start = page * USERS_PER_PAGE
    chunk = users[start:start + USERS_PER_PAGE]
    sel = _bc_pick_get(aid)
    sel.update(chunk)
    await _edit_or_answer(
        call,
        f"📋 <b>Выбор пользователей для рассылки</b>\n{DIV}\nНажмите на пользователя, чтобы добавить/убрать из выборки. Нажмите 🚀 для отправки.\n\nВсего доступно: <b>{len(users)}</b>",
        _build_broadcast_pick_kb(users, page, sel),
    )


async def cb_bcast_page_none(call: CallbackQuery, state: FSMContext) -> None:
    """Снять выбор со всех пользователей на текущей странице."""
    aid = call.from_user.id
    page = int((call.data or "").split(":")[-1] or 0)
    users = _bc_pick_all_users()
    start = page * USERS_PER_PAGE
    chunk = users[start:start + USERS_PER_PAGE]
    sel = _bc_pick_get(aid)
    sel.difference_update(chunk)
    await _edit_or_answer(
        call,
        f"📋 <b>Выбор пользователей для рассылки</b>\n{DIV}\nНажмите на пользователя, чтобы добавить/убрать из выборки. Нажмите 🚀 для отправки.\n\nВсего доступно: <b>{len(users)}</b>",
        _build_broadcast_pick_kb(users, page, sel),
    )


async def cb_bcast_reset(call: CallbackQuery, state: FSMContext) -> None:
    """Сбросить весь выбор админа."""
    aid = call.from_user.id
    _BC_PICK.pop(aid, None)
    users = _bc_pick_all_users()
    await _edit_or_answer(
        call,
        f"📋 <b>Выбор пользователей для рассылки</b>\n{DIV}\nНажмите на пользователя, чтобы добавить/убрать из выборки. Нажмите 🚀 для отправки.\n\nВсего доступно: <b>{len(users)}</b>",
        _build_broadcast_pick_kb(users, 0, _bc_pick_get(aid)),
    )


async def cb_bcast_done(call: CallbackQuery, state: FSMContext) -> None:
    """Готово: переход в состояние ожидания текста рассылки."""
    aid = call.from_user.id
    sel = _bc_pick_get(aid)
    if not sel:
        return await call.answer("⚠️ Никто не выбран", show_alert=True)
    await state.set_state(AdminStates.wait_broadcast_text_picked)
    await _edit_or_answer(
        call,
        f"📋 Выбрано: <b>{len(sel)}</b> пользователей.\n\nВведите текст для рассылки:",
        InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🔙 Назад к выбору", callback_data="admin:broadcast_pick:0")]
        ]),
    )


async def process_broadcast_text_picked(message: Message, state: FSMContext) -> None:
    """Отправляет сообщение всем выбранным пользователям."""
    aid = message.from_user.id if message.from_user else None
    sel = _BC_PICK.pop(aid, None) if aid is not None else None
    text = message.text or ""
    if not sel:
        await state.clear()
        return await message.answer("❌ Никто не выбран.")
    targets = list(sel)
    sent = 0
    failed = 0
    for uid in targets:
        try:
            await message.bot.send_message(uid, text)
            sent += 1
        except Exception:
            failed += 1
    await state.clear()
    await message.answer(
        f"📢 Рассылка завершена.\nДоставлено: <b>{sent}/{len(targets)}</b>" + (f"\nНе доставлено: <b>{failed}</b>" if failed else ""),
        reply_markup=_admin_main_kb(),
    )


# ── back / exit ───────────────────────────────────────────────────────────────

async def cb_back_main(call: CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    await _edit_or_answer(
        call,
        f"⚙️ <b>Админ-панель</b>\n{DIV}\nВыберите действие:",
        _admin_main_kb(),
    )


async def cb_admin_exit(call: CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    try:
        await call.message.delete()
    except TelegramBadRequest:
        pass


# ── router registration ──────────────────────────────────────────────────────

# Регистрация обработчиков (декораторы, т.к. register() из main.py не вызывается)

@router.message(F.text == "⚙️ Настройки")
async def _entry_admin(message: Message, state: FSMContext) -> None:
    await admin_entry(message, state)

@router.callback_query(F.data.startswith("admin:manage_users:"))
async def _cb_manage_users(call: CallbackQuery, state: FSMContext) -> None:
    await cb_manage_users(call, state)

@router.callback_query(F.data.startswith("admin:user_card:"))
async def _cb_user_card(call: CallbackQuery, state: FSMContext) -> None:
    await cb_user_card(call, state)

@router.callback_query(F.data == "admin:set_role")
async def _cb_set_role_start(call: CallbackQuery, state: FSMContext) -> None:
    await cb_set_role_start(call, state)

@router.message(AdminStates.wait_target_id)
async def _process_target_id(message: Message, state: FSMContext) -> None:
    await process_target_id(message, state)

@router.callback_query(F.data.startswith("admin:toggle:"))
async def _cb_toggle_role(call: CallbackQuery) -> None:
    await cb_toggle_role(call)

@router.callback_query(F.data.startswith("admin:geo:"))
async def _cb_toggle_geo(call: CallbackQuery) -> None:
    await cb_toggle_geo(call)

@router.callback_query(F.data.startswith("admin:clear:"))
async def _cb_clear_roles(call: CallbackQuery) -> None:
    await cb_clear_roles(call)

@router.callback_query(F.data.startswith("admin:demote:"))
async def _cb_demote_admin(call: CallbackQuery) -> None:
    await cb_demote_admin(call)

@router.callback_query(F.data.startswith("admin:promote:"))
async def _cb_promote_admin(call: CallbackQuery) -> None:
    await cb_promote_admin(call)

@router.callback_query(F.data.startswith("admin:toggle_ban:"))
async def _cb_toggle_ban(call: CallbackQuery) -> None:
    await cb_toggle_ban(call)

@router.callback_query(F.data == "admin:ban_menu")
async def _cb_ban_menu(call: CallbackQuery) -> None:
    await cb_ban_menu(call)

@router.callback_query(F.data == "admin:blacklist_menu")
async def _cb_blacklist_menu(call: CallbackQuery) -> None:
    await cb_blacklist_menu(call)

@router.callback_query(F.data == "admin:broadcast_menu")
async def _cb_broadcast_menu(call: CallbackQuery) -> None:
    await cb_broadcast_menu(call)

@router.callback_query(F.data == "admin:broadcast_all")
async def _cb_broadcast_all(call: CallbackQuery, state: FSMContext) -> None:
    await cb_broadcast_all(call, state)

@router.callback_query(F.data == "admin:broadcast_indiv")
async def _cb_broadcast_indiv(call: CallbackQuery, state: FSMContext) -> None:
    await cb_broadcast_indiv(call, state)

@router.message(AdminStates.wait_broadcast_text_all)
async def _process_broadcast_text_all(message: Message, state: FSMContext) -> None:
    await process_broadcast_text_all(message, state)

@router.message(AdminStates.wait_broadcast_id_indiv)
async def _process_broadcast_id_indiv(message: Message, state: FSMContext) -> None:
    await process_broadcast_id_indiv(message, state)

@router.message(AdminStates.wait_broadcast_text_indiv)
async def _process_broadcast_text_indiv(message: Message, state: FSMContext) -> None:
    await process_broadcast_text_indiv(message, state)


@router.callback_query(F.data == "admin:broadcast_pick")
async def _cb_broadcast_pick(call: CallbackQuery, state: FSMContext) -> None:
    await cb_broadcast_pick(call, state)


@router.callback_query(F.data.startswith("admin:broadcast_pick:"))
async def _cb_broadcast_pick_page(call: CallbackQuery, state: FSMContext) -> None:
    await cb_broadcast_pick_page(call, state)


@router.callback_query(F.data.startswith("admin:bcast_toggle:"))
async def _cb_bcast_toggle(call: CallbackQuery, state: FSMContext) -> None:
    await cb_bcast_toggle(call, state)


@router.callback_query(F.data.startswith("admin:bcast_page_all:"))
async def _cb_bcast_page_all(call: CallbackQuery, state: FSMContext) -> None:
    await cb_bcast_page_all(call, state)


@router.callback_query(F.data.startswith("admin:bcast_page_none:"))
async def _cb_bcast_page_none(call: CallbackQuery, state: FSMContext) -> None:
    await cb_bcast_page_none(call, state)


@router.callback_query(F.data == "admin:bcast_done")
async def _cb_bcast_done(call: CallbackQuery, state: FSMContext) -> None:
    await cb_bcast_done(call, state)


@router.callback_query(F.data == "admin:bcast_reset")
async def _cb_bcast_reset(call: CallbackQuery, state: FSMContext) -> None:
    await cb_bcast_reset(call, state)


@router.message(AdminStates.wait_broadcast_text_picked)
async def _process_broadcast_text_picked(message: Message, state: FSMContext) -> None:
    await process_broadcast_text_picked(message, state)

@router.callback_query(F.data == "admin:back_main")
async def _cb_back_main(call: CallbackQuery, state: FSMContext) -> None:
    await cb_back_main(call, state)

@router.callback_query(F.data == "admin:exit")
async def _cb_admin_exit(call: CallbackQuery, state: FSMContext) -> None:
    await cb_admin_exit(call, state)
