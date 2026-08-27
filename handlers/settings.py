"""
Управление настройками пользователя: рандомайзер, закрепление даты, AM/PM.
"""
from aiogram import Router
from aiogram import F
from aiogram.enums import ParseMode
from aiogram.types import CallbackQuery, Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from data.db import get_settings, update_setting, get_available_names, clear_name_blacklist
from keyboards.inline import cancel_kb
from utils.logger import log

router = Router()

# ── Дизайн-токены ──────────────────────────────────────────────────────────────
PM = ParseMode.HTML
DIV = "━━━━━━━━━━━━━━━━━━━━"
BULLET = "▫️"

class SettingStates(StatesGroup):
    wait_min = State()
    wait_max = State()
    wait_percent_min = State()
    wait_percent_max = State()
    wait_pinned_date = State()
    wait_pinned_name = State()
    wait_pinned_bank = State()
    wait_rocket_min = State()
    wait_rocket_max = State()
    wait_custom_name_val = State()

def settings_kb(user_id: int, confirm_clear: bool = False) -> InlineKeyboardMarkup:
    s = get_settings(user_id)
    
    rand_text = "✅ Рандомайзер сумм: ВКЛ" if s["rand_enabled"] else "❌ Рандомайзер сумм: ВЫКЛ"
    rand_percent_text = "✅ Рандомайзер процентов: ВКЛ" if s.get("rand_percent_enabled") else "❌ Рандомайзер процентов: ВЫКЛ"
    rand_bank_text = "✅ Рандомайзер банков: ВКЛ" if s.get("rand_bank_enabled") else "❌ Рандомайзер банков: ВЫКЛ"
    rand_acc_text = "✅ Рандомайзер счетов: ВКЛ" if s.get("rand_acc_enabled") else "❌ Рандомайзер счетов: ВЫКЛ"
    rand_name_text = f"✅ Рандом имен: ВКЛ (осталось {len(get_available_names())})" if s.get("rand_name_enabled") else f"❌ Рандом имен: ВЫКЛ (осталось {len(get_available_names())})"
    blur_checks_text = "🌫 Блюр чеков: ВКЛ" if s.get("blur_enabled", 1) else "👁 Блюр чеков: ВЫКЛ"
    blur_qr_text = "🌫 Блюр КР / счета: ВКЛ" if s.get("blur_qr_enabled", 1) else "👁 Блюр КР / счета: ВЫКЛ"
    jose_sender_text = "👤 Отправитель JOSE: ВКЛ" if s.get("jose_sender_enabled") else "👤 Отправитель JOSE: ВЫКЛ"
    jose_recipient_text = "👤 Получатель JOSE: ВКЛ" if s.get("jose_recipient_enabled") else "👤 Получатель JOSE: ВЫКЛ"
    
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

    custom_name_enabled_text = "✅ Авто-ФИО: ВКЛ" if s.get("custom_name_enabled") else "❌ Авто-ФИО: ВЫКЛ"
    custom_name_target_text = "➡️ Направление: Отправитель" if s.get("custom_name_target") == "sender" else "➡️ Направление: Получатель"
    custom_name_val_text = f"👤 Авто-ФИО: {s.get('custom_name_val') or 'Не задано'}"

    if confirm_clear:
        blacklist_btn = [
            InlineKeyboardButton(text="⚠️ Подтвердить сброс?", callback_data="set:confirm_clear_name_blacklist"),
            InlineKeyboardButton(text="❌ Отмена", callback_data="set:cancel_clear_name_blacklist")
        ]
    else:
        blacklist_btn = [InlineKeyboardButton(text="🔄 Сбросить блэклист имен", callback_data="set:clear_name_blacklist")]

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
        [InlineKeyboardButton(text="🚀 Ракетки: диапазон X", callback_data="set:noop")],
        [
            InlineKeyboardButton(text=f"Min X: {s.get('rand_rocket_min', 10)}", callback_data="set:rocket_min"),
            InlineKeyboardButton(text=f"Max X: {s.get('rand_rocket_max', 1000)}", callback_data="set:rocket_max")
        ],
        [InlineKeyboardButton(text=rand_bank_text, callback_data="set:toggle_rand_bank")],
        [InlineKeyboardButton(text=rand_acc_text, callback_data="set:toggle_rand_acc")],
        [InlineKeyboardButton(text=rand_name_text, callback_data="set:toggle_rand_name")],
        [InlineKeyboardButton(text=blur_checks_text, callback_data="set:toggle_blur_checks")],
        [InlineKeyboardButton(text=blur_qr_text, callback_data="set:toggle_blur_qr")],
        [InlineKeyboardButton(text=jose_sender_text, callback_data="set:toggle_jose_sender")],
        [InlineKeyboardButton(text=jose_recipient_text, callback_data="set:toggle_jose_recipient")],
        [InlineKeyboardButton(text=custom_name_enabled_text, callback_data="set:toggle_custom_name")],
        [InlineKeyboardButton(text=custom_name_target_text, callback_data="set:toggle_custom_target")],
        [InlineKeyboardButton(text=custom_name_val_text, callback_data="set:custom_name_val")],
        blacklist_btn,
        [InlineKeyboardButton(text=suffix_text, callback_data="set:toggle_suffix")],
        [InlineKeyboardButton(text=date_text, callback_data="set:pinned_date")],
        [InlineKeyboardButton(text=name_text, callback_data="set:pinned_name")],
        [InlineKeyboardButton(text=bank_text, callback_data="set:pinned_bank")],
        [InlineKeyboardButton(text="🏠 Главное меню", callback_data="back:welcome")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


@router.callback_query(F.data == "start:settings")
async def cb_settings_main(call: CallbackQuery, state: FSMContext):
    try: await call.answer()
    except Exception: pass
    await state.clear()
    log.open_settings(call.from_user.id, call.from_user.username)
    await call.message.edit_text("⚙️ <b>Настройки пользователя</b>\n\nЗдесь вы можете настроить автоматизацию для ускорения работы.", 
                                 reply_markup=settings_kb(call.from_user.id), parse_mode="HTML")


@router.callback_query(F.data == "set:toggle_rand")
async def cb_toggle_rand(call: CallbackQuery):
    try: await call.answer("Рандомайзер сумм изменен", parse_mode=PM)
    except Exception: pass
    s = get_settings(call.from_user.id)
    new_val = 0 if s["rand_enabled"] else 1
    update_setting(call.from_user.id, "rand_enabled", new_val)
    log.setting_changed(call.from_user.id, "rand_enabled", new_val, call.from_user.username)
    await call.message.edit_reply_markup(reply_markup=settings_kb(call.from_user.id))


@router.callback_query(F.data == "set:toggle_rand_percent")
async def cb_toggle_rand_percent(call: CallbackQuery):
    try: await call.answer("Рандомайзер процентов изменен", parse_mode=PM)
    except Exception: pass
    s = get_settings(call.from_user.id)
    new_val = 0 if s.get("rand_percent_enabled") else 1
    update_setting(call.from_user.id, "rand_percent_enabled", new_val)
    log.setting_changed(call.from_user.id, "rand_percent_enabled", new_val, call.from_user.username)
    await call.message.edit_reply_markup(reply_markup=settings_kb(call.from_user.id))


@router.callback_query(F.data == "set:toggle_rand_bank")
async def cb_toggle_rand_bank(call: CallbackQuery):
    try: await call.answer("Рандомайзер банков изменен", parse_mode=PM)
    except Exception: pass
    s = get_settings(call.from_user.id)
    new_val = 0 if s.get("rand_bank_enabled") else 1
    update_setting(call.from_user.id, "rand_bank_enabled", new_val)
    log.setting_changed(call.from_user.id, "rand_bank_enabled", new_val, call.from_user.username)
    await call.message.edit_reply_markup(reply_markup=settings_kb(call.from_user.id))


@router.callback_query(F.data == "set:toggle_rand_acc")
async def cb_toggle_rand_acc(call: CallbackQuery):
    try: await call.answer("Рандомайзер счетов изменен", parse_mode=PM)
    except Exception: pass
    s = get_settings(call.from_user.id)
    new_val = 0 if s.get("rand_acc_enabled") else 1
    update_setting(call.from_user.id, "rand_acc_enabled", new_val)
    log.setting_changed(call.from_user.id, "rand_acc_enabled", new_val, call.from_user.username)
    await call.message.edit_reply_markup(reply_markup=settings_kb(call.from_user.id))


@router.callback_query(F.data == "set:toggle_rand_name")
async def cb_toggle_rand_name(call: CallbackQuery):
    try: await call.answer("Рандомайзер имен изменен", parse_mode=PM)
    except Exception: pass
    s = get_settings(call.from_user.id)
    new_val = 0 if s.get("rand_name_enabled") else 1
    update_setting(call.from_user.id, "rand_name_enabled", new_val)
    log.setting_changed(call.from_user.id, "rand_name_enabled", new_val, call.from_user.username)
    await call.message.edit_reply_markup(reply_markup=settings_kb(call.from_user.id))


@router.callback_query(F.data == "set:toggle_blur_checks")
async def cb_toggle_blur_checks(call: CallbackQuery):
    try: await call.answer("Блюр чеков изменен", parse_mode=PM)
    except Exception: pass
    s = get_settings(call.from_user.id)
    new_val = 0 if s.get("blur_enabled", 1) else 1
    update_setting(call.from_user.id, "blur_enabled", new_val)
    log.setting_changed(call.from_user.id, "blur_enabled", new_val, call.from_user.username)
    await call.message.edit_reply_markup(reply_markup=settings_kb(call.from_user.id))


@router.callback_query(F.data == "set:toggle_blur_qr")
async def cb_toggle_blur_qr(call: CallbackQuery):
    try: await call.answer("Блюр КР / счета изменен", parse_mode=PM)
    except Exception: pass
    s = get_settings(call.from_user.id)
    new_val = 0 if s.get("blur_qr_enabled", 1) else 1
    update_setting(call.from_user.id, "blur_qr_enabled", new_val)
    log.setting_changed(call.from_user.id, "blur_qr_enabled", new_val, call.from_user.username)
    await call.message.edit_reply_markup(reply_markup=settings_kb(call.from_user.id))


@router.callback_query(F.data.in_({"set:toggle_jose", "set:toggle_jose_sender"}))
async def cb_toggle_jose_sender(call: CallbackQuery):
    try: await call.answer("Отправитель JOSE изменен", parse_mode=PM)
    except Exception: pass
    s = get_settings(call.from_user.id)
    new_val = 0 if s.get("jose_sender_enabled") else 1
    if new_val == 1:
        update_setting(call.from_user.id, "jose_sender_enabled", 1)
        update_setting(call.from_user.id, "jose_recipient_enabled", 0)
        log.setting_changed(call.from_user.id, "jose_sender_enabled", 1, call.from_user.username)
        log.setting_changed(call.from_user.id, "jose_recipient_enabled", 0, call.from_user.username)
        if s.get("custom_name_enabled") and s.get("custom_name_target") == "sender":
            update_setting(call.from_user.id, "custom_name_enabled", 0)
            log.setting_changed(call.from_user.id, "custom_name_enabled", 0, call.from_user.username)
    else:
        update_setting(call.from_user.id, "jose_sender_enabled", 0)
        log.setting_changed(call.from_user.id, "jose_sender_enabled", 0, call.from_user.username)
    await call.message.edit_reply_markup(reply_markup=settings_kb(call.from_user.id))


@router.callback_query(F.data == "set:toggle_jose_recipient")
async def cb_toggle_jose_recipient(call: CallbackQuery):
    try: await call.answer("Получатель JOSE изменен", parse_mode=PM)
    except Exception: pass
    s = get_settings(call.from_user.id)
    new_val = 0 if s.get("jose_recipient_enabled") else 1
    if new_val == 1:
        update_setting(call.from_user.id, "jose_recipient_enabled", 1)
        update_setting(call.from_user.id, "jose_sender_enabled", 0)
        log.setting_changed(call.from_user.id, "jose_recipient_enabled", 1, call.from_user.username)
        log.setting_changed(call.from_user.id, "jose_sender_enabled", 0, call.from_user.username)
        if s.get("custom_name_enabled") and s.get("custom_name_target") == "recipient":
            update_setting(call.from_user.id, "custom_name_enabled", 0)
            log.setting_changed(call.from_user.id, "custom_name_enabled", 0, call.from_user.username)
    else:
        update_setting(call.from_user.id, "jose_recipient_enabled", 0)
        log.setting_changed(call.from_user.id, "jose_recipient_enabled", 0, call.from_user.username)
    await call.message.edit_reply_markup(reply_markup=settings_kb(call.from_user.id))


@router.callback_query(F.data == "set:toggle_custom_name")
async def cb_toggle_custom_name(call: CallbackQuery):
    try: await call.answer("Авто-ФИО изменено", parse_mode=PM)
    except Exception: pass
    s = get_settings(call.from_user.id)
    new_val = 0 if s.get("custom_name_enabled") else 1
    update_setting(call.from_user.id, "custom_name_enabled", new_val)
    log.setting_changed(call.from_user.id, "custom_name_enabled", new_val, call.from_user.username)
    
    if new_val == 1:
        target = s.get("custom_name_target", "sender")
        if target == "sender":
            update_setting(call.from_user.id, "jose_sender_enabled", 0)
            log.setting_changed(call.from_user.id, "jose_sender_enabled", 0, call.from_user.username)
        else:
            update_setting(call.from_user.id, "jose_recipient_enabled", 0)
            log.setting_changed(call.from_user.id, "jose_recipient_enabled", 0, call.from_user.username)
            
    await call.message.edit_reply_markup(reply_markup=settings_kb(call.from_user.id))


@router.callback_query(F.data == "set:toggle_custom_target")
async def cb_toggle_custom_target(call: CallbackQuery):
    s = get_settings(call.from_user.id)
    new_target = "recipient" if s.get("custom_name_target") == "sender" else "sender"
    try: await call.answer(f"Направление: {'Отправитель' if new_target == 'sender' else 'Получатель'}", parse_mode=PM)
    except Exception: pass
    update_setting(call.from_user.id, "custom_name_target", new_target)
    log.setting_changed(call.from_user.id, "custom_name_target", new_target, call.from_user.username)
    
    if s.get("custom_name_enabled"):
        if new_target == "sender":
            update_setting(call.from_user.id, "jose_sender_enabled", 0)
            log.setting_changed(call.from_user.id, "jose_sender_enabled", 0, call.from_user.username)
        else:
            update_setting(call.from_user.id, "jose_recipient_enabled", 0)
            log.setting_changed(call.from_user.id, "jose_recipient_enabled", 0, call.from_user.username)
            
    await call.message.edit_reply_markup(reply_markup=settings_kb(call.from_user.id))


@router.callback_query(F.data == "set:custom_name_val")
async def cb_set_custom_name_val(call: CallbackQuery, state: FSMContext):
    try: await call.answer()
    except Exception: pass
    await state.set_state(SettingStates.wait_custom_name_val)
    await state.update_data(settings_msg_id=call.message.message_id)
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🗑️ Сбросить значение", callback_data="set:clear_custom_name_val")],
        [InlineKeyboardButton(text="❌ Отмена",                 callback_data="set:cancel")]
    ])
    await call.message.edit_text("⌨️ Введите Авто-ФИО (например, Ivanov Ivan):", reply_markup=kb, parse_mode=PM)


