"""handlers/auto.py — автоматизация создания чеков по расписанию.

Изолировано от ручного режима: отдельная таблица `automation_presets`
и отдельная кнопка входа в меню «▶️ Автоматизация».

Сценарий:
  1. Пользователь жмёт «▶️ Автоматизация» → бот показывает пресет
     (если есть) и кнопки: «Изменить настройки» / «Запустить».
  2. В настройках автоматизации (auto:menu) — отдельное FSM-подменю:
       auto:geo     — выбор гео (из доступных)
       auto:line    — выбор линейки (внутри гео)
       auto:items   — мультивыбор типов чеков (item_key)
       auto:sum     — мин/макс сумма (текстом «1000-5000»)
       auto:date    — дата dd.mm.yyyy
       auto:slots   — расписание слотов текстом:
                      14:30x3
                      15:00x2
                      16:30x4
                      19:30x1
  3. Кнопка «🚀 Запустить» — генерация медиагруппы.
"""
from __future__ import annotations

import asyncio
import json
import random
import re
from datetime import datetime
from io import BytesIO

from aiogram import Bot, F, Router
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

    preset = _load_preset(user_id)
    text_lines = ["🤖 <b>Автоматизация создания чеков</b>\n"]
    if preset:
        text_lines.append(_format_preset(preset))
    else:
        text_lines.append("Пресет не настроен. Нажмите «⚙️ Настройки».")

    await call.message.edit_text("\n".join(text_lines), reply_markup=auto_main_kb(has_preset=bool(preset)))
    await call.answer()


# ── Меню настроек ─────────────────────────────────────────────────────────────
@router.callback_query(F.data == "auto:settings")
async def auto_settings(call: CallbackQuery, state: FSMContext):
    geos = get_geos(call.from_user.id)
    if is_admin(call.from_user.id):
        geos = list(GEO_CATALOG.keys())
    if not geos:
        await call.answer("⛔ Нет доступных гео", show_alert=True)
        return
    await state.set_state(AutoFSM.picking_geo)
    if not geos:
        await call.answer("⛔ Нет доступных гео", show_alert=True)
        return
    await call.message.edit_text(
        "1️⃣ Выберите <b>ГЕО</b> для автоматизации:",
        reply_markup=auto_pick_geo_kb(geos),
    )
    await call.answer()


# ── Выбор гео ─────────────────────────────────────────────────────────────────
@router.callback_query(AutoFSM.picking_geo, F.data.startswith("auto:geo:"))
async def auto_geo_picked(call: CallbackQuery, state: FSMContext):
    geo = call.data.split(":", 2)[2]
    if geo not in GEO_CATALOG:
        await call.answer("Неизвестное гео", show_alert=True)
        return
    await state.update_data(geo=geo)
    await state.set_state(AutoFSM.picking_line)
    await call.message.edit_text(
        f"2️⃣ ГЕО: <b>{GEO_CATALOG[geo]['label']}</b>\n"
        "Выберите <b>линейку</b> шаблонов:",
        reply_markup=auto_pick_line_kb(geo, call.from_user.id),
    )
    await call.answer()


