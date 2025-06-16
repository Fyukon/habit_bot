import asyncio

import dotenv
from aiogram import Bot, Dispatcher, Router
from aiogram.filters import Command
from aiogram.types import (KeyboardButton, Message, ReplyKeyboardMarkup,
                           ReplyKeyboardRemove)
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from environs import Env

from bot.service.logs import setup_logging
from config import load_config
from handlers import routers


async def main():
    config = load_config(r"C:\Users\Алексей\PycharmProjects\Bot\.env")
    bot = Bot(token=config.tg_bot.token)
    dp = Dispatcher()

    dp['bot_token'] = config.tg_bot.token

    logger = setup_logging("HabitBot")

    for router in routers:
        dp.include_router(router)
    await dp.start_polling(bot)


asyncio.run(main())
