"""keyboards/auto_kb.py — клавиатуры модуля автоматизации.

Дизайн:
  • Каждое действие — эмодзи + текст.
  • «Готово» / «Запустить» / «Назад» — единый стиль.
  • Чекбоксы — ✅ / ◻️.
"""
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from data.config import GEO_CATALOG


def auto_main_kb(has_preset: bool) -> InlineKeyboardMarkup:
    """Главное меню автоматизации."""
    rows = []
    if has_preset:
        rows.append([InlineKeyboardButton(
            text="🚀 Запустить автоматизацию",
            callback_data="auto:run",
        )])
        rows.append([InlineKeyboardButton(
            text="⚙️ Изменить настройки",
            callback_data="auto:settings",
        )])
        rows.append([InlineKeyboardButton(
            text="🗑 Сбросить пресет",
            callback_data="auto:reset",
        )])
    else:
        rows.append([InlineKeyboardButton(
            text="⚙️ Настроить автоматизацию",
            callback_data="auto:settings",
        )])
    rows.append([InlineKeyboardButton(
        text="� В главное меню",
        callback_data="back:welcome",
    )])
    return InlineKeyboardMarkup(inline_keyboard=rows)


def auto_pick_geo_kb(geos: list[str]) -> InlineKeyboardMarkup:
    """Шаг 1 — выбор ГЕО."""
    rows = []
    for gk in geos:
        label = GEO_CATALOG.get(gk, {}).get("label", gk)
        rows.append([InlineKeyboardButton(
            text=f"🌍 {label}",
            callback_data=f"auto:geo:{gk}",
        )])
    rows.append([InlineKeyboardButton(
        text="🔙 Назад",
        callback_data="auto:open",
    )])
    return InlineKeyboardMarkup(inline_keyboard=rows)


def auto_pick_line_kb(geo: str, user_id: int) -> InlineKeyboardMarkup:
    """Шаг 2 — выбор линейки шаблонов внутри гео."""
    from data.db import is_admin
    admin = is_admin(user_id)
    allowed = None if admin else _allowed_lines("all")  # упрощённо: максимум

    catalog = GEO_CATALOG.get(geo, {}).get("catalog", {})
    rows = []
    for line_key, line in catalog.items():
        if allowed is not None and line_key not in allowed:
            continue
        if not line.get("sections"):
            continue
        has_items = any(sec.get("items") for sec in line["sections"].values())
        if not has_items:
            continue
        rows.append([InlineKeyboardButton(
            text=f"📂 {line['label']}",
            callback_data=f"auto:line:{geo}:{line_key}",
        )])
    if not rows:
        rows.append([InlineKeyboardButton(
            text="⛔ Нет доступных линеек",
            callback_data="noop",
        )])
    rows.append([InlineKeyboardButton(
        text="🔙 Назад",
        callback_data="auto:settings",
    )])
    return InlineKeyboardMarkup(inline_keyboard=rows)


def auto_pick_items_kb(geo: str, line_key: str, selected: set[str]) -> InlineKeyboardMarkup:
    """Шаг 3 — мультивыбор типов чеков."""
    sections = GEO_CATALOG[geo]["catalog"][line_key]["sections"]
    rows = []
    for sec_key, sec in sections.items():
        if not sec.get("items"):
            continue
        rows.append([InlineKeyboardButton(
            text=f"— {sec['label']} —",
            callback_data="noop",
        )])
        for item_key, item in sec["items"].items():
            mark = "✅ " if item_key in selected else "◻️ "
            rows.append([InlineKeyboardButton(
                text=f"{mark}{item['label']}",
                callback_data=f"auto:item:{geo}:{line_key}:{item_key}",
            )])
    rows.append([InlineKeyboardButton(
        text="✅ Готово",
        callback_data="auto:items:done",
    )])
    rows.append([InlineKeyboardButton(
        text="🔙 Назад",
        callback_data="auto:settings",
    )])
    return InlineKeyboardMarkup(inline_keyboard=rows)


def auto_back_kb() -> InlineKeyboardMarkup:
    """Универсальная клавиатура «назад» для FSM-состояний ввода."""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔙 Отмена", callback_data="auto:open")],
    ])


def auto_run_kb() -> InlineKeyboardMarkup:
    """Клавиатура после сохранения пресета."""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text="🚀 Запустить автоматизацию",
            callback_data="auto:run",
        )],
        [InlineKeyboardButton(
            text="⚙️ Изменить настройки",
            callback_data="auto:settings",
        )],
        [InlineKeyboardButton(
            text="🔙 В главное меню",
            callback_data="back:welcome",
        )],
    ])


def _allowed_lines(role: str | None) -> list[str] | None:
    """Возвращает список разрешённых линеек по роли.
    None — нет ограничений (супер-админ / 'all')."""
    if not role:
        return ["fd", "rd", "check", "qr", "support", "rocket", "fire", "payment"]
    if role == "all":
        return None
    roles = set(role.split("+"))
    result = []
    if "fd" in roles:
        result.append("fd")
    if "rd" in roles:
        result.append("rd")
    if "cr" in roles:
        result += ["check", "qr", "rocket", "fire", "payment"]
    if "fd" in roles or "rd" in roles:
        result += ["qr", "support", "fire"]
    seen = set()
    return [x for x in result if not (x in seen or seen.add(x))]
