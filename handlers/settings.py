"""
Управление настройками пользователя: рандомайзер, закрепление даты, AM/PM.
"""
from aiogram import Router, F
from aiogram.types import CallbackQuery, Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from data.db import get_settings, update_setting
from keyboards.inline import cancel_kb
from utils.logger import log

router = Router()

class SettingStates(StatesGroup):
    wait_min = State()
    wait_max = State()
    wait_percent_min = State()
    wait_percent_max = State()
    wait_pinned_date = State()
    wait_pinned_name = State()
    wait_pinned_bank = State()

def settings_kb(user_id: int) -> InlineKeyboardMarkup:
    s = get_settings(user_id)
    
    # Текст для кнопок в зависимости от состояния
    rand_text = "✅ Рандомайзер сумм: ВКЛ" if s["rand_enabled"] else "❌ Рандомайзер сумм: ВЫКЛ"
    rand_percent_text = "✅ Рандомайзер процентов: ВКЛ" if s.get("rand_percent_enabled") else "❌ Рандомайзер процентов: ВЫКЛ"
    
    # AM/PM
    suffix = s["time_suffix"] or "Нет"
    suffix_text = f"🕒 Суффикс: {suffix}"
    
    # Дата
    p_date = s["pinned_date"] or "Не задана"
    date_text = f"📅 Закреп даты: {p_date}"
    
    # ФИО
    p_name = s["pinned_name"] or "Не задано"
    name_text = f"👤 ФИО: {p_name}"
    
    # Банк
    p_bank = s["pinned_bank"] or "Не задан"
    bank_text = f"🏦 Банк: {p_bank}"

    buttons = [
        [InlineKeyboardButton(text=rand_text, callback_data="set:toggle_rand")],
        [
            InlineKeyboardButton(text=f"Min: {s['rand_min']}", callback_data="set:min"),
            InlineKeyboardButton(text=f"Max: {s['rand_max']}", callback_data="set:max")
        ],
        [InlineKeyboardButton(text=rand_percent_text, callback_data="set:toggle_rand_percent")],
        [
            InlineKeyboardButton(text=f"Min: {s.get('rand_percent_min', 1.0)}", callback_data="set:percent_min"),
            InlineKeyboardButton(text=f"Max: {s.get('rand_percent_max', 100.0)}", callback_data="set:percent_max")
        ],
        [InlineKeyboardButton(text=suffix_text, callback_data="set:toggle_suffix")],
        [InlineKeyboardButton(text=date_text, callback_data="set:pinned_date")],
        [InlineKeyboardButton(text=name_text, callback_data="set:pinned_name")],
        [InlineKeyboardButton(text=bank_text, callback_data="set:pinned_bank")],
        [InlineKeyboardButton(text="🏠 Главное меню", callback_data="back:welcome")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


@router.callback_query(F.data == "start:settings")
async def cb_settings_main(call: CallbackQuery, state: FSMContext):
    await state.clear()
    log.open_settings(call.from_user.id, call.from_user.username)
    await call.message.edit_text("⚙️ <b>Настройки пользователя</b>\n\nЗдесь вы можете настроить автоматизацию для ускорения работы.", 
                                 reply_markup=settings_kb(call.from_user.id), parse_mode="HTML")
    await call.answer()


@router.callback_query(F.data == "set:toggle_rand")
async def cb_toggle_rand(call: CallbackQuery):
    s = get_settings(call.from_user.id)
    new_val = 0 if s["rand_enabled"] else 1
    update_setting(call.from_user.id, "rand_enabled", new_val)
    log.setting_changed(call.from_user.id, "rand_enabled", new_val, call.from_user.username)
    await call.message.edit_reply_markup(reply_markup=settings_kb(call.from_user.id))
    await call.answer("Рандомайзер сумм изменен")


@router.callback_query(F.data == "set:toggle_rand_percent")
async def cb_toggle_rand_percent(call: CallbackQuery):
    s = get_settings(call.from_user.id)
    new_val = 0 if s.get("rand_percent_enabled") else 1
    update_setting(call.from_user.id, "rand_percent_enabled", new_val)
    log.setting_changed(call.from_user.id, "rand_percent_enabled", new_val, call.from_user.username)
    await call.message.edit_reply_markup(reply_markup=settings_kb(call.from_user.id))
    await call.answer("Рандомайзер процентов изменен")


@router.callback_query(F.data == "set:toggle_suffix")
async def cb_toggle_suffix(call: CallbackQuery):
    s = get_settings(call.from_user.id)
    options = [None, "A.M.", "P.M."]
    try:
        idx = options.index(s["time_suffix"])
    except ValueError:
        idx = 0
    new_suffix = options[(idx + 1) % len(options)]
    update_setting(call.from_user.id, "time_suffix", new_suffix)
    log.setting_changed(call.from_user.id, "time_suffix", new_suffix, call.from_user.username)
    await call.message.edit_reply_markup(reply_markup=settings_kb(call.from_user.id))
    await call.answer(f"Суффикс: {new_suffix or 'Отключен'}")


@router.callback_query(F.data == "set:min")
async def cb_set_min(call: CallbackQuery, state: FSMContext):
    await state.set_state(SettingStates.wait_min)
    await state.update_data(settings_msg_id=call.message.message_id)
    await call.message.edit_text("⌨️ Введите минимальную сумму для рандомайзера:", reply_markup=cancel_kb("set:cancel"))
    await call.answer()

@router.callback_query(F.data == "set:max")
async def cb_set_max(call: CallbackQuery, state: FSMContext):
    await state.set_state(SettingStates.wait_max)
    await state.update_data(settings_msg_id=call.message.message_id)
    await call.message.edit_text("⌨️ Введите максимальную сумму для рандомайзера:", reply_markup=cancel_kb("set:cancel"))
    await call.answer()

@router.callback_query(F.data == "set:percent_min")
async def cb_set_percent_min(call: CallbackQuery, state: FSMContext):
    await state.set_state(SettingStates.wait_percent_min)
    await state.update_data(settings_msg_id=call.message.message_id)
    await call.message.edit_text("⌨️ Введите минимальный процент для рандомайзера (например, 1.0):", reply_markup=cancel_kb("set:cancel"))
    await call.answer()

@router.callback_query(F.data == "set:percent_max")
async def cb_set_percent_max(call: CallbackQuery, state: FSMContext):
    await state.set_state(SettingStates.wait_percent_max)
    await state.update_data(settings_msg_id=call.message.message_id)
    await call.message.edit_text("⌨️ Введите максимальный процент для рандомайзера (например, 100.0):", reply_markup=cancel_kb("set:cancel"))
    await call.answer()

@router.callback_query(F.data == "set:pinned_date")
async def cb_set_pinned(call: CallbackQuery, state: FSMContext):
    await state.set_state(SettingStates.wait_pinned_date)
    await state.update_data(settings_msg_id=call.message.message_id)
    
    # Добавляем кнопку сброса
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🗑️ Сбросить дату", callback_data="set:clear_date")],
        [InlineKeyboardButton(text="❌ Отмена",        callback_data="set:cancel")]
    ])
    
    await call.message.edit_text("⌨️ Введите дату, которую нужно закрепить (например, 12.04.2026):", reply_markup=kb)
    await call.answer()


