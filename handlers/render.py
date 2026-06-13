"""
FSM-рендеринг: превью + интерактивный чеклист → рендер PNG.

При отмене:
  - удаляет сообщение с превью И отдельные вопросы
  - возвращает в последний открытый раздел (из FSM state)
"""
import os
import io
from aiogram import Router, F
from aiogram.types import CallbackQuery, Message, BufferedInputFile, FSInputFile, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import CommandStart, Command

from data.config import GEO_CATALOG
from data.db import get_role_string, get_settings
from keyboards.inline import cancel_kb, after_render_kb, main_menu, sections_menu, items_menu, geo_menu, geo_menu_for
from utils.logger import log
import random

router = Router()


def _is_name_field(field_key: str) -> bool:
    return field_key in ("name", "fullname", "recipient_name", "sender_name", "receiver_name", "client_name", "name_1", "name_2", "name1", "name2", "payer_1", "payer_2", "destino", "origen")

def _format_name(full_name: str, item: dict) -> str:
    fmt = item.get("name_format", "raw")
    parts = full_name.split()
    
    if fmt == "upper":
        return full_name.upper()
        
    if len(parts) == 4:
        surname1, surname2, name1, name2 = parts
        if fmt == "4_words":
            return f"{name1} {name2} {surname1} {surname2}"
        if fmt == "2_words":
            return f"{name1} {surname1}"
        if fmt == "py_fio":
            return f"{name1} {name2} {surname1} {surname2}"
    elif len(parts) >= 2:
        if fmt == "py_fio" or fmt == "2_words":
            return f"{parts[1]} {parts[0]}"
            
    return full_name

def _format_date_for_item(val: str, item: dict) -> str:
    fmt = item.get("date_format", "raw")
    if fmt == "es_long": return _to_es_date(val)
    if fmt == "es_slash": return _to_es_date2(val)
    if fmt == "es_short": return _to_es_date3(val)
    if fmt == "fire": return _to_es_date_fire(val)
    if fmt == "uy": return _to_es_date_uy(val)
    if fmt == "dot_slash": return val.replace(".", "/")
    if fmt == "py": return _to_es_date_py(val)
    if fmt == "py3": return _to_es_date_py_check3(val)
    if fmt == "dot_slash_year20":
        val = val.replace(".", "/")
        parts = val.split("/")
        if len(parts) == 3 and len(parts[2]) == 2:
            parts[2] = "20" + parts[2]
            val = "/".join(parts)
        return val
    return val

def _advance_steps(askable: list, start_step: int, values: dict, s: dict, item: dict, item_key: str) -> int:
    import random
    done_step = start_step
    while done_step < len(askable):
        if s.get("pinned_date") and "date" in askable[done_step]["key"]:
            values[askable[done_step]["key"]] = _format_date_for_item(s["pinned_date"], item)
            done_step += 1
            continue
        key = askable[done_step]["key"]
        if key == "bank" and s.get("rand_bank_enabled") and not item_key.startswith("rd") and item_key not in ("check2_py", "check3_py", "check2_uy", "check3_uy", "check4_uy", "check3_bo"):
            val_rand = random.choice(item.get("banks", ["Banco"]))
            values["bank"] = val_rand
            if item_key == "check2_py":
                values["_bank_image"] = f"assets/Paraguay/Чек/bank/{val_rand}.jpg"
            if item_key == "check3_py":
                values["_bank_image"] = f"assets/Paraguay/Чек/bank2/{val_rand}.png"
            done_step += 1
        else:
            break
    return done_step

# ── Испанские сокращения месяцев ──────────────────────────────────────────────
_ES_MONTHS = {
    "01": "ene", "02": "feb", "03": "mar", "04": "abr",
    "05": "may", "06": "jun", "07": "jul", "08": "ago",
    "09": "sep", "10": "oct", "11": "nov", "12": "dic",
}

def _to_es_date(val: str) -> str:
    """Конвертирует '24.04.2026' или '24/04/2026' в '24 abr. 2026'."""
    import re
    m = re.match(r"(\d{1,2})[./](\d{2})[./](\d{4})", val.strip())
    if m:
        day, month, year = m.group(1), m.group(2), m.group(3)
        month_es = _ES_MONTHS.get(month, month)
        return f"{int(day)} {month_es}. {year}"
    return val

_ES_MONTHS_FULL = {
    "01": "Enero",    "02": "Febrero", "03": "Marzo",    "04": "Abril",
    "05": "Mayo",     "06": "Junio",   "07": "Julio",    "08": "Agosto",
    "09": "Septiembre","10": "Octubre","11": "Noviembre","12": "Diciembre",
}
_ES_DAYS = ["Lunes","Martes","Miércoles","Jueves","Viernes","Sábado","Domingo"]

def _to_es_date2(val: str) -> str:
    """Конвертирует '22.04.2026' в 'Lunes 22 Abril 2026'."""
    import re, datetime
    m = re.match(r"(\d{1,2})[./](\d{2})[./](\d{4})", val.strip())
    if m:
        day, month, year = int(m.group(1)), int(m.group(2)), int(m.group(3))
        try:
            dt = datetime.date(year, month, day)
            day_name = _ES_DAYS[dt.weekday()]
            month_name = _ES_MONTHS_FULL[f"{month:02d}"]
            return f"{day_name} {day} {month_name} {year}"
        except Exception:
            pass
    return val
    
def _to_es_date3(val: str) -> str:
    """Конвертирует '19.04.2026' в '19 Abr 2026'."""
    import re
    m = re.match(r"(\d{1,2})[./](\d{2})[./](\d{4})", val.strip())
    if m:
        day, month, year = m.group(1), m.group(2), m.group(3)
        month_es = _ES_MONTHS.get(month, month).capitalize()
        return f"{int(day)} {month_es} {year}"
    return val

def _to_es_date_fire(val: str) -> str:
    """Конвертирует '20.05.2026' в '20 de mayo de 2026' (формат Yasta)."""
    import re
    _MONTHS = ['enero','febrero','marzo','abril','mayo','junio',
               'julio','agosto','septiembre','octubre','noviembre','diciembre']
    m = re.match(r'(\d{1,2})[./](\d{1,2})[./](\d{4})', val.strip())
    if m:
        day, month, year = int(m.group(1)), int(m.group(2)), int(m.group(3))
        if 1 <= month <= 12:
            return f"{day} de {_MONTHS[month-1]} de {year}"
    return val

def _to_es_date_uy(val: str) -> str:
    """Конвертирует '20.04.2026' в '20 de abril 2026'."""
    import re
    _MONTHS = ['enero','febrero','marzo','abril','mayo','junio',
               'julio','agosto','septiembre','octubre','noviembre','diciembre']
    m = re.match(r'(\d{1,2})[./](\d{1,2})[./](\d{4})', val.strip())
    if m:
        day, month, year = int(m.group(1)), int(m.group(2)), int(m.group(3))
        if 1 <= month <= 12:
            return f"{day} de {_MONTHS[month-1]} {year}"
    return val

