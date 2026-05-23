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

from data.config import CATALOG, GEO_CATALOG
from data.db import get_role, get_settings
from keyboards.inline import cancel_kb, after_render_kb, main_menu, sections_menu, items_menu, geo_menu, geo_menu_for
from utils.logger import log
import random

router = Router()


def _get_random_bank(item_key: str) -> str:
    """Возвращает рандомный банк в зависимости от шаблона."""
    if item_key.endswith("_pe"):
        return random.choice(["BCP", "BBVA", "Scotiabank", "Interbank", "Banco de la Nación", "Banco Falabella Perú"])
    elif item_key.endswith("_py"):
        return random.choice(["ATLAS", "CONTINENTAL", "SOLAR", "INTERFISA", "SUDAMERIS", "GNB", "familiar", "interfisa"])
    else:
        return random.choice(["Banco Mercantil Santa Cruz", "Banco Fie", "Banco Bisa", "Banco Union", "Banco Económico", "Banco Nacional de Bolivia"])

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

BASE_DIR = os.path.normpath(os.path.join(os.path.dirname(__file__), ".."))


class RenderStates(StatesGroup):
    collecting = State()


def _get_field_keyboard(field_key: str, s: dict, item_key: str = None) -> InlineKeyboardMarkup:
    buttons = []
    
    # 🎲 Рандомайзер сумм
    if s["rand_enabled"] and field_key in ("sum", "amount", "commission"):
        buttons.append([InlineKeyboardButton(text="🎲 Сгенерировать", callback_data="render:random")])
        
    # 🎲 Рандомайзер счетов
    if s.get("rand_acc_enabled") and field_key in ("number", "account", "transaction", "operation", "card_recipient", "card_sender", "phone", "order", "acc_1", "acc_2", "ref_num"):
        buttons.append([InlineKeyboardButton(text="🎲 Сгенерировать", callback_data="render:random")])
        
    # 🎲 Рандомайзер процентов
    if s.get("rand_percent_enabled") and field_key == "percentage":
        buttons.append([InlineKeyboardButton(text="🎲 Сгенерировать", callback_data="render:random")])
        
    # 🎲 Рандомайзер банков
    if s.get("rand_bank_enabled") and field_key == "bank":
        buttons.append([InlineKeyboardButton(text="🎲 Сгенерировать", callback_data="render:random")])
        
    if field_key == "bank" and item_key == "check2_py":
        buttons.append([
            InlineKeyboardButton(text="ATLAS", callback_data="render:set:ATLAS"),
            InlineKeyboardButton(text="CONTINENTAL", callback_data="render:set:CONTINENTAL")
        ])
        buttons.append([
            InlineKeyboardButton(text="SOLAR", callback_data="render:set:SOLAR"),
            InlineKeyboardButton(text="INTERFISA", callback_data="render:set:INTERFISA")
        ])
        buttons.append([
            InlineKeyboardButton(text="SUDAMERIS", callback_data="render:set:SUDAMERIS"),
            InlineKeyboardButton(text="GNB", callback_data="render:set:GNB")
        ])
        buttons.append([
            InlineKeyboardButton(text="familiar", callback_data="render:set:familiar"),
            InlineKeyboardButton(text="interfisa", callback_data="render:set:interfisa")
        ])
        
    # 📅 Закрепленная дата
    if s["pinned_date"] and "date" in field_key:
        buttons.append([InlineKeyboardButton(text=f"📅 {s['pinned_date']}", callback_data="render:pin_date")])
        
    # 👤 Закрепленное ФИО
    if s.get("pinned_name") and field_key in ("name", "fullname"):
        buttons.append([InlineKeyboardButton(text=f"👤 {s['pinned_name']}", callback_data="render:pin_name")])
        
    # 🏦 Закрепленный банк
    if s.get("pinned_bank") and field_key == "bank":
        buttons.append([InlineKeyboardButton(text=f"🏦 {s['pinned_bank']}", callback_data="render:pin_bank")])
        
    # 🕒 AM/PM
    if "time" in field_key and item_key not in ("rd6", "rd7", "qr_pe", "check1_py"):
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
    _ALL_RD_AMOUNTS = {**_PE_RD_AMOUNTS, **_BO_RD_AMOUNTS}
    if item_key in _ALL_RD_AMOUNTS:
        _fkey, _label, _val = _ALL_RD_AMOUNTS[item_key]
        if field_key == _fkey:
            buttons.append([InlineKeyboardButton(
                text=f"💡 Рекомендация {_label}",
                callback_data=f"render:set:{_val}"
            )])
    
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
            from utils.renderer import render_support, FONTS, BASE_DIR, _resolve_geo_asset_path
            import os
            asset_path = _resolve_geo_asset_path(item["asset"], geo)
            asset_path = os.path.normpath(os.path.join(BASE_DIR, asset_path))
            font_path  = os.path.join(BASE_DIR, FONTS["montserrat"])
            media_bytes  = render_support(values, asset_path, font_path, font_size_pt=20)
        elif render_mode == "video":
            from utils.renderer import render_video
            media_bytes = render_video(item_key, values, geo)
        else:
            from utils.renderer import render_image
            media_bytes = render_image(item_key, values, geo)

        # Небольшая пауза чтобы пользователь увидел сообщение
        import asyncio
        await asyncio.sleep(3.8)

        # Удаляем промежуточное сообщение
        await _try_delete(message.bot, message.chat.id, wait_msg.message_id)

        log.render_done(message.from_user.id, item.get("label", item_key), message.from_user.username)
        
        if render_mode == "video":
            await message.answer_video(
                video=BufferedInputFile(media_bytes.read(), filename="result.mp4"),
                caption=f"✅ Готово! Видео: <b>{item['label']}</b>",
                parse_mode="HTML",
                reply_markup=after_render_kb(geo, item_key)
            )
        else:
            await message.answer_photo(
                photo=BufferedInputFile(media_bytes.read(), filename="result.png"),
                caption=f"✅ Готово! Шаблон: <b>{item['label']}</b>",
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
    role = get_role(call.from_user.id)

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
    await state.update_data(current_geo=geo)
    item = _find_item(item_key, geo)

    if not item:
        await call.answer("❌ Шаблон не найден.", show_alert=True)
        return

    askable = _askable_fields(item["fields"])
    log.open_template(call.from_user.id, item.get("label", item_key), call.from_user.username)

    if not askable:
        await state.clear()
        render_mode = item.get("render_mode")
        wait_text = "⏳ Генерирую видео..." if render_mode == "video" else "⏳ Генерирую..."
        wait = await call.message.answer(wait_text)
        try:
            if render_mode == "video":
                from utils.renderer import render_video
                media_bytes = render_video(item_key, {}, geo)
                await _try_delete(call.bot, call.message.chat.id, wait.message_id)
                await call.message.answer_video(
                    video=BufferedInputFile(media_bytes.read(), filename="result.mp4"),
                    caption=f"✅ Готово! Видео: <b>{item['label']}</b>",
                    parse_mode="HTML",
                    reply_markup=after_render_kb(geo, item_key)
                )
            else:
                from utils.renderer import render_image
                media_bytes = render_image(item_key, {}, geo)
                await _try_delete(call.bot, call.message.chat.id, wait.message_id)
                await call.message.answer_photo(
                    photo=BufferedInputFile(media_bytes.read(), filename="result.png"),
                    caption=f"✅ Готово! Шаблон: <b>{item['label']}</b>",
                    parse_mode="HTML",
                    reply_markup=after_render_kb(geo, item_key)
                )
        except Exception as e:
            await wait.edit_text(f"❌ Ошибка рендеринга: {e}")
        await call.answer()
        return

    preview_path = _has_preview(item)
    has_photo = preview_path is not None

    s = get_settings(call.from_user.id)
    s_temp = s.copy()
    s_temp["perc_sign"] = "+"

    # Авто-рандом банков: если первое поле — bank и рандом включён, пропускаем его
    start_step = 0
    auto_values = {}
    while start_step < len(askable) and askable[start_step]["key"] == "bank" and s.get("rand_bank_enabled") and item_key != "check2_py":
        auto_values["bank"] = _get_random_bank(item_key)
        start_step += 1

    checklist = _build_checklist(item["label"], askable, done_step=start_step, values=auto_values)
    caption = checklist + f"\n\n{askable[start_step]['prompt']}"

    kb = _get_field_keyboard(askable[start_step]["key"], s_temp, item_key)

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
        
        item = _find_item(item_key, geo)
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

        # Конвертация даты в испанский формат для чеков Перу
        if item_key == "check_pe" and askable[step]["key"] == "date":
            val = _to_es_date(val)
        if item_key in ("check2_pe", "check4_pe") and askable[step]["key"] == "date":
            val = _to_es_date2(val)
        if item_key == "check3_pe" and askable[step]["key"] == "date":
            val = _to_es_date3(val)
        if item_key == "fire_check" and askable[step]["key"] == "date":
            val = _to_es_date_fire(val)
        if item_key == "check1_uy" and askable[step]["key"] == "date":
            val = _to_es_date_uy(val)
        if item_key == "check2_py" and askable[step]["key"] == "date":
            val = _to_es_date_py(val)
        if item_key in ("check2_pe", "check4_pe") and askable[step]["key"] == "time":
            val = val.replace("A.M.", "am.").replace("P.M.", "pm.").replace("a. m.", "am.").replace("p. m.", "pm.")\
                     .replace("a.m.", "am.").replace("p.m.", "pm.").replace("AM", "am.").replace("PM", "pm.")

        if askable[step]["key"] == "percentage":
            if not val.startswith("+") and not val.startswith("-"):
                val = data.get("perc_sign", "+") + val

        values[askable[step]["key"]] = val
        if item_key == "check2_py" and askable[step]["key"] == "bank":
            values["_bank_image"] = f"assets/Paraguay/Чек/bank/{val}.jpg"
        done_step = step + 1

        if done_step < len(askable):
            s = get_settings(message.from_user.id)
            s_temp = s.copy()
            s_temp["perc_sign"] = data.get("perc_sign", "+")

            # Авто-рандом банков на промежуточных шагах
            while done_step < len(askable) and askable[done_step]["key"] == "bank" and s.get("rand_bank_enabled") and item_key != "check2_py":
                val_rand = _get_random_bank(item_key)
                values["bank"] = val_rand
                if item_key == "check2_py":
                    values["_bank_image"] = f"assets/Paraguay/Чек/bank/{val_rand}.jpg"
                done_step += 1

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
            
        item = _find_item(item_key, geo)
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

        if done_step < len(askable):
            s = get_settings(message.from_user.id)

            # Авто-рандом банков на промежуточных шагах
            while done_step < len(askable) and askable[done_step]["key"] == "bank" and s.get("rand_bank_enabled"):
                values["bank"] = _get_random_bank(item_key)
                done_step += 1

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
    role = get_role(call.from_user.id)
    geo: str | None = data.get("current_geo")
    if geo:
        await call.message.answer("📂 Выберите категорию:", reply_markup=main_menu(role, geo))
    else:
        await call.message.answer("🌍 Выберите регион:", reply_markup=geo_menu_for(call.from_user.id, role))
    await call.answer()


# ── Главное меню после рендера ────────────────────────────────────────────────

@router.callback_query(F.data == "back:main")
async def cb_back_main_from_render(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await state.clear()
    role = get_role(call.from_user.id)
    geo: str | None = data.get("current_geo")
    # Всегда отправляем новое сообщение — не трогаем фото с результатом
    if geo:
        await call.message.answer("📂 Выберите категорию:", reply_markup=main_menu(role, geo))
    else:
        await call.message.answer("🌍 Выберите регион:", reply_markup=geo_menu_for(call.from_user.id, role))
    await call.answer()


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
    item = _find_item(item_key, geo)
    
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
        elif key == "percentage":
            val_float = random.uniform(s.get("rand_percent_min", 1.0), s.get("rand_percent_max", 100.0))
            sign = data.get("perc_sign", "+")
            formatted = f"{abs(val_float):,.2f}"
            val = f"{sign}{formatted}"
        elif key == "bank":
            val = _get_random_bank(item_key)
        elif key == "number":
            val = "".join([str(random.randint(0, 9)) for _ in range(8)])
        elif key == "account":
            if item_key == "check_pe":
                length = 3
            elif item_key == "qr_pe":
                length = 9
            elif item_key == "check2_py":
                length = 11
            else:
                length = 8
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
    if item_key == "check2_py" and askable[step]["key"] == "date":
        val = _to_es_date_py(val)
    values[askable[step]["key"]] = val
    if item_key == "check2_py" and askable[step]["key"] == "bank":
        values["_bank_image"] = f"assets/Paraguay/Чек/bank/{val}.jpg"
    done_step = step + 1

    if done_step < len(askable):
        s = get_settings(call.from_user.id)
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