@router.callback_query(F.data == "set:clear_custom_name_val")
async def cb_clear_custom_name_val(call: CallbackQuery, state: FSMContext):
    try: await call.answer()
    except Exception: pass
    await state.clear()
    update_setting(call.from_user.id, "custom_name_val", None)
    log.setting_changed(call.from_user.id, "custom_name_val", None, call.from_user.username)
    await call.message.edit_text("✅ Авто-ФИО удалено.\n\n⚙️ <b>Настройки пользователя</b>", 
                                 reply_markup=settings_kb(call.from_user.id), parse_mode="HTML")


@router.callback_query(F.data == "set:clear_name_blacklist")
async def cb_clear_name_blacklist(call: CallbackQuery):
    try: await call.answer()
    except Exception: pass
    await call.message.edit_reply_markup(reply_markup=settings_kb(call.from_user.id, confirm_clear=True))


@router.callback_query(F.data == "set:confirm_clear_name_blacklist")
async def cb_confirm_clear_name_blacklist(call: CallbackQuery):
    try: await call.answer("Блэклист имен успешно очищен!", parse_mode=PM)
    except Exception: pass
    clear_name_blacklist()
    log.setting_changed(call.from_user.id, "name_blacklist", "cleared", call.from_user.username)
    await call.message.edit_reply_markup(reply_markup=settings_kb(call.from_user.id, confirm_clear=False))


