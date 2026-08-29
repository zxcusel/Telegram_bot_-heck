"""Тикеты (поддержка) — общий модуль для пользователей и админов.

Пользователь:
  • /start → 🎫 Поддержка → создать новое обращение или открыть существующее
  • FSM: ввод темы → ввод текста → подтверждение
  • В существующем тикете можно дописывать сообщения (чат)

Админ:
  • Админ-панель → 🎫 Тикеты → список открытых тикетов
  • Просмотр треда, ответ, закрытие
  • Уведомления всем админам при новом тикете и при новом сообщении в тикете

БД:
  • tickets(id, user_id, subject, status, created_at, updated_at)
  • ticket_messages(id, ticket_id, author_id, author_role, text, created_at)
"""
from __future__ import annotations

import asyncio
from aiogram import Router, F
from aiogram.enums import ParseMode
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.exceptions import TelegramBadRequest

from data.db import (
    _conn, get_all_admins, is_admin,
)
from utils.logger import log

router = Router()

PM = ParseMode.HTML
DIV = "━━━━━━━━━━━━━━━━━━━━"
BULLET = "▫️"

TICKETS_PER_PAGE = 10
NOTIFY_BATCH = 25  # как часто даём паузу при рассылке админам


# ── FSM ──────────────────────────────────────────────────────────────────────
class TicketStates(StatesGroup):
    choosing_action = State()    # главное меню тикетов (юзер)
    entering_subject = State()   # ввод темы нового тикета
    entering_body = State()      # ввод первого сообщения
    viewing = State()            # просмотр треда (можно дописать)
    replying = State()          # дописывание сообщения в существующий тикет (юзер)
    admin_viewing = State()     # админ просматривает тикет
    admin_replying = State()    # админ пишет ответ в тикет
    admin_viewing = State()      # админ смотрит тред


# ── DB helpers ──────────────────────────────────────────────────────────────
def _ensure_tickets_tables() -> None:
    with _conn() as con:
        con.execute("""
            CREATE TABLE IF NOT EXISTS tickets (
                id         INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id    INTEGER NOT NULL,
                subject    TEXT    NOT NULL,
                status     TEXT    NOT NULL DEFAULT 'open'
                          CHECK(status IN ('open','closed')),
                created_at TEXT    DEFAULT (datetime('now')),
                updated_at TEXT    DEFAULT (datetime('now'))
            )
        """)
        con.execute("""
            CREATE TABLE IF NOT EXISTS ticket_messages (
                id           INTEGER PRIMARY KEY AUTOINCREMENT,
                ticket_id    INTEGER NOT NULL,
                author_id    INTEGER NOT NULL,
                author_role  TEXT    NOT NULL CHECK(author_role IN ('user','admin')),
                text         TEXT    NOT NULL,
                created_at   TEXT    DEFAULT (datetime('now'))
            )
        """)
        con.execute(
            "CREATE INDEX IF NOT EXISTS idx_tickets_user ON tickets(user_id, status, updated_at DESC)"
        )
        con.execute(
            "CREATE INDEX IF NOT EXISTS idx_tm_ticket ON ticket_messages(ticket_id, created_at)"
        )


def create_ticket(user_id: int, subject: str, body: str) -> int:
    _ensure_tickets_tables()
    with _conn() as con:
        cur = con.execute(
            "INSERT INTO tickets (user_id, subject) VALUES (?, ?)",
            (user_id, subject.strip()[:200]),
        )
        tid = cur.lastrowid
        con.execute(
            "INSERT INTO ticket_messages (ticket_id, author_id, author_role, text) VALUES (?, ?, 'user', ?)",
            (tid, user_id, body.strip()[:4000]),
        )
    return tid


def add_message(ticket_id: int, author_id: int, role: str, text: str) -> None:
    _ensure_tickets_tables()
    with _conn() as con:
        con.execute(
            "INSERT INTO ticket_messages (ticket_id, author_id, author_role, text) VALUES (?, ?, ?, ?)",
            (ticket_id, author_id, role, text.strip()[:4000]),
        )
        con.execute(
            "UPDATE tickets SET updated_at = datetime('now') WHERE id = ?", (ticket_id,)
        )


