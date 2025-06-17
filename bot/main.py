import asyncio

import dotenv
from aiogram import Bot, Dispatcher, Router
from aiogram.filters import Command
from aiogram.types import (KeyboardButton, Message, ReplyKeyboardMarkup,
                           ReplyKeyboardRemove, BotCommand
                           )
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from environs import Env

from bot.service.logs import setup_logging
from bot.service.reminder import scheduler
from config import load_config
from handlers import routers


async def main():
    config = load_config(r"C:\Users\Алексей\PycharmProjects\Bot\.env")
    bot = Bot(token=config.tg_bot.token)
    dp = Dispatcher()
    commands = [
        BotCommand(command="start", description="Запустить бота"),
        BotCommand(command="add", description="Добавить привычку"),
        BotCommand(command="del", description="Удалить привычку"),
        BotCommand(command="list", description="Показать привычки"),
        BotCommand(command="help", description="Помощь"),
        BotCommand(command="cancel", description="Отменить действие"),
        BotCommand(command="menu", description="Главное меню"),
    ]
    await bot.set_my_commands(commands)

    dp['bot_token'] = config.tg_bot.token
    scheduler.start()

    logger = setup_logging("HabitBot")

    for router in routers:
        dp.include_router(router)
    await dp.start_polling(bot)


asyncio.run(main())