@router.callback_query(F.data == "set:cancel_clear_name_blacklist")
async def cb_cancel_clear_name_blacklist(call: CallbackQuery):
    try: await call.answer("Сброс отменен", parse_mode=PM)
    except Exception: pass
    await call.message.edit_reply_markup(reply_markup=settings_kb(call.from_user.id, confirm_clear=False))


@router.callback_query(F.data == "set:toggle_suffix")
async def cb_toggle_suffix(call: CallbackQuery):
    s = get_settings(call.from_user.id)
    options = [None, "A.M.", "P.M."]
    try:
        idx = options.index(s["time_suffix"])
    except ValueError:
        idx = 0
    new_suffix = options[(idx + 1) % len(options)]
    try: await call.answer(f"Суффикс: {new_suffix or 'Отключен'}", parse_mode=PM)
    except Exception: pass
    update_setting(call.from_user.id, "time_suffix", new_suffix)
    log.setting_changed(call.from_user.id, "time_suffix", new_suffix, call.from_user.username)
    await call.message.edit_reply_markup(reply_markup=settings_kb(call.from_user.id))


@router.callback_query(F.data == "set:min")
async def cb_set_min(call: CallbackQuery, state: FSMContext):
    try: await call.answer()
    except Exception: pass
    await state.set_state(SettingStates.wait_min)
    await state.update_data(settings_msg_id=call.message.message_id)
    await call.message.edit_text("⌨️ Введите минимальную сумму для рандомайзера:", reply_markup=cancel_kb("set:cancel"), parse_mode=PM)