def list_user_tickets(user_id: int, status: str | None = None) -> list:
    _ensure_tickets_tables()
    with _conn() as con:
        if status:
            return con.execute(
                "SELECT * FROM tickets WHERE user_id = ? AND status = ? "
                "ORDER BY updated_at DESC LIMIT 50",
                (user_id, status),
            ).fetchall()
        return con.execute(
            "SELECT * FROM tickets WHERE user_id = ? ORDER BY updated_at DESC LIMIT 50",
            (user_id,),
        ).fetchall()


def list_open_tickets() -> list:
    _ensure_tickets_tables()
    with _conn() as con:
        return con.execute(
            "SELECT * FROM tickets WHERE status='open' ORDER BY updated_at DESC LIMIT 200"
        ).fetchall()


def list_recent_tickets(limit: int = 50) -> list:
    _ensure_tickets_tables()
    with _conn() as con:
        return con.execute(
            "SELECT * FROM tickets ORDER BY updated_at DESC LIMIT ?", (limit,)
        ).fetchall()


def get_ticket(tid: int) -> dict | None:
    _ensure_tickets_tables()
    with _conn() as con:
        row = con.execute("SELECT * FROM tickets WHERE id = ?", (tid,)).fetchone()
        if not row:
            return None
        t = dict(row)
        t["messages"] = [
            dict(r) for r in con.execute(
                "SELECT * FROM ticket_messages WHERE ticket_id = ? ORDER BY created_at ASC",
                (tid,),
            ).fetchall()
        ]
        return t


def close_ticket(tid: int) -> None:
    _ensure_tickets_tables()
    with _conn() as con:
        con.execute(
            "UPDATE tickets SET status='closed', updated_at=datetime('now') WHERE id = ?",
            (tid,),
        )


def reopen_ticket(tid: int) -> None:
    _ensure_tickets_tables()
    with _conn() as con:
        con.execute(
            "UPDATE tickets SET status='open', updated_at=datetime('now') WHERE id = ?",
            (tid,),
        )


def get_username(uid: int) -> str | None:
    with _conn() as con:
        row = con.execute(
            "SELECT username, first_name FROM users WHERE user_id = ?", (uid,)
        ).fetchone()
        if not row:
            return None
        return row["username"] or row["first_name"]


def _user_label(uid: int) -> str:
    name = get_username(uid) or str(uid)
    return f"@{name}" if name and not name.startswith("@") else name


# ── keyboards ───────────────────────────────────────────────────────────────
def user_tickets_main_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✏️ Новое обращение", callback_data="tkt:new")],
        [InlineKeyboardButton(text="📂 Мои тикеты",      callback_data="tkt:my:0")],
        [InlineKeyboardButton(text="🔙 Назад",            callback_data="back:welcome")],
    ])


def user_tickets_list_kb(rows: list, page: int = 0) -> InlineKeyboardMarkup:
    buttons = []
    for r in rows:
        icon = "🟢" if r["status"] == "open" else "⚫"
        title = (r["subject"] or "(без темы)").strip()
        if len(title) > 36:
            title = title[:35] + "…"
        buttons.append([
            InlineKeyboardButton(
                text=f"{icon} #{r['id']} · {title}",
                callback_data=f"tkt:view:{r['id']}",
            )
        ])
    buttons.append([InlineKeyboardButton(text="🔙 Назад", callback_data="tkt:menu")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def admin_tickets_list_kb(rows: list, page: int = 0) -> InlineKeyboardMarkup:
    buttons = []
    for r in rows:
        icon = "🟢" if r["status"] == "open" else "⚫"
        title = (r["subject"] or "(без темы)").strip()
        if len(title) > 32:
            title = title[:31] + "…"
        who = _user_label(r["user_id"])
        buttons.append([
            InlineKeyboardButton(
                text=f"{icon} #{r['id']} · {who} · {title}",
                callback_data=f"tkt:admin_view:{r['id']}",
            )
        ])
    buttons.append([InlineKeyboardButton(text="🔙 Назад", callback_data="admin:back_main")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def ticket_view_kb(tid: int, is_admin_view: bool) -> InlineKeyboardMarkup:
    if is_admin_view:
        return InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="✏️ Ответить",   callback_data=f"tkt:admin_reply:{tid}")],
            [InlineKeyboardButton(text="✅ Закрыть",     callback_data=f"tkt:admin_close:{tid}")],
            [InlineKeyboardButton(text="🔁 Переоткрыть", callback_data=f"tkt:admin_reopen:{tid}")],
            [InlineKeyboardButton(text="🔙 К списку",    callback_data="tkt:admin_list:0")],
        ])
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✏️ Дописать", callback_data=f"tkt:reply:{tid}")],
        [InlineKeyboardButton(text="🔙 К списку", callback_data="tkt:my:0")],
    ])


