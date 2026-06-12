from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import StateFilter
from utils.logger import log

router = Router()

@router.message(StateFilter(None), F.text, ~F.text.startswith("/"))
async def fallback_text_handler(message: Message):
    log.unhandled_text(message.from_user.id, message.text, message.from_user.username)