# ── Выбор линейки ─────────────────────────────────────────────────────────────
@router.callback_query(AutoFSM.picking_line, F.data.startswith("auto:line:"))
async def auto_line_picked(call: CallbackQuery, state: FSMContext):
    _, _, geo, line_key = call.data.split(":", 3)
    line = GEO_CATALOG[geo]["catalog"].get(line_key)
    if not line:
        await call.answer("Неизвестная линейка", show_alert=True)
        return
    await state.update_data(line_key=line_key)
    await state.set_state(AutoFSM.picking_items)
    await call.message.edit_text(
        f"3️⃣ Линейка: <b>{line['label']}</b>\n"
        "Выберите <b>типы чеков</b> (мультивыбор).\n"
        "Нажмите «✅ Готово» когда выберете все нужные:",
        reply_markup=auto_pick_items_kb(geo, line_key, selected=set()),
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
    await call.message.edit_reply_markup(
        reply_markup=auto_pick_items_kb(geo, line_key, selected=selected)
    )
    await call.answer()


@router.callback_query(AutoFSM.picking_items, F.data == "auto:items:done")
async def auto_items_done(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    items = data.get("items") or []
    if not items:
        await call.answer("Выберите хотя бы 1 тип чека", show_alert=True)
        return
    await state.set_state(AutoFSM.entering_sum)
    await call.message.edit_text(
        "4️⃣ <b>Мин / Макс суммы</b> для одного чека.\n"
        "Отправьте два числа через дефис, например:\n"
        "<code>1000-5000</code>",
        reply_markup=auto_back_kb(),
    )
    await call.answer()


# ── Суммы ─────────────────────────────────────────────────────────────────────
@router.message(AutoFSM.entering_sum)
async def auto_sum_entered(message: Message, state: FSMContext):
    raw = (message.text or "").strip()
    m = re.fullmatch(r"\s*(\d{1,9})\s*[-–]\s*(\d{1,9})\s*", raw)
    if not m:
        await message.answer("❌ Неверный формат. Пример: <code>1000-5000</code>")
        return
    lo, hi = int(m.group(1)), int(m.group(2))
    if lo > hi:
        lo, hi = hi, lo
    await state.update_data(sum_min=lo, sum_max=hi)
    await state.set_state(AutoFSM.entering_date)
    await message.answer(
        "5️⃣ <b>Дата</b> чеков в формате <code>dd.mm.yyyy</code>.\n"
        "Например: <code>26.08.2026</code>",
        reply_markup=auto_back_kb(),
    )


# ── Дата ──────────────────────────────────────────────────────────────────────
@router.message(AutoFSM.entering_date)
async def auto_date_entered(message: Message, state: FSMContext):
    raw = (message.text or "").strip()
    try:
        datetime.strptime(raw, "%d.%m.%Y")
    except ValueError:
        await message.answer("❌ Неверный формат даты. Пример: <code>26.08.2026</code>")
        return
    await state.update_data(date=raw)
    await state.set_state(AutoFSM.entering_slots)
    await message.answer(
        "6️⃣ <b>Расписание слотов</b>.\n"
        "Каждый слот — строка <code>ЧЧ:ММxN</code>, где N — сколько чеков в это время.\n"
        "Слоты по одному на строку, время должно идти на <b>увеличение</b>.\n\n"
        "Пример:\n"
        "<code>14:30x3\n15:30x2\n17:00x4\n19:30x1</code>",
        reply_markup=auto_back_kb(),
    )


# ── Слоты → пресет ────────────────────────────────────────────────────────────
@router.message(AutoFSM.entering_slots)
async def auto_slots_entered(message: Message, state: FSMContext):
    slots = _parse_slots(message.text or "")
    if not slots:
        await message.answer(
            "❌ Не удалось разобрать расписание.\n"
            "Каждая строка: <code>ЧЧ:ММxN</code>. Пример:\n"
            "<code>14:30x3\n15:30x2</code>"
        )
        return
    # Проверка возрастания времени
    for i in range(1, len(slots)):
        if slots[i]["minutes"] <= slots[i - 1]["minutes"]:
            await message.answer("❌ Время должно идти на увеличение (от меньшего к большему).")
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

    await message.answer(
        "✅ Пресет сохранён:\n\n" + _format_preset(preset),
        reply_markup=auto_run_kb(),
    )


# ── Запуск ────────────────────────────────────────────────────────────────────
@router.callback_query(F.data == "auto:run")
async def auto_run(call: CallbackQuery, state: FSMContext):
    user_id = call.from_user.id
    if not has_any_access(user_id):
        await call.answer("⛔ Доступ запрещён", show_alert=True)
        return
    preset = _load_preset(user_id)
    if not preset:
        await call.answer("Сначала настройте пресет", show_alert=True)
        return

    await call.message.edit_text("⏳ Генерирую чеки…")
    await call.answer()

    bot: Bot = call.bot
    n = sum(s["count"] for s in preset["slots"])
    await call.message.answer(f"🚀 Запущено: {n} чеков в {len(preset['slots'])} слотов.")

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
            caption = f"{time_str} — чек {i + 1}/{count} ({item_key})"
            media.append(
                InputMediaPhoto(
                    media=BufferedInputFile(png_bytes, filename="check.png"),
                    caption=caption if i == 0 else None,
                )
            )
        if media:
            try:
                await bot.send_media_group(call.message.chat.id, media=media)
            except TelegramBadRequest as e:
                log.error(f"auto_run send_media_group error: {e}")
        # Небольшая пауза между слотами, чтобы Telegram не считал спамом
        await asyncio.sleep(1.5)


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
    lines = [
        f"🌍 ГЕО: <b>{geo_label}</b>",
        f"📂 Линейка: <b>{p['line_key']}</b>",
        f"🎯 Типы: <code>{', '.join(p['items'])}</code>",
        f"💰 Суммы: <b>{p['sum_min']}–{p['sum_max']}</b>",
        f"📅 Дата: <b>{p['date']}</b>",
        "⏰ Слоты:",
    ]
    for s in p["slots"]:
        lines.append(f"   • <b>{s['time']}</b> × {s['count']}")
    return "\n".join(lines)


# ── Хранение пресетов (SQLite рядом с bot.db) ─────────────────────────────────
# Мы добавим таблицу automation_presets миграцией 027 в data/db.py,
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
    await call.message.edit_text(
        "🤖 <b>Автоматизация создания чеков</b>\n\nПресет удалён. Настройте новый.",
        reply_markup=auto_main_kb(has_preset=False),
    )
    await call.answer()


def clear_preset(user_id: int):
    _ensure_presets_table()
    with _PRESETS_LOCK:
        con = _presets_conn()
        con.execute("DELETE FROM automation_presets WHERE user_id = ?", (user_id,))
        con.commit()
        con.close()