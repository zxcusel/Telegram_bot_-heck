"""Раздел «📖 Инструкция» — подробное описание функционала бота.

Структура:
  📖 Инструкция (главная)
     ├─ 🚀 Начать работу
     ├─ 🤖 Автоматизация (подробно)
     ├─ 🎨 Генерация чеков
     ├─ ⚙️ Настройки
     ├─ 🎫 Поддержка (тикеты)
     └─ 👨‍💼 Админ-панель (если админ)
"""
from aiogram import Router, F
from aiogram.enums import ParseMode
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.exceptions import TelegramBadRequest
from data.db import is_admin

router = Router()
PM = ParseMode.HTML
DIV = "━━━━━━━━━━━━━━━━━━━━"
BULLET = "▫️"


def _safe_edit(call: CallbackQuery, text: str, kb: InlineKeyboardMarkup):
    """Безопасный edit_text: если под сообщением есть медиа — отправляем новое."""
    try:
        return call.message.edit_text(text, reply_markup=kb, parse_mode=PM)
    except TelegramBadRequest:
        return call.message.answer(text, reply_markup=kb, parse_mode=PM)


# ── Клавиатуры ──────────────────────────────────────────────────────────────

def instruction_main_kb(is_adm: bool) -> InlineKeyboardMarkup:
    """Главное меню инструкции (доступно всем)."""
    rows = [
        [InlineKeyboardButton(text="🚀 Начать работу", callback_data="ins:start")],
        [InlineKeyboardButton(text="🤖 Автоматизация (как настроить)", callback_data="ins:auto")],
        [InlineKeyboardButton(text="🎨 Генерация чеков", callback_data="ins:render")],
        [InlineKeyboardButton(text="⚙️ Настройки", callback_data="ins:settings")],
        [InlineKeyboardButton(text="🎫 Поддержка (тикеты)", callback_data="ins:tickets")],
    ]
    if is_adm:
        rows.append([InlineKeyboardButton(text="👨‍💼 Админ-панель", callback_data="ins:admin")])
    rows.append([InlineKeyboardButton(text="🔙 В главное меню", callback_data="back:welcome")])
    return InlineKeyboardMarkup(inline_keyboard=rows)


def _back_to_instruction_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔙 Назад к инструкции", callback_data="ins:main")],
        [InlineKeyboardButton(text="🏠 В главное меню",     callback_data="back:welcome")],
    ])


# ── Главная инструкции ──────────────────────────────────────────────────────

INSTRUCTION_MAIN = (
    f"📖 <b>Инструкция к BCKPS F-BOT</b>\n"
    f"{DIV}\n"
    f"Короткое и понятное описание всех разделов бота.\n\n"
    f"{BULLET} <b>🚀 Начать работу</b> — что нажимать сразу после /start\n"
    f"{BULLET} <b>🤖 Автоматизация</b> — как запускать чеки по расписанию\n"
    f"{BULLET} <b>🎨 Генерация чеков</b> — как создавать одиночные чеки\n"
    f"{BULLET} <b>⚙️ Настройки</b> — что можно настроить под себя\n"
    f"{BULLET} <b>🎫 Поддержка</b> — как написать в поддержку и приложить файл\n"
    f"{BULLET} <b>👨‍💼 Админ-панель</b> — управление пользователями (админам)\n"
    f"{DIV}\n"
    f"<i>Выберите раздел ниже 👇</i>"
)


# ── Тексты разделов ──────────────────────────────────────────────────────────

TEXT_START = (
    f"🚀 <b>Начать работу</b>\n"
    f"{DIV}\n"
    f"1️⃣ <b>Регион (гео)</b> — в каждой стране свой набор шаблонов и "
    f"настроек. Нажмите <i>«▶️ Начать»</i> и выберите нужный регион.\n\n"
    f"2️⃣ <b>Линейка</b> — внутри региона есть линейки чеков "
    f"(FD / RD / CHECK / QR / и др.). Доступные линейки зависят от вашей "
    f"<b>роли</b> (выдаётся админом).\n\n"
    f"3️⃣ <b>Шаблон</b> — выбираете конкретный шаблон чека "
    f"(например: <i>«Visa Сбербанк»</i>, <i>«Mastercard Тинькофф»</i>).\n\n"
    f"4️⃣ <b>Заполнение</b> — бот попросит:\n"
    f"   • <b>Сумму</b> (число, в нужной валюте)\n"
    f"   • <b>Дату</b> на чеке (формат: <code>ДД.ММ.ГГГГ ЧЧ:ММ</code>)\n"
    f"   • Доп. поля (ФИО, последние 4 цифры и т.п.) — если шаблон требует.\n\n"
    f"5️⃣ <b>Готовый чек</b> — бот пришлёт PNG-картинку. Её можно сразу "
    f"открыть, скачать или переслать.\n\n"
    f"💡 <b>Совет:</b> все действия делаются <i>кнопками</i> — текст вводить "
    f"нужно только для значений (сумма, дата)."
)