@router.callback_query(F.data == "set:max")
async def cb_set_max(call: CallbackQuery, state: FSMContext):
    try: await call.answer()
    except Exception: pass
    await state.set_state(SettingStates.wait_max)
    await state.update_data(settings_msg_id=call.message.message_id)
    await call.message.edit_text("⌨️ Введите максимальную сумму для рандомайзера:", reply_markup=cancel_kb("set:cancel"), parse_mode=PM)


@router.callback_query(F.data == "set:percent_min")
async def cb_set_percent_min(call: CallbackQuery, state: FSMContext):
    try: await call.answer()
    except Exception: pass
    await state.set_state(SettingStates.wait_percent_min)
    await state.update_data(settings_msg_id=call.message.message_id)
    await call.message.edit_text("⌨️ Введите минимальный процент для рандомайзера (например, 1.0):", reply_markup=cancel_kb("set:cancel"), parse_mode=PM)


@router.callback_query(F.data == "set:percent_max")
async def cb_set_percent_max(call: CallbackQuery, state: FSMContext):
    try: await call.answer()
    except Exception: pass
    await state.set_state(SettingStates.wait_percent_max)
    await state.update_data(settings_msg_id=call.message.message_id)
    await call.message.edit_text("⌨️ Введите максимальный процент для рандомайзера (например, 100.0):", reply_markup=cancel_kb("set:cancel"), parse_mode=PM)


