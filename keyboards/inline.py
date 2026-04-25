from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from data.config import GEO_CATALOG, GEO_LABELS


def geo_menu() -> InlineKeyboardMarkup:
    """Выбор геолокации — первый экран после 'Начать'."""
    buttons = [
        [InlineKeyboardButton(text=info["label"], callback_data=f"geo:{gk}")]
        for gk, info in GEO_CATALOG.items()
    ]
    buttons.append([InlineKeyboardButton(text="🔙 Назад", callback_data="back:welcome")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def main_menu(role: str | None, geo: str) -> InlineKeyboardMarkup:
    """Меню категорий для конкретного гео."""
    catalog = GEO_CATALOG.get(geo, {}).get("catalog", {})
    allowed = _allowed_lines(role)
    buttons = []
    for line_key, line in catalog.items():
        if line_key in allowed and line.get("sections"):
            # Пропускаем пустые секции
            has_items = any(
                sec.get("items")
                for sec in line["sections"].values()
            )
            if has_items:
                buttons.append([InlineKeyboardButton(
                    text=line["label"], callback_data=f"line:{geo}:{line_key}"
                )])
    if not buttons:
        buttons.append([InlineKeyboardButton(
            text="⛔ В этом регионе пока нет доступных шаблонов",
            callback_data="noop"
        )])
    buttons.append([InlineKeyboardButton(text="🔙 Назад", callback_data="back:geo")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def sections_menu(geo: str, line_key: str) -> InlineKeyboardMarkup:
    line = GEO_CATALOG[geo]["catalog"][line_key]
    buttons = [
        [InlineKeyboardButton(text=sec["label"],
                              callback_data=f"section:{geo}:{line_key}:{sec_key}")]
        for sec_key, sec in line["sections"].items()
        if sec.get("items")
    ]
    buttons.append([InlineKeyboardButton(text="🔙 Назад", callback_data=f"back:geo_menu:{geo}")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def items_menu(geo: str, line_key: str, sec_key: str) -> InlineKeyboardMarkup:
    section = GEO_CATALOG[geo]["catalog"][line_key]["sections"][sec_key]
    buttons = [
        [InlineKeyboardButton(text=item["label"],
                              callback_data=f"item:{geo}:{item_key}")]
        for item_key, item in section["items"].items()
    ]
    buttons.append([InlineKeyboardButton(
        text="🔙 Назад", callback_data=f"back:geo_section:{geo}:{line_key}"
    )])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def cancel_kb(callback_data: str = "cancel") -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="❌ Отмена", callback_data=callback_data)]
    ])


def after_render_kb(geo: str, item_key: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔄 Создать новый шаблон",
                              callback_data=f"item:{geo}:{item_key}")],
        [InlineKeyboardButton(text="🏠 Главное меню", callback_data="back:main")],
    ])


def _allowed_lines(role: str | None) -> list[str]:
    """
    fd       → fd, qr, support
    rd       → rd, qr, support
    cr       → check
    fd+rd    → fd, rd, qr, support
    fd+cr    → fd, qr, support, check
    rd+cr    → rd, qr, support, check
    fd+rd+cr → fd, rd, qr, support, check
    all      → всё
    """
    if not role:
        return []
    if role == "all":
        return ["fd", "rd", "check", "qr", "support"]
    roles = set(role.split("+"))
    result = []
    if "fd" in roles: result.append("fd")
    if "rd" in roles: result.append("rd")
    if "cr" in roles: result.append("check")
    if "fd" in roles or "rd" in roles:
        result += ["qr", "support"]
    return result
