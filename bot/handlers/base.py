import logging

from aiogram import Router, types, F, Bot
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery

from bot.keyboards.inline import menu_keyboard
from bot.service import *

logger = logging.getLogger("HabitBot")
router = Router(name="Base command")


@router.message(Command("start"))
async def start(message: Message):
    user = message.from_user.id
    user_name = message.from_user.first_name
    try:
        await add_user(user, user_name)
        await message.answer(f"Привет, {user}! Я помогу тебе с привычками!", reply_markup=menu_keyboard())
    except Exception as error:
        await message.answer("Мы уже знакомы!", reply_markup=menu_keyboard())


@router.callback_query(F.data == "help_button")
async def help(callback: CallbackQuery, bot: Bot):
    url = await get_dog_url()
    try:
        await bot.send_photo(chat_id=callback.from_user.id, photo=url)
    except Exception as e:
        logger.error(url, e)
    await callback.message.answer("Этот бот существует для тренировки создания ботов в телеграме!",
                                  reply_markup=menu_keyboard())
    logger.info("ОН ПОПРОСИЛ ПОМОЩИ!!")
    await callback.answer("На самом деле помощи я тебе не предложу, но зато могу предложить картинку с собачкой!")
