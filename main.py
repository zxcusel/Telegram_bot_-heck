import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from handlers import admin, catalog, render, settings
from middlewares.role_check import RoleMiddleware
from data.db import init_db, get_token
from utils.logger import log


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
    dp.include_router(render.router)

    log.startup()
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())

    
if __name__ == "__main__":
    asyncio.run(main())