TEXT_AUTO = (
    f"🤖 <b>Автоматизация — пошаговая настройка</b>\n"
    f"{DIV}\n"
    f"<b>Что это:</b> бот сам генерирует заданное количество чеков и "
    f"раскидывает их по времени в выбранном диапазоне.\n\n"
    f"<b>Когда полезно:</b> нужно много чеков за период, а не один прямо "
    f"сейчас — например, на день/неделю.\n\n"
    f"{DIV}\n"
    f"<b>Как настроить (5 шагов):</b>\n\n"
    f"1️⃣ <b>Регион</b> — выберите страну.\n\n"
    f"2️⃣ <b>Линейка</b> — какие чеки генерировать.\n\n"
    f"3️⃣ <b>Шаблоны</b> — отметьте галочками нужные (можно несколько). "
    f"Кнопка <i>«✅ Готово»</i> внизу.\n\n"
    f"4️⃣ <b>Сумма</b> — введите одно число, оно применится ко всем "
    f"чекам. Если нужны разные суммы — запустите несколько автоматизаций.\n\n"
    f"5️⃣ <b>Дата и таймлайн</b>:\n"
    f"   • <b>Дата отправки</b> — когда бот начнёт (по Москве).\n"
    f"   • <b>Таймлайн</b> — диапазон в часах, в течение которого раскидать "
    f"чеки (например <code>2</code> = в течение 2 часов от старта).\n\n"
    f"{DIV}\n"
    f"<b>Что сделает бот:</b>\n"
    f"{BULLET} Возьмёт ваши суммы и распределит <i>случайно</i> по таймлайну\n"
    f"{BULLET} Для каждого слота сгенерирует свой чек (с уникальной датой/временем)\n"
    f"{BULLET} Отправит вам все готовые PNG-картинки <i>одним пакетом</i>\n\n"
    f"<b>⚠️ Важно:</b>\n"
    f"{BULLET} Автоматизация одноразовая — она не повторяется сама.\n"
    f"{BULLET} Чтобы перенести дату старта — кнопка <i>«⏰ Изменить дату»</i>.\n"
    f"{BULLET} Чтобы отменить — <i>«🔄 Сбросить»</i> и начать заново."
)

TEXT_RENDER = (
    f"🎨 <b>Генерация чеков (разовые)</b>\n"
    f"{DIV}\n"
    f"<b>Что это:</b> создать <i>один</i> чек прямо сейчас, без расписания.\n\n"
    f"<b>Где найти:</b> <i>▶️ Начать</i> → регион → линейка → шаблон.\n\n"
    f"<b>Что умеет бот:</b>\n"
    f"{BULLET} Подставляет ваш текст в выбранный шаблон чека\n"
    f"{BULLET} Поддерживает разные валюты, логотипы банков, фоны\n"
    f"{BULLET} Возвращает готовую PNG-картинку с вашими данными\n\n"
    f"<b>После получения чека доступны кнопки:</b>\n"
    f"{BULLET} <i>🔄 Создать новый шаблон</i> — сгенерировать ещё, "
    f"с другими данными\n"
    f"{BULLET} <i>🏠 Главное меню</i> — назад\n\n"
    f"💡 <b>Если картинка не отправилась</i> — бот сообщит, сколько чеков "
    f"создано и сколько ошибок рендера (бывает при редких комбинациях)."
)

TEXT_SETTINGS = (
    f"⚙️ <b>Настройки</b>\n"
    f"{DIV}\n"
    f"<b>Где:</b> <i>⚙️ Настройки</i> в главном меню.\n\n"
    f"В этом разделе можно изменить <i>параметры по умолчанию</i> для "
    f"генерации — например, часовой пояс, формат даты, мелочи отображения.\n\n"
    f"Настройки <b>применяются только к вашему аккаунту</b> и не влияют на "
    f"других пользователей.\n\n"
    f"💡 <b>Подсказка:</b> если что-то в чеке выглядит «не так» — сначала "
    f"загляните в <i>Настройки</i>, возможно там переключается формат."
)

