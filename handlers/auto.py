"""handlers/auto.py — автоматизация создания чеков по расписанию.

Изолировано от ручного режима: отдельная таблица `automation_presets`
и отдельная кнопка входа в меню «� Автоматизация».

Сценарий:
  1. Пользователь жмёт «� Автоматизация» → бот показывает пресет
     (если есть) и кнопки: «⚙️ Изменить настройки» / «🚀 Запустить».
  2. В настройках автоматизации (auto:settings) — отдельное FSM-подменю:
       1. ГЕО
       2. Линейка
       3. Типы чеков (мультивыбор)
       4. Мин / Макс суммы
       5. Дата
       6. Таймлайн: диапазон «start–end» + количество чеков (бот сам распределит)
  3. Кнопка «🚀 Запустить автоматизацию» — генерация медиагруппы.
"""
from __future__ import annotations

import asyncio
import json
import random
import re
from datetime import datetime
from io import BytesIO

from aiogram import Bot, F, Router
from aiogram.enums import ParseMode
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import (
    BufferedInputFile,
    CallbackQuery,
    InputMediaPhoto,
    Message,
)

from data.config import GEO_CATALOG
from data.db import (
    get_available_names,
    get_geos,
    has_any_access,
    is_admin,
)
from keyboards.auto_kb import (
    auto_back_kb,
    auto_batch_done_kb,
    auto_main_kb,
    auto_pick_geo_kb,
    auto_pick_items_kb,
    auto_pick_line_kb,
    auto_run_kb,
)
from utils.logger import log
from utils.renderer import render_image

router = Router()

# ── Дизайн-токены ──────────────────────────────────────────────────────────────
PM = ParseMode.HTML  # parse_mode по умолчанию для всех сообщений модуля
DIV = "━━━━━━━━━━━━━━━━━━━━"  # горизонтальный разделитель
BULLET = "�️"  # маркер списка


# ── FSM состояния автоматизации ────────────────────────────────────────────────
class AutoFSM(StatesGroup):
    picking_geo = State()
    picking_line = State()
    picking_items = State()
    entering_sum = State()
    entering_date = State()
    entering_timeline = State()
    changing_date = State()


# ── Точка входа ───────────────────────────────────────────────────────────────
@router.callback_query(F.data == "auto:open")
async def auto_open(call: CallbackQuery, state: FSMContext):
    """Открывает меню автоматизации. Показывает текущий пресет."""
    user_id = call.from_user.id
    if not has_any_access(user_id):
        await call.answer("⛔ Доступ запрещён", show_alert=True)
        return
    await state.clear()

    preset = _load_preset(user_id)
    if preset:
        text = (
            f"🤖 <b>Автоматизация чеков</b>\n"
            f"{DIV}\n"
            f"✨ <i>Сохранённый пресет готов к запуску</i>\n\n"
            f"{_format_preset(preset)}\n\n"
            f"{DIV}\n"
            f"<i>Можно изменить настройки или сразу запустить.</i>"
        )
    else:
        text = (
            f"🤖 <b>Автоматизация чеков</b>\n"
            f"{DIV}\n"
            f"⚠️ <i>Пресет ещё не настроен.</i>\n\n"
            f"Нажмите <b>«⚙️ Настроить автоматизацию»</b> чтобы задать:\n"
            f"{BULLET} гео и линейку шаблонов\n"
            f"{BULLET} типы чеков\n"
            f"{BULLET} диапазон сумм\n"
            f"{BULLET} дату\n"
            f"{BULLET} расписание слотов"
        )

    await call.message.edit_text(text, reply_markup=auto_main_kb(has_preset=bool(preset)), parse_mode=PM)
    await call.answer()


# ── Настройки: выбор гео ──────────────────────────────────────────────────────
@router.callback_query(F.data == "auto:settings")
async def auto_settings(call: CallbackQuery, state: FSMContext):
    user_id = call.from_user.id
    geos = get_geos(user_id)
    if is_admin(user_id):
        geos = list(GEO_CATALOG.keys())
    if not geos:
        await call.answer("⛔ Нет доступных гео", show_alert=True)
        return
    await state.set_state(AutoFSM.picking_geo)

    text = (
        f"⚙️ <b>Настройка автоматизации</b>\n"
        f"{DIV}\n"
        f"📍 <b>Шаг 1 / 6 — ГЕО</b>\n\n"
        f"Выберите <b>гео</b>, под которым будут создаваться чеки:"
    )
    await call.message.edit_text(text, reply_markup=auto_pick_geo_kb(geos), parse_mode=PM)
    await call.answer()


