import logging

from aiogram import Router, F
from aiogram.filters import Command, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, CallbackQuery

from bot.service.database import delete_habit, get_habit, get_habits, add_habit

logger = logging.getLogger("HabitBot")

router = Router(name="habits_commands")


@router.message(Command("/del"))
async def del_habit(message: Message, command: CommandObject):
    habit = command.args
    if not habit:
        await message.answer("Формат: /del <название привычки>")
        return

    resp = await delete_habit(message.from_user.id, habit)
    if resp:
        await message.answer(f"Привычка {resp} удалена")
    else:
        await message.answer(f"У вас нет привычки {habit}")


@router.message(Command("/add"))
async def add_habit(message: Message, command: CommandObject):
    logger.info("Зашел в /add")
    try:
        habit = command.args
        if not habit:
            raise ValueError("Нет аргументов")
        name, count = habit.rsplit(" ", 1)
        count = int(count)

        resp = await get_habit(message.from_user.id, name)
        if resp:
            await message.answer(f"Привычка {name} уже существует!")
            return

        await add_habit(message.from_user.id, name, count)
        await message.answer(f"Привычка {name} добавлена!")
    except Exception as e:
        await message.answer(f"Формат: /add <название> <кол-во повторений>")
        logger.error(e)


@router.message(Command("/list"))
async def list_habit(message: Message):
    habits = await get_habits(message.from_user.id)
    if not habits:
        await message.answer("У вас нет привычек!")
        return
    text = "\n".join([habit[1] for habit in habits])
    await callback.message.edit_text("Ваши привычки:\n" + text)