def cancel_kb(cb: str = "tkt:menu") -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="❌ Отмена", callback_data=cb)],
    ])


# ── Рендер треда ────────────────────────────────────────────────────────────
def _format_ticket_thread(t: dict, is_admin_view: bool) -> str:
    status = "🟢 открыт" if t["status"] == "open" else "⚫ закрыт"
    header = (
        f"🎫 <b>Тикет #{t['id']}</b> · {status}\n"
        f"{DIV}\n"
        f"<b>Тема:</b> {t['subject']}\n"
        f"<b>Создан:</b> {t['created_at']}\n"
        f"<b>Обновлён:</b> {t['updated_at']}\n"
        f"{DIV}\n"
    )
    # В шапке автор тикета виден только админу. Пользователь автора и так знает (это он).
    if is_admin_view:
        header += f"<b>Автор:</b> {_user_label(t['user_id'])} (<code>{t['user_id']}</code>)\n{DIV}\n"
    body_lines = []
    for m in t["messages"]:
        # Пользователю не показываем, кто именно из админов ответил — только «Поддержка».
        if m["author_role"] == "user":
            who = "👤 Вы"
        else:
            who = "💼 Поддержка" if not is_admin_view else f"👨‍💼 Админ ({m['author_id']})"
        body_lines.append(f"<b>{who}</b> · <i>{m['created_at']}</i>")
        body_lines.append(m["text"])
        body_lines.append("")
    if not body_lines:
        body_lines = ["<i>(пусто)</i>"]
    return header + "\n".join(body_lines)


# ── Уведомления админам ────────────────────────────────────────────────────
async def _notify_admins(bot, text: str, reply_markup: InlineKeyboardMarkup | None = None) -> None:
    """Шлёт сообщение всем админам из таблицы admins."""
    admins = get_all_admins() or []
    for i, uid in enumerate(admins):
        try:
            await bot.send_message(uid, text, parse_mode=PM, reply_markup=reply_markup)
        except Exception as e:
            log.error(f"notify admin {uid} failed: {e}")
        if (i + 1) % NOTIFY_BATCH == 0:
            await asyncio.sleep(0.5)


# ── Хендлеры: пользователь ──────────────────────────────────────────────────
@router.callback_query(F.data == "tkt:menu")
async def cb_tkt_menu(call: CallbackQuery, state: FSMContext):
    """Главное меню тикетов (пользователь)."""
    try: await call.answer()
    except Exception: pass
    if is_admin(call.from_user.id):
        await call.answer("Раздел «Поддержка» только для пользователей.\nАдмины: «🎫 Тикеты» в админ-панели.", show_alert=True)
        return
    await state.clear()
    rows = list_user_tickets(call.from_user.id, "open")
    open_n = len(rows)
    text = (
        f"🎫 <b>Поддержка</b>\n"
        f"{DIV}\n"
        f"Здесь можно задать вопрос или сообщить о проблеме.\n\n"
        f"📨 Открытых тикетов: <b>{open_n}</b>\n\n"
        f"{BULLET} <b>Новое обращение</b> — создать новый тикет\n"
        f"{BULLET} <b>Мои тикеты</b> — посмотреть историю\n"
        f"{DIV}\n"
        f"<i>Выберите действие:</i>"
    )
    if call.message.photo:
        await call.message.answer(text, reply_markup=user_tickets_main_kb(), parse_mode=PM)
    else:
        try:
            await call.message.edit_text(text, reply_markup=user_tickets_main_kb(), parse_mode=PM)
        except TelegramBadRequest:
            await call.message.answer(text, reply_markup=user_tickets_main_kb(), parse_mode=PM)


@router.callback_query(F.data == "tkt:new")
async def cb_tkt_new(call: CallbackQuery, state: FSMContext):
    try: await call.answer()
    except Exception: pass
    if is_admin(call.from_user.id):
        await call.answer("Создавать тикеты могут только пользователи.", show_alert=True)
        return
    await state.set_state(TicketStates.entering_subject)
    text = (
        f"✏️ <b>Новое обращение</b>\n"
        f"{DIV}\n"
        f"Введите <b>тему</b> обращения одним коротким сообщением.\n\n"
        f"<i>Например: <code>Не запускается автоматизация</code></i>"
    )
    if call.message.photo:
        await call.message.answer(text, reply_markup=cancel_kb("tkt:menu"), parse_mode=PM)
    else:
        try:
            await call.message.edit_text(text, reply_markup=cancel_kb("tkt:menu"), parse_mode=PM)
        except TelegramBadRequest:
            await call.message.answer(text, reply_markup=cancel_kb("tkt:menu"), parse_mode=PM)


