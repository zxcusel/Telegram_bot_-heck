from typing import Any, Callable, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message, CallbackQuery
from data.db import upsert_user, has_any_access, is_admin
from utils.logger import log


class RoleMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        user = None
        if isinstance(event, (Message, CallbackQuery)):
            user = event.from_user

        if user:
            is_new = False
            from data.db import get_username
            if get_username(user.id) is None:
                is_new = True
            upsert_user(user.id, user.username, user.first_name)
            if is_new:
                log.user_seen(user.id, user.username)

            if not has_any_access(user.id):
                log.access_denied(user.id, user.username)
                return

        return await handler(event, data)



