import sys
import traceback

try:
    import asyncio
    from aiogram import Bot, Dispatcher
    from aiogram.fsm.storage.memory import MemoryStorage

    from handlers import admin, catalog, render, settings, bulk
    from middlewares.role_check import RoleMiddleware
    from data.db import init_db, get_token
    from utils.logger import log

    # Глобальный патч CallbackQuery.answer для предотвращения падений при старых/таймаутнутых callback-запросах
    from aiogram.types import CallbackQuery
    from aiogram.exceptions import TelegramBadRequest, TelegramAPIError

    _original_callback_answer = CallbackQuery.answer

    async def _safe_callback_answer(self, *args, **kwargs):
        try:
            return await _original_callback_answer(self, *args, **kwargs)
        except (TelegramBadRequest, TelegramAPIError) as e:
            err_msg = str(e).lower()
            if any(substring in err_msg for substring in ("query is too old", "query id is invalid", "timeout expired")):
                return False
            raise

    CallbackQuery.answer = _safe_callback_answer


    async def main():
        init_db()
        log.db_ready()

        bot = Bot(token=get_token())
        storage = MemoryStorage()
        dp = Dispatcher(storage=storage)

        dp.message.middleware(RoleMiddleware())
        dp.callback_query.middleware(RoleMiddleware())

        dp.include_router(settings.router)
        dp.include_router(admin.router)
        dp.include_router(catalog.router)
        dp.include_router(bulk.router)
        dp.include_router(render.router)

        from handlers import fallback
        dp.include_router(fallback.router)

        log.startup()
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


    if __name__ == "__main__":
        asyncio.run(main())

except Exception as e:
    with open("crash_log.txt", "w", encoding="utf-8") as f:
        traceback.print_exc(file=f)
    print("CRITICAL CRASH SAVED TO crash_log.txt:")
    traceback.print_exc(file=sys.stdout)
    sys.exit(1)
    