@router.message(TicketStates.entering_subject)
async def tkt_subject_entered(message: Message, state: FSMContext):
    if is_admin(message.from_user.id):
        await state.clear()
        return
    subject = (message.text or "").strip()
    if not subject:
        await message.answer("❌ Тема не может быть пустой. Введите тему:", parse_mode=PM)
        return
    if len(subject) > 200:
        subject = subject[:200]
    await state.update_data(subject=subject)
    await state.set_state(TicketStates.entering_body)
    await message.answer(
        f"✏️ <b>Тема принята</b>: <code>{subject}</code>\n"
        f"{DIV}\n"
        f"Теперь опишите проблему или вопрос <b>одним сообщением</b>.\n"
        f"После отправки тикет будет создан и админы получат уведомление.",
        reply_markup=cancel_kb("tkt:menu"),
        parse_mode=PM,
    )


@router.message(TicketStates.entering_body)
async def tkt_body_entered(message: Message, state: FSMContext):
    if is_admin(message.from_user.id):
        await state.clear()
        return
    body = (message.text or "").strip()
    if not body:
        await message.answer("❌ Текст не может быть пустым. Опишите ваш вопрос:", parse_mode=PM)
        return
    data = await state.get_data()
    subject = data.get("subject", "(без темы)")
    user = message.from_user
    tid = create_ticket(user.id, subject, body)
    await state.clear()
    await message.answer(
        f"🎫 <b>Тикет #{tid} создан!</b>\n"
        f"{DIV}\n"
        f"<b>Тема:</b> <code>{subject}</code>\n"
        f"Админы уведомлены. Ожидайте ответа.\n\n"
        f"Можно дописать что-то ещё через «🎫 Поддержка» → «Мои тикеты».",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="📂 Открыть тикет", callback_data=f"tkt:view:{tid}")],
            [InlineKeyboardButton(text="🔙 В меню",        callback_data="tkt:menu")],
        ]),
        parse_mode=PM,
    )
    # Notify admins
    note = (
        f"🆕 <b>Новый тикет #{tid}</b>\n"
        f"<b>От:</b> {_user_label(user.id)} (<code>{user.id}</code>)\n"
        f"<b>Тема:</b> <code>{subject}</code>\n"
        f"{DIV}\n"
        f"<i>{body[:600]}{'…' if len(body) > 600 else ''}</i>"
    )
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="👀 Открыть", callback_data=f"tkt:admin_view:{tid}")],
    ])
    bot = message.bot
    if bot is not None:
        await _notify_admins(bot, note, reply_markup=kb)


@router.callback_query(F.data.startswith("tkt:my:"))
async def cb_tkt_my(call: CallbackQuery, state: FSMContext):
    try: await call.answer()
    except Exception: pass
    if is_admin(call.from_user.id):
        await call.answer("Админы не ведут свои тикеты. Управление — «🎫 Тикеты» в админ-панели.", show_alert=True)
        return
    await state.clear()
    rows = list_user_tickets(call.from_user.id)
    if not rows:
        text = (
            f"📂 <b>Мои тикеты</b>\n"
            f"{DIV}\n"
            f"У вас пока нет обращений. Создайте новое через «✏️ Новое обращение»."
        )
        if call.message.photo:
            await call.message.answer(text, reply_markup=cancel_kb("tkt:menu"), parse_mode=PM)
        else:
            try:
                await call.message.edit_text(text, reply_markup=cancel_kb("tkt:menu"), parse_mode=PM)
            except TelegramBadRequest:
                await call.message.answer(text, reply_markup=cancel_kb("tkt:menu"), parse_mode=PM)
        return
    text = f"📂 <b>Мои тикеты</b> ({len(rows)})\n{DIV}\nВыберите тикет:"
    kb = user_tickets_list_kb(rows)
    if call.message.photo:
        await call.message.answer(text, reply_markup=kb, parse_mode=PM)
    else:
        try:
            await call.message.edit_text(text, reply_markup=kb, parse_mode=PM)
        except TelegramBadRequest:
            await call.message.answer(text, reply_markup=kb, parse_mode=PM)