TEXT_TICKETS = (
    f"🎫 <b>Поддержка (тикеты)</b>\n"
    f"{DIV}\n"
    f"<b>Кому доступно:</b> только обычным пользователям. Админы управляют "
    f"тикетами из <i>Админ-панели</i>.\n\n"
    f"<b>Как создать тикет:</b>\n"
    f"1️⃣ <i>🎫 Поддержка</i> → <i>✏️ Новое обращение</i>\n"
    f"2️⃣ Введите <b>тему</b> одним сообщением\n"
    f"3️⃣ Опишите проблему <b>одним сообщением</b> и нажмите Enter\n\n"
    f"<b>Что можно прикрепить:</b>\n"
    f"{BULLET} 📷 фото\n"
    f"{BULLET} 🎬 видео\n"
    f"{BULLET} 🎞 GIF / анимацию\n"
    f"{BULLET} 🎙 голосовое сообщение\n"
    f"{BULLET} 📹 видеосообщение (кружок)\n"
    f"{BULLET} 📎 любой файл / документ\n"
    f"{BULLET} 😺 стикер\n\n"
    f"Просто <b>отправьте файл</b> как обычное сообщение — бот сам "
    f"перешлёт его админу вместе с подписью.\n\n"
    f"<b>Что умеет тикет:</b>\n"
    f"{BULLET} Переписка с админом прямо в боте\n"
    f"{BULLET} Можно дописывать сообщения сверху (кнопка <i>«✏️ Дописать»</i>)\n"
    f"{BULLET} Админ может закрыть тикет — после этого дописать нельзя\n"
    f"{BULLET} Все сообщения и файлы хранятся в истории тикета\n\n"
    f"<b>Уведомления:</b>\n"
    f"Админы получают сообщения о новых тикетах и ответах сразу. "
    f"Вы получите уведомление, как только админ ответит."
)

TEXT_ADMIN = (
    f"👨‍💼 <b>Админ-панель</b>\n"
    f"{DIV}\n"
    f"<b>Доступ:</b> только админам (определяется в таблице <code>admins</code>).\n\n"
    f"<b>Основные разделы:</b>\n\n"
    f"🎫 <b>Тикеты</b>\n"
    f"{BULLET} Список открытых / всех тикетов\n"
    f"{BULLET} Просмотр переписки\n"
    f"{BULLET} Ответ пользователю (с поддержкой медиа)\n"
    f"{BULLET} Закрытие / переоткрытие тикета\n\n"
    f"📊 <b>Рассылки</b>\n"
    f"{BULLET} Текстовая рассылка всем пользователям\n"
    f"{BULLET} Выборочная рассылка (по ролям / гео)\n"
    f"{BULLET} Есть защита от лимитов Telegram\n\n"
    f"👥 <b>Пользователи</b>\n"
    f"{BULLET} Список всех юзеров\n"
    f"{BULLET} Изменение роли, доступных регионов\n\n"
    f"⚙️ <b>Прочее</b>\n"
    f"{BULLET} Управление админами\n"
    f"{BULLET} Глобальные настройки\n\n"
    f"💡 <b>Совет:</b> если раздел недоступен — значит, ваш id не добавлен "
    f"в таблицу <code>admins</code>. Обратитесь к старшему админу."
)


# ── Хендлеры ────────────────────────────────────────────────────────────────

@router.callback_query(F.data == "ins:main")
async def cb_ins_main(call: CallbackQuery, state):
    """Главная инструкции (на случай повторного захода)."""
    try: await call.answer()
    except Exception: pass
    await _safe_edit(call, INSTRUCTION_MAIN, instruction_main_kb(is_admin(call.from_user.id)))


@router.callback_query(F.data == "ins:start")
async def cb_ins_start(call: CallbackQuery):
    try: await call.answer()
    except Exception: pass
    await _safe_edit(call, TEXT_START, _back_to_instruction_kb())


@router.callback_query(F.data == "ins:auto")
async def cb_ins_auto(call: CallbackQuery):
    try: await call.answer()
    except Exception: pass
    await _safe_edit(call, TEXT_AUTO, _back_to_instruction_kb())


@router.callback_query(F.data == "ins:render")
async def cb_ins_render(call: CallbackQuery):
    try: await call.answer()
    except Exception: pass
    await _safe_edit(call, TEXT_RENDER, _back_to_instruction_kb())


@router.callback_query(F.data == "ins:settings")
async def cb_ins_settings(call: CallbackQuery):
    try: await call.answer()
    except Exception: pass
    await _safe_edit(call, TEXT_SETTINGS, _back_to_instruction_kb())


@router.callback_query(F.data == "ins:tickets")
async def cb_ins_tickets(call: CallbackQuery):
    try: await call.answer()
    except Exception: pass
    await _safe_edit(call, TEXT_TICKETS, _back_to_instruction_kb())


@router.callback_query(F.data == "ins:admin")
async def cb_ins_admin(call: CallbackQuery):
    try: await call.answer()
    except Exception: pass
    if not is_admin(call.from_user.id):
        await call.answer("Раздел только для админов", show_alert=True)
        return
    await _safe_edit(call, TEXT_ADMIN, _back_to_instruction_kb())