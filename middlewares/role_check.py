import time
from threading import Lock
from typing import Any, Callable, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message, CallbackQuery
from data.db import upsert_user, has_any_access, is_admin
from utils.logger import log

_user_last_seen = {}
_lock = Lock()


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
            now = time.time()
            user_id = user.id
            username = user.username
            first_name = user.first_name

            need_upsert = False
            with _lock:
                cached = _user_last_seen.get(user_id)
                if not cached or (now - cached["time"] > 300) or cached["username"] != username or cached["first_name"] != first_name:
                    need_upsert = True
                    _user_last_seen[user_id] = {
                        "time": now,
                        "username": username,
                        "first_name": first_name
                    }

            if need_upsert:
                is_new = False
                from data.db import get_username
                if get_username(user_id) is None:
                    is_new = True
                upsert_user(user_id, username, first_name)
                if is_new:
                    log.user_seen(user_id, username)

            if not has_any_access(user_id):
                log.access_denied(user_id, username)
                return

        return await handler(event, data)