@router.callback_query(F.data == "set:pinned_name")
async def cb_set_name(call: CallbackQuery, state: FSMContext):
    await state.set_state(SettingStates.wait_pinned_name)
    await state.update_data(settings_msg_id=call.message.message_id)
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🗑️ Сбросить ФИО", callback_data="set:clear_name")],
        [InlineKeyboardButton(text="❌ Отмена",         callback_data="set:cancel")]
    ])
    await call.message.edit_text("⌨️ Введите ФИО (например, Ivanov Ivan):", reply_markup=kb)
    await call.answer()


@router.callback_query(F.data == "set:pinned_bank")
async def cb_set_bank(call: CallbackQuery, state: FSMContext):
    await state.set_state(SettingStates.wait_pinned_bank)
    await state.update_data(settings_msg_id=call.message.message_id)
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🗑️ Сбросить банк", callback_data="set:clear_bank")],
        [InlineKeyboardButton(text="❌ Отмена",         callback_data="set:cancel")]
    ])
    await call.message.edit_text("⌨️ Введите название банка (например, YAPE):", reply_markup=kb)
    await call.answer()


@router.callback_query(F.data == "set:cancel")
async def cb_settings_cancel(call: CallbackQuery, state: FSMContext):
    await state.clear()
    # Просто редактируем это же сообщение обратно в меню настроек
    await call.message.edit_text("⚙️ <b>Настройки пользователя</b>\n\nЗдесь вы можете настроить автоматизацию для ускорения работы.", 
                                 reply_markup=settings_kb(call.from_user.id), parse_mode="HTML")
    await call.answer()


