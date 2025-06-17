import logging

from aiogram import Router, types, F, Bot
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery

from bot.keyboards.inline import menu_keyboard
from bot.keyboards.reply import get_main_keyboard
from bot.service import *
from bot.text import texts

logger = logging.getLogger("HabitBot")
router = Router(name="Base command")


@router.message(Command("start"))
async def start(message: Message):
    user = message.from_user.id
    user_name = message.from_user.first_name
    try:
        await add_user(user, user_name)
        await message.answer(texts["start"].format(user=user_name),
                             reply_markup=get_main_keyboard())
    except Exception as error:
        await message.answer(texts['already_registered'], reply_markup=get_main_keyboard())


@router.callback_query(F.data == "help_button")
async def help(callback: CallbackQuery, bot: Bot):
    url = await get_dog_url()
    try:
        await bot.send_photo(chat_id=callback.from_user.id, photo=url)
    except Exception as e:
        logger.error(url, e)
    await callback.message.answer(texts["help"],
                                  reply_markup=menu_keyboard())
    logger.info("ОН ПОПРОСИЛ ПОМОЩИ!!")
    await callback.answer()
