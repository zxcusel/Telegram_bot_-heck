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

from data.config import CATALOG, GEO_CATALOG
from data.db import get_role, get_settings
from keyboards.inline import cancel_kb, after_render_kb, main_menu, sections_menu, items_menu, geo_menu
from utils.logger import log
import random

router = Router()

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

BASE_DIR = os.path.normpath(os.path.join(os.path.dirname(__file__), ".."))


class RenderStates(StatesGroup):
    collecting = State()


def _get_field_keyboard(field_key: str, s: dict, item_key: str = None) -> InlineKeyboardMarkup:
    buttons = []
    
    # 🎲 Рандомайзер
    if s["rand_enabled"] and field_key in ("sum", "amount", "number", "account", "transaction", "operation", "card_recipient", "card_sender"):
        buttons.append([InlineKeyboardButton(text="🎲 Сгенерировать", callback_data="render:random")])
        
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
    if "time" in field_key and item_key not in ("rd6", "rd7"):
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
        
    # 💰 Рекомендация суммы (RD3 PE)
    if field_key == "amount" and item_key == "rd3_pe":
        buttons.append([InlineKeyboardButton(text="Рекомендация S/. 1 165", callback_data="render:set:1 165")])
    elif field_key == "amount" and item_key == "rd2_pe":
        buttons.append([InlineKeyboardButton(text="Рекомендация S/. 809", callback_data="render:set:809")])
    
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
        log.render_error(message.from_user.id, item.get("label", item_key), str(e), message.from_user.username)
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
        kb   = geo_menu()

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

    checklist = _build_checklist(item["label"], askable, done_step=0, values={})
    caption = checklist + f"\n\n{askable[0]['prompt']}"

    preview_path = _has_preview(item)
    has_photo = preview_path is not None

    from keyboards.inline import cancel_kb
    s = get_settings(call.from_user.id)
    kb = _get_field_keyboard(askable[0]["key"], s, item_key)

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
        step=0,
        values={},
        checklist_msg_id=sent.message_id,
        has_photo=has_photo,
        last_line=prev_data.get("last_line"),
        last_section=prev_data.get("last_section"),
        time_suffix=s["time_suffix"], # Копируем из настроек в state на время сессии
    )
    await call.answer()


@router.message(RenderStates.collecting, F.text)
async def collect_text_field(message: Message, state: FSMContext):
    data       = await state.get_data()
    askable:   list = data["askable"]
    step:      int  = data["step"]
    values:    dict = data["values"]
    item_key:  str  = data["item_key"]
    msg_id:    int  = data["checklist_msg_id"]
    has_photo: bool = data["has_photo"]
    geo: str = data.get("current_geo", "bo")
    item = _find_item(item_key, geo)

    if _is_image_field(askable[step]):
        await _try_delete(message.bot, message.chat.id, message.message_id)
        await message.answer("⚠️ Это поле ожидает <b>фото</b>. Отправьте изображение.", parse_mode="HTML")
        return

    await _try_delete(message.bot, message.chat.id, message.message_id)
    
    val = message.text.strip()
    # Применяем суффикс времени если он выбран в state
    if data.get("time_suffix") and "time" in askable[step]["key"]:
        if "M." not in val.upper(): # Если пользователь сам не написал AM/PM
            suff = data['time_suffix']
            if item_key in ("check_doc", "check_pe"):
                suff = suff.lower().replace("a.m.", "a. m.").replace("p.m.", "p. m.")
            val = f"{val} {suff}"
    
    # Если пользователь сам ввел AM/PM в чеке — тоже в нижний регистр
    if item_key in ("check_doc", "check_pe") and "time" in askable[step]["key"]:
        val = val.replace("AM", "a. m.").replace("PM", "p. m.").replace("A.M.", "a. m.").replace("P.M.", "p. m.")
    
    # Конвертация даты в испанский формат для чеков Перу
    if item_key == "check_pe" and askable[step]["key"] == "date":
        val = _to_es_date(val)
    if item_key == "check2_pe" and askable[step]["key"] == "date":
        val = _to_es_date2(val)
    if item_key == "check2_pe" and askable[step]["key"] == "time":
        val = val.replace("A.M.", "am.").replace("P.M.", "pm.").replace("a. m.", "am.").replace("p. m.", "pm.")\
                 .replace("a.m.", "am.").replace("p.m.", "pm.").replace("AM", "am.").replace("PM", "pm.")

    values[askable[step]["key"]] = val
    done_step = step + 1

    if done_step < len(askable):
        s = get_settings(message.from_user.id)
        checklist = _build_checklist(item["label"], askable, done_step=done_step, values=values)
        await _update_checklist(message.bot, message.chat.id, msg_id, has_photo,
                                checklist + f"\n\n{askable[done_step]['prompt']}",
                                reply_markup=_get_field_keyboard(askable[done_step]["key"], s, item_key))
        # Сбрасываем временный суффикс на дефолт из настроек для следующего поля
        await state.update_data(step=done_step, values=values, time_suffix=s["time_suffix"])
    else:
        await state.clear()
        geo: str = data.get("current_geo", "bo")
        await _finish_render(message, item_key, values, item,
                             checklist_msg_id=msg_id, has_photo=has_photo,
                             geo=geo)