@router.callback_query(F.data == "set:rocket_min")
async def cb_set_rocket_min(call: CallbackQuery, state: FSMContext):
    try: await call.answer()
    except Exception: pass
    await state.set_state(SettingStates.wait_rocket_min)
    await state.update_data(settings_msg_id=call.message.message_id)
    await call.message.edit_text("⌨️ Введите минимальное число X для ракеток:", reply_markup=cancel_kb("set:cancel"), parse_mode=PM)


@router.callback_query(F.data == "set:rocket_max")
async def cb_set_rocket_max(call: CallbackQuery, state: FSMContext):
    try: await call.answer()
    except Exception: pass
    await state.set_state(SettingStates.wait_rocket_max)
    await state.update_data(settings_msg_id=call.message.message_id)
    await call.message.edit_text("⌨️ Введите максимальное число X для ракеток:", reply_markup=cancel_kb("set:cancel"), parse_mode=PM)


@router.callback_query(F.data == "set:noop")
async def cb_noop(call: CallbackQuery):
    try: await call.answer()
    except Exception: pass


@router.callback_query(F.data == "set:pinned_date")
async def cb_set_pinned(call: CallbackQuery, state: FSMContext):
    try: await call.answer()
    except Exception: pass
    await state.set_state(SettingStates.wait_pinned_date)
    await state.update_data(settings_msg_id=call.message.message_id)
    
    # Добавляем кнопку сброса
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🗑️ Сбросить дату", callback_data="set:clear_date")],
        [InlineKeyboardButton(text="❌ Отмена",        callback_data="set:cancel")]
    ])
    
    await call.message.edit_text("⌨️ Введите дату, которую нужно закрепить (например, 12.04.2026):", reply_markup=kb, parse_mode=PM)


