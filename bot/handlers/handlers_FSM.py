import logging

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, CallbackQuery

from bot.handlers.states import AddHabit
from bot.keyboards import menu_keyboard
from bot.keyboards.inline import cancel_keyboard
from bot.service import database
from bot.text import texts

logger = logging.getLogger("HabitBot")

router = Router(name="habit_FSM")


@router.message(AddHabit.waiting_for_name)
async def name_add_habit(message: Message, state: FSMContext):
    habit = message.text
    if await database.get_habit(message.from_user.id, habit):
        await message.answer(texts["add_duplicate"].format(name=habit))
        await state.clear()
    else:
        await message.bot.send_message(text=texts["input_habit_times"], chat_id=message.from_user.id,
                                       reply_markup=cancel_keyboard())
        await state.update_data(habit_name=message.text)
        await state.set_state(AddHabit.waiting_for_times)


@router.message(AddHabit.waiting_for_times)
async def times_add_habit(message: Message, state: FSMContext):
    text = message.text
    try:
        if int(text) <= 0:
            raise ValueError

        logger.info("Привычка завершает добавление в БД...")
        data = await state.get_data()
        logger.info(data)
        await database.add_habit(message.from_user.id, data['habit_name'], int(text))
        await message.bot.send_message(text=texts["add_success"].format(name=data["habit_name"]),
                                       chat_id=message.from_user.id,
                                       reply_markup=menu_keyboard())
        await state.clear()
    except ValueError:
        await message.bot.send_message(text=texts["bad_number"], chat_id=message.from_user.id,
                                       reply_markup=cancel_keyboard())
        logger.exception("Плохое число выбрал пользователь!")
