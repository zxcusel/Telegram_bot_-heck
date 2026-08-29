"""
FSM-калькулятор часовых поясов.

Пользователь выбирает исходный пояс, вводит время (HH:MM),
затем выбирает целевой пояс — бот отвечает соответствующим временем.

DST учитывается автоматически через pytz.
"""
import re
from datetime import datetime
from aiogram import Router, F
from aiogram.enums import ParseMode
from aiogram.types import (
    Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton,
)
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
try:
    import pytz
except Exception:  # pragma: no cover
    pytz = None  # type: ignore

from utils.logger import log
from middlewares.role_check import has_any_access

router = Router()
PM = ParseMode.HTML
DIV = "━━━━━━━━━━━━━━━━━━━━"

# (callback_suffix, label, pytz_tz_or_none)
# Если pytz отсутствует или имя не найдено — fallback на фиксированные смещения.
_ZONES: list[tuple[str, str, str]] = [
    ("msk",  "🇷🇺 Москва",            "Europe/Moscow"),
    ("bol",  "🇧🇴 Боливия",           "America/La_Paz"),
    ("pry",  "🇵🇾 Парагвай",           "America/Asuncion"),
    ("uru",  "🇺🇾 Уругвай",            "America/Montevideo"),
    ("per",  "🇵🇪 Перу",               "America/Lima"),
    ("mrc",  "🇲🇦 Марокко",            "Africa/Casablanca"),
    ("utc",  "🌐 UTC",                 "UTC"),
    ("ny",   "🇺🇸 Нью-Йорк",           "America/New_York"),
    ("lon",  "🇬🇧 Лондон",             "Europe/London"),
    ("br",   "🇧🇷 Бразилия (СП)",      "America/Sao_Paulo"),
    ("arg",  "🇦🇷 Аргентина",          "America/Argentina/Buenos_Aires"),
    ("mex",  "🇲🇽 Мехико",             "America/Mexico_City"),
]

# Fallback-смещения (часы) для случая, если pytz недоступен.
_FALLBACK_OFFSET = {
    "Europe/Moscow": 3,
    "America/La_Paz": -4,
    "America/Asuncion": -3,  # может быть -4 зимой; pytz точнее
    "America/Montevideo": -3,
    "America/Lima": -5,
    "Africa/Casablanca": 1,
    "UTC": 0,
    "America/New_York": -5,  # EST; DST не учитываем без pytz
    "Europe/London": 0,
    "America/Sao_Paulo": -3,
    "America/Argentina/Buenos_Aires": -3,
    "America/Mexico_City": -6,
}


class TZFSM(StatesGroup):
    pick_source = State()
    pick_target = State()
    enter_time = State()


def _label_for(suffix: str) -> str:
    for s, label, _ in _ZONES:
        if s == suffix:
            return label
    return suffix


def _zone_for(suffix: str) -> tuple[str, str | None]:
    for s, label, name in _ZONES:
        if s == suffix:
            return label, name
    return suffix, None


def _zone_kb(prefix: str) -> InlineKeyboardMarkup:
    rows: list[list[InlineKeyboardButton]] = []
    row: list[InlineKeyboardButton] = []
    for s, label, _ in _ZONES:
        row.append(InlineKeyboardButton(text=label, callback_data=f"tz:{prefix}:{s}"))
        if len(row) == 2:
            rows.append(row)
            row = []
    if row:
        rows.append(row)
    rows.append([InlineKeyboardButton(text="❌ Отмена", callback_data="tz:cancel")])
    return InlineKeyboardMarkup(inline_keyboard=rows)