@router.callback_query(F.data == "set:clear_date")
async def cb_clear_date(call: CallbackQuery, state: FSMContext):
    await state.clear()
    update_setting(call.from_user.id, "pinned_date", None)
    log.setting_changed(call.from_user.id, "pinned_date", None, call.from_user.username)
    await call.message.edit_text("✅ Закрепленная дата удалена.\n\n⚙️ <b>Настройки пользователя</b>", 
                                 reply_markup=settings_kb(call.from_user.id), parse_mode="HTML")
    await call.answer()


@router.callback_query(F.data == "set:clear_name")
async def cb_clear_name(call: CallbackQuery, state: FSMContext):
    await state.clear()
    update_setting(call.from_user.id, "pinned_name", None)
    log.setting_changed(call.from_user.id, "pinned_name", None, call.from_user.username)
    await call.message.edit_text("✅ Закрепленное ФИО удалено.\n\n⚙️ <b>Настройки пользователя</b>", 
                                 reply_markup=settings_kb(call.from_user.id), parse_mode="HTML")
    await call.answer()


@router.callback_query(F.data == "set:clear_bank")
async def cb_clear_bank(call: CallbackQuery, state: FSMContext):
    await state.clear()
    update_setting(call.from_user.id, "pinned_bank", None)
    log.setting_changed(call.from_user.id, "pinned_bank", None, call.from_user.username)
    await call.message.edit_text("✅ Закрепленный банк удален.\n\n⚙️ <b>Настройки пользователя</b>", 
                                 reply_markup=settings_kb(call.from_user.id), parse_mode="HTML")
    await call.answer()


@router.message(SettingStates.wait_min, F.text)
async def process_min(message: Message, state: FSMContext):
    data = await state.get_data()
    msg_id = data.get("settings_msg_id")
    try:
        val = int(message.text.strip().replace(" ", ""))
        update_setting(message.from_user.id, "rand_min", val)
        log.setting_changed(message.from_user.id, "rand_min", val, message.from_user.username)
        await message.delete()
        if msg_id:
            await message.bot.edit_message_text(
                chat_id=message.chat.id, message_id=msg_id,
                text=f"✅ Минимум установлен: {val}\n\n⚙️ <b>Настройки пользователя</b>",
                reply_markup=settings_kb(message.from_user.id), parse_mode="HTML"
            )
        await state.clear()
    except Exception:
        await message.answer("❌ Введите целое число.")

@router.message(SettingStates.wait_max, F.text)
async def process_max(message: Message, state: FSMContext):
    data = await state.get_data()
    msg_id = data.get("settings_msg_id")
    try:
        val = int(message.text.strip().replace(" ", ""))
        update_setting(message.from_user.id, "rand_max", val)
        log.setting_changed(message.from_user.id, "rand_max", val, message.from_user.username)
        await message.delete()
        if msg_id:
            await message.bot.edit_message_text(
                chat_id=message.chat.id, message_id=msg_id,
                text=f"✅ Максимум установлен: {val}\n\n⚙️ <b>Настройки пользователя</b>",
                reply_markup=settings_kb(message.from_user.id), parse_mode="HTML"
            )
        await state.clear()
    except Exception:
        await message.answer("❌ Введите целое число.")