@router.callback_query(F.data.startswith("tkt:view:"))
async def cb_tkt_view(call: CallbackQuery, state: FSMContext):
    try: await call.answer()
    except Exception: pass
    if is_admin(call.from_user.id):
        await call.answer("Админы просматривают тикеты через «🎫 Тикеты» в админ-панели.", show_alert=True)
        return
    tid = int(call.data.split(":")[2])
    t = get_ticket(tid)
    if not t or t["user_id"] != call.from_user.id:
        await call.answer("Тикет не найден или не ваш", show_alert=True)
        return
    await state.set_state(TicketStates.viewing)
    text = _format_ticket_thread(t, is_admin_view=False)
    kb = ticket_view_kb(tid, is_admin_view=False)
    if call.message.photo:
        await call.message.answer(text, reply_markup=kb, parse_mode=PM)
    else:
        try:
            await call.message.edit_text(text, reply_markup=kb, parse_mode=PM)
        except TelegramBadRequest:
            await call.message.answer(text, reply_markup=kb, parse_mode=PM)


@router.callback_query(F.data.startswith("tkt:reply:"))
async def cb_tkt_reply(call: CallbackQuery, state: FSMContext):
    try: await call.answer()
    except Exception: pass
    if is_admin(call.from_user.id):
        await call.answer("Отвечать на тикеты из админ-раздела «🎫 Тикеты».", show_alert=True)
        return
    tid = int(call.data.split(":")[2])
    t = get_ticket(tid)
    if not t or t["user_id"] != call.from_user.id:
        await call.answer("Тикет не найден", show_alert=True)
        return
    if t["status"] == "closed":
        await call.answer("Тикет закрыт. Дописать нельзя.", show_alert=True)
        return
    await state.set_state(TicketStates.replying)
    await state.update_data(reply_tid=tid)
    await call.message.answer(
        f"✏️ <b>Дописывание в тикет #{tid}</b>\n"
        f"{DIV}\n"
        f"Отправьте сообщение одним текстом.",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="❌ Отмена", callback_data=f"tkt:view:{tid}")],
        ]),
        parse_mode=PM,
    )


@router.message(TicketStates.replying)
async def tkt_reply_entered(message: Message, state: FSMContext):
    body = (message.text or "").strip()
    if not body:
        await message.answer("❌ Пустое сообщение. Напишите текст:", parse_mode=PM)
        return
    data = await state.get_data()
    tid = data.get("reply_tid")
    if not tid:
        await state.clear()
        await message.answer("⚠️ Контекст потерян, начните заново.", parse_mode=PM)
        return
    t = get_ticket(tid)
    if not t or t["user_id"] != message.from_user.id:
        await state.clear()
        await message.answer("⚠️ Тикет не найден.", parse_mode=PM)
        return
    if t["status"] == "closed":
        await state.clear()
        await message.answer("⚠️ Тикет уже закрыт.", parse_mode=PM)
        return
    add_message(tid, message.from_user.id, "user", body)
    await state.set_state(TicketStates.viewing)
    # Notify admins
    note = (
        f"💬 <b>Новое сообщение в тикете #{tid}</b>\n"
        f"<b>От:</b> {_user_label(message.from_user.id)} (<code>{message.from_user.id}</code>)\n"
        f"{DIV}\n"
        f"<i>{body[:600]}{'…' if len(body) > 600 else ''}</i>"
    )
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="👀 Открыть", callback_data=f"tkt:admin_view:{tid}")],
    ])
    await _notify_admins(message.bot, note, reply_markup=kb)
    await message.answer(
        f"✅ Сообщение добавлено в тикет #{tid}.",
        reply_markup=ticket_view_kb(tid, is_admin_view=False),
        parse_mode=PM,
    )