@router.callback_query(AutoFSM.picking_geo, F.data.startswith("auto:geo:"))
async def auto_geo_picked(call: CallbackQuery, state: FSMContext):
    geo = call.data.split(":", 2)[2]
    if geo not in GEO_CATALOG:
        await call.answer("⛔ Неизвестное гео", show_alert=True)
        return
    await state.update_data(geo=geo)
    await state.set_state(AutoFSM.picking_line)
    label = GEO_CATALOG[geo]["label"]
    text = (
        f"⚙️ <b>Настройка автоматизации</b>\n"
        f"{DIV}\n"
        f"📍 <b>Шаг 2 / 6 — Линейка шаблонов</b>\n\n"
        f"✅ Выбрано ГЕО: <b>{label}</b>\n\n"
        f"Выберите <b>линейку</b> шаблонов:"
    )
    await call.message.edit_text(text, reply_markup=auto_pick_line_kb(geo, call.from_user.id), parse_mode=PM)
    await call.answer()


# ── Выбор линейки ─────────────────────────────────────────────────────────────
@router.callback_query(AutoFSM.picking_line, F.data.startswith("auto:line:"))
async def auto_line_picked(call: CallbackQuery, state: FSMContext):
    _, _, geo, line_key = call.data.split(":", 3)
    line = GEO_CATALOG[geo]["catalog"].get(line_key)
    if not line:
        await call.answer("� Неизвестная линейка", show_alert=True)
        return
    await state.update_data(line_key=line_key)
    await state.set_state(AutoFSM.picking_items)
    text = (
        f"⚙️ <b>Настройка автоматизации</b>\n"
        f"{DIV}\n"
        f"🎨 <b>Шаг 3 / 6 — Типы чеков</b>\n\n"
        f"✅ Линейка: <b>{line['label']}</b>\n\n"
        f"Отметьте <b>типы чеков</b>, которые нужно использовать "
        f"(мультивыбор).\n"
        f"Когда всё выбрано — нажмите <b>«✅ Готово»</b>."
    )
    await call.message.edit_text(
        text,
        reply_markup=auto_pick_items_kb(geo, line_key, selected=set()),
        parse_mode=PM,
    )
    await call.answer()


# ── Мультивыбор item'ов ───────────────────────────────────────────────────────
@router.callback_query(AutoFSM.picking_items, F.data.startswith("auto:item:"))
async def auto_item_toggle(call: CallbackQuery, state: FSMContext):
    _, _, geo, line_key, item_key = call.data.split(":", 4)
    data = await state.get_data()
    selected: set[str] = set(data.get("items", set()))
    if item_key in selected:
        selected.discard(item_key)
    else:
        selected.add(item_key)
    await state.update_data(items=list(selected))
    try:
        await call.message.edit_reply_markup(
            reply_markup=auto_pick_items_kb(geo, line_key, selected=selected)
        )
    except TelegramBadRequest:
        pass
    await call.answer()