@router.callback_query(F.data == "set:pinned_name")
async def cb_set_name(call: CallbackQuery, state: FSMContext):
    try: await call.answer()
    except Exception: pass
    await state.set_state(SettingStates.wait_pinned_name)
    await state.update_data(settings_msg_id=call.message.message_id)
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🗑️ Сбросить ФИО", callback_data="set:clear_name")],
        [InlineKeyboardButton(text="❌ Отмена",         callback_data="set:cancel")]
    ])
    await call.message.edit_text("⌨️ Введите ФИО (например, Ivanov Ivan):", reply_markup=kb, parse_mode=PM)


@router.callback_query(F.data == "set:pinned_bank")
async def cb_set_bank(call: CallbackQuery, state: FSMContext):
    try: await call.answer()
    except Exception: pass
    await state.set_state(SettingStates.wait_pinned_bank)
    await state.update_data(settings_msg_id=call.message.message_id)
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🗑️ Сбросить банк", callback_data="set:clear_bank")],
        [InlineKeyboardButton(text="❌ Отмена",         callback_data="set:cancel")]
    ])
    await call.message.edit_text("⌨️ Введите название банка (например, YAPE):", reply_markup=kb, parse_mode=PM)


@router.callback_query(F.data == "set:cancel")
async def cb_settings_cancel(call: CallbackQuery, state: FSMContext):
    try: await call.answer()
    except Exception: pass
    await state.clear()
    # Просто редактируем это же сообщение обратно в меню настроек
    await call.message.edit_text("⚙️ <b>Настройки пользователя</b>\n\nЗдесь вы можете настроить автоматизацию для ускорения работы.", 
                                 reply_markup=settings_kb(call.from_user.id), parse_mode="HTML")


@router.callback_query(F.data == "set:clear_date")
async def cb_clear_date(call: CallbackQuery, state: FSMContext):
    try: await call.answer()
    except Exception: pass
    await state.clear()
    update_setting(call.from_user.id, "pinned_date", None)
    log.setting_changed(call.from_user.id, "pinned_date", None, call.from_user.username)
    await call.message.edit_text("✅ Закрепленная дата удалена.\n\n⚙️ <b>Настройки пользователя</b>", 
                                 reply_markup=settings_kb(call.from_user.id), parse_mode="HTML")