@router.message(SettingStates.wait_percent_min, F.text)
async def process_percent_min(message: Message, state: FSMContext):
    data = await state.get_data()
    msg_id = data.get("settings_msg_id")
    try:
        val = float(message.text.strip().replace(" ", "").replace(",", "."))
        update_setting(message.from_user.id, "rand_percent_min", val)
        log.setting_changed(message.from_user.id, "rand_percent_min", val, message.from_user.username)
        await message.delete()
        if msg_id:
            await message.bot.edit_message_text(
                chat_id=message.chat.id, message_id=msg_id,
                text=f"✅ Минимальный процент установлен: {val}\n\n⚙️ <b>Настройки пользователя</b>",
                reply_markup=settings_kb(message.from_user.id), parse_mode="HTML"
            )
        await state.clear()
    except Exception:
        await message.answer("❌ Введите число (например, 1.5).")

@router.message(SettingStates.wait_percent_max, F.text)
async def process_percent_max(message: Message, state: FSMContext):
    data = await state.get_data()
    msg_id = data.get("settings_msg_id")
    try:
        val = float(message.text.strip().replace(" ", "").replace(",", "."))
        update_setting(message.from_user.id, "rand_percent_max", val)
        log.setting_changed(message.from_user.id, "rand_percent_max", val, message.from_user.username)
        await message.delete()
        if msg_id:
            await message.bot.edit_message_text(
                chat_id=message.chat.id, message_id=msg_id,
                text=f"✅ Максимальный процент установлен: {val}\n\n⚙️ <b>Настройки пользователя</b>",
                reply_markup=settings_kb(message.from_user.id), parse_mode="HTML"
            )
        await state.clear()
    except Exception:
        await message.answer("❌ Введите число (например, 100.0).")

@router.message(SettingStates.wait_pinned_date, F.text)
async def process_pinned_date(message: Message, state: FSMContext):
    data = await state.get_data()
    msg_id = data.get("settings_msg_id")
    val = message.text.strip()
    update_setting(message.from_user.id, "pinned_date", val)
    log.setting_changed(message.from_user.id, "pinned_date", val, message.from_user.username)
    await message.delete()
    if msg_id:
        await message.bot.edit_message_text(
            chat_id=message.chat.id, message_id=msg_id,
            text=f"✅ Дата закреплена: {val}\n\n⚙️ <b>Настройки пользователя</b>",
            reply_markup=settings_kb(message.from_user.id), parse_mode="HTML"
        )
    await state.clear()

@router.message(SettingStates.wait_pinned_name, F.text)
async def process_pinned_name(message: Message, state: FSMContext):
    data = await state.get_data()
    msg_id = data.get("settings_msg_id")
    val = message.text.strip()
    update_setting(message.from_user.id, "pinned_name", val)
    log.setting_changed(message.from_user.id, "pinned_name", val, message.from_user.username)
    await message.delete()
    if msg_id:
        await message.bot.edit_message_text(
            chat_id=message.chat.id, message_id=msg_id,
            text=f"✅ ФИО закреплено: {val}\n\n⚙️ <b>Настройки пользователя</b>",
            reply_markup=settings_kb(message.from_user.id), parse_mode="HTML"
        )
    await state.clear()

@router.message(SettingStates.wait_pinned_bank, F.text)
async def process_pinned_bank(message: Message, state: FSMContext):
    data = await state.get_data()
    msg_id = data.get("settings_msg_id")
    val = message.text.strip()
    update_setting(message.from_user.id, "pinned_bank", val)
    log.setting_changed(message.from_user.id, "pinned_bank", val, message.from_user.username)
    await message.delete()
    if msg_id:
        await message.bot.edit_message_text(
            chat_id=message.chat.id, message_id=msg_id,
            text=f"✅ Банк закреплен: {val}\n\n⚙️ <b>Настройки пользователя</b>",
            reply_markup=settings_kb(message.from_user.id), parse_mode="HTML"
        )
    await state.clear()
