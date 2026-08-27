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
       6. Расписание слотов «ЧЧ:ММxN» по строкам
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
    get_geos,
    has_any_access,
    is_admin,
)
from keyboards.auto_kb import (
    auto_back_kb,
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
    entering_slots = State()


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
    await state.set_state(AutoFSM.entering_slots)
    text = (
        f"⚙️ <b>Настройка автоматизации</b>\n"
        f"{DIV}\n"
        f"⏰ <b>Шаг 6 / 6 — Расписание слотов</b>\n\n"
        f"✅ Дата: <b>{raw}</b>\n\n"
        f"Каждый слот — строка <code>ЧЧ:ММxN</code>, где N — сколько чеков в это время.\n"
        f"Слоты по одному на строку. <b>Время должно возрастать</b>.\n\n"
        f"<b>Пример:</b>\n<code>14:30x3\n15:30x2\n17:00x4\n19:30x1</code>"
    )
    await message.answer(text, reply_markup=auto_back_kb(), parse_mode=PM)


# ── Слоты → пресет ────────────────────────────────────────────────────────────
@router.message(AutoFSM.entering_slots)
async def auto_slots_entered(message: Message, state: FSMContext):
    slots = _parse_slots(message.text or "")
    if not slots:
        await message.answer(
            f"❌ <b>Не удалось разобрать расписание</b>\n\n"
            f"Каждая строка: <code>ЧЧ:ММxN</code>. Пример:\n"
            f"<code>14:30x3\n15:30x2</code>",
            parse_mode=PM,
        )
        return
    # Проверка возрастания времени
    for i in range(1, len(slots)):
        if slots[i]["minutes"] <= slots[i - 1]["minutes"]:
            await message.answer(
                f"� <b>Время должно возрастать</b>\n\n"
                f"Строка <code>{slots[i]['time']}</code> идёт раньше или равна "
                f"<code>{slots[i - 1]['time']}</code>.",
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
        "slots": slots,
    }
    _save_preset(message.from_user.id, preset)
    await state.clear()

    total = sum(s["count"] for s in slots)
    text = (
        f"🎉 <b>Пресет сохранён!</b>\n"
        f"{DIV}\n"
        f"{_format_preset(preset)}\n\n"
        f"{DIV}\n"
        f"📦 Всего чеков: <b>{total}</b> в <b>{len(slots)}</b> слотов\n\n"
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

    total = sum(s["count"] for s in preset["slots"])
    await call.message.edit_text(
        f"⏳ <b>Генерация запущена…</b>\n"
        f"{DIV}\n"
        f"Будет создано <b>{total}</b> чеков в <b>{len(preset['slots'])}</b> слотов.\n\n"
        f"<i>Это может занять несколько секунд.</i>",
        parse_mode=PM,
    )
    await call.answer()

    bot: Bot = call.bot
    # Краткое уведомление в чат, чтобы пользователь видел, что процесс пошёл
    await call.message.answer(
        f"🚀 <b>Автоматизация запущена</b>\n"
        f"{DIV}\n"
        f"📦 Чеков: <b>{total}</b>\n"
        f"⏰ Слотов: <b>{len(preset['slots'])}</b>",
        parse_mode=PM,
    )

    for slot in preset["slots"]:
        time_str = slot["time"]
        count = slot["count"]
        # Соберём медиагруппу альбомом — все чеки этого слота одним сообщением
        media = []
        for i in range(count):
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
                rendered = render_image(item_key, values, preset["geo"], item=item)
                png_bytes = rendered.getvalue()
            except Exception as e:
                log.error(f"auto_run render error: {e}")
                continue
            caption = (
                f"⏰ <b>{time_str}</b>  ·  чек <b>{i + 1}/{count}</b>  ·  <code>{item_key}</code>"
            )
            media.append(
                InputMediaPhoto(
                    media=BufferedInputFile(png_bytes, filename="check.png"),
                    caption=caption if i == 0 else None,
                    parse_mode=PM if i == 0 else None,
                )
            )
        if media:
            try:
                await bot.send_media_group(call.message.chat.id, media=media)
            except TelegramBadRequest as e:
                log.error(f"auto_run send_media_group error: {e}")
        # Небольшая пауза между слотами, чтобы Telegram не считал спамом
        await asyncio.sleep(1.5)

    # Финальное уведомление
    await call.message.answer(
        f"✅ <b>Готово!</b>\n{DIV}\nВсе слоты отработаны. 🎉",
        parse_mode=PM,
    )


# ── Утилиты ───────────────────────────────────────────────────────────────────
def _parse_slots(text: str) -> list[dict]:
    """Разбирает текст вида '14:30x3\n15:30x2' → [{'time':'14:30','count':3,'minutes':870}, ...]"""
    out = []
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        m = re.fullmatch(r"(\d{1,2}):(\d{2})\s*[xх*]\s*(\d{1,3})", line)
        if not m:
            return []
        hh, mm, cnt = int(m.group(1)), int(m.group(2)), int(m.group(3))
        if not (0 <= hh <= 23 and 0 <= mm <= 59 and 1 <= cnt <= 50):
            return []
        out.append({"time": f"{hh:02d}:{mm:02d}", "count": cnt, "minutes": hh * 60 + mm})
    return out


def _format_preset(p: dict) -> str:
    geo_label = GEO_CATALOG.get(p["geo"], {}).get("label", p["geo"])
    items_str = ", ".join(f"<code>{x}</code>" for x in p["items"])
    total = sum(s["count"] for s in p["slots"])
    lines = [
        f"🌍 <b>ГЕО:</b> {geo_label}",
        f"📂 <b>Линейка:</b> <code>{p['line_key']}</code>",
        f"🎯 <b>Типы чеков:</b> {items_str}",
        f"💰 <b>Суммы:</b> <b>{p['sum_min']}–{p['sum_max']}</b>",
        f"📅 <b>Дата:</b> <b>{p['date']}</b>",
        f"⏰ <b>Слоты ({len(p['slots'])} · {total} чеков):</b>",
    ]
    for s in p["slots"]:
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
        "sender_name": "AUTOMATION SENDER",
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