def _to_es_date_py(val: str) -> str:
    """Конвертирует '19.05.2026' в '19 may 2026'."""
    import re
    m = re.match(r'(\d{1,2})[./](\d{1,2})[./](\d{4})', val.strip())
    if m:
        day, month, year = int(m.group(1)), f"{int(m.group(2)):02d}", int(m.group(3))
        month_es = _ES_MONTHS.get(month, month)
        return f"{day} {month_es} {year}"
    return val

def _to_es_date_py_check3(val: str) -> str:
    """Конвертирует '18.05.2026' в '18/may/2026'."""
    import re
    m = re.match(r'(\d{1,2})[./](\d{1,2})[./](\d{4})', val.strip())
    if m:
        day, month, year = int(m.group(1)), f"{int(m.group(2)):02d}", int(m.group(3))
        month_es = _ES_MONTHS.get(month, month)
        return f"{day:02d}/{month_es}/{year}"
    return val

BASE_DIR = os.path.normpath(os.path.join(os.path.dirname(__file__), ".."))


class RenderStates(StatesGroup):
    collecting = State()


def _get_field_keyboard(field_key: str, s: dict, item_key: str = None) -> InlineKeyboardMarkup:
    buttons = []
    
    # 🎲 Рандомайзер сумм
    if s["rand_enabled"] and field_key in ("sum", "amount", "commission"):
        buttons.append([InlineKeyboardButton(text="🎲 Сгенерировать", callback_data="render:random")])
        
    # 🎲 Рандомайзер счетов
    if s.get("rand_acc_enabled") and field_key in ("number", "account", "transaction", "operation", "card_recipient", "card_sender", "phone", "order", "acc_1", "acc_2", "ref_num", "acc_num", "acc_num_2", "sender_acc", "sender_num", "receiver_num", "receiver_acc", "account_end"):
        buttons.append([InlineKeyboardButton(text="🎲 Сгенерировать", callback_data="render:random")])
        
    # 🎲 Рандомайзер процентов
    if s.get("rand_percent_enabled") and field_key == "percentage":
        buttons.append([InlineKeyboardButton(text="🎲 Сгенерировать", callback_data="render:random")])
        
    # 🎲 Рандомайзер банков
    if s.get("rand_bank_enabled") and field_key == "bank":
        buttons.append([InlineKeyboardButton(text="🎲 Сгенерировать", callback_data="render:random")])
        
    if field_key in ("bank_name", "bank_name_sender") and item_key == "check1_py":
        buttons.append([
            InlineKeyboardButton(text="ATLAS", callback_data="render:set:BANCO ATLAS S.A."),
            InlineKeyboardButton(text="SOLAR", callback_data="render:set:SOLAR BANCO S.A.E")
        ])
        buttons.append([
            InlineKeyboardButton(text="GNB", callback_data="render:set:BANCO GNB PARAGUAY SA"),
            InlineKeyboardButton(text="familiar", callback_data="render:set:BANCO FAMILIAR S.A.E.C.A.")
        ])
        buttons.append([
            InlineKeyboardButton(text="INTERFISA", callback_data="render:set:INTERFISA BANCO SAECA-GRUPO"),
            InlineKeyboardButton(text="SUDAMERIS", callback_data="render:set:SUDAMERIS BANK S.A.E.C.A.")
        ])

    if field_key == "bank" and item_key in ("check2_py", "payment1_py"):
        buttons.append([
            InlineKeyboardButton(text="ATLAS", callback_data="render:set:ATLAS"),
            InlineKeyboardButton(text="SOLAR", callback_data="render:set:SOLAR")
        ])
        buttons.append([
            InlineKeyboardButton(text="GNB", callback_data="render:set:GNB"),
            InlineKeyboardButton(text="familiar", callback_data="render:set:familiar")
        ])
        buttons.append([
            InlineKeyboardButton(text="INTERFISA", callback_data="render:set:interfisa"),
            InlineKeyboardButton(text="SUDAMERIS", callback_data="render:set:SUDAMERIS")
        ])

    if field_key == "bank" and item_key == "check3_py":
        buttons.append([
            InlineKeyboardButton(text="ATLAS", callback_data="render:set:ATLAS"),
            InlineKeyboardButton(text="SOLAR", callback_data="render:set:SOLAR")
        ])
        buttons.append([
            InlineKeyboardButton(text="GNB", callback_data="render:set:GNB")
        ])

    if field_key == "bank" and item_key == "check3_bo":
        buttons.append([
            InlineKeyboardButton(text="Banco Union", callback_data="render:set:Banco Union"),
            InlineKeyboardButton(text="Banco Fassil", callback_data="render:set:Banco Fassil")
        ])
        buttons.append([
            InlineKeyboardButton(text="Banco Ganadero", callback_data="render:set:Banco Ganadero"),
            InlineKeyboardButton(text="Banco BISA", callback_data="render:set:Banco BISA")
        ])

    if field_key == "comment":
        buttons.append([
            InlineKeyboardButton(text="WhiteTrade", callback_data="render:set:WhiteTrade"),
            InlineKeyboardButton(text="Tus ganancias!", callback_data="render:set:Tus ganancias!")
        ])

    if field_key == "bank" and item_key == "check3_uy":
        buttons.append([
            InlineKeyboardButton(text="Itaú", callback_data="render:set:Itaú"),
            InlineKeyboardButton(text="Santander", callback_data="render:set:Santander")
        ])
        buttons.append([
            InlineKeyboardButton(text="BBVA", callback_data="render:set:BBVA"),
            InlineKeyboardButton(text="Scotiabank", callback_data="render:set:Scotiabank")
        ])
        buttons.append([
            InlineKeyboardButton(text="Oca blue", callback_data="render:set:Oca blue")
        ])

    if field_key == "bank" and item_key == "check4_uy":
        buttons.append([
            InlineKeyboardButton(text="Oca Blue", callback_data="render:set:Oca Blue"),
            InlineKeyboardButton(text="Itaú", callback_data="render:set:Itaú")
        ])
        buttons.append([
            InlineKeyboardButton(text="Mi Dinero", callback_data="render:set:Mi Dinero")
        ])
        
    # 📅 Закрепленная дата
    if s["pinned_date"] and "date" in field_key:
        buttons.append([InlineKeyboardButton(text=f"📅 {s['pinned_date']}", callback_data="render:pin_date")])
        
    # 👤 Закрепленное ФИО
    if s.get("pinned_name") and _is_name_field(field_key):
        buttons.append([InlineKeyboardButton(text=f"👤 {s['pinned_name']}", callback_data="render:pin_name")])
        
    # 🎲 Рандомайзер имен
    if s.get("rand_name_enabled") and _is_name_field(field_key):
        buttons.append([InlineKeyboardButton(text="🎲 Имя со списка", callback_data="render:random_name")])
        
    # 🏦 Закрепленный банк
    if s.get("pinned_bank") and field_key == "bank":
        buttons.append([InlineKeyboardButton(text=f"🏦 {s['pinned_bank']}", callback_data="render:pin_bank")])
        
    # 🕒 AM/PM
    def _is_24h(ik, fk):
        for g in GEO_CATALOG.values():
            for c in g.get("catalog", {}).values():
                for sc in c.get("sections", {}).values():
                    items = sc.get("items", {})
                    if ik in items:
                        for f in items[ik].get("fields", []):
                            if f["key"] == fk:
                                return "(24-часовой формат)" in f.get("prompt", "")
        return False

    if "time" in field_key and item_key not in ("rd6", "rd7", "qr_pe", "check1_py") and not _is_24h(item_key, field_key):
        row = []
        am_label = "☀️ A.M."
        pm_label = "🌙 P.M."
        if item_key == "check_doc":
            am_label = am_label.lower()
            pm_label = pm_label.lower()

        am_text = am_label.split(" ", 1)[1]
        pm_text = pm_label.split(" ", 1)[1]

        if s.get("time_suffix") == "A.M.":
            row.append(InlineKeyboardButton(text=f"☀️ [{am_text}]", callback_data="render:suffix:none"))
            row.append(InlineKeyboardButton(text=pm_label,   callback_data="render:suffix:PM"))
        elif s.get("time_suffix") == "P.M.":
            row.append(InlineKeyboardButton(text=am_label,   callback_data="render:suffix:AM"))
            row.append(InlineKeyboardButton(text=f"🌙 [{pm_text}]", callback_data="render:suffix:none"))
        else:
            row.append(InlineKeyboardButton(text=am_label, callback_data="render:suffix:AM"))
            row.append(InlineKeyboardButton(text=pm_label, callback_data="render:suffix:PM"))
        buttons.append(row)
        
    # 👦👩 Кнопки пола
    if field_key == "gender":
        buttons.append([
            InlineKeyboardButton(text="👦 Мальчик", callback_data="render:set:o"),
            InlineKeyboardButton(text="👩 Женщина", callback_data="render:set:a")
        ])
        
    # Кнопки для ROCKET
    if field_key == "currency":
        buttons.append([
            InlineKeyboardButton(text="SOL", callback_data="render:set:SOL"),
            InlineKeyboardButton(text="BTC", callback_data="render:set:BTC")
        ])
        buttons.append([
            InlineKeyboardButton(text="BNB", callback_data="render:set:BNB"),
            InlineKeyboardButton(text="XRP", callback_data="render:set:XRP")
        ])
        buttons.append([
            InlineKeyboardButton(text="ETH", callback_data="render:set:ETH")
        ])

    # Кнопки для Uruguay Check 3 (Иконки)
    if field_key == "network":
        buttons.append([
            InlineKeyboardButton(text="2 из 4", callback_data="render:set:assets/Uruguay/Чек/icon/M1.png"),
            InlineKeyboardButton(text="3 из 4", callback_data="render:set:assets/Uruguay/Чек/icon/M2.png"),
            InlineKeyboardButton(text="4 из 4", callback_data="render:set:assets/Uruguay/Чек/icon/M3.png")
        ])

    if field_key == "wifi":
        buttons.append([
            InlineKeyboardButton(text="2 из 3", callback_data="render:set:assets/Uruguay/Чек/icon/W1.png"),
            InlineKeyboardButton(text="3 из 3", callback_data="render:set:assets/Uruguay/Чек/icon/W2.png")
        ])

    if field_key == "battery":
        buttons.append([
            InlineKeyboardButton(text="30 из 100", callback_data="render:set:assets/Uruguay/Чек/icon/B1.png"),
            InlineKeyboardButton(text="50 из 100", callback_data="render:set:assets/Uruguay/Чек/icon/B2.png"),
            InlineKeyboardButton(text="100 из 100", callback_data="render:set:assets/Uruguay/Чек/icon/B3.png")
        ])

    if field_key == "long_short":
        buttons.append([
            InlineKeyboardButton(text="Long", callback_data="render:set:Long"),
            InlineKeyboardButton(text="Short", callback_data="render:set:Short")
        ])

    if field_key == "percentage":
        sign = s.get("perc_sign", "+")
        buttons.append([
            InlineKeyboardButton(text="🟢 [+]" if sign == "+" else "⚫️ [+]", callback_data="render:perc_sign:+"),
            InlineKeyboardButton(text="🔴 [-]" if sign == "-" else "⚫️ [-]", callback_data="render:perc_sign:-")
        ])
        
    # 💰 Рекомендуемые суммы — Peru RD
    _PE_RD_AMOUNTS = {
        # item_key: (field_key, label, value)
        "rd2_pe":  ("amount",     "S/. 809",   "809"),
        "rd3_pe":  ("amount",     "S/. 1 165", "1 165"),
        "rd5_pe":  ("amount",     "S/. 739",   "739"),
        "rd7_pe":  ("amount",     "S/. 633",   "633"),
        "rd6_pe":  ("commission", "S/. 1 246", "1 246"),
    }
    # 💰 Рекомендуемые суммы — Bolivia RD
    _BO_RD_AMOUNTS = {
        "rd2":  ("amount",     "Bs. 2 102", "2 102"),
        "rd3":  ("amount",     "Bs. 2 343", "2 343"),
        "rd4":  ("amount",     "Bs. 2 258", "2 258"),
        "rd5":  ("amount",     "Bs. 2 100", "2 100"),
        "rd7":  ("amount",     "Bs. 1 745", "1 745"),
        "rd8":  ("amount",     "Bs. 3 500", "3 500"),
        "rd6":  ("commission", "Bs. 1 920", "1 920"),
    }
    _UY_RD_AMOUNTS = {
        "rd1_uy":  ("commission", "6720", "6720"),
        "rd2_uy":  ("amount",     "10920", "10920"),
        "rd3_uy":  ("amount",     "13860", "13860"),
        "rd4_uy":  ("amount",     "7980",  "7980"),
        "rd5_uy":  ("amount",     "23520", "23520"),
        "rd7_uy":  ("amount",     "29400", "29400"),
        "rd6_uy":  ("commission", "33600", "33600"),
    }
    _PY_RD_AMOUNTS = {
        "rd1_py":  ("commission", "980000", "980000"),
        "rd2_py":  ("amount",     "1560000", "1560000"),
        "rd3_py":  ("amount",     "1980000", "1980000"),
        "rd4_py":  ("amount",     "1140000", "1140000"),
        "rd5_py":  ("amount",     "3360000", "3360000"),
        "rd7_py":  ("amount",     "4200000", "4200000"),
        "rd6_py":  ("commission", "4800000", "4800000"),
    }
    _ALL_RD_AMOUNTS = {**_PE_RD_AMOUNTS, **_BO_RD_AMOUNTS, **_UY_RD_AMOUNTS, **_PY_RD_AMOUNTS}
    if item_key in _ALL_RD_AMOUNTS:
        _fkey, _label, _val = _ALL_RD_AMOUNTS[item_key]
        if field_key == _fkey:
            buttons.append([InlineKeyboardButton(
                text=f"💡 {_label}",
                callback_data=f"render:set:{_val}"
            )])
            
    if item_key == "rd1" and field_key == "commission":
        buttons.append([
            InlineKeyboardButton(text="💡 1590", callback_data="render:set:1590"),
            InlineKeyboardButton(text="💡 890", callback_data="render:set:890")
        ])
    
    buttons.append([InlineKeyboardButton(text="❌ Отмена", callback_data="cancel")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


# ─────────────────────────── helpers ─────────────────────────────────────────

def _find_item(item_key: str, geo: str = "bo") -> dict | None:
    from data.config import GEO_CATALOG
    catalog = GEO_CATALOG.get(geo, {}).get("catalog", {})
    for line in catalog.values():
        for section in line["sections"].values():
            if item_key in section["items"]:
                return section["items"][item_key]
    return None


def _get_item_for_user(item_key: str, geo: str, user_id: int) -> dict | None:
    item = _find_item(item_key, geo)
    if not item:
        return None
    from data.db import get_settings
    s = get_settings(user_id)
    if s.get("jose_sender_enabled") and item_key in ("check1_py", "check2_py", "check3_py", "check1_uy", "check4_uy", "check_doc", "fire_check"):
        import copy
        item = copy.deepcopy(item)
        if item_key == "check1_py":
            item["asset"] = "assets/Paraguay/Чек/jose/Check1 jose.jpg"
            item["fields"] = [f for f in item["fields"] if f["key"] != "name_1"]
        elif item_key == "check2_py":
            item["asset"] = "assets/Paraguay/Чек/jose/Check2 jose.jpg"
            item["fields"] = [f for f in item["fields"] if f["key"] != "name2"]
        elif item_key == "check3_py":
            item["asset"] = "assets/Paraguay/Чек/jose/Check3 jose.jpg"
            item["fields"] = [f for f in item["fields"] if f["key"] != "sender_name"]
        elif item_key == "check1_uy":
            item["asset"] = "assets/Uruguay/Чек/jose/Check1.jpg"
            item["fields"] = [f for f in item["fields"] if f["key"] not in ("payer_2", "acc_2")]
        elif item_key == "check4_uy":
            item["asset"] = "assets/Uruguay/Чек/jose/Check4.jpg"
            item["fields"] = [f for f in item["fields"] if f["key"] not in ("sender_name", "account")]
        elif item_key == "check_doc":
            item["asset"] = "assets/Bolivia/Чек/jose/Check1.jpg"
            item["fields"] = [f for f in item["fields"] if f["key"] != "sender_name"]
        elif item_key == "fire_check":
            item["asset"] = "assets/Bolivia/Чек/jose/Check2.jpg"
            item["fields"] = [f for f in item["fields"] if f["key"] != "origen"]
    return item


def _askable_fields(fields: list[dict]) -> list[dict]:
    return [f for f in fields if f.get("prompt", "").strip()]


def _is_image_field(field: dict) -> bool:
    return field.get("text_config", {}).get("image_paste", False)


def _build_checklist(item_label: str, askable: list[dict],
                     done_step: int, values: dict) -> str:
    lines = [f"🖼 Шаблон: <b>{item_label}</b>\n"]
    for i, field in enumerate(askable):
        short = field["prompt"].split("(")[0].strip()
        if i < done_step:
            val_str = "✓" if _is_image_field(field) else values.get(field["key"], "")
            lines.append(f"🟢 {i + 1}. {short} [{val_str}]")
        else:
            lines.append(f"⚪️ {i + 1}. {short}")
    return "\n".join(lines)


def _has_preview(item: dict) -> str | None:
    p = item.get("preview")
    if not p:
        return None
    full = os.path.normpath(os.path.join(BASE_DIR, p))
    return full if os.path.exists(full) else None


async def _update_checklist(bot, chat_id: int, msg_id: int, has_photo: bool,
                             text: str, reply_markup=None):
    try:
        if has_photo:
            await bot.edit_message_caption(
                chat_id=chat_id, message_id=msg_id,
                caption=text, parse_mode="HTML", reply_markup=reply_markup
            )
        else:
            await bot.edit_message_text(
                chat_id=chat_id, message_id=msg_id,
                text=text, parse_mode="HTML", reply_markup=reply_markup
            )
    except TelegramBadRequest:
        pass


async def _try_delete(bot, chat_id: int, message_id: int):
    try:
        await bot.delete_message(chat_id=chat_id, message_id=message_id)
    except TelegramBadRequest:
        pass


async def _finish_render(message: Message, item_key: str, values: dict, item: dict,
                        checklist_msg_id: int = None, has_photo: bool = False,
                        geo: str = "bo"):
    try:
        # Удаляем чеклист/превью
        if checklist_msg_id:
            await _try_delete(message.bot, message.chat.id, checklist_msg_id)

        render_mode = item.get("render_mode")
        wait_text = "🎞 Создание видео..." if render_mode == "video" else "🖼 Создание изображения..."
        wait_msg = await message.answer(wait_text)
        log.render_start(message.from_user.id, item.get("label", item_key), message.from_user.username)
        if render_mode == "support_bubbles":
            from utils.renderer import render_support, FONTS, BASE_DIR
            import os
            asset_path = item["asset"]
            asset_path = os.path.normpath(os.path.join(BASE_DIR, asset_path))
            font_path  = os.path.join(BASE_DIR, FONTS["montserrat"])
            media_bytes  = render_support(values, asset_path, font_path, font_size_pt=20)
        elif render_mode == "video":
            from utils.renderer import render_video
            media_bytes = render_video(item_key, values, geo, item=item)
        else:
            from utils.renderer import render_image
            media_bytes = render_image(item_key, values, geo, item=item)

        # Небольшая пауза чтобы пользователь увидел сообщение
        import asyncio
        await asyncio.sleep(3.8)

        # Удаляем промежуточное сообщение
        await _try_delete(message.bot, message.chat.id, wait_msg.message_id)

        log.render_done(message.from_user.id, item.get("label", item_key), message.from_user.username)
        
        warning_suffix = ""
        try:
            from data.db import get_available_names
            rem_count = len(get_available_names())
            if rem_count <= 50:
                warning_suffix = f"\n\n⚠️ <b>Внимание! Имена заканчиваются: осталось всего {rem_count} шт. Пожалуйста, пополните name.json!</b>"
        except Exception:
            pass

        if render_mode == "video":
            await message.answer_video(
                video=BufferedInputFile(media_bytes.read(), filename="result.mp4"),
                caption=f"✅ Готово! Видео: <b>{item['label']}</b>" + warning_suffix,
                parse_mode="HTML",
                reply_markup=after_render_kb(geo, item_key)
            )
        else:
            await message.answer_photo(
                photo=BufferedInputFile(media_bytes.read(), filename="result.png"),
                caption=f"✅ Готово! Шаблон: <b>{item['label']}</b>" + warning_suffix,
                parse_mode="HTML",
                reply_markup=after_render_kb(geo, item_key)
            )
    except Exception as e:
        lbl = item.get("label", item_key) if item else item_key
        log.render_error(message.from_user.id, lbl, str(e), message.from_user.username)
        await message.answer(f"❌ Ошибка рендеринга: {e}")


async def _return_to_last_section(call: CallbackQuery, state: FSMContext):
    """Возвращает пользователя в последний открытый раздел."""
    data = await state.get_data()
    last_line    = data.get("last_line")
    last_section = data.get("last_section")
    geo          = data.get("current_geo")
    role = get_role_string(call.from_user.id)

    if last_section and last_line and geo:
        text = "📄 Выберите шаблон:"
        kb   = items_menu(geo, last_line, last_section)
    elif last_line and geo:
        text = "📂 Выберите раздел:"
        kb   = sections_menu(geo, last_line)
    elif geo:
        text = "📂 Выберите категорию:"
        kb   = main_menu(role, geo)
    else:
        text = "🌍 Выберите регион:"
        kb   = geo_menu_for(call.from_user.id, role)

    await call.message.answer(text, reply_markup=kb)


# ─────────────────────────── handlers ────────────────────────────────────────

PREVIEW_FILE_IDS = {}

@router.callback_query(F.data.startswith("item:"))
async def cb_item_selected(call: CallbackQuery, state: FSMContext):
    parts    = call.data.split(":")
    geo      = parts[1] if len(parts) > 2 else "bo"
    item_key = parts[2] if len(parts) > 2 else parts[1]

    s = get_settings(call.from_user.id)
    if item_key in ("fire_check", "check4_bo", "check1_py", "check2_py", "check3_py", "check3_bo", "check1_uy", "check2_uy", "check4_uy"):
        blur_mode = "with_blur" if s.get("blur_enabled", 1) else "no_blur"
    elif item_key == "payment1_py":
        blur_mode = "with_blur" if s.get("blur_qr_enabled", 1) else "no_blur"
    else:
        blur_mode = "no_blur"

    await state.update_data(current_geo=geo)
    item = _get_item_for_user(item_key, geo, call.from_user.id)

    if not item:
        await call.answer("❌ Шаблон не найден.", show_alert=True)
        return

    import copy
    askable = copy.deepcopy(_askable_fields(item["fields"]))
    
    if blur_mode == "with_blur":
        if item_key == "fire_check":
            for f in askable:
                if f["key"] in ("destino", "origen"):
                    f["prompt"] = f["prompt"].split("\n")[0] + "\n(Бот сам сгенерирует рандомный счёт, введите только 4 слова ФИО)"
        elif item_key == "check4_bo":
            askable = [f for f in askable if f["key"] != "sender_acc"]
        elif item_key == "payment1_py":
            askable = [f for f in askable if f["key"] != "account"]

    # Auto-generate x_amount for rocket templates if present
    has_x_amount = any(f["key"] == "x_amount" for f in askable)
    if has_x_amount:
        askable = [f for f in askable if f["key"] != "x_amount"]

    log.open_template(call.from_user.id, item.get("label", item_key), call.from_user.username)

    if not askable:
        await state.clear()
        await _finish_render(call.message, item_key, {}, item, geo=geo)
        await call.answer()
        return

    preview_path = _has_preview(item)
    has_photo = preview_path is not None

    s = get_settings(call.from_user.id)
    s_temp = s.copy()
    s_temp["perc_sign"] = "+"

    auto_values = {"_blur_mode": blur_mode}
    if has_x_amount:
        import random
        r_min = s.get("rand_rocket_min", 10)
        r_max = s.get("rand_rocket_max", 1000)
        if r_min > r_max:
            r_min, r_max = r_max, r_min
        auto_values["x_amount"] = str(random.randint(r_min, r_max))

    if item_key == "check4_bo" and blur_mode == "with_blur":
        import random
        auto_values["sender_acc"] = "1" + "".join([str(random.randint(0, 9)) for _ in range(9)])
    elif item_key == "payment1_py":
        import random
        if blur_mode == "with_blur":
            auto_values["account"] = "922" + "".join([str(random.randint(0, 9)) for _ in range(8)])
        
    try:
        start_step = _advance_steps(askable, 0, auto_values, s, item, item_key)
    except ValueError:
        await call.answer("❌ В списке name.json не осталось имен! Пополните список или отключите 'Рандом имен' в настройках.", show_alert=True)
        return

    if start_step >= len(askable):
        await state.clear()
        await _finish_render(call.message, item_key, auto_values, item, geo=geo)
        await call.answer()
        return

    checklist = _build_checklist(item["label"], askable, done_step=start_step, values=auto_values)
    caption = checklist + f"\n\n{askable[start_step]['prompt']}"

    kb = _get_field_keyboard(askable[start_step]["key"], s_temp, item_key)

    try:
        if call.message.caption and "✅ Готово!" in call.message.caption:
            pass
        else:
            await call.message.delete()
    except Exception:
        pass

    if has_photo:
        file_id = PREVIEW_FILE_IDS.get(item_key)
        if preview_path.lower().endswith(".mp4"):
            if file_id:
                sent = await call.message.answer_video(
                    video=file_id,
                    caption=caption,
                    parse_mode="HTML",
                    reply_markup=kb
                )
            else:
                msg = await call.message.answer("⏳ Загружаю превью видео, подождите...")
                try:
                    sent = await call.message.answer_video(
                        video=FSInputFile(preview_path),
                        caption=caption,
                        parse_mode="HTML",
                        reply_markup=kb,
                        request_timeout=300
                    )
                    PREVIEW_FILE_IDS[item_key] = sent.video.file_id
                except Exception as e:
                    await call.message.answer(f"❌ Ошибка загрузки превью: {e}")
                    return
                finally:
                    await _try_delete(call.bot, call.message.chat.id, msg.message_id)
        else:
            if file_id:
                sent = await call.message.answer_photo(
                    photo=file_id,
                    caption=caption,
                    parse_mode="HTML",
                    reply_markup=kb
                )
            else:
                sent = await call.message.answer_photo(
                    photo=FSInputFile(preview_path),
                    caption=caption,
                    parse_mode="HTML",
                    reply_markup=kb
                )
                PREVIEW_FILE_IDS[item_key] = sent.photo[-1].file_id
    else:
        sent = await call.message.answer(
            caption, parse_mode="HTML", reply_markup=kb
        )

    # Сохраняем state (last_line/last_section остаются из catalog)
    prev_data = await state.get_data()
    await state.set_state(RenderStates.collecting)
    await state.update_data(
        item_key=item_key,
        askable=askable,
        step=start_step,
        values=auto_values,
        checklist_msg_id=sent.message_id,
        has_photo=has_photo,
        last_line=prev_data.get("last_line"),
        last_section=prev_data.get("last_section"),
        time_suffix=s["time_suffix"],
        perc_sign="+",
    )
    try:
        await call.answer()
    except Exception:
        pass


@router.message(RenderStates.collecting, CommandStart())
async def cmd_start_in_render(message: Message, state: FSMContext):
    """Обрабатывает /start в процессе рендера — сбрасывает и показывает главное меню."""
    data = await state.get_data()
    msg_id = data.get("checklist_msg_id")
    if msg_id:
        await _try_delete(message.bot, message.chat.id, msg_id)
    await state.clear()
    await _try_delete(message.bot, message.chat.id, message.message_id)
    from data.db import is_admin as _is_admin_check
    from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
    from handlers.catalog import _start_kb
    await message.answer("👋 Добро пожаловать!", reply_markup=_start_kb(message.from_user.id))


@router.message(RenderStates.collecting, F.text, ~Command(commands=["start"]))
async def collect_text_field(message: Message, state: FSMContext):
    try:
        data = await state.get_data()
        
        # Проверяем, что все необходимые данные присутствуют
        if not data:
            import logging
            logging.warning(f"collect_text: пустые данные state для {message.from_user.id}")
            await message.answer("⚠️ Ошибка: состояние пусто. Начните заново.")
            return
            
        askable: list = data.get("askable")
        step: int = data.get("step")
        values: dict = data.get("values")
        item_key: str = data.get("item_key")
        msg_id: int = data.get("checklist_msg_id")
        has_photo: bool = data.get("has_photo", False)
        geo: str = data.get("current_geo", "bo")
        
        if not all([askable, isinstance(step, int), values is not None, item_key, msg_id is not None]):
            import logging
            logging.warning(f"collect_text: неполные данные state для {message.from_user.id}: {list(data.keys())}")
            await message.answer("⚠️ Ошибка: некорректное состояние. Начните заново с /start")
            await state.clear()
            return
        
        item = _get_item_for_user(item_key, geo, message.from_user.id)
        if not item:
            import logging
            logging.warning(f"collect_text: шаблон {item_key} не найден для {message.from_user.id}")
            await message.answer(f"⚠️ Ошибка: шаблон {item_key} не найден")
            await state.clear()
            return

        if _is_image_field(askable[step]):
            await _try_delete(message.bot, message.chat.id, message.message_id)
            await message.answer("⚠️ Это поле ожидает <b>фото</b>. Отправьте изображение.", parse_mode="HTML")
            return

        # Удаляем пользовательское сообщение
        await _try_delete(message.bot, message.chat.id, message.message_id)

        val = message.text.strip()
        
        # Если это текстовое поле для ФИО и юзер ввел 4 слова, пытаемся его отформатировать
        if _is_name_field(askable[step]["key"]):
            val = _format_name(val, item)
        
        # Применяем суффикс времени если он выбран в state
        if data.get("time_suffix") and "time" in askable[step]["key"] and item_key not in ("qr_pe", "check1_py"):
            if "M." not in val.upper():  # Если пользователь сам не написал AM/PM
                suff = data['time_suffix']
                if item_key in ("check_doc", "check_pe"):
                    suff = suff.lower().replace("a.m.", "a. m.").replace("p.m.", "p. m.")
                if item_key == "check3_pe":
                    suff = suff.replace(".", "")
                val = f"{val} {suff}"

        # Если пользователь сам ввел AM/PM в чеке — тоже в нижний регистр
        if item_key in ("check_doc", "check_pe") and "time" in askable[step]["key"]:
            val = val.replace("AM", "a. m.").replace("PM", "p. m.").replace("A.M.", "a. m.").replace("P.M.", "p. m.")

        if item_key == "check3_pe" and "time" in askable[step]["key"]:
            val = val.replace(".", "").upper()

        # Автоматический подгон даты для чеков
        if "date" in askable[step]["key"]:
            val = _format_date_for_item(val, item)
        if item_key in ("check2_pe", "check4_pe") and askable[step]["key"] == "time":
            val = val.replace("A.M.", "am.").replace("P.M.", "pm.").replace("a. m.", "am.").replace("p. m.", "pm.")\
                     .replace("a.m.", "am.").replace("p.m.", "pm.").replace("AM", "am.").replace("PM", "pm.")

        if askable[step]["key"] == "percentage":
            if not val.startswith("+") and not val.startswith("-"):
                val = data.get("perc_sign", "+") + val

        values[askable[step]["key"]] = val
        if item_key == "check2_py" and askable[step]["key"] == "bank":
            values["_bank_image"] = f"assets/Paraguay/Чек/bank/{val}.jpg"
        if item_key == "check3_py" and askable[step]["key"] == "bank":
            values["_bank_image"] = f"assets/Paraguay/Чек/bank2/{val}.png"
        done_step = step + 1

        s = get_settings(message.from_user.id)
        s_temp = s.copy()
        s_temp["perc_sign"] = data.get("perc_sign", "+")

        try:
            done_step = _advance_steps(askable, done_step, values, s, item, item_key)
        except ValueError:
            await message.answer("❌ В списке name.json не осталось имен! Пополните список или отключите 'Рандом имен' в настройках.")
            await state.clear()
            return

        if done_step < len(askable):
            checklist = _build_checklist(item["label"], askable, done_step=done_step, values=values)
            await _update_checklist(message.bot, message.chat.id, msg_id, has_photo,
                                    checklist + f"\n\n{askable[done_step]['prompt']}",
                                    reply_markup=_get_field_keyboard(askable[done_step]["key"], s_temp, item_key))
            await state.update_data(step=done_step, values=values, time_suffix=s["time_suffix"])
        else:
            await state.clear()
            await _finish_render(message, item_key, values, item,
                                 checklist_msg_id=msg_id, has_photo=has_photo,
                                 geo=geo)

    except Exception as e:
        import logging
        logging.exception(f"Error in collect_text_field for user {message.from_user.id}: {e}")
        await state.clear()
        try:
            await message.answer(f"❌ Произошла ошибка: {e}\n\nНажмите /start и попробуйте снова.")
        except Exception as send_err:
            logging.exception(f"Ошибка при отправке сообщения об ошибке: {send_err}")


@router.message(RenderStates.collecting, F.photo | F.document)
async def collect_photo_field(message: Message, state: FSMContext):
    try:
        data = await state.get_data()
        
        # Проверяем, что все необходимые данные присутствуют
        if not data:
            import logging
            logging.warning(f"collect_photo: пустые данные state для {message.from_user.id}")
            await message.answer("⚠️ Ошибка: состояние пусто. Начните заново.")
            return
            
        askable: list = data.get("askable")
        step: int = data.get("step")
        values: dict = data.get("values")
        item_key: str = data.get("item_key")
        msg_id: int = data.get("checklist_msg_id")
        has_photo: bool = data.get("has_photo", False)
        geo: str = data.get("current_geo", "bo")
        
        if not all([askable, isinstance(step, int), values is not None, item_key, msg_id is not None]):
            import logging
            logging.warning(f"collect_photo: неполные данные state для {message.from_user.id}")
            await message.answer("⚠️ Ошибка: некорректное состояние. Начните заново с /start")
            await state.clear()
            return
            
        item = _get_item_for_user(item_key, geo, message.from_user.id)
        if not item:
            import logging
            logging.warning(f"collect_photo: шаблон {item_key} не найден для {message.from_user.id}")
            await message.answer(f"⚠️ Ошибка: шаблон {item_key} не найден")
            await state.clear()
            return

        if not _is_image_field(askable[step]):
            await _try_delete(message.bot, message.chat.id, message.message_id)
            await message.answer("⚠️ Это поле ожидает <b>текст</b>, а не фото.", parse_mode="HTML")
            return

        await _try_delete(message.bot, message.chat.id, message.message_id)

        if message.photo:
            file_id = message.photo[-1].file_id
        elif message.document:
            if not message.document.mime_type or not message.document.mime_type.startswith("image/"):
                await message.answer("⚠️ Пожалуйста, отправьте именно изображение (в виде фото или файла).", parse_mode="HTML")
                return
            file_id = message.document.file_id
        else:
            return

        file = await message.bot.get_file(file_id)
        file_bytes = await message.bot.download_file(file.file_path)
        values[askable[step]["key"]] = file_bytes.read()
        done_step = step + 1

        s = get_settings(message.from_user.id)
        try:
            done_step = _advance_steps(askable, done_step, values, s, item, item_key)
        except ValueError:
            await message.answer("❌ В списке name.json не осталось имен! Пополните список или отключите 'Рандом имен' в настройках.")
            await state.clear()
            return

        if done_step < len(askable):
            checklist = _build_checklist(item["label"], askable, done_step=done_step, values=values)
            await _update_checklist(message.bot, message.chat.id, msg_id, has_photo,
                                    checklist + f"\n\n{askable[done_step]['prompt']}",
                                    reply_markup=_get_field_keyboard(askable[done_step]["key"], s, item_key))
            await state.update_data(step=done_step, values=values, time_suffix=s["time_suffix"])
        else:
            await state.clear()
            await _finish_render(message, item_key, values, item,
                                 checklist_msg_id=msg_id, has_photo=has_photo,
                                 geo=geo)

    except Exception as e:
        import logging
        logging.exception(f"Error in collect_photo_field for user {message.from_user.id}: {e}")
        await state.clear()
        try:
            await message.answer(f"❌ Произошла ошибка при обработке фото: {e}\n\nНажмите /start и попробуйте снова.")
        except Exception as send_err:
            logging.exception(f"Ошибка при отправке сообщения об ошибке: {send_err}")


# ── Отмена ────────────────────────────────────────────────────────────────────

@router.callback_query(F.data == "cancel")
async def cb_cancel(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    has_photo = data.get("has_photo", False)
    msg_id    = data.get("checklist_msg_id")

    # Удаляем сообщение с превью/чеклистом
    if msg_id:
        await _try_delete(call.bot, call.message.chat.id, msg_id)
    if has_photo:
        await _try_delete(call.bot, call.message.chat.id, call.message.message_id)

    await state.clear()
    log.cancel(call.from_user.id, data.get("item_key", "?"), call.from_user.username)

    # Возвращаем в выбор категории
    role = get_role_string(call.from_user.id)
    geo: str | None = data.get("current_geo")
    if geo:
        await call.message.answer("📂 Выберите категорию:", reply_markup=main_menu(role, geo))
    else:
        await call.message.answer("🌍 Выберите регион:", reply_markup=geo_menu_for(call.from_user.id, role))
    try:
        await call.answer()
    except Exception:
        pass


# ── Главное меню после рендера ────────────────────────────────────────────────

@router.callback_query(F.data == "back:main")
async def cb_back_main_from_render(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await state.clear()
    role = get_role_string(call.from_user.id)
    geo: str | None = data.get("current_geo")
    # Всегда отправляем новое сообщение — не трогаем фото с результатом
    if geo:
        await call.message.answer("📂 Выберите категорию:", reply_markup=main_menu(role, geo))
    else:
        await call.message.answer("🌍 Выберите регион:", reply_markup=geo_menu_for(call.from_user.id, role))
    try:
        await call.answer()
    except Exception:
        pass


# ── Shortcuts (Random, Pin, Suffix) ──────────────────────────────────────────

@router.callback_query(F.data.startswith("render:"))
async def cb_render_shortcuts(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    if not data or "askable" not in data:
        try:
            await call.answer()
        except Exception:
            pass
        return

    askable:   list = data["askable"]
    step:      int  = data["step"]
    values:    dict = data["values"]
    item_key:  str  = data["item_key"]
    msg_id:    int  = data["checklist_msg_id"]
    has_photo: bool = data["has_photo"]
    geo: str = data.get("current_geo", "bo")
    item = _get_item_for_user(item_key, geo, call.from_user.id)
    
    parts = call.data.split(":")
    action = parts[1]
    
    val = None
    if action == "pin_date":
        s = get_settings(call.from_user.id)
        val = s["pinned_date"]
    elif action == "pin_name":
        s = get_settings(call.from_user.id)
        val = s["pinned_name"]
    elif action == "pin_bank":
        s = get_settings(call.from_user.id)
        val = s["pinned_bank"]
    elif action == "pin": # Fallback для совместимости если где-то осталось
        s = get_settings(call.from_user.id)
        val = s["pinned_date"]
    elif action == "random":
        s = get_settings(call.from_user.id)
        key = askable[step]["key"]
        if key in ("sum", "amount", "commission"):
            val = str(random.randint(s["rand_min"], s["rand_max"]))
        elif key == "x_amount":
            r_min = s.get("rand_rocket_min", 10)
            r_max = s.get("rand_rocket_max", 1000)
            if r_min > r_max:
                r_min, r_max = r_max, r_min
            val = str(random.randint(r_min, r_max))
        elif key == "percentage":
            val_float = random.uniform(s.get("rand_percent_min", 1.0), s.get("rand_percent_max", 100.0))
            sign = data.get("perc_sign", "+")
            formatted = f"{abs(val_float):,.2f}"
            val = f"{sign}{formatted}"
        elif key == "bank":
            val = random.choice(item.get("banks", ["Banco"]))
        elif key == "number":
            val = "".join([str(random.randint(0, 9)) for _ in range(8)])
        elif key in ("account", "sender_acc", "receiver_acc", "acc_num", "acc_num_2"):
            if key == "sender_acc" and item_key == "check2_uy":
                length = 10
            elif key == "receiver_acc" and item_key == "check2_uy":
                length = 7
            elif item_key == "check_pe":
                length = 3
            elif item_key == "qr_pe":
                length = 9
            elif item_key == "check2_py":
                length = 11
            elif item_key == "check3_py":
                length = 7
            elif item_key == "check2_uy":
                length = 10
            elif item_key == "check1_py":
                length = 9
            elif item_key == "check4_uy" and key in ("account", "receiver_acc"):
                length = 7
            else:
                length = 8
            
            if item_key == "check3_bo":
                val = "1" + "".join([str(random.randint(0, 9)) for _ in range(13)])
            elif item_key == "check4_bo" and key == "sender_acc":
                val = "".join([str(random.randint(0, 9)) for _ in range(10)])
            elif item_key == "payment1_py" and key == "account":
                val = "922" + "".join([str(random.randint(0, 9)) for _ in range(8)])
            else:
                val = "".join([str(random.randint(0, 9)) for _ in range(length)])
        elif key == "account_end":
            if item_key == "check2_py":
                length = 3
                val = "".join([str(random.randint(0, 9)) for _ in range(length)])
        elif key in ("acc_1", "acc_2"):
            val = "".join([str(random.randint(0, 9)) for _ in range(7)])
        elif key == "ref_num":
            val = "".join([str(random.randint(0, 9)) for _ in range(8)])
        elif key == "transaction":
            if item_key == "fire_check":
                digits = 9
                val = "".join([str(random.randint(0, 9)) for _ in range(digits)])
            elif item_key == "check_pe":
                digits = 8
                val = "".join([str(random.randint(0, 9)) for _ in range(digits)])
            elif item_key == "check2_py":
                val = "".join(random.choices("0123456789abcdef", k=24))
            elif item_key == "check1_py":
                digits = 13
                val = "".join([str(random.randint(0, 9)) for _ in range(digits)])
            elif item_key == "check4_bo":
                val = "1" + "".join([str(random.randint(0, 9)) for _ in range(18)])
            else:
                digits = 9
                val = "".join([str(random.randint(0, 9)) for _ in range(digits)])
        elif key == "order":
            # fire_check: 20-значный номер заказа Yasta
            digits = 20 if item_key == "fire_check" else 12
            val = "".join([str(random.randint(0, 9)) for _ in range(digits)])
        elif key == "operation":
            val = "".join([str(random.randint(0, 9)) for _ in range(8)])
        elif key in ("card_recipient", "card_sender"):
            val = "".join([str(random.randint(0, 9)) for _ in range(4)])
        elif key == "phone":
            # Генерация перуанского номера: +51 9XX XXX XXX
            if item_key.endswith("_pe") or "pe" in item_key:
                val = f"+51 9{''.join([str(random.randint(0, 9)) for _ in range(8)])}"
            else:
                val = f"+{''.join([str(random.randint(0, 9)) for _ in range(11)])}"
        else:
            val = "0"
    elif action == "random_name":
        from data.db import get_and_blacklist_random_name
        try:
            val = get_and_blacklist_random_name()
            val = _format_name(val, item)
        except ValueError:
            try:
                await call.answer("❌ В списке name.json не осталось доступных имен!", show_alert=True)
            except Exception:
                pass
            return
    elif action == "perc_sign":
        new_sign = parts[2]
        await state.update_data(perc_sign=new_sign)
        s = get_settings(call.from_user.id)
        s_temp = s.copy()
        s_temp["perc_sign"] = new_sign
        try:
            await call.message.edit_reply_markup(reply_markup=_get_field_keyboard(askable[step]["key"], s_temp, item_key))
        except Exception:
            pass
        try:
            await call.answer(f"Знак изменен на {new_sign}")
        except Exception:
            pass
        return
    elif action == "suffix":
        suffix_type = parts[2]
        new_suffix = None
        if suffix_type == "AM":
            new_suffix = "A.M."
        elif suffix_type == "PM":
            new_suffix = "P.M."
        
        await state.update_data(time_suffix=new_suffix)
        
        # Обновляем клавиатуру чтобы показать выбор
        s = get_settings(call.from_user.id)
        s_temp = s.copy()
        s_temp["time_suffix"] = new_suffix
        
        try:
            await call.message.edit_reply_markup(reply_markup=_get_field_keyboard(askable[step]["key"], s_temp, item_key))
        except Exception:
            pass
        try:
            await call.answer(f"Выбрано: {new_suffix or 'Без суффикса'}")
        except Exception:
            pass
        return
    elif action == "set":
        val = parts[2]
    else:
        try:
            await call.answer()
        except Exception:
            pass
        return

    # Если мы здесь, значит получили значение (pin или random)
    # Конвертация даты в испанский формат для чека Перу
    if item_key == "check_pe" and askable[step]["key"] == "date":
        val = _to_es_date(val)
    if item_key == "check2_pe" and askable[step]["key"] == "date":
        val = _to_es_date2(val)
    if item_key == "check1_uy" and askable[step]["key"] == "date":
        val = _to_es_date_uy(val)
    if item_key == "check2_uy" and askable[step]["key"] == "date":
        val = val.replace(".", "/")
    if item_key == "check2_py" and askable[step]["key"] == "date":
        val = _to_es_date_py(val)
    if item_key == "check3_py" and askable[step]["key"] == "date":
        val = _to_es_date_py_check3(val)
    values[askable[step]["key"]] = val
    if item_key == "check2_py" and askable[step]["key"] == "bank":
        values["_bank_image"] = f"assets/Paraguay/Чек/bank/{val}.jpg"
    if item_key == "check3_py" and askable[step]["key"] == "bank":
        values["_bank_image"] = f"assets/Paraguay/Чек/bank2/{val}.png"
    done_step = step + 1

    s = get_settings(call.from_user.id)
    try:
        done_step = _advance_steps(askable, done_step, values, s, item, item_key)
    except ValueError:
        await call.answer("❌ В списке name.json не осталось имен! Пополните список или отключите 'Рандом имен' в настройках.", show_alert=True)
        await state.clear()
        return

    if done_step < len(askable):
        s_temp = s.copy()
        s_temp["perc_sign"] = data.get("perc_sign", "+")
        checklist = _build_checklist(item["label"], askable, done_step=done_step, values=values)
        await _update_checklist(call.bot, call.message.chat.id, msg_id, has_photo,
                                checklist + f"\n\n{askable[done_step]['prompt']}",
                                reply_markup=_get_field_keyboard(askable[done_step]["key"], s_temp, item_key))
        await state.update_data(step=done_step, values=values, time_suffix=s["time_suffix"])
        try:
            await call.answer()
        except Exception:
            pass
    else:
        await state.clear()
        try:
            await call.answer()  # отвечаем ДО рендера, иначе истечёт таймаут
        except Exception:
            pass
        await _finish_render(call.message, item_key, values, item,
                             checklist_msg_id=msg_id, has_photo=has_photo,
                             geo=geo)
