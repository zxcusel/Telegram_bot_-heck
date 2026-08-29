import sys
import traceback

try:
    import asyncio
    from aiogram import Bot, Dispatcher
    from aiogram.fsm.storage.memory import MemoryStorage

    from handlers import admin, auto, catalog, render, settings, bulk, tickets, instruction, clock, timezone
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

        storage = MemoryStorage()
        dp = Dispatcher(storage=storage)

        dp.message.middleware(RoleMiddleware())
        dp.callback_query.middleware(RoleMiddleware())

        dp.include_router(settings.router)
        dp.include_router(admin.router)
        dp.include_router(catalog.router)
        dp.include_router(auto.router)
        # dp.include_router(bulk.router)
        dp.include_router(render.router)
        dp.include_router(tickets.router)
        dp.include_router(instruction.router)
        dp.include_router(clock.router)
        dp.include_router(timezone.router)

        from handlers import fallback
        dp.include_router(fallback.router)

        log.startup()

        from aiogram.client.session.aiohttp import AiohttpSession

        while True:
            bot = None
            try:
                # Настройка сессии с таймаутами и поддержкой Keep-Alive соединений
                session = AiohttpSession()
                bot = Bot(token=get_token(), session=session)
                
                # Удаляем вебхук перед стартом, не удаляя накопившиеся сообщения
                await bot.delete_webhook(drop_pending_updates=False)

                # Запуск фонового обновления часов (60 сек период)
                from handlers.clock import clock_updater
                asyncio.create_task(clock_updater(bot))
                
                # Запуск поллинга
                await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
                break
            except (KeyboardInterrupt, SystemExit, asyncio.CancelledError):
                break
            except Exception as e:
                import datetime
                err_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                print(f"[{err_time}] Polling crashed with error: {e}. Reconnecting in 5 seconds...")
                with open("polling_crash_log.txt", "a", encoding="utf-8") as f:
                    f.write(f"[{err_time}] Error: {e}\n")
                    traceback.print_exc(file=f)
                await asyncio.sleep(5)
            finally:
                if bot:
                    try:
                        await bot.session.close()
                    except Exception:
                        pass


    if __name__ == "__main__":
        asyncio.run(main())

except KeyboardInterrupt:
    print("\n🛑 Запуск бота прерван пользователем или системой.")
    sys.exit(0)
except Exception as e:
    with open("crash_log.txt", "w", encoding="utf-8") as f:
        traceback.print_exc(file=f)
    print("CRITICAL CRASH SAVED TO crash_log.txt:")
    traceback.print_exc(file=sys.stdout)
    sys.exit(1)
    