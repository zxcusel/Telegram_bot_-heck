import io
import os
import random
import zipfile
import datetime
import asyncio
from aiogram import Router, F
from aiogram.types import CallbackQuery, Message, BufferedInputFile, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.exceptions import TelegramBadRequest

from data.config import GEO_CATALOG, GEO_LABELS
from data.db import get_role_string, get_geos, is_admin, get_settings, get_available_names, get_all_names
from keyboards.inline import _allowed_lines, cancel_kb
from utils.logger import log
from utils.renderer import render_image, render_video
from handlers.render import _format_date_for_item, _format_name, _is_name_field, _to_es_date, _to_es_date2, _to_es_date_uy, _to_es_date_py, _to_es_date_py_check3, _get_item_for_user

router = Router()

async def edit_or_send_next(message: Message, state: FSMContext, text: str, reply_markup: InlineKeyboardMarkup):
    data = await state.get_data()
    last_msg_id = data.get("last_bot_msg_id")
    sent_msg = None
    if last_msg_id:
        try:
            sent_msg = await message.bot.edit_message_text(
                chat_id=message.chat.id,
                message_id=last_msg_id,
                text=text,
                reply_markup=reply_markup,
                parse_mode="HTML"
            )
        except Exception:
            pass
    if not sent_msg:
        sent_msg = await message.answer(text, reply_markup=reply_markup, parse_mode="HTML")
        await state.update_data(last_bot_msg_id=sent_msg.message_id)
    return sent_msg


