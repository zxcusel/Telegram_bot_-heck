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




    async def _run_announcement(bot):
        """Разовая рассылка апдейта про закреп-часы всем админам/контентщикам.
        Гейтится через bot_meta, чтобы выполниться ровно один раз после деплоя.
        Любые ошибки глушатся — функционал бота важнее."""
        import sqlite3
        try:
            await asyncio.sleep(15)
            with sqlite3.connect("/home/container/bot.db") as con:
                con.execute(
                    "CREATE TABLE IF NOT EXISTS bot_meta ("
                    " key TEXT PRIMARY KEY, value TEXT)"
                )
                row = con.execute(
                    "SELECT value FROM bot_meta WHERE key='announce_clock_v1'"
                ).fetchone()
                if row and row[0] == "done":
                    return
                con.execute(
                    "INSERT INTO bot_meta(key, value) VALUES('announce_clock_v1','pending')"
                    " ON CONFLICT(key) DO UPDATE SET value='pending'"
                )
                con.commit()
                cur = con.cursor()
                ids = set()
                # Реальная схема: таблица admins и таблица roles (cr/rd/fd - права создателей).
                for q in (
                    "SELECT user_id FROM admins",
                    "SELECT user_id FROM roles WHERE role IN ('cr','rd','fd')",
                    "SELECT user_id FROM users",
                ):
                    try:
                        for r in cur.execute(q):
                            ids.add(int(r[0]))
                    except Exception:
                        pass
                ids = sorted(ids)

            text = (
                "🛠 <b>Тех. обновление — просьба проверить</b>\n"
                "━━━━━━━━━━━━━━━━━━━━\n"
                "Дорогие админы и контентщики! Выкатили пару улучшений:\n\n"
                "1️⃣ <b>Закреп с часами</b> теперь тикает <b>каждую секунду</b> "
                "(формат HH:MM:SS по Москве, Боливии, Парагваю).\n"
                "2️⃣ В разделе <b>«⚙️ Настройки»</b> появился тумблер "
                "<b>«🕒 Закреп с часами»</b> — можно ВКЛ/ВЫКЛ.\n\n"
                "Просьба:\n"
                "• Зайти в бот, нажать /start — убедиться, что часы идут.\n"
                "• Открыть Настройки → «Закреп с часами» → выключить — "
                "убедиться, что пин снят. Затем включить обратно.\n\n"
                "Если что-то не так — напишите владельцу, пофиксим. "
                "Спасибо! 🙏"
            )

            sent = fail = 0
            for uid in ids:
                try:
                    await bot.send_message(chat_id=uid, text=text, parse_mode="HTML")
                    sent += 1
                except Exception as e:
                    fail += 1
                await asyncio.sleep(0.05)

            print(f"[announce] sent={sent} fail={fail} total={len(ids)}")

            with sqlite3.connect("/home/container/bot.db") as con:
                con.execute(
                    "UPDATE bot_meta SET value='done' WHERE key='announce_clock_v1'"
                )
                con.commit()
        except Exception as e:
            print(f"[announce] error: {e}")




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

                # Запуск фонового обновления часов (каждую секунду)
                from handlers.clock import clock_updater
                asyncio.create_task(clock_updater(bot))

                # Разовая рассылка апдейта про новый закреп-часы + тумблер
                asyncio.create_task(_run_announcement(bot))
                
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
    