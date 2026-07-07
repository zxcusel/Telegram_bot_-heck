# Инструкция по включению функции массовой генерации чеков

Для того чтобы вернуть функцию массовой генерации в бота, выполните следующие два шага:

---

### Шаг 1. Включение кнопки в главном меню
Откройте файл: `handlers/catalog.py`
Найдите строки в функции `_start_kb` (примерно 20-22 строки):
```python
def _start_kb(user_id: int) -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text="▶️ Начать", callback_data="start:begin")],
        # [InlineKeyboardButton(text="🎲 Массовая генерация", callback_data="start:bulk_gen")],
        [InlineKeyboardButton(text="⚙️ Настройки", callback_data="start:settings")],
    ]
```
**Действие:** Уберите символ решетки `#` в начале строки с кнопкой массовой генерации, чтобы она выглядела так:
```python
        [InlineKeyboardButton(text="🎲 Массовая генерация", callback_data="start:bulk_gen")],
```

---

### Шаг 2. Активация роутера (обработчика команд)
Откройте файл: `main.py`
Найдите строки регистрации роутеров в функции `main` (примерно 43-47 строки):
```python
        dp.include_router(settings.router)
        dp.include_router(admin.router)
        dp.include_router(catalog.router)
        # dp.include_router(bulk.router)
        dp.include_router(render.router)
```
**Действие:** Уберите символ решетки `#` в начале строки с регистрацией bulk роутера, чтобы она выглядела так:
```python
        dp.include_router(bulk.router)
```

---

После раскомментирования этих двух строк перезапустите бота, и функция массовой генерации полностью восстановит свою работу!