@router.callback_query(F.data == "set:clear_name")
async def cb_clear_name(call: CallbackQuery, state: FSMContext):
    try: await call.answer()
    except Exception: pass
    await state.clear()
    update_setting(call.from_user.id, "pinned_name", None)
    log.setting_changed(call.from_user.id, "pinned_name", None, call.from_user.username)
    await call.message.edit_text("✅ Закрепленное ФИО удалено.\n\n⚙️ <b>Настройки пользователя</b>", 
                                 reply_markup=settings_kb(call.from_user.id), parse_mode="HTML")


@router.callback_query(F.data == "set:clear_bank")
async def cb_clear_bank(call: CallbackQuery, state: FSMContext):
    try: await call.answer()
    except Exception: pass
    await state.clear()
    update_setting(call.from_user.id, "pinned_bank", None)
    log.setting_changed(call.from_user.id, "pinned_bank", None, call.from_user.username)
    await call.message.edit_text("✅ Закрепленный банк удален.\n\n⚙️ <b>Настройки пользователя</b>", 
                                 reply_markup=settings_kb(call.from_user.id), parse_mode="HTML")


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
        await message.answer("❌ Введите целое число.", parse_mode=PM)

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
        await message.answer("❌ Введите целое число.", parse_mode=PM)

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
        await message.answer("❌ Введите число (например, 1.5).", parse_mode=PM)

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
        await message.answer("❌ Введите число (например, 100.0).", parse_mode=PM)

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

@router.message(SettingStates.wait_rocket_min, F.text)
async def process_rocket_min(message: Message, state: FSMContext):
    data = await state.get_data()
    msg_id = data.get("settings_msg_id")
    try:
        val = int(message.text.strip().replace(" ", ""))
        update_setting(message.from_user.id, "rand_rocket_min", val)
        log.setting_changed(message.from_user.id, "rand_rocket_min", val, message.from_user.username)
        await message.delete()
        if msg_id:
            await message.bot.edit_message_text(
                chat_id=message.chat.id, message_id=msg_id,
                text=f"✅ Минимальный X для ракеток установлен: {val}\n\n⚙️ <b>Настройки пользователя</b>",
                reply_markup=settings_kb(message.from_user.id), parse_mode="HTML"
            )
        await state.clear()
    except Exception:
        await message.answer("❌ Введите целое число.", parse_mode=PM)

@router.message(SettingStates.wait_rocket_max, F.text)
async def process_rocket_max(message: Message, state: FSMContext):
    data = await state.get_data()
    msg_id = data.get("settings_msg_id")
    try:
        val = int(message.text.strip().replace(" ", ""))
        update_setting(message.from_user.id, "rand_rocket_max", val)
        log.setting_changed(message.from_user.id, "rand_rocket_max", val, message.from_user.username)
        await message.delete()
        if msg_id:
            await message.bot.edit_message_text(
                chat_id=message.chat.id, message_id=msg_id,
                text=f"✅ Максимальный X для ракеток установлен: {val}\n\n⚙️ <b>Настройки пользователя</b>",
                reply_markup=settings_kb(message.from_user.id), parse_mode="HTML"
            )
        await state.clear()
    except Exception:
        await message.answer("❌ Введите целое число.", parse_mode=PM)

@router.message(SettingStates.wait_custom_name_val, F.text)
async def process_custom_name_val(message: Message, state: FSMContext):
    data = await state.get_data()
    msg_id = data.get("settings_msg_id")
    val = message.text.strip()
    update_setting(message.from_user.id, "custom_name_val", val)
    log.setting_changed(message.from_user.id, "custom_name_val", val, message.from_user.username)
    await message.delete()
    if msg_id:
        await message.bot.edit_message_text(
            chat_id=message.chat.id, message_id=msg_id,
            text=f"✅ Авто-ФИО установлено: {val}\n\n⚙️ <b>Настройки пользователя</b>",
            reply_markup=settings_kb(message.from_user.id), parse_mode="HTML"
        )
    await state.clear()
