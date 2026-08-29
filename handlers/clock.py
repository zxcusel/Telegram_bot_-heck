"""Закреплённое сообщение с часами по Москве / Боливии / Парагваю
и кнопкой-калькулятором времени."""
from aiogram import Router, F, Bot
from aiogram.enums import ParseMode
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from datetime import datetime
import asyncio
import sqlite3
import pytz

from data.db import _conn  # type: ignore  # используем общий коннектор

router = Router()
PM = ParseMode.HTML
DIV = "━━━━━━━━━━━━━━━━━━━━"

# Пояса
TZ_MSK = pytz.timezone("Europe/Moscow")
TZ_BOL = pytz.timezone("America/La_Paz")        # UTC-4 (без перехода на летнее)
TZ_PRY = pytz.timezone("America/Asuncion")      # UTC-4 (зима) / UTC-3 (лето) — pytz сам учитывает


def _now_in(tz) -> datetime:
    return datetime.now(tz)


def _fmt(dt: datetime) -> str:
    return dt.strftime("%H:%M:%S")


def _clock_text() -> str:
    m = _fmt(_now_in(TZ_MSK))
    b = _fmt(_now_in(TZ_BOL))
    p = _fmt(_now_in(TZ_PRY))
    d_m = _now_in(TZ_MSK).strftime("%d.%m.%Y")
    d_b = _now_in(TZ_BOL).strftime("%d.%m.%Y")
    d_p = _now_in(TZ_PRY).strftime("%d.%m.%Y")
    return (
        f"🕒 <b>Часы по регионам</b>\n"
        f"{DIV}\n"
        f"🇷🇺 Москва: <b>{m}</b>  <i>({d_m})</i>\n"
        f"🇧🇴 Боливия: <b>{b}</b>  <i>({d_b})</i>\n"
        f"🇵🇾 Парагвай: <b>{p}</b>  <i>({d_p})</i>\n"
        f"{DIV}\n"
        f"⏱ Время обновляется автоматически"
    )


def _clock_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🧮", callback_data="clock:calc")],
    ])


# ── миграция и хранение ID закреплённого сообщения ─────────────────────────────

_INIT_DONE = False

def _ensure_table() -> None:
    """Ленивая миграция: создаём таблицу pinned_clock при первом обращении.
    Не падаем, если data.db недоступен — тогда просто пропускаем pin."""
    try:
        with _conn() as c:
            c.execute(
                "CREATE TABLE IF NOT EXISTS pinned_clock ("
                " chat_id INTEGER PRIMARY KEY,"
                " message_id INTEGER NOT NULL"
                ")"
            )
            c.commit()
    except Exception as e:
        # Не критично — функционал не заблокирует, просто без закрепа
        print(f"clock: pinned_clock table init failed: {e}")


def _get_pinned(chat_id: int) -> int | None:
    try:
        with _conn() as c:
            row = c.execute(
                "SELECT message_id FROM pinned_clock WHERE chat_id=?",
                (chat_id,),
            ).fetchone()
            return int(row[0]) if row else None
    except Exception:
        return None


def _set_pinned(chat_id: int, message_id: int) -> None:
    try:
        with _conn() as c:
            c.execute(
                "INSERT INTO pinned_clock(chat_id, message_id) VALUES(?, ?)"
                " ON CONFLICT(chat_id) DO UPDATE SET message_id=excluded.message_id",
                (chat_id, message_id),
            )
            c.commit()
    except Exception as e:
        print(f"clock: _set_pinned failed: {e}")


def _clear_pinned(chat_id: int) -> None:
    try:
        with _conn() as c:
            c.execute("DELETE FROM pinned_clock WHERE chat_id=?", (chat_id,))
            c.commit()
    except Exception:
        pass


# ── основной хелпер ────────────────────────────────────────────────────────────