@router.callback_query(AutoFSM.picking_items, F.data == "auto:items:done")
async def auto_items_done(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    items = data.get("items") or []
    if not items:
        await call.answer("⚠️ Выберите хотя бы 1 тип чека", show_alert=True)
        return
    await state.set_state(AutoFSM.entering_sum)
    text = (
        f"⚙️ <b>Настройка автоматизации</b>\n"
        f"{DIV}\n"
        f"💰 <b>Шаг 4 / 6 — Диапазон сумм</b>\n\n"
        f"✅ Выбрано типов: <b>{len(items)}</b>\n\n"
        f"Отправьте <b>мин</b> и <b>макс</b> сумму одного чека через дефис.\n\n"
        f"Пример: <code>1000-5000</code>"
    )
    await call.message.edit_text(text, reply_markup=auto_back_kb(), parse_mode=PM)
    await call.answer()


# ── Суммы ─────────────────────────────────────────────────────────────────────
@router.message(AutoFSM.entering_sum)
async def auto_sum_entered(message: Message, state: FSMContext):
    raw = (message.text or "").strip()
    m = re.fullmatch(r"\s*(\d{1,9})\s*[-–]\s*(\d{1,9})\s*", raw)
    if not m:
        await message.answer(
            f"❌ <b>Неверный формат</b>\n\n"
            f"Нужны два числа через дефис, например:\n<code>1000-5000</code>",
            parse_mode=PM,
        )
        return
    lo, hi = int(m.group(1)), int(m.group(2))
    if lo > hi:
        lo, hi = hi, lo
    await state.update_data(sum_min=lo, sum_max=hi)
    await state.set_state(AutoFSM.entering_date)
    text = (
        f"⚙️ <b>Настройка автоматизации</b>\n"
        f"{DIV}\n"
        f"📅 <b>Шаг 5 / 6 — Дата чеков</b>\n\n"
        f"✅ Суммы: <b>{lo}–{hi}</b>\n\n"
        f"Отправьте дату в формате <code>dd.mm.yyyy</code>\n"
        f"Пример: <code>26.08.2026</code>"
    )
    await message.answer(text, reply_markup=auto_back_kb(), parse_mode=PM)


# ── Дата ──────────────────────────────────────────────────────────────────────
@router.message(AutoFSM.entering_date)
async def auto_date_entered(message: Message, state: FSMContext):
    raw = (message.text or "").strip()
    try:
        datetime.strptime(raw, "%d.%m.%Y")
    except ValueError:
        await message.answer(
            f"❌ <b>Неверный формат даты</b>\n\n"
            f"Используйте <code>dd.mm.yyyy</code>, например <code>26.08.2026</code>",
            parse_mode=PM,
        )
        return
    await state.update_data(date=raw)
    await state.set_state(AutoFSM.entering_timeline)
    text = (
        f"⚙️ <b>Настройка автоматизации</b>\n"
        f"{DIV}\n"
        f"⏰ <b>Шаг 6 / 6 — Таймлайн и количество</b>\n\n"
        f"✅ Дата: <b>{raw}</b>\n\n"
        f"Можно указать один или несколько диапазонов через запятую или с новой строки.\n"
        f"Формат одной записи: <code>start–end N</code>\n\n"
        f"<b>Пример 1 (один диапазон):</b>\n"
        f"<code>14:30–18:00 10</code>\n\n"
        f"<b>Пример 2 (несколько диапазонов за раз):</b>\n"
        f"<code>14:30–15:30 5, 16:30–17:30 3, 18:30–19:30 6</code>\n\n"
        f"Бот сам распределит время внутри каждого диапазона "
        f"с шагом <b>5–20 мин</b>, не вылезая за границы."
    )
    await message.answer(text, reply_markup=auto_back_kb(), parse_mode=PM)


# ── Слоты → пресет ────────────────────────────────────────────────────────────
@router.message(AutoFSM.entering_timeline)
async def auto_timeline_entered(message: Message, state: FSMContext):
    """Парсит одну или несколько записей «start–end N» (через запятую или с новой строки),
    валидирует и сохраняет пресет с timelines (список диапазонов)."""
    parsed_list = _parse_timeline(message.text or "")
    if not parsed_list:
        await message.answer(
            f"❌ <b>Неверный формат</b>\n\n"
            f"Нужно: <code>ЧЧ:ММ–ЧЧ:ММ N</code> (1–3 диапазона)\n"
            f"Пример 1: <code>14:30–18:00 10</code>\n"
            f"Пример 2: <code>14:30–15:30 5, 16:30–17:30 3, 18:30–19:30 6</code>",
            parse_mode=PM,
        )
        return

    total_count = 0
    for start_min, end_min, count in parsed_list:
        span = end_min - start_min
        if span < 5:
            await message.answer(
                f"❌ <b>Диапазон слишком мал</b>\n\n"
                f"Между <b>{start_min // 60:02d}:{start_min % 60:02d}</b> и "
                f"<b>{end_min // 60:02d}:{end_min % 60:02d}</b> меньше 5 минут. "
                f"Расширьте диапазон.",
                parse_mode=PM,
            )
            return
        if count < 1 or count > 200:
            await message.answer(
                f"❌ <b>Количество чеков</b> в диапазоне должно быть от 1 до 200.",
                parse_mode=PM,
            )
            return
        total_count += count
        if total_count > 300:
            await message.answer(
                f"❌ <b>Слишком много чеков</b> суммарно (>300). Сократите.",
                parse_mode=PM,
            )
            return

    data = await state.get_data()
    preset = {
        "geo": data["geo"],
        "line_key": data["line_key"],
        "items": sorted(data["items"]),
        "sum_min": data["sum_min"],
        "sum_max": data["sum_max"],
        "date": data["date"],
        "timelines": [
            {"start_min": s, "end_min": e, "count": n}
            for (s, e, n) in parsed_list
        ],
    }
    _save_preset(message.from_user.id, preset)
    await state.clear()

    lines = []
    for s, e, n in parsed_list:
        lines.append(
            f"   {BULLET} <b>{s // 60:02d}:{s % 60:02d}</b>"
            f" – <b>{e // 60:02d}:{e % 60:02d}</b> · <b>{n}</b> чек(ов)"
        )
    timeline_text = "\n".join(lines)
    text = (
        f"🎉 <b>Пресет сохранён!</b>\n"
        f"{DIV}\n"
        f"{_format_preset(preset)}\n\n"
        f"{DIV}\n"
        f"⏰ <b>Таймлайн ({total_count} чеков):</b>\n"
        f"{timeline_text}\n\n"
        f"▶️ Нажмите <b>«🚀 Запустить автоматизацию»</b> для старта."
    )
    await message.answer(text, reply_markup=auto_run_kb(), parse_mode=PM)


# ── Запуск ────────────────────────────────────────────────────────────────────
@router.callback_query(F.data == "auto:run")
async def auto_run(call: CallbackQuery, state: FSMContext):
    user_id = call.from_user.id
    if not has_any_access(user_id):
        await call.answer("⛔ Доступ запрещён", show_alert=True)
        return
    preset = _load_preset(user_id)
    if not preset:
        await call.answer("⚠️ Сначала настройте пресет", show_alert=True)
        return

    # Строим таймлайн (рандомные моменты времени с шагом 5-20 мин)
    if "timelines" in preset:
        times_list = []
        for tl in preset["timelines"]:
            times_list.extend(
                _build_random_timeline(tl["start_min"], tl["end_min"], tl["count"])
            )
        total = len(times_list)
    elif "timeline" in preset:
        # Backward compat: одиночный timeline (старый формат)
        tl = preset["timeline"]
        times_list = _build_random_timeline(tl["start_min"], tl["end_min"], tl["count"])
        total = len(times_list)
    else:
        # Backward compat: старые пресеты с ручными слотами
        times_list = []
        for slot in preset.get("slots", []):
            for _ in range(slot["count"]):
                times_list.append(slot["time"])
        total = len(times_list)

    await call.message.edit_text(
        f"⏳ <b>Генерация запущена…</b>\n"
        f"{DIV}\n"
        f"Будет создано <b>{total}</b> чеков.\n\n"
        f"<i>Это может занять несколько секунд.</i>",
        parse_mode=PM,
    )
    await call.answer()

    bot: Bot = call.bot
    await call.message.answer(
        f"🚀 <b>Автоматизация запущена</b>\n"
        f"{DIV}\n"
        f"📦 Чеков: <b>{total}</b>",
        parse_mode=PM,
    )

    media: list = []
    BATCH = 10
    render_errors = 0  # FIX (Bug F): трекать неудачные рендеры
    for i, time_str in enumerate(times_list):
        item_key = random.choice(preset["items"])
        amount = random.randint(preset["sum_min"], preset["sum_max"])
        try:
            line = GEO_CATALOG[preset["geo"]]["catalog"][preset["line_key"]]
            item = next(
                section["items"][item_key]
                for section in line.get("sections", {}).values()
                if item_key in section.get("items", {})
            )
            values = _render_values(item, preset["date"], time_str, amount)
            # Рандомный банк на каждый чек (если у item есть список banks)
            banks = item.get("banks")
            if banks:
                values["bank"] = random.choice(banks)
            # 50/50 мужские/женские имена: чередуем по индексу
            prefer_gender = "male" if (i % 2 == 0) else "female"
            name = _pick_random_name(prefer_gender)
            values["name"] = name
            values["fullname"] = name
            values["name_1"] = name
            values["name_2"] = name
            # Прокидываем ФИО во все ключи шаблона, похожие на имя/получателя/отправителя
            # (включая destino, origen, recipient_name, sender_name, *_destino и т.п.).
            _fill_name_fields(item, values, name)
            _apply_gender_field(item, values, prefer_gender)
            rendered = render_image(item_key, values, preset["geo"], item=item)
            png_bytes = rendered.getvalue()
        except Exception as e:
            log.error(f"auto_run render error: {e}")
            # FIX (Bug F): считать ошибки рендеринга, чтобы итоговое сообщение не врало
            render_errors += 1
            continue
        caption = (
            f"⏰ <b>{time_str}</b>  ·  чек <b>{i + 1}/{total}</b>  ·  "
            f"<code>{item_key}</code>"
        )
        media.append(
            InputMediaPhoto(
                media=BufferedInputFile(png_bytes, filename="check.png"),
                caption=caption if i == 0 else None,
                parse_mode=PM if i == 0 else None,
            )
        )
        if len(media) >= BATCH:
            try:
                await bot.send_media_group(call.message.chat.id, media=media)
            except TelegramBadRequest as e:
                log.error(f"auto_run send_media_group error: {e}")
            media = []
            await asyncio.sleep(1.0)
    if media:
        try:
            await bot.send_media_group(call.message.chat.id, media=media)
        except TelegramBadRequest as e:
            log.error(f"auto_run send_media_group error: {e}")

    sent_ok = total - render_errors
    await call.message.answer(
        f"✅ <b>Готово!</b>\n{DIV}\n"
        f"Удачно создано: <b>{sent_ok}/{total}</b> чеков"
        + (f"\nОшибок рендера: <b>{render_errors}</b>" if render_errors else "")
        + " 🎉",
        reply_markup=auto_batch_done_kb(),
        parse_mode=PM,
    )


# ── Смена даты без перенастройки всего пресета ──────────────────────────────
@router.callback_query(F.data == "auto:change_date")
async def auto_change_date(call: CallbackQuery, state: FSMContext):
    user_id = call.from_user.id
    if not has_any_access(user_id):
        await call.answer("⛔ Доступ запрещён", show_alert=True)
        return
    preset = _load_preset(user_id)
    if not preset:
        await call.answer("⚠️ Сначала настройте пресет", show_alert=True)
        return
    await state.set_state(AutoFSM.changing_date)
    cur = preset.get("date", "—")
    text = (
        f"📅 <b>Изменить дату</b>\n"
        f"{DIV}\n"
        f"Текущая дата: <b>{cur}</b>\n\n"
        f"Отправьте новую дату в формате <code>dd.mm.yyyy</code>\n"
        f"Пример: <code>26.08.2026</code>"
    )
    await call.message.answer(text, reply_markup=auto_back_kb(), parse_mode=PM)
    await call.answer()


@router.message(AutoFSM.changing_date)
async def auto_change_date_entered(message: Message, state: FSMContext):
    raw = (message.text or "").strip()
    try:
        datetime.strptime(raw, "%d.%m.%Y")
    except ValueError:
        await message.answer(
            f"❌ <b>Неверный формат даты</b>\n\n"
            f"Используйте <code>dd.mm.yyyy</code>, например <code>26.08.2026</code>",
            parse_mode=PM,
        )
        return
    user_id = message.from_user.id
    preset = _load_preset(user_id)
    if not preset:
        await state.clear()
        await message.answer(
            f"⚠️ Пресет не найден, настройте автоматизацию заново.",
            reply_markup=auto_main_kb(has_preset=False),
            parse_mode=PM,
        )
        return
    preset["date"] = raw
    _save_preset(user_id, preset)
    await state.clear()
    text = (
        f"✅ <b>Дата обновлена!</b>\n"
        f"{DIV}\n"
        f"📅 Новая дата: <b>{raw}</b>\n\n"
        f"{_format_preset(preset)}\n\n"
        f"{DIV}\n"
        f"▶️ Нажмите <b>«🚀 Запустить автоматизацию»</b> для старта."
    )
    await message.answer(text, reply_markup=auto_run_kb(), parse_mode=PM)


# ── Утилиты ───────────────────────────────────────────────────────────────────
def _parse_hhmm(s: str) -> int | None:
    m = re.fullmatch(r"\s*(\d{1,2}):(\d{2})\s*", s)
    if not m:
        return None
    hh, mm = int(m.group(1)), int(m.group(2))
    if not (0 <= hh <= 23 and 0 <= mm <= 59):
        return None
    return hh * 60 + mm


_RANGE_RE = re.compile(r"(\d{1,2}:\d{2})\s*[-–—]\s*(\d{1,2}:\d{2})\s+(\d{1,3})")


def _parse_timeline(text: str) -> list[tuple[int, int, int]] | None:
    """Парсит одну или несколько записей «14:30–18:00 10».

    Разделители: запятая или перевод строки. Возвращает список кортежей
    [(start_min, end_min, count), ...] в порядке ввода.
    Возвращает None, если ни одной валидной записи не найдено.
    """
    if not text:
        return None
    result: list[tuple[int, int, int]] = []
    # Разбиваем по запятой или новой строке
    parts = re.split(r"[,\n]+", text)
    for part in parts:
        s = part.strip()
        if not s:
            continue
        m = _RANGE_RE.fullmatch(s)
        if not m:
            return None
        a, b, n = m.group(1), m.group(2), int(m.group(3))
        start = _parse_hhmm(a)
        end = _parse_hhmm(b)
        if start is None or end is None:
            return None
        if start > end:
            start, end = end, start
        result.append((start, end, n))
    return result or None


def _bias_round_minute(t: int, start_min: int, end_min: int) -> int:
    """Сдвигает минуту так, чтобы избежать «красивых» :00 / :30.
    Делает «круглые» значения исключением (≈ 15% шанс сохранить).
    Сдвиг — случайная дельта в [-14, -1] ∪ [1, 14] (модуль 30).
    Не выходит за границы диапазона.
    """
    if t % 30 != 0:
        return t
    # 15% шанс оставить как есть
    if random.random() < 0.05:
        return t
    for _ in range(8):
        # Знак берём случайно, чтобы сдвигать и вверх, и вниз
        sign = random.choice([-1, 1])
        delta = random.randint(1, 14) * sign
        new_t = t + delta
        if start_min <= new_t <= end_min:
            return new_t
    # Не удалось сдвинуть — оставляем
    return t


def _build_random_timeline(start_min: int, end_min: int, count: int) -> list[str]:
    """Распределяет count чеков между start_min и end_min со случайным
    шагом 5–20 минут, не вылезая за end_min.
    Возвращает список строк времени (HH:MM), отсортированный по возрастанию.
    После построения прогоняет каждое время через _bias_round_minute —
    чтобы избежать слишком «круглых» :00/:30.

    Логика:
      * Если span/(count-1) ≤ 20 (все чеки помещаются с шагом ≤ 20) —
        используем случайные шаги в [5, 20] и последний принудительно
        равен end_min. Алгоритм итеративный: на каждом шаге гарантируем,
        что оставшийся span вмещает минимум 5 мин между оставшимися точками.
      * Если span/(count-1) > 20 (span слишком велик для шага ≤ 20) —
        равномерно распределяем count точек по span (последняя = end_min),
        джиттер не нужен, потому что иначе один gap всё равно будет >20.
    """
    if count <= 0:
        return []
    span = end_min - start_min
    if span < 0:
        return []
    if count == 1:
        t = _bias_round_minute(start_min, start_min, end_min)
        return [f"{t // 60:02d}:{t % 60:02d}"]

    n_intervals = count - 1
    ideal_step = span / n_intervals  # float

    if ideal_step > 20:
        # span свободный — расставляем равномерно, не вписываемся в шаг 5–20.
        # Возвращаем равномерную сетку с лёгким случайным джиттером.
        jitter_range = max(1, int((ideal_step - 20) / 2))
        times = [start_min]  # первая точка жёстко start_min
        for i in range(1, count):
            if i == count - 1:
                t = end_min
            else:
                ideal = start_min + round(ideal_step * i)
                t = ideal + random.randint(-jitter_range, jitter_range)
                if t < start_min:
                    t = start_min
                if t > end_min:
                    t = end_min
            times.append(t)
        # Прогоняем все точки (кроме граничных) через bias
        out = []
        for i, t in enumerate(times):
            if i == 0 or i == len(times) - 1:
                out.append(t)
            else:
                out.append(_bias_round_minute(t, start_min, end_min))
        return [f"{t // 60:02d}:{t % 60:02d}" for t in out]

    # span плотный — укладываемся в шаг 5–20 мин, последний = end_min.
    # На каждой итерации: выбираем шаг в [5,20], но не больше оставшегося
    # span за вычетом минимальных 5 мин на оставшиеся точки.
    times = [start_min]
    cur = start_min
    for i in range(1, count):
        if i == count - 1:
            t = end_min
        else:
            # Осталось (n_intervals - i + 1) шагов, минимум по 5 каждый
            remaining_steps = count - i  # включая текущий
            max_gap = (end_min - cur) - 5 * (remaining_steps - 1)
            hi = min(20, max_gap)
            lo = 5
            if hi < lo:
                hi = lo
            gap = random.randint(lo, hi)
            t = cur + gap
            if t > end_min:
                t = end_min
        times.append(t)
        cur = t

    # Если последний не равен end_min (например из-за экстремальной случайности),
    # форсируем последний.
    if times[-1] != end_min:
        times[-1] = end_min

    # Прогоняем внутренние точки через bias (граничные start/end не трогаем)
    out = []
    for i, t in enumerate(times):
        if i == 0 or i == len(times) - 1:
            out.append(t)
        else:
            out.append(_bias_round_minute(t, start_min, end_min))

    return [f"{t // 60:02d}:{t % 60:02d}" for t in out]


def _format_preset(p: dict) -> str:
    geo_label = GEO_CATALOG.get(p["geo"], {}).get("label", p["geo"])
    items_str = ", ".join(f"<code>{x}</code>" for x in p["items"])
    if "timelines" in p:
        total = sum(tl["count"] for tl in p["timelines"])
    elif "timeline" in p:
        total = p["timeline"]["count"]
    else:
        total = sum(s["count"] for s in p["slots"])
    lines = [
        f"🌍 <b>ГЕО:</b> {geo_label}",
        f"📂 <b>Линейка:</b> <code>{p['line_key']}</code>",
        f"🎯 <b>Типы чеков:</b> {items_str}",
        f"💰 <b>Суммы:</b> <b>{p['sum_min']}–{p['sum_max']}</b>",
        f"📅 <b>Дата:</b> <b>{p['date']}</b>",
        f"⏰ <b>Таймлайн ({total} чеков):</b>",
    ]
    if "timelines" in p:
        for tl in p["timelines"]:
            s_min = tl["start_min"]
            e_min = tl["end_min"]
            lines.append(
                f"   {BULLET} <b>{s_min // 60:02d}:{s_min % 60:02d}</b>"
                f" – <b>{e_min // 60:02d}:{e_min % 60:02d}</b> · "
                f"<b>{tl['count']}</b> чек(ов) (ранд. шаг 5–20 мин)"
            )
    elif "timeline" in p:
        tl = p["timeline"]
        s_min = tl["start_min"]
        e_min = tl["end_min"]
        lines.append(
            f"   {BULLET} <b>{s_min // 60:02d}:{s_min % 60:02d}</b>"
            f" – <b>{e_min // 60:02d}:{e_min % 60:02d}</b> · "
            f"<b>{tl['count']}</b> чек(ов) (ранд. шаг 5–20 мин)"
        )
    else:
        for s in p.get("slots", []):
            lines.append(f"   {BULLET} <b>{s['time']}</b> × <b>{s['count']}</b>")
    return "\n".join(lines)


# ── Хранение пресетов (SQLite рядом с bot.db) ─────────────────────────────────
# Мы добавим таблицу automation_presets миграцией в data/db.py,
# а здесь работаем через голый sqlite3, чтобы не зависеть от внутреннего _conn.
import sqlite3
import threading
from pathlib import Path

_PRESETS_LOCK = threading.Lock()
_PRESETS_PATH = Path(__file__).resolve().parent.parent / "bot.db"


def _presets_conn() -> sqlite3.Connection:
    con = sqlite3.connect(_PRESETS_PATH)
    con.row_factory = sqlite3.Row
    con.execute("PRAGMA journal_mode=WAL")
    return con


def _ensure_presets_table():
    with _PRESETS_LOCK:
        con = _presets_conn()
        con.execute("""
            CREATE TABLE IF NOT EXISTS automation_presets (
                user_id INTEGER PRIMARY KEY,
                preset_json TEXT NOT NULL,
                updated_at TEXT DEFAULT (datetime('now'))
            )
        """)
        con.commit()
        con.close()


def _save_preset(user_id: int, preset: dict):
    _ensure_presets_table()
    with _PRESETS_LOCK:
        con = _presets_conn()
        con.execute(
            """INSERT INTO automation_presets (user_id, preset_json, updated_at)
               VALUES (?, ?, datetime('now'))
               ON CONFLICT(user_id) DO UPDATE SET
                   preset_json=excluded.preset_json,
                   updated_at=excluded.updated_at""",
            (user_id, json.dumps(preset, ensure_ascii=False)),
        )
        con.commit()
        con.close()


def _load_preset(user_id: int) -> dict | None:
    _ensure_presets_table()
    with _PRESETS_LOCK:
        con = _presets_conn()
        row = con.execute(
            "SELECT preset_json FROM automation_presets WHERE user_id = ?",
            (user_id,),
        ).fetchone()
        con.close()
    if not row:
        return None
    return json.loads(row["preset_json"])


# ── Генератор имён 50/50 M/F ─────────────────────────────────────────────
_FEMALE_NAME_RE = re.compile(r"[aá]\s*$", re.IGNORECASE)
_MALE_NAME_RE = re.compile(r"o\s*$", re.IGNORECASE)


def _classify_fio_gender(fio: str) -> str:
    """Эвристика пола по последнему слову ФИО.
    Испанские имена: женские обычно заканчиваются на 'a', мужские на 'o'.
    Если непонятно — возвращаем 'unknown'.
    """
    parts = (fio or "").strip().split()
    if not parts:
        return "unknown"
    last = parts[-1]
    if _FEMALE_NAME_RE.search(last):
        return "female"
    if _MALE_NAME_RE.search(last):
        return "male"
    return "unknown"


def _pick_random_name(prefer: str) -> str:
    """Берёт случайное ФИО из name.json с учётом предпочтительного пола.
    prefer: 'male' | 'female' | что угодно (тогда без фильтра).
    Если подходящих нет — fallback на любое случайное.
    """
    pool = get_available_names() or []
    if not pool:
        return "AUTOMATION USER"
    if prefer in ("male", "female"):
        filtered = [n for n in pool if _classify_fio_gender(n) == prefer]
        if not filtered:
            filtered = pool
    else:
        filtered = pool
    return random.choice(filtered)


def _apply_gender_field(item: dict, values: dict, prefer: str) -> None:
    """Если в item.fields есть поле с key='gender' — подставляем значение пола.
    Испанские шаблоны: 'o' (male) / 'a' (female).
    Арабские (Morocco): 'y' (male) / 't' (female).
    Определяем по уже существующему default значения: если в default встречается
    'o'/'a' — испанский; если 'y'/'t' — арабский.
    """
    for field in item.get("fields", []):
        if field.get("key") != "gender":
            continue
        default = str(field.get("default", ""))
        if prefer == "male":
            if "o" in default and "y" not in default and "t" not in default:
                values["gender"] = "o"
            elif "y" in default:
                values["gender"] = "y"
            else:
                values["gender"] = default or "o"
        elif prefer == "female":
            if "a" in default and "t" not in default:
                values["gender"] = "a"
            elif "t" in default:
                values["gender"] = "t"
            else:
                values["gender"] = default or "a"
        break


# Ключи, которые выглядят как ФИО — перезаписываем рандомным именем
_NAME_FIELD_HINTS = ("name", "destino", "origen", "fio")


def _fill_name_fields(item: dict, values: dict, name: str) -> None:
    """Проставляет ФИО во все поля шаблона, которые выглядят как ФИО.
    Заменяет плейсхолдеры AUTOMATION USER / AUTOMATION SENDER и заполняет
    поля, которых нет в values (например destino, origen, _recipient_name_destino)."""
    for field in item.get("fields", []):
        fkey = field.get("key", "")
        if not fkey:
            continue
        fl = fkey.lower()
        if any(h in fl for h in _NAME_FIELD_HINTS):
            cur = values.get(fkey)
            if not cur or cur in ("AUTOMATION USER", "AUTOMATION SENDER", "Jose Garcia"):
                values[fkey] = name
    # Явно проставляем известные ключи-получатели/отправители
    for k in (
        "destino", "origen", "recipient_name", "sender_name",
        "receiver_name", "client_name", "payer_1", "payer_2",
        "name1", "name2", "_recipient_name_destino",
    ):
        if k not in values or values[k] in ("AUTOMATION USER", "AUTOMATION SENDER", "Jose Garcia", ""):
            values[k] = name


def _render_values(item: dict, date: str, time: str, amount: int) -> dict:
    """Готовит значения полей для render_image из выбранного шаблона."""
    values = {
        "date": date,
        "time": time,
        "amount": str(amount),
        "name": "AUTOMATION USER",
        "fullname": "AUTOMATION USER",
        "name_1": "AUTOMATION USER",
        "name_2": "AUTOMATION USER",
        "sender_name": "Jose Garcia",
        "account": "00000000",
        "acc_num": "00000000",
        "transaction": "000000000",
        "order": "00000000",
        "bank": "Banco Unión",
        "currency": "USD",
        "msg1": "",
        "msg2": "",
    }
    for field in item.get("fields", []):
        key = field.get("key")
        if not key or key in values:
            continue
        default = field.get("default")
        if default is not None:
            values[key] = str(default)
    return values


@router.callback_query(F.data == "auto:reset")
async def auto_reset(call: CallbackQuery, state: FSMContext):
    """Удаляет сохранённый пресет и возвращает меню автоматизации."""
    if not has_any_access(call.from_user.id):
        await call.answer("⛔ Доступ запрещён", show_alert=True)
        return
    await state.clear()
    clear_preset(call.from_user.id)
    text = (
        f"🤖 <b>Автоматизация чеков</b>\n"
        f"{DIV}\n"
        f"🗑 Пресет <b>удалён</b>.\n\n"
        f"Нажмите <b>«⚙️ Настроить автоматизацию»</b> чтобы задать новый."
    )
    await call.message.edit_text(text, reply_markup=auto_main_kb(has_preset=False), parse_mode=PM)
    await call.answer()


def clear_preset(user_id: int):
    _ensure_presets_table()
    with _PRESETS_LOCK:
        con = _presets_conn()
        con.execute("DELETE FROM automation_presets WHERE user_id = ?", (user_id,))
        con.commit()
        con.close()