# ── Хендлеры: админ ─────────────────────────────────────────────────────────
@router.callback_query(F.data == "tkt:admin_menu")
async def cb_tkt_admin_menu(call: CallbackQuery, state: FSMContext):
    if not is_admin(call.from_user.id):
        await call.answer("⛔ Доступ запрещён", show_alert=True)
        return
    try: await call.answer()
    except Exception: pass
    await state.clear()
    open_rows = list_open_tickets()
    total_recent = len(list_recent_tickets(100))
    text = (
        f"🎫 <b>Тикеты</b>\n"
        f"{DIV}\n"
        f"🟢 Открытых: <b>{len(open_rows)}</b>\n"
        f"📊 Всего недавних: <b>{total_recent}</b>\n\n"
        f"{BULLET} <b>Открытые</b> — список ожидающих ответа\n"
        f"{BULLET} <b>Все тикеты</b> — последние 50\n"
    )
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🟢 Открытые", callback_data="tkt:admin_list:0")],
        [InlineKeyboardButton(text="📋 Все тикеты", callback_data="tkt:admin_list_all:0")],
        [InlineKeyboardButton(text="🔙 Назад", callback_data="admin:back_main")],
    ])
    if call.message.photo:
        await call.message.answer(text, reply_markup=kb, parse_mode=PM)
    else:
        try:
            await call.message.edit_text(text, reply_markup=kb, parse_mode=PM)
        except TelegramBadRequest:
            await call.message.answer(text, reply_markup=kb, parse_mode=PM)


@router.callback_query(F.data == "tkt:admin_list:0")
async def cb_tkt_admin_list(call: CallbackQuery, state: FSMContext):
    if not is_admin(call.from_user.id):
        await call.answer("⛔ Доступ запрещён", show_alert=True)
        return
    try: await call.answer()
    except Exception: pass
    await state.clear()
    rows = list_open_tickets()
    text = f"🟢 <b>Открытые тикеты</b> ({len(rows)})\n{DIV}\n"
    if not rows:
        text += "<i>Нет открытых тикетов. 🎉</i>"
    else:
        text += "Выберите тикет:"
    kb = admin_tickets_list_kb(rows) if rows else InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔙 Назад", callback_data="tkt:admin_menu")]
    ])
    if call.message.photo:
        await call.message.answer(text, reply_markup=kb, parse_mode=PM)
    else:
        try:
            await call.message.edit_text(text, reply_markup=kb, parse_mode=PM)
        except TelegramBadRequest:
            await call.message.answer(text, reply_markup=kb, parse_mode=PM)


@router.callback_query(F.data == "tkt:admin_list_all:0")
async def cb_tkt_admin_list_all(call: CallbackQuery, state: FSMContext):
    if not is_admin(call.from_user.id):
        await call.answer("⛔ Доступ запрещён", show_alert=True)
        return
    try: await call.answer()
    except Exception: pass
    await state.clear()
    rows = list_recent_tickets(50)
    text = f"📋 <b>Все тикеты</b> (последние {len(rows)})\n{DIV}\n"
    if not rows:
        text += "<i>Пусто.</i>"
    else:
        text += "Выберите тикет:"
    kb = admin_tickets_list_kb(rows) if rows else InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔙 Назад", callback_data="tkt:admin_menu")]
    ])
    if call.message.photo:
        await call.message.answer(text, reply_markup=kb, parse_mode=PM)
    else:
        try:
            await call.message.edit_text(text, reply_markup=kb, parse_mode=PM)
        except TelegramBadRequest:
            await call.message.answer(text, reply_markup=kb, parse_mode=PM)


@router.callback_query(F.data.startswith("tkt:admin_view:"))
async def cb_tkt_admin_view(call: CallbackQuery, state: FSMContext):
    if not is_admin(call.from_user.id):
        await call.answer("⛔ Доступ запрещён", show_alert=True)
        return
    try: await call.answer()
    except Exception: pass
    tid = int(call.data.split(":")[2])
    t = get_ticket(tid)
    if not t:
        await call.answer("Тикет не найден", show_alert=True)
        return
    await state.set_state(TicketStates.admin_viewing)
    await state.update_data(admin_view_tid=tid)
    text = _format_ticket_thread(t, is_admin_view=True)
    kb = ticket_view_kb(tid, is_admin_view=True)
    if call.message.photo:
        await call.message.answer(text, reply_markup=kb, parse_mode=PM)
    else:
        try:
            await call.message.edit_text(text, reply_markup=kb, parse_mode=PM)
        except TelegramBadRequest:
            await call.message.answer(text, reply_markup=kb, parse_mode=PM)