@router.message(RenderStates.collecting, F.photo | F.document)
async def collect_photo_field(message: Message, state: FSMContext):
    data       = await state.get_data()
    askable:   list = data["askable"]
    step:      int  = data["step"]
    values:    dict = data["values"]
    item_key:  str  = data["item_key"]
    msg_id:    int  = data["checklist_msg_id"]
    has_photo: bool = data["has_photo"]
    geo: str = data.get("current_geo", "bo")
    item = _find_item(item_key, geo)

    if not _is_image_field(askable[step]):
        await _try_delete(message.bot, message.chat.id, message.message_id)
        await message.answer("⚠️ Это поле ожидает <b>текст</b>.", parse_mode="HTML")
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
        checklist = _build_checklist(item["label"], askable, done_step=done_step, values=values)
        await _update_checklist(message.bot, message.chat.id, msg_id, has_photo,
                                checklist + f"\n\n{askable[done_step]['prompt']}",
                                reply_markup=_get_field_keyboard(askable[done_step]["key"], s, item_key))
        await state.update_data(step=done_step, values=values, time_suffix=s["time_suffix"])
    else:
        await state.clear()
        geo: str = data.get("current_geo", "bo")
        await _finish_render(message, item_key, values, item,
                             checklist_msg_id=msg_id, has_photo=has_photo,
                             geo=geo)


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
        await call.message.answer("🌍 Выберите регион:", reply_markup=_geo_menu_for(call.from_user.id, role))
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
        await call.message.answer("🌍 Выберите регион:", reply_markup=_geo_menu_for(call.from_user.id, role))
    await call.answer()


# ── Shortcuts (Random, Pin, Suffix) ──────────────────────────────────────────

@router.callback_query(F.data.startswith("render:"))
async def cb_render_shortcuts(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    if not data or "askable" not in data:
        await call.answer()
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
        if key in ("sum", "amount"):
            val = str(random.randint(s["rand_min"], s["rand_max"]))
        elif key == "number":
            val = "".join([str(random.randint(0, 9)) for _ in range(8)])
        elif key == "account":
            val = "".join([str(random.randint(0, 9)) for _ in range(3)])
        elif key == "transaction":
            digits = 8 if item_key == "check_pe" else 9
            val = "".join([str(random.randint(0, 9)) for _ in range(digits)])
        elif key == "operation":
            val = "".join([str(random.randint(0, 9)) for _ in range(8)])
        elif key in ("card_recipient", "card_sender"):
            val = "".join([str(random.randint(0, 9)) for _ in range(4)])
        else:
            val = "0"
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
        await call.answer(f"Выбрано: {new_suffix or 'Без суффикса'}")
        return
    elif action == "set":
        val = parts[2]
    else:
        await call.answer()
        return

    # Если мы здесь, значит получили значение (pin или random)
    # Конвертация даты в испанский формат для чека Перу
    if item_key == "check_pe" and askable[step]["key"] == "date":
        val = _to_es_date(val)
    if item_key == "check2_pe" and askable[step]["key"] == "date":
        val = _to_es_date2(val)
    values[askable[step]["key"]] = val
    done_step = step + 1

    if done_step < len(askable):
        s = get_settings(call.from_user.id)
        checklist = _build_checklist(item["label"], askable, done_step=done_step, values=values)
        await _update_checklist(call.bot, call.message.chat.id, msg_id, has_photo,
                                checklist + f"\n\n{askable[done_step]['prompt']}",
                                reply_markup=_get_field_keyboard(askable[done_step]["key"], s, item_key))
        await state.update_data(step=done_step, values=values, time_suffix=s["time_suffix"])
    else:
        await state.clear()
        await _finish_render(call.message, item_key, values, item,
                             checklist_msg_id=msg_id, has_photo=has_photo,
                             geo=geo)
    await call.answer()