def _convert(src_name: str, dst_name: str, hh: int, mm: int):
    """Возвращает (datetime в dst, label смещения в src, label смещения в dst).
    Использует pytz если доступен, иначе fallback на фиксированные смещения.
    """
    if pytz is not None:
        try:
            src_tz = pytz.timezone(src_name)
            dst_tz = pytz.timezone(dst_name)
            naive = datetime(2000, 1, 1, hh, mm)
            # localize — для нейтральной даты DST не важен, но берём середину года,
            # чтобы часовой пояс вёл себя естественно.
            naive = datetime(2026, 6, 15, hh, mm)
            src_dt = src_tz.localize(naive)
            dst_dt = src_dt.astimezone(dst_tz)
            return dst_dt, src_dt.strftime("%z"), dst_dt.strftime("%z")
        except Exception as e:
            log.error(f"tz calc pytz error: {e}")

    # Fallback: без pytz — фиксированные смещения.
    s_off = _FALLBACK_OFFSET.get(src_name, 0)
    d_off = _FALLBACK_OFFSET.get(dst_name, 0)
    total = hh * 60 + mm + (d_off - s_off) * 60
    total %= 24 * 60
    if total < 0:
        total += 24 * 60
    return (
        datetime(2000, 1, 1, total // 60, total % 60),
        f"{'+' if s_off >= 0 else '-'}{abs(s_off):02d}:00",
        f"{'+' if d_off >= 0 else '-'}{abs(d_off):02d}:00",
    )


def _fmt_dt(dt) -> str:
    return dt.strftime("%H:%M")


@router.message(F.text == "🧮 Калькулятор времени")
@router.message(F.text.regexp(r"(?i)^(🧮|/calc|/tz|/time)\b"))
async def tz_start(message: Message, state: FSMContext):
    if not has_any_access(message.from_user.id):
        await message.answer("⛔ Доступ запрещён", parse_mode=PM)
        return
    await state.clear()
    await state.set_state(TZFSM.pick_source)
    await message.answer(
        f"🧮 <b>Калькулятор часовых поясов</b>\n{DIV}\n\n"
        f"Шаг <b>1 / 3</b> — выбери <b>исходный</b> часовой пояс:",
        reply_markup=_zone_kb("src"),
        parse_mode=PM,
    )


@router.callback_query(F.data.startswith("tz:src:"), TZFSM.pick_source)
async def tz_src_chosen(call: CallbackQuery, state: FSMContext):
    suffix = call.data.split(":")[-1]
    await state.update_data(src=suffix)
    await state.set_state(TZFSM.pick_target)
    await call.message.edit_text(
        f"🧮 <b>Калькулятор часовых поясов</b>\n{DIV}\n\n"
        f"Исходный пояс: <b>{_label_for(suffix)}</b>\n\n"
        f"Шаг <b>2 / 3</b> — выбери <b>целевой</b> часовой пояс:",
        reply_markup=_zone_kb("dst"),
        parse_mode=PM,
    )
    await call.answer()


@router.callback_query(F.data.startswith("tz:dst:"), TZFSM.pick_target)
async def tz_dst_chosen(call: CallbackQuery, state: FSMContext):
    suffix = call.data.split(":")[-1]
    await state.update_data(dst=suffix)
    await state.set_state(TZFSM.enter_time)
    src = (await state.get_data()).get("src", "?")
    await call.message.edit_text(
        f"🧮 <b>Калькулятор часовых поясов</b>\n{DIV}\n\n"
        f"Исходный пояс: <b>{_label_for(src)}</b>\n"
        f"Целевой пояс:  <b>{_label_for(suffix)}</b>\n\n"
        f"Шаг <b>3 / 3</b> — отправь время в формате <code>HH:MM</code>\n"
        f"Например: <code>14:30</code>",
        parse_mode=PM,
    )
    await call.answer()


_HHMM = re.compile(r"^\s*(\d{1,2}):(\d{2})\s*$")


@router.message(TZFSM.enter_time)
async def tz_time_entered(message: Message, state: FSMContext):
    raw = (message.text or "").strip()
    m = _HHMM.match(raw)
    if not m:
        await message.answer(
            f"❌ Неверный формат. Пришли время как <code>HH:MM</code>, например <code>14:30</code>.",
            parse_mode=PM,
        )
        return
    hh, mm = int(m.group(1)), int(m.group(2))
    if not (0 <= hh <= 23 and 0 <= mm <= 59):
        await message.answer(
            f"❌ Время вне диапазона. Часы 0–23, минуты 0–59.",
            parse_mode=PM,
        )
        return
    data = await state.get_data()
    src, dst = data.get("src"), data.get("dst")
    if not src or not dst:
        await state.clear()
        await message.answer(
            f"⚠️ Сессия сбросилась, начни заново: нажми <b>🧮 Калькулятор времени</b>.",
            parse_mode=PM,
        )
        return
    src_label, src_name = _zone_for(src)
    dst_label, dst_name = _zone_for(dst)
    if not src_name or not dst_name:
        await message.answer("❌ Не удалось определить один из поясов.", parse_mode=PM)
        await state.clear()
        return
    converted, src_off, dst_off = _convert(src_name, dst_name, hh, mm)
    await state.clear()
    await message.answer(
        f"🧮 <b>Результат</b>\n{DIV}\n"
        f"Исходно: <b>{hh:02d}:{mm:02d}</b>  <i>({src_label}, UTC{src_off})</i>\n"
        f"В поясе: <b>{_fmt_dt(converted)}</b>  <i>({dst_label}, UTC{dst_off})</i>",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🔁 Ещё раз", callback_data="tz:again")],
            [InlineKeyboardButton(text="❌ Закрыть", callback_data="tz:cancel")],
        ]),
        parse_mode=PM,
    )


@router.callback_query(F.data == "tz:again")
async def tz_again(call: CallbackQuery, state: FSMContext):
    await state.clear()
    await state.set_state(TZFSM.pick_source)
    await call.message.edit_text(
        f"🧮 <b>Калькулятор часовых поясов</b>\n{DIV}\n\n"
        f"Шаг <b>1 / 3</b> — выбери <b>исходный</b> часовой пояс:",
        reply_markup=_zone_kb("src"),
        parse_mode=PM,
    )
    await call.answer()


@router.callback_query(F.data == "tz:cancel")
async def tz_cancel(call: CallbackQuery, state: FSMContext):
    await state.clear()
    try:
        await call.message.edit_text("🧮 Калькулятор закрыт.", parse_mode=PM)
    except Exception:
        pass
    await call.answer()