def get_progress_bar(percent: int) -> str:
    filled_length = int(10 * percent // 100)
    return "🟩" * filled_length + "⬜" * (10 - filled_length)


class BulkStates(StatesGroup):
    choose_geo = State()
    choose_line = State()
    choose_section = State()
    choose_item = State()
    enter_dates = State()
    enter_times = State()
    enter_amounts = State()
    choose_names_source = State()
    upload_names_file = State()
    enter_quantity = State()
    configure_effects = State()
    confirm = State()


# ── Keyboards ─────────────────────────────────────────────────────────────────

def bulk_geo_menu(user_id: int, role: str | None) -> InlineKeyboardMarkup:
    allowed_geos = get_geos(user_id) if not is_admin(user_id) else list(GEO_CATALOG.keys())
    buttons = [
        [InlineKeyboardButton(
            text=GEO_CATALOG[gk]["label"],
            callback_data=f"bulk_geo:{gk}"
        )]
        for gk in allowed_geos if gk in GEO_CATALOG
    ]
    if not buttons:
        buttons.append([InlineKeyboardButton(text="⛔ Нет доступа к регионам", callback_data="noop")])
    buttons.append([InlineKeyboardButton(text="🔙 Назад в меню", callback_data="bulk_back:welcome")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def bulk_main_menu(role: str | None, geo: str) -> InlineKeyboardMarkup:
    catalog = GEO_CATALOG.get(geo, {}).get("catalog", {})
    allowed = _allowed_lines(role)
    buttons = []
    for line_key, line in catalog.items():
        if line_key in allowed and line.get("sections"):
            has_items = any(
                sec.get("items")
                for sec in line["sections"].values()
            )
            if has_items:
                buttons.append([InlineKeyboardButton(
                    text=line["label"], callback_data=f"bulk_line:{geo}:{line_key}"
                )])
    if not buttons:
        buttons.append([InlineKeyboardButton(text="⛔ Нет доступных шаблонов", callback_data="noop")])
    buttons.append([InlineKeyboardButton(text="🔙 Назад к регионам", callback_data="bulk_back:geo")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def bulk_sections_menu(geo: str, line_key: str) -> InlineKeyboardMarkup:
    line = GEO_CATALOG[geo]["catalog"][line_key]
    buttons = [
        [InlineKeyboardButton(text=sec["label"],
                              callback_data=f"bulk_section:{geo}:{line_key}:{sec_key}")]
        for sec_key, sec in line["sections"].items()
        if sec.get("items")
    ]
    buttons.append([InlineKeyboardButton(text="🔙 Назад в категории", callback_data=f"bulk_back:main_menu:{geo}")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def bulk_items_menu(geo: str, line_key: str, sec_key: str) -> InlineKeyboardMarkup:
    section = GEO_CATALOG[geo]["catalog"][line_key]["sections"][sec_key]
    buttons = [
        [InlineKeyboardButton(text=item["label"],
                              callback_data=f"bulk_item:{geo}:{item_key}")]
        for item_key, item in section["items"].items()
    ]
    buttons.append([InlineKeyboardButton(text="🔙 Назад в разделы", callback_data=f"bulk_back:sections_menu:{geo}:{line_key}")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def bulk_effects_menu(blur: int, jose_mode: str) -> InlineKeyboardMarkup:
    blur_text = "💧 Размытие: ✅ ВКЛ" if blur == 1 else "💧 Размытие: ❌ ВЫКЛ"
    
    if jose_mode == "sender":
        jose_text = "👤 Режим JOSE: 👨‍✈️ Отправитель"
    elif jose_mode == "recipient":
        jose_text = "👤 Режим JOSE: 👩‍💼 Получатель"
    else:
        jose_text = "👤 Режим JOSE: ❌ Отключен"
        
    buttons = [
        [InlineKeyboardButton(text=blur_text, callback_data="bulk_toggle:blur")],
        [InlineKeyboardButton(text=jose_text, callback_data="bulk_toggle:jose")],
        [InlineKeyboardButton(text="➡️ Продолжить", callback_data="bulk_toggle:done")],
        [InlineKeyboardButton(text="❌ Отмена", callback_data="bulk_cancel")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


from handlers.render import JOSE_RULES

def get_item_with_jose(item_key: str, geo: str, jose_mode: str) -> dict | None:
    from utils.renderer import _find_item
    item = _find_item(item_key, geo)
    if not item:
        return None
    if jose_mode in ("sender", "recipient") and (item_key, jose_mode) in JOSE_RULES:
        import copy
        item = copy.deepcopy(item)
        asset_path, excluded_fields = JOSE_RULES[(item_key, jose_mode)]
        item["asset"] = asset_path
        item["fields"] = [f for f in item["fields"] if f["key"] not in excluded_fields]
    return item


# ── Navigation & Initiation Handlers ──────────────────────────────────────────

@router.callback_query(F.data == "start:bulk_gen")
async def cb_start_bulk_gen(call: CallbackQuery, state: FSMContext):
    await state.clear()
    log.bulk_started(call.from_user.id, call.from_user.username)
    role = get_role_string(call.from_user.id)
    kb = bulk_geo_menu(call.from_user.id, role)
    await state.set_state(BulkStates.choose_geo)
    sent_msg = await call.message.edit_text("🌍 <b>[Массовая генерация]</b> Выберите регион:", reply_markup=kb, parse_mode="HTML")
    await state.update_data(last_bot_msg_id=sent_msg.message_id)
    await call.answer()


@router.callback_query(F.data.startswith("bulk_back:"))
async def cb_bulk_back(call: CallbackQuery, state: FSMContext):
    parts = call.data.split(":")
    dest = parts[1]

    if dest == "welcome":
        await state.clear()
        from handlers.catalog import _start_kb
        await call.message.edit_text("👋 Добро пожаловать!", reply_markup=_start_kb(call.from_user.id))

    elif dest == "geo":
        role = get_role_string(call.from_user.id)
        await state.set_state(BulkStates.choose_geo)
        sent_msg = await call.message.edit_text("🌍 <b>[Массовая генерация]</b> Выберите регион:", reply_markup=bulk_geo_menu(call.from_user.id, role), parse_mode="HTML")
        await state.update_data(last_bot_msg_id=sent_msg.message_id)

    elif dest == "main_menu":
        geo = parts[2]
        role = get_role_string(call.from_user.id)
        await state.set_state(BulkStates.choose_line)
        geo_label = GEO_CATALOG[geo]["label"]
        sent_msg = await call.message.edit_text(f"{geo_label}\n📂 <b>[Массовая генерация]</b> Выберите категорию:", reply_markup=bulk_main_menu(role, geo), parse_mode="HTML")
        await state.update_data(last_bot_msg_id=sent_msg.message_id)

    elif dest == "sections_menu":
        geo = parts[2]
        line_key = parts[3]
        await state.set_state(BulkStates.choose_section)
        sent_msg = await call.message.edit_text("📂 <b>[Массовая генерация]</b> Выберите раздел:", reply_markup=bulk_sections_menu(geo, line_key), parse_mode="HTML")
        await state.update_data(last_bot_msg_id=sent_msg.message_id)

    await call.answer()


@router.callback_query(F.data.startswith("bulk_geo:"))
async def cb_bulk_geo(call: CallbackQuery, state: FSMContext):
    geo = call.data.split(":")[1]
    if geo not in GEO_CATALOG:
        await call.answer("⛔ Неизвестный регион", show_alert=True)
        return
    if not is_admin(call.from_user.id) and geo not in get_geos(call.from_user.id):
        await call.answer("⛔ Нет доступа к этому региону", show_alert=True)
        return

    await state.update_data(current_geo=geo)
    role = get_role_string(call.from_user.id)
    geo_label = GEO_CATALOG[geo]["label"]
    await state.set_state(BulkStates.choose_line)
    sent_msg = await call.message.edit_text(f"{geo_label}\n📂 <b>[Массовая генерация]</b> Выберите категорию:", reply_markup=bulk_main_menu(role, geo), parse_mode="HTML")
    await state.update_data(last_bot_msg_id=sent_msg.message_id)
    await call.answer()


@router.callback_query(F.data.startswith("bulk_line:"))
async def cb_bulk_line(call: CallbackQuery, state: FSMContext):
    parts = call.data.split(":")
    geo = parts[1]
    line_key = parts[2]
    await state.update_data(current_geo=geo, last_line=line_key, last_section=None)
    await state.set_state(BulkStates.choose_section)
    sent_msg = await call.message.edit_text("📂 <b>[Массовая генерация]</b> Выберите раздел:", reply_markup=bulk_sections_menu(geo, line_key), parse_mode="HTML")
    await state.update_data(last_bot_msg_id=sent_msg.message_id)
    await call.answer()


@router.callback_query(F.data.startswith("bulk_section:"))
async def cb_bulk_section(call: CallbackQuery, state: FSMContext):
    _, geo, line_key, sec_key = call.data.split(":")
    await state.update_data(current_geo=geo, last_line=line_key, last_section=sec_key)
    await state.set_state(BulkStates.choose_item)
    sent_msg = await call.message.edit_text("📄 <b>[Массовая генерация]</b> Выберите шаблон:", reply_markup=bulk_items_menu(geo, line_key, sec_key), parse_mode="HTML")
    await state.update_data(last_bot_msg_id=sent_msg.message_id)
    await call.answer()


@router.callback_query(F.data.startswith("bulk_item:"))
async def cb_bulk_item(call: CallbackQuery, state: FSMContext):
    _, geo, item_key = call.data.split(":")
    item = _get_item_for_user(item_key, geo, call.from_user.id)
    if not item:
        await call.answer("❌ Шаблон не найден.", show_alert=True)
        return

    await state.update_data(current_geo=geo, item_key=item_key, item_label=item["label"])
    await state.set_state(BulkStates.enter_dates)
    sent_msg = await call.message.edit_text(
        "📅 <b>Шаг 1 из 6: Диапазон дат</b>\n"
        "[ 🟩⬜⬜⬜⬜⬜ ]\n\n"
        "Введите диапазон дат, за которые нужно сгенерировать чеки.\n"
        "<i>Примеры форматов:</i>\n"
        "• <code>01.07.2026-07.07.2026</code> (диапазон)\n"
        "• <code>05.07.2026</code> (один конкретный день):",
        reply_markup=cancel_kb("bulk_cancel"),
        parse_mode="HTML"
    )
    await state.update_data(last_bot_msg_id=sent_msg.message_id)
    await call.answer()


# ── FSM Text/File Input Handlers ──────────────────────────────────────────────

@router.callback_query(F.data == "bulk_cancel")
async def cb_bulk_cancel(call: CallbackQuery, state: FSMContext):
    await state.clear()
    from handlers.catalog import _start_kb
    await call.message.edit_text("👋 Добро пожаловать!", reply_markup=_start_kb(call.from_user.id))
    await call.answer("Отменено")


@router.message(BulkStates.enter_dates, F.text)
async def process_bulk_dates(message: Message, state: FSMContext):
    text = message.text.strip().replace(" ", "")
    try:
        if "-" in text:
            start_str, end_str = text.split("-", 1)
            start_date = datetime.datetime.strptime(start_str, "%d.%m.%Y").date()
            end_date = datetime.datetime.strptime(end_str, "%d.%m.%Y").date()
            if start_date > end_date:
                start_date, end_date = end_date, start_date
        else:
            single_date = datetime.datetime.strptime(text, "%d.%m.%Y").date()
            start_date, end_date = single_date, single_date
    except ValueError:
        await message.answer("❌ Неверный формат даты. Используйте формат ДД.ММ.ГГГГ-ДД.ММ.ГГГГ или ДД.ММ.ГГГГ. Попробуйте еще раз:")
        return

    await state.update_data(start_date=start_date.strftime("%d.%m.%Y"), end_date=end_date.strftime("%d.%m.%Y"))
    await state.set_state(BulkStates.enter_times)
    
    try:
        await message.delete()
    except Exception:
        pass

    await edit_or_send_next(
        message, state,
        "🕐 <b>Шаг 2 из 6: Диапазон времени</b>\n"
        "[ 🟩🟩⬜⬜⬜⬜ ]\n\n"
        "Введите диапазон времени для чеков.\n"
        "<i>Примеры форматов:</i>\n"
        "• <code>09:00-18:00</code> (диапазон)\n"
        "• <code>14:30</code> (точное время):",
        cancel_kb("bulk_cancel")
    )


@router.message(BulkStates.enter_times, F.text)
async def process_bulk_times(message: Message, state: FSMContext):
    text = message.text.strip().replace(" ", "")
    try:
        if "-" in text:
            start_str, end_str = text.split("-", 1)
            start_time = datetime.datetime.strptime(start_str, "%H:%M").time()
            end_time = datetime.datetime.strptime(end_str, "%H:%M").time()
        else:
            single_time = datetime.datetime.strptime(text, "%H:%M").time()
            start_time, end_time = single_time, single_time
    except ValueError:
        await message.answer("❌ Неверный формат времени. Используйте ЧЧ:ММ-ЧЧ:ММ. Попробуйте еще раз:")
        return

    await state.update_data(start_time=start_time.strftime("%H:%M"), end_time=end_time.strftime("%H:%M"))
    await state.set_state(BulkStates.enter_amounts)
    
    try:
        await message.delete()
    except Exception:
        pass

    await edit_or_send_next(
        message, state,
        "💰 <b>Шаг 3 из 6: Диапазон сумм</b>\n"
        "[ 🟩🟩🟩⬜⬜⬜ ]\n\n"
        "Введите сумму или диапазон сумм чеков.\n"
        "<i>Примеры форматов:</i>\n"
        "• <code>10000-25000</code> (диапазон)\n"
        "• <code>15000</code> (фиксированная сумма):",
        cancel_kb("bulk_cancel")
    )


@router.message(BulkStates.enter_amounts, F.text)
async def process_bulk_amounts(message: Message, state: FSMContext):
    text = message.text.strip().replace(" ", "").replace(",", "")
    try:
        if "-" in text:
            parts = text.split("-", 1)
            min_amt = int(parts[0])
            max_amt = int(parts[1])
            if min_amt > max_amt:
                min_amt, max_amt = max_amt, min_amt
        else:
            val = int(text)
            min_amt, max_amt = val, val
    except ValueError:
        await message.answer("❌ Неверный формат суммы. Введите целое число или диапазон чисел через дефис:")
        return

    await state.update_data(min_amount=min_amt, max_amount=max_amt)
    await state.set_state(BulkStates.choose_names_source)
    
    try:
        await message.delete()
    except Exception:
        pass

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎲 Системные (из name.json)", callback_data="bulk_names:system")],
        [InlineKeyboardButton(text="📎 Загрузить свой TXT/CSV файл", callback_data="bulk_names:upload")],
        [InlineKeyboardButton(text="❌ Отмена", callback_data="bulk_cancel")]
    ])

    await edit_or_send_next(
        message, state,
        "👤 <b>Шаг 4 из 6: Источник имён</b>\n"
        "[ 🟩🟩🟩🟩⬜⬜ ]\n\n"
        "Выберите источник имён, которые будут случайно распределяться по чекам:\n"
        "• <b>Системная база</b>: имена из встроенного файла name.json.\n"
        "• <b>Свой файл</b>: загрузка текстового файла с именами.",
        kb
    )


@router.callback_query(F.data.startswith("bulk_names:"))
async def cb_bulk_names_source(call: CallbackQuery, state: FSMContext):
    source = call.data.split(":")[1]
    if source == "system":
        names = get_available_names()
        if not names:
            names = get_all_names()
        if not names:
            await call.answer("❌ В базе name.json нет имён. Пожалуйста, выберите загрузку файла.", show_alert=True)
            return

        # Deduplicate and preserve order
        names = list(dict.fromkeys(name.strip() for name in names if name.strip()))
        if not names:
            await call.answer("❌ В базе name.json нет имён. Пожалуйста, выберите загрузку файла.", show_alert=True)
            return

        await state.update_data(names_source="system", names_count=len(names), names_list=names)
        await state.set_state(BulkStates.enter_quantity)
        sent_msg = await call.message.edit_text(
            "🔢 <b>Шаг 5 из 6: Количество чеков</b>\n"
            "[ 🟩🟩🟩🟩🟩⬜ ]\n\n"
            "Введите необходимое количество чеков для генерации (например, <code>50</code>, максимум 500):",
            reply_markup=cancel_kb("bulk_cancel"),
            parse_mode="HTML"
        )
        await state.update_data(last_bot_msg_id=sent_msg.message_id)
    else:
        await state.update_data(names_source="file")
        await state.set_state(BulkStates.upload_names_file)
        sent_msg = await call.message.edit_text(
            "📎 <b>Шаг 4 из 6: Загрузка файла имён</b>\n"
            "[ 🟩🟩🟩🟩⬜⬜ ]\n\n"
            "Отправьте текстовый файл (<b>.txt</b> или <b>.csv</b>), где каждое имя написано с новой строки.\n"
            "Бот будет случайно выбирать имена из этого файла при генерации.",
            reply_markup=cancel_kb("bulk_cancel"),
            parse_mode="HTML"
        )
        await state.update_data(last_bot_msg_id=sent_msg.message_id)
    await call.answer()


@router.message(BulkStates.upload_names_file, F.document)
async def process_names_file(message: Message, state: FSMContext):
    doc = message.document
    if not doc.file_name.lower().endswith((".txt", ".csv")):
        await message.answer("⚠️ Пожалуйста, отправьте именно файл с расширением .txt или .csv:")
        return

    try:
        file = await message.bot.get_file(doc.file_id)
        file_bytes = await message.bot.download_file(file.file_path)
        content = file_bytes.read().decode("utf-8")
        names = [line.strip() for line in content.splitlines() if line.strip()]
        # Deduplicate and preserve order
        names = list(dict.fromkeys(name.strip() for name in names if name.strip()))
        if not names:
            await message.answer("❌ Файл пуст или содержит некорректные символы. Попробуйте другой файл:")
            return
    except Exception as e:
        await message.answer(f"❌ Ошибка чтения файла: {e}. Пожалуйста, попробуйте еще раз:")
        return

    await state.update_data(names_list=names, names_count=len(names))
    await state.set_state(BulkStates.enter_quantity)
    
    try:
        await message.delete()
    except Exception:
        pass

    await edit_or_send_next(
        message, state,
        "🔢 <b>Шаг 5 из 6: Количество чеков</b>\n"
        "[ 🟩🟩🟩🟩🟩⬜ ]\n\n"
        "Введите необходимое количество чеков для генерации (например, <code>50</code>, максимум 500):",
        cancel_kb("bulk_cancel")
    )


@router.message(BulkStates.enter_quantity, F.text)
async def process_bulk_quantity(message: Message, state: FSMContext):
    text = message.text.strip()
    try:
        quantity = int(text)
        if quantity <= 0 or quantity > 500:
            raise ValueError()
    except ValueError:
        await message.answer("❌ Пожалуйста, введите корректное число от 1 до 500:")
        return

    data = await state.get_data()
    geo = data.get("current_geo")
    item_key = data.get("item_key")
    jose_mode = data.get("jose_mode", "none")

    item = get_item_with_jose(item_key, geo, jose_mode)
    if not item:
        await message.answer("❌ Шаблон не найден. Пожалуйста, начните заново.")
        return

    name_fields_count = sum(1 for f in item["fields"] if _is_name_field(f["key"]))
    total_names_needed = quantity * name_fields_count

    names_list = data.get("names_list", [])
    names_count = len(names_list)

    if total_names_needed > 0 and names_count < total_names_needed:
        try:
            await message.delete()
        except Exception:
            pass

        error_text = (
            f"❌ <b>Недостаточно уникальных имён в источнике!</b>\n"
            f"Для выбранного шаблона требуется по {name_fields_count} имён на чек.\n"
            f"Для генерации {quantity} чеков необходимо минимум <b>{total_names_needed}</b> уникальных имён.\n"
            f"В вашем источнике доступно всего: <b>{names_count}</b> уникальных имён.\n\n"
            f"🔢 <b>Шаг 5 из 6: Количество чеков</b>\n"
            f"[ 🟩🟩🟩🟩🟩⬜ ]\n\n"
            f"Пожалуйста, введите меньшее количество чеков (максимум {names_count // name_fields_count if name_fields_count > 0 else quantity}):"
        )
        await edit_or_send_next(message, state, error_text, cancel_kb("bulk_cancel"))
        return

    await state.update_data(quantity=quantity)
    
    try:
        await message.delete()
    except Exception:
        pass

    user_settings = get_settings(message.from_user.id)
    blur = user_settings.get("blur_enabled", 1)
    jose_mode = "sender" if user_settings.get("jose_sender_enabled") else ("recipient" if user_settings.get("jose_recipient_enabled") else "none")
    
    await state.update_data(blur_enabled=blur, jose_mode=jose_mode)
    await state.set_state(BulkStates.configure_effects)

    await edit_or_send_next(
        message, state,
        "⚙️ <b>Шаг 6 из 6: Настройка эффектов</b>\n"
        "[ 🟩🟩🟩🟩🟩🟩 ]\n\n"
        "Настройте размытие и режим JOSE для этой генерации чеков:",
        bulk_effects_menu(blur, jose_mode)
    )


@router.callback_query(F.data.startswith("bulk_toggle:"), BulkStates.configure_effects)
async def cb_bulk_toggle_effects(call: CallbackQuery, state: FSMContext):
    action = call.data.split(":")[1]
    data = await state.get_data()
    
    blur = data.get("blur_enabled", 1)
    jose_mode = data.get("jose_mode", "none")
    
    if action == "blur":
        blur = 1 if blur == 0 else 0
        await state.update_data(blur_enabled=blur)
        await call.message.edit_reply_markup(reply_markup=bulk_effects_menu(blur, jose_mode))
        await call.answer("Размытие переключено")
        
    elif action == "jose":
        if jose_mode == "none":
            jose_mode = "sender"
        elif jose_mode == "sender":
            jose_mode = "recipient"
        else:
            jose_mode = "none"
        await state.update_data(jose_mode=jose_mode)
        await call.message.edit_reply_markup(reply_markup=bulk_effects_menu(blur, jose_mode))
        await call.answer("Режим JOSE изменен")
        
    elif action == "done":
        await state.set_state(BulkStates.confirm)
        
        geo_label = GEO_CATALOG[data["current_geo"]]["label"]
        names_src_display = "Системная база (name.json)" if data["names_source"] == "system" else "Загруженный файл"
        
        blur_display = "✅ Включено" if blur == 1 else "❌ Выключено"
        if jose_mode == "sender":
            jose_display = "👨‍✈️ Отправитель JOSE"
        elif jose_mode == "recipient":
            jose_display = "👩‍💼 Получатель JOSE"
        else:
            jose_display = "❌ Отключен"

        kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🚀 Начать генерацию", callback_data="bulk_start")],
            [InlineKeyboardButton(text="❌ Отмена", callback_data="bulk_cancel")]
        ])

        confirm_text = (
            "📋 <b>Подтверждение массовой генерации:</b>\n"
            "══════════════════════\n"
            f"🌍 <b>Регион:</b> <code>{geo_label}</code>\n"
            f"🖼 <b>Шаблон:</b> <code>{data['item_label']}</code>\n"
            f"📅 <b>Даты:</b> <code>{data['start_date']} — {data['end_date']}</code>\n"
            f"🕐 <b>Время:</b> <code>{data['start_time']} — {data['end_time']}</code>\n"
            f"💰 <b>Суммы:</b> <code>{data['min_amount']} — {data['max_amount']}</code>\n"
            f"👤 <b>Имена:</b> <code>{names_src_display}</code> ({data['names_count']} шт.)\n"
            f"🔢 <b>Количество:</b> <code>{data['quantity']} шт.</code>\n"
            f"💧 <b>Размытие:</b> <code>{blur_display}</code>\n"
            f"👤 <b>Режим JOSE:</b> <code>{jose_display}</code>\n"
            "══════════════════════\n\n"
            "<i>Генерация начнется в фоновом режиме. Чеки будут упакованы в ZIP-архив при большом количестве.</i>"
        )

        sent_msg = await call.message.edit_text(confirm_text, reply_markup=kb, parse_mode="HTML")
        await state.update_data(last_bot_msg_id=sent_msg.message_id)
        await call.answer()


# ── Bulk Execution Helpers ────────────────────────────────────────────────────

def format_bulk_date(dt: datetime.date, field_prompt: str, item: dict) -> str:
    prompt_lower = field_prompt.lower()
    
    eng_days = ["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"]
    esp_days = ["Lu", "Ma", "Mi", "Ju", "Vi", "Sa", "Do"]
    
    if "fr" in prompt_lower:
        weekday = eng_days[dt.weekday()]
    elif any(d in prompt_lower for d in ("lu", "ma", "mi", "ju", "vi", "sa", "do")):
        weekday = esp_days[dt.weekday()]
    else:
        weekday = None

    if "01/01/2026" in prompt_lower or "01/01/26" in prompt_lower or "/" in prompt_lower:
        if "2026" in prompt_lower or str(dt.year) in prompt_lower or "yyyy" in prompt_lower:
            date_part = dt.strftime("%d/%m/%Y")
        elif "26" in prompt_lower or "yy" in prompt_lower:
            date_part = dt.strftime("%d/%m/%y")
        else:
            date_part = dt.strftime("%d/%m")
            
        if weekday:
            return f"{weekday} {date_part}"
        return date_part
        
    elif "01.01" in prompt_lower or "." in prompt_lower:
        if "2026" in prompt_lower or "yyyy" in prompt_lower:
            date_part = dt.strftime("%d.%m.%Y")
        elif "26" in prompt_lower or "yy" in prompt_lower:
            date_part = dt.strftime("%d.%m.%y")
        else:
            date_part = dt.strftime("%d.%m")
            
        if weekday:
            return f"{weekday} {date_part}"
        return date_part
        
    val_str = dt.strftime("%d.%m.%Y")
    return _format_date_for_item(val_str, item)


def format_bulk_time(tm: datetime.time, field_prompt: str, time_suffix: str = None) -> str:
    prompt_lower = field_prompt.lower()
    is_24h = "24-часовой" in prompt_lower or not any(x in prompt_lower for x in ["a.m.", "p.m.", "am", "pm"])
    
    if is_24h:
        return tm.strftime("%H:%M")
    else:
        hour = tm.hour
        if time_suffix:
            suffix = time_suffix
        else:
            suffix = "A.M." if hour < 12 else "P.M."
            
        hour_12 = hour % 12
        if hour_12 == 0:
            hour_12 = 12
            
        time_str = f"{hour_12}:{tm.minute:02d}"
        
        if "a. m." in prompt_lower or "p. m." in prompt_lower:
            suff = suffix.lower().replace("a.m.", "a. m.").replace("p.m.", "p. m.")
        elif "am." in prompt_lower or "pm." in prompt_lower:
            suff = suffix.lower().replace("a.m.", "am.").replace("p.m.", "pm.")
        elif "a.m." in prompt_lower or "p.m." in prompt_lower:
            suff = suffix.lower()
        else:
            suff = suffix.upper().replace(".", "")
            
        return f"{time_str} {suff}".strip()


def generate_field_val(key: str, prompt: str, item_key: str, item: dict, s: dict, 
                       base_date: datetime.date, base_time: datetime.time, 
                       base_amount: int, name_pool: list[str]) -> str:
    # 1. Names (Fallback only)
    if _is_name_field(key):
        val = random.choice(name_pool) if name_pool else "Juan Perez"
        if item_key == "check1_uy" and key == "name":
            name_parts = val.split()
            if len(name_parts) >= 3:
                val = name_parts[2]
        return _format_name(val, item)
        
    # 2. Dates
    if "date" in key:
        return format_bulk_date(base_date, prompt, item)
        
    # 3. Time
    if "time" in key:
        return format_bulk_time(base_time, prompt, s.get("time_suffix"))
        
    # 4. Amount / Commission
    if key in ("sum", "amount", "commission"):
        return str(base_amount)
        
    # 5. Percentage
    if key == "percentage":
        val_float = random.uniform(s.get("rand_percent_min", 1.0), s.get("rand_percent_max", 100.0))
        sign = s.get("perc_sign", "+")
        formatted = f"{abs(val_float):,.2f}"
        return f"{sign}{formatted}"
        
    # 6. Bank / Service
    if key in ("bank", "sender_bank", "service"):
        return random.choice(item.get("banks", ["Banco"]))
        
    # 7. Wifi / Battery / Network / Long-Short / Currency / Gender
    if key == "wifi":
        return random.choice(["assets/Uruguay/Чек/icon/W1.png", "assets/Uruguay/Чек/icon/W2.png"])
    if key == "network":
        return random.choice(["assets/Uruguay/Чек/icon/M1.png", "assets/Uruguay/Чек/icon/M2.png", "assets/Uruguay/Чек/icon/M3.png"])
    if key == "battery":
        return random.choice(["assets/Uruguay/Чек/icon/B1.png", "assets/Uruguay/Чек/icon/B2.png", "assets/Uruguay/Чек/icon/B3.png"])
    if key == "long_short":
        return random.choice(["Long", "Short"])
    if key == "currency":
        return random.choice(["SOL", "BTC", "BNB", "XRP", "ETH"])
    if key == "gender":
        return random.choice(["o", "a"])
        
    # 8. Rocket x_amount
    if key == "x_amount":
        r_min = s.get("rand_rocket_min", 10)
        r_max = s.get("rand_rocket_max", 1000)
        if r_min > r_max:
            r_min, r_max = r_max, r_min
        return str(random.randint(r_min, r_max))
        
    # 9. Accounts, Transactions, Cards, Phones, Reference numbers
    if key == "number":
        return "".join([str(random.randint(0, 9)) for _ in range(8)])
    if key in ("account", "sender_acc", "receiver_acc", "acc_num", "acc_num_2"):
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
            return "1" + "".join([str(random.randint(0, 9)) for _ in range(13)])
        elif item_key == "check4_bo" and key == "sender_acc":
            return "".join([str(random.randint(0, 9)) for _ in range(10)])
        elif item_key in ("payment1_py", "payment1_uy") and key == "account":
            return "922" + "".join([str(random.randint(0, 9)) for _ in range(8)])
        else:
            return "".join([str(random.randint(0, 9)) for _ in range(length)])
            
    if key == "account_end":
        if item_key == "check2_py":
            return "".join([str(random.randint(0, 9)) for _ in range(3)])
            
    if key in ("acc_1", "acc_2"):
        return "".join([str(random.randint(0, 9)) for _ in range(7)])
        
    if key == "ref_num":
        return "".join([str(random.randint(0, 9)) for _ in range(8)])
        
    if key == "transaction":
        if item_key == "fire_check":
            return "".join([str(random.randint(0, 9)) for _ in range(9)])
        elif item_key == "check_pe":
            return "".join([str(random.randint(0, 9)) for _ in range(8)])
        elif item_key == "check2_py":
            return "".join(random.choices("0123456789abcdef", k=24))
        elif item_key == "check1_py":
            return "".join([str(random.randint(0, 9)) for _ in range(13)])
        elif item_key == "check4_bo":
            return "1" + "".join([str(random.randint(0, 9)) for _ in range(18)])
        else:
            return "".join([str(random.randint(0, 9)) for _ in range(9)])
            
    if key == "order":
        digits = 20 if item_key == "fire_check" else 12
        return "".join([str(random.randint(0, 9)) for _ in range(digits)])
        
    if key == "operation":
        return "".join([str(random.randint(0, 9)) for _ in range(8)])
        
    if key in ("card_recipient", "card_sender"):
        return "".join([str(random.randint(0, 9)) for _ in range(4)])
        
    if key == "phone":
        if item_key.endswith("_pe") or "pe" in item_key:
            return f"+51 9{''.join([str(random.randint(0, 9)) for _ in range(8)])}"
        else:
            return f"+{''.join([str(random.randint(0, 9)) for _ in range(11)])}"
            
    return "0"


def get_random_date(start: datetime.date, end: datetime.date) -> datetime.date:
    if start == end:
        return start
    delta = end - start
    random_days = random.randint(0, delta.days)
    return start + datetime.timedelta(days=random_days)


def get_random_time(start: datetime.time, end: datetime.time) -> datetime.time:
    start_minutes = start.hour * 60 + start.minute
    end_minutes = end.hour * 60 + end.minute
    if start_minutes == end_minutes:
        return start
    if start_minutes > end_minutes:
        start_minutes, end_minutes = end_minutes, start_minutes
    rand_minutes = random.randint(start_minutes, end_minutes)
    return datetime.time(hour=rand_minutes // 60, minute=rand_minutes % 60)


def get_clean_filename(idx: int, item_key: str, item: dict, geo: str, check_values: dict, ext: str) -> str:
    # Clean GEO
    geo_clean = "".join(c for c in geo if c.isalnum() or c in (" ", "_", "-"))
    geo_clean = geo_clean.replace(" ", "_").strip("_ ")
    
    # Clean Label
    label_clean = item.get("label", item_key)
    label_clean = "".join(c for c in label_clean if c.isalnum() or c in (" ", "_", "-"))
    label_clean = label_clean.replace(" ", "_").strip("_ ")
    
    # Avoid duplicate geo prefix in label
    if label_clean.lower().startswith(geo_clean.lower()):
        label_part = label_clean
    else:
        label_part = f"{geo_clean}_{label_clean}"
        
    name_val = ""
    for k in ("name", "fullname", "sender_name"):
        if k in check_values and check_values[k]:
            name_val = "".join(c for c in str(check_values[k]) if c.isalnum() or c in (" ", "_", "-"))
            name_val = name_val.replace(" ", "_").strip("_ ")
            if name_val:
                break
                
    amount_val = ""
    for k in ("amount", "sum"):
        if k in check_values and check_values[k]:
            amount_val = "".join(c for c in str(check_values[k]) if c.isdigit())
            if amount_val:
                break
                
    parts = [label_part, f"check_{idx+1}"]
    if name_val:
        parts.append(name_val)
    if amount_val:
        parts.append(amount_val)
        
    filename = "_".join(p for p in parts if p) + f".{ext}"
    filename = "".join(c for c in filename if c.isalnum() or c in (".", "_", "-"))
    return filename


def find_item_hierarchy(geo: str, item_key: str) -> tuple[str, str]:
    catalog = GEO_CATALOG.get(geo, {}).get("catalog", {})
    for line_key, line in catalog.items():
        line_label = line.get("label", line_key)
        for sec_key, sec in line.get("sections", {}).items():
            sec_label = sec.get("label", sec_key)
            if item_key in sec.get("items", {}):
                return line_label, sec_label
    return "", ""


@router.callback_query(F.data == "bulk_start", BulkStates.confirm)
async def cb_bulk_start_execution(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await state.clear()
    
    geo = data["current_geo"]
    item_key = data["item_key"]
    quantity = data["quantity"]
    
    start_date = datetime.datetime.strptime(data["start_date"], "%d.%m.%Y").date()
    end_date = datetime.datetime.strptime(data["end_date"], "%d.%m.%Y").date()
    
    start_time = datetime.datetime.strptime(data["start_time"], "%H:%M").time()
    end_time = datetime.datetime.strptime(data["end_time"], "%H:%M").time()
    
    min_amt = data["min_amount"]
    max_amt = data["max_amount"]
    
    name_pool = data["names_list"]
    
    blur_override = data.get("blur_enabled", 1)
    jose_mode_override = data.get("jose_mode", "none")
    
    user_id = call.from_user.id
    user_settings = get_settings(user_id)
    
    settings_override = user_settings.copy()
    settings_override["blur_enabled"] = blur_override
    settings_override["jose_sender_enabled"] = 1 if jose_mode_override == "sender" else 0
    settings_override["jose_recipient_enabled"] = 1 if jose_mode_override == "recipient" else 0
    
    item = get_item_with_jose(item_key, geo, jose_mode_override)
    
    if not item:
        await call.message.edit_text("❌ Ошибка: шаблон более не доступен.")
        return

    # Log user parameters configuration
    log.bulk_params_configured(
        uid=user_id,
        geo=geo,
        template=item_key,
        quantity=quantity,
        start_date=data["start_date"],
        end_date=data["end_date"],
        start_time=data["start_time"],
        end_time=data["end_time"],
        min_amt=min_amt,
        max_amt=max_amt,
        username=call.from_user.username
    )

    # Log render start
    log.bulk_render_start(
        uid=user_id,
        template=item.get("label", item_key),
        quantity=quantity,
        username=call.from_user.username
    )

    line_label, sec_label = find_item_hierarchy(geo, item_key)
    item_label = item.get("label", item_key)

    progress_text_template = (
        "⏳ <b>Выполняется генерация чеков...</b>\n\n"
        f"🌍 <b>Регион:</b> {geo}\n"
        f"📂 <b>Категория:</b> {line_label}\n"
        f"🖼️ <b>Шаблон:</b> {item_label}\n\n"
        "[ {bar} ] {percent}%\n"
        "Выполнено: <b>{current}</b> из <b>{total}</b> чеков."
    )

    progress_msg = await call.message.edit_text(
        progress_text_template.format(
            bar=get_progress_bar(0),
            percent=0,
            current=0,
            total=quantity
        ),
        reply_markup=None,
        parse_mode="HTML"
    )
    
    media_list = []
    render_mode = item.get("render_mode")
    
    last_update_time = asyncio.get_event_loop().time()
    
    loop = asyncio.get_running_loop()
    
    # Prepare unique names for the run and shuffle them
    run_names = list(name_pool)
    random.shuffle(run_names)
    
    for idx in range(quantity):
        base_date = get_random_date(start_date, end_date)
        base_time = get_random_time(start_time, end_time)
        base_amount = random.randint(min_amt, max_amt) if min_amt != max_amt else min_amt
        
        check_values = {"_blur_mode": "with_blur" if settings_override.get("blur_enabled", 1) else "no_blur"}
        for field in item["fields"]:
            key = field["key"]
            if _is_name_field(key):
                val = run_names.pop(0) if run_names else "Juan Perez"
                if item_key == "check1_uy" and key == "name":
                    name_parts = val.split()
                    if len(name_parts) >= 3:
                        val = name_parts[2]
                check_values[key] = _format_name(val, item)
            else:
                val = generate_field_val(
                    key=key,
                    prompt=field.get("prompt", ""),
                    item_key=item_key,
                    item=item,
                    s=settings_override,
                    base_date=base_date,
                    base_time=base_time,
                    base_amount=base_amount,
                    name_pool=[]
                )
                # Handle image_paste fields dynamically to prevent trying to open "0" as a path in Pillow.
                if field.get("text_config", {}).get("image_paste"):
                    if item_key == "check2_py" and key == "_bank_image":
                        bank_val = check_values.get("bank", "ATLAS")
                        val = f"assets/Paraguay/Чек/bank/{bank_val}.jpg"
                    elif item_key == "check3_py" and key == "_bank_image":
                        bank_val = check_values.get("bank", "ATLAS")
                        val = f"assets/Paraguay/Чек/bank2/{bank_val}.png"
                    elif item_key == "check3_py" and key == "_sender_bank_image":
                        sender_bank_val = check_values.get("sender_bank", "ATLAS")
                        val = f"assets/Paraguay/Чек/bank2/{sender_bank_val}.png"
                    elif key in ("wifi", "network", "battery"):
                        # Keep value generated by generate_field_val
                        pass
                    else:
                        val = None if val == "0" else val
                check_values[key] = val

        try:
            if render_mode == "video":
                media_bytes = await loop.run_in_executor(None, render_video, item_key, check_values, geo, item)
            else:
                media_bytes = await loop.run_in_executor(None, render_image, item_key, check_values, geo, item)
            
            ext = "mp4" if render_mode == "video" else "png"
            filename = get_clean_filename(idx, item_key, item, geo, check_values, ext)
            media_list.append((media_bytes, filename))
        except Exception as e:
            log.render_error(user_id, item.get("label", item_key), f"Bulk rendering error at index {idx}: {e}", call.from_user.username)
        
        now = asyncio.get_event_loop().time()
        if now - last_update_time >= 2.0 or idx == quantity - 1:
            percent = int((idx + 1) / quantity * 100)
            bar = get_progress_bar(percent)
            progress_text = progress_text_template.format(
                bar=bar,
                percent=percent,
                current=idx + 1,
                total=quantity
            )
            try:
                await progress_msg.edit_text(progress_text, parse_mode="HTML")
            except TelegramBadRequest:
                pass
            last_update_time = now
            
    if not media_list:
        await progress_msg.edit_text("❌ Все попытки рендеринга завершились ошибкой. Проверьте логи.")
        return

    # Log render completion
    log.bulk_render_done(
        uid=user_id,
        template=item.get("label", item_key),
        quantity=len(media_list),
        username=call.from_user.username
    )

    try:
        await progress_msg.delete()
    except Exception:
        pass

    if quantity <= 10:
        await call.message.answer(
            f"✅ <b>Массовая генерация завершена!</b>\n\n"
            f"🌍 <b>Регион:</b> {geo}\n"
            f"📂 <b>Категория:</b> {line_label}\n"
            f"🖼️ <b>Шаблон:</b> {item_label}\n"
            f"Сгенерировано чеков: <b>{len(media_list)} шт.</b>\n\n"
            "Отправляю чеки по отдельности:",
            parse_mode="HTML"
        )
        for idx, (media, filename) in enumerate(media_list):
            media.seek(0)
            if render_mode == "video":
                await call.message.answer_video(
                    video=BufferedInputFile(media.read(), filename=filename),
                    caption=f"Чек {idx+1}/{len(media_list)}"
                )
            else:
                await call.message.answer_photo(
                    photo=BufferedInputFile(media.read(), filename=filename),
                    caption=f"Чек {idx+1}/{len(media_list)}"
                )
        await call.message.answer(
            "✅ Все чеки успешно отправлены!",
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(text="◀️ В главное меню", callback_data="back:welcome")]
                ]
            )
        )
    else:
        zip_msg = await call.message.answer("📦 Архивирую сгенерированные файлы...")
        
        geo_clean = "".join(c for c in geo if c.isalnum() or c in (" ", "_", "-"))
        geo_clean = geo_clean.replace(" ", "_").strip("_ ")
        label_clean = item.get("label", item_key)
        label_clean = "".join(c for c in label_clean if c.isalnum() or c in (" ", "_", "-"))
        label_clean = label_clean.replace(" ", "_").strip("_ ")
        if label_clean.lower().startswith(geo_clean.lower()):
            label_part = label_clean
        else:
            label_part = f"{geo_clean}_{label_clean}"
        zip_filename = f"{label_part}.zip"
        
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
            for media, filename in media_list:
                media.seek(0)
                zip_file.writestr(filename, media.read())
        
        zip_buffer.seek(0)
        
        try:
            await zip_msg.delete()
        except Exception:
            pass
            
        await call.message.answer_document(
            document=BufferedInputFile(zip_buffer.read(), filename=zip_filename),
            caption=(
                f"✅ <b>Массовая генерация завершена!</b>\n\n"
                f"🌍 <b>Регион:</b> {geo}\n"
                f"📂 <b>Категория:</b> {line_label}\n"
                f"🖼️ <b>Шаблон:</b> {item_label}\n"
                f"Сгенерировано чеков: <b>{len(media_list)} шт.</b>\n\n"
                "Все файлы упакованы в ZIP-архив."
            ),
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(text="◀️ В главное меню", callback_data="back:welcome")]
                ]
            )
        )