@router.callback_query(F.data.startswith("tkt:admin_reply:"))
async def cb_tkt_admin_reply(call: CallbackQuery, state: FSMContext):
    if not is_admin(call.from_user.id):
        await call.answer("⛔ Доступ запрещён", show_alert=True)
        return
    try: await call.answer()
    except Exception: pass
    tid = int(call.data.split(":")[2])
    t = get_ticket(tid)
    if not t:
        await call.answer("Тикет не найден", show_alert=True)
        return
    await state.set_state(TicketStates.admin_replying)
    await state.update_data(reply_tid=tid)
    await call.message.answer(
        f"✏️ <b>Ответ на тикет #{tid}</b>\n"
        f"<b>Кому:</b> {_user_label(t['user_id'])} (<code>{t['user_id']}</code>)\n"
        f"{DIV}\n"
        f"Напишите ответ одним сообщением — он уйдёт пользователю.",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="❌ Отмена", callback_data=f"tkt:admin_view:{tid}")],
        ]),
        parse_mode=PM,
    )


@router.message(TicketStates.admin_replying)
async def admin_reply_entered(message: Message, state: FSMContext):
    """Обработчик ответа админа."""
    if not is_admin(message.from_user.id):
        await state.clear()
        return
    body = (message.text or "").strip()
    if not body:
        await message.answer("❌ Пустой ответ. Напишите текст:", parse_mode=PM)
        return
    data = await state.get_data()
    tid = data.get("reply_tid")
    t = get_ticket(tid) if tid else None
    if not t:
        await state.clear()
        await message.answer("⚠️ Тикет не найден.", parse_mode=PM)
        return
    add_message(tid, message.from_user.id, "admin", body)
    await state.set_state(TicketStates.admin_viewing)
    await message.answer(
        f"✅ Ответ отправлен в тикет #{tid}.",
        reply_markup=ticket_view_kb(tid, is_admin_view=True),
        parse_mode=PM,
    )
    # Notify user about admin reply
    try:
        await message.bot.send_message(
            t["user_id"],
            f"💬 <b>Ответ в тикете #{tid}</b>\n"
            f"<b>Тема:</b> <code>{t['subject']}</code>\n"
            f"{DIV}\n"
            f"{body[:3500]}",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="📂 Открыть тикет", callback_data=f"tkt:view:{tid}")],
            ]),
            parse_mode=PM,
        )
    except Exception as e:
        log.error(f"notify user {t['user_id']} about admin reply failed: {e}")


@router.callback_query(F.data.startswith("tkt:admin_close:"))
async def cb_tkt_admin_close(call: CallbackQuery, state: FSMContext):
    if not is_admin(call.from_user.id):
        await call.answer("⛔ Доступ запрещён", show_alert=True)
        return
    try: await call.answer("✅ Закрыто")
    except Exception: pass
    tid = int(call.data.split(":")[2])
    close_ticket(tid)
    t = get_ticket(tid)
    # Notify user
    if t:
        try:
            await call.bot.send_message(
                t["user_id"],
                f"⚫ <b>Тикет #{tid} закрыт</b>\n"
                f"<b>Тема:</b> <code>{t['subject']}</code>\n"
                f"{DIV}\n"
                f"Если вопрос остался — создайте новый через «🎫 Поддержка».",
                parse_mode=PM,
            )
        except Exception as e:
            log.error(f"notify user about close failed: {e}")
    await state.set_state(TicketStates.admin_viewing)
    if t:
        text = _format_ticket_thread(t, is_admin_view=True)
        kb = ticket_view_kb(tid, is_admin_view=True)
        if call.message.photo:
            await call.message.answer(text, reply_markup=kb, parse_mode=PM)
        else:
            try:
                await call.message.edit_text(text, reply_markup=kb, parse_mode=PM)
            except TelegramBadRequest:
                await call.message.answer(text, reply_markup=kb, parse_mode=PM)


@router.callback_query(F.data.startswith("tkt:admin_reopen:"))
async def cb_tkt_admin_reopen(call: CallbackQuery, state: FSMContext):
    if not is_admin(call.from_user.id):
        await call.answer("⛔ Доступ запрещён", show_alert=True)
        return
    try: await call.answer("🔁 Переоткрыт")
    except Exception: pass
    tid = int(call.data.split(":")[2])
    reopen_ticket(tid)
    t = get_ticket(tid)
    if t:
        text = _format_ticket_thread(t, is_admin_view=True)
        kb = ticket_view_kb(tid, is_admin_view=True)
        if call.message.photo:
            await call.message.answer(text, reply_markup=kb, parse_mode=PM)
        else:
            try:
                await call.message.edit_text(text, reply_markup=kb, parse_mode=PM)
            except TelegramBadRequest:
                await call.message.answer(text, reply_markup=kb, parse_mode=PM)
