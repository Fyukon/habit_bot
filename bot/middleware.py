import logging

from aiogram import BaseMiddleware
from aiogram.types import Message

logger = logging.getLogger(__name__)

logger.setLevel(logging.INFO)


class AutoReplyMarkupMiddleware(BaseMiddleware):
    async def __call__(self, handler, event: Message, data):
        response = await handler(event, data)
        logger.debug("MiddleWare works")
        if response and isinstance(event, Message):
            await event.answer(response, reply_markup=get_main_keyboard())
        return response
