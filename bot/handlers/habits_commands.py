import logging

from aiogram import Router
from aiogram.filters import Command, CommandObject
from aiogram.types import Message
from text import texts

from bot.keyboards.inline import menu_keyboard
from bot.service import database

logger = logging.getLogger("HabitBot")

router = Router(name="habits_commands")


@router.message(Command("menu"))
async def menu(message: Message):
    await message.answer(texts["menu"], reply_markup=menu_keyboard())


@router.message(Command("del"))
async def del_habit(message: Message, command: CommandObject):
    habit = command.args
    if not habit:
        await message.answer(texts["del_bad_format"])
        return

    resp = await database.delete_habit(message.from_user.id, habit)
    if resp:
        await message.answer(texts["del_success"].format(name=habit))
    else:
        await message.answer(texts["del_fail"].format(name=habit))


@router.message(Command("add"))
async def add_habit(message: Message, command: CommandObject):
    logger.info("Зашел в /add")
    try:
        habit = command.args
        if not habit:
            raise ValueError("Нет аргументов")
        name, count, reminder = habit.split(" ")
        count = int(count)
        hours, minutes = tuple(map(int, reminder.split(":")))
        if not (0 <= hours <= 24) or not (0 <= minutes <= 60):
            raise ValueError
        resp = await database.get_habit(message.from_user.id, name)
        if resp:
            await message.answer(texts["add_duplicate"].format(name=name))
            return
        reminder = (hours, minutes)
        await database.add_habit(message.from_user.id, name, count, reminder)
        await message.answer(texts["add_success"].format(name=name))
    except Exception as e:
        await message.answer(texts["add_bad_format"])
        logger.exception(e)


@router.message(Command("list"))
async def list_habit(message: Message):
    habits = await database.get_habits(message.from_user.id)
    if not habits:
        await message.answer(texts["list_empty"])
        return
    text = "\n".join([habit[1] for habit in habits])
    await message.answer(texts["list"].format(habits=text))