async def ensure_pinned(bot: Bot, chat_id: int) -> None:
    """Гарантирует наличие закреплённого сообщения с часами в чате.
    - Если для chat_id уже есть message_id — пробуем edit (без unpin, чтобы
      закреп сохранялся при обновлении текста).
    - Если нет — отправляем и pin'им.
    - Любые ошибки глохнут — функция best-effort, не должна ломать /start.
    """
    _ensure_table()
    text = _clock_text()
    kb = _clock_kb()
    pinned_mid = _get_pinned(chat_id)
    print(f"[clock] ensure_pinned chat={chat_id} pinned_mid={pinned_mid}")

    # Если уже есть закреп — пробуем обновить содержимое.
    if pinned_mid:
        try:
            await bot.edit_message_text(
                chat_id=chat_id,
                message_id=pinned_mid,
                text=text,
                reply_markup=kb,
                parse_mode=PM,
            )
            print(f"[clock] ensure_pinned edit OK mid={pinned_mid}")
            return
        except Exception as e:
            # Сообщение было удалено / недоступно — снимаем запись и
            # отправим заново ниже.
            print(f"[clock] ensure_pinned edit FAIL mid={pinned_mid}: {e!r}")
            _clear_pinned(chat_id)

    # Отправляем и пиним.
    try:
        msg = await bot.send_message(
            chat_id=chat_id,
            text=text,
            reply_markup=kb,
            parse_mode=PM,
        )
        print(f"[clock] ensure_pinned sent mid={msg.message_id}")
        _set_pinned(chat_id, msg.message_id)
        # Небольшая задержка, чтобы _bg_wipe в catalog.py не конкурировал
        # с этим сообщением (wipe удаляет диапазон до cmd_mid-1, и если
        # бот успеет — может попытаться удалить наш только что отправленный
        # clock; на практике clock всегда > cmd_mid, но защитимся явно).
        import asyncio as _aio
        await _aio.sleep(0.2)
        print(f"[clock] ensure_pinned pinning mid={msg.message_id}")
        # Бот должен иметь право pin в личке — обычно есть в личке с ботом,
        # в группе нужно явно назначить админом с правом pin.
        try:
            await bot.pin_chat_message(
                chat_id=chat_id,
                message_id=msg.message_id,
                disable_notification=True,
            )
            print(f"[clock] ensure_pinned pin OK mid={msg.message_id}")
        except Exception:
            # Если бот не может pin — ничего, сообщение просто висит сверху.
            pass
    except Exception as e:
        print(f"clock: ensure_pinned send failed for {chat_id}: {e}")


# ── callback: калькулятор времени ──────────────────────────────────────────────

@router.callback_query(F.data == "clock:calc")
async def cb_calc_time(call: CallbackQuery, state: FSMContext):
    """Показывает разницу между поясами в часах и текущее время по каждому."""
    try:
        await call.answer()
    except Exception:
        pass

    m_now = _now_in(TZ_MSK)
    b_now = m_now.astimezone(TZ_BOL)
    p_now = m_now.astimezone(TZ_PRY)

    # Разница Москва ↔ Боливия / Парагвай
    msk_off = m_now.utcoffset().total_seconds() / 3600
    bol_off = b_now.utcoffset().total_seconds() / 3600
    pry_off = p_now.utcoffset().total_seconds() / 3600

    diff_bol = msk_off - bol_off
    diff_pry = msk_off - pry_off

    sign_bol = "+" if diff_bol >= 0 else ""
    sign_pry = "+" if diff_pry >= 0 else ""

    body = (
        f"🧮 <b>Калькулятор времени</b>\n"
        f"{DIV}\n"
        f"🇷🇺 Москва (UTC{msk_off:+.0f}): <b>{_fmt(m_now)}</b>\n"
        f"🇧🇴 Боливия (UTC{bol_off:+.0f}): <b>{_fmt(b_now)}</b>\n"
        f"🇵🇾 Парагвай (UTC{pry_off:+.0f}): <b>{_fmt(p_now)}</b>\n"
        f"{DIV}\n"
        f"📐 Москва опережает Боливию на <b>{sign_bol}{diff_bol:g}h</b>\n"
        f"📐 Москва опережает Парагвай на <b>{sign_pry}{diff_pry:g}h</b>\n"
        f"{DIV}\n"
        f"🕓 Обновлено: <i>{_fmt(m_now)} МСК</i>"
    )

    # Пытаемся отредактировать само закреплённое сообщение, чтобы
    # кнопка осталась в нём же; если не вышло — отвечаем alert'ом.
    try:
        await call.message.edit_text(body, reply_markup=_clock_kb(), parse_mode=PM)
    except Exception:
        try:
            await call.answer(body, show_alert=True)
        except Exception:
            pass


# ── авто-миграция при импорте модуля ─────────────────────────────────────────
_ensure_table()


# ── фоновый авто-refresh закреплённого сообщения ────────────────────────────────

async def clock_updater(bot: Bot, period_sec: int = 60) -> None:
    """Каждые period_sec секунд обновляет все известные закреплённые
    сообщения. Никогда не падает."""
    while True:
        try:
            try:
                _ensure_table()
            except Exception:
                pass
            with _conn() as c:
                rows = c.execute("SELECT chat_id, message_id FROM pinned_clock").fetchall()
            for chat_id, mid in rows:
                try:
                    await bot.edit_message_text(
                        chat_id=chat_id,
                        message_id=int(mid),
                        text=_clock_text(),
                        reply_markup=_clock_kb(),
                        parse_mode=PM,
                    )
                except Exception:
                    # Если сообщение пропало — почистим запись
                    _clear_pinned(int(chat_id))
                # Чтобы не словить flood — короткая пауза между чатами
                await asyncio.sleep(0.2)
        except Exception as e:
            print(f"clock_updater loop error: {e}")
        await asyncio.sleep(period_sec)
