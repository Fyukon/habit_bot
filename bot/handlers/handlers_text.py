import logging

from aiogram import Router, F
from aiogram.filters import Command, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from text import texts

from bot.handlers.states import AddHabit, DeleteHabit
from bot.keyboards.inline import menu_keyboard, cancel_keyboard, delete_habits_keyboard
from bot.service import database

logger = logging.getLogger("HabitBot")

router = Router(name="habits_text")


@router.message(F.text == "Меню 🏠")
async def menu(message: Message):
    await message.answer(texts["menu"], reply_markup=menu_keyboard())


@router.message(F.text == "Удалить привычку ❌")
async def start_delete_habit(message: Message, state: FSMContext):
    await state.set_state(DeleteHabit.waiting_for_name)
    habits = await database.get_habits(message.from_user.id)
    logger.debug(habits)
    await message.answer(texts["prompt_remove"],
                         reply_markup=delete_habits_keyboard(habits))


@router.message(F.text == "Добавить привычку ➕")
async def start_add_habit(message: Message, state: FSMContext):
    user_id = message.from_user.id
    await state.set_state(AddHabit.waiting_for_name)
    await message.answer(texts["input_habit_name"],
                         reply_markup=cancel_keyboard())
    logger.info("Пользователь вводит привычку!", extra={"user_id": user_id})


@router.message(F.text == "Мои привычки 📋")
async def list_habit(message: Message):
    habits = await database.get_habits(message.from_user.id)
    if not habits:
        await message.answer(texts["list_empty"])
        return
    text = "\n".join([habit[1] for habit in habits])
    await message.answer(texts["list"].format(habits=text))


@router.message(F.text == "Отмена 🔙")
async def cancel(message: Message, state: FSMContext):
    await message.answer(texts["cancelled"])
    await state.clear()
