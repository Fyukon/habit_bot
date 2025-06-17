import logging

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, CallbackQuery

from bot.keyboards import menu_keyboard
from bot.keyboards.inline import cancel_keyboard, delete_habits_keyboard
from bot.service import database
from bot.text import texts
from bot.handlers.states import AddHabit, DeleteHabit

logger = logging.getLogger("HabitBot")

router = Router(name="habit_buttons")


@router.callback_query(F.data == "cancel_button")
async def cancel(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    logger.info("Пользователь отменил ввод привычки!")
    await callback.answer(texts["cancelled"])

    await callback.message.edit_text("Меню",
                                     reply_markup=menu_keyboard())

    logger.debug("Сообщение должно быть удалено!")
    await callback.answer()


@router.callback_query(F.data == "add_button")
async def start_add_habit(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    await state.set_state(AddHabit.waiting_for_name)
    await callback.message.edit_text(texts["input_habit_name"],
                                     reply_markup=cancel_keyboard())
    logger.info("Пользователь вводит привычку!", extra={"user_id": user_id})
    await callback.answer()


@router.callback_query(F.data == "get_button")
async def show_habits(callback: CallbackQuery):
    habits = await database.get_habits(callback.from_user.id)
    if len(habits) == 0:
        await callback.message.edit_text(texts["no_habits"],
                                         reply_markup=menu_keyboard())
    else:
        logger.info([habit[1] for habit in habits])
        text = "\n".join([habit[1] for habit in habits])
        await callback.message.edit_text(texts["list"] + text,
                                         reply_markup=menu_keyboard())
    await callback.answer()


@router.callback_query(F.data == "remove_button")
async def start_delete_habit(callback: CallbackQuery, state: FSMContext):
    await state.set_state(DeleteHabit.waiting_for_name)
    habits = await database.get_habits(callback.from_user.id)
    logger.debug(habits)
    await callback.message.edit_text(texts["prompt_remove"],
                                     reply_markup=delete_habits_keyboard(habits))
    await callback.answer()


@router.callback_query(F.data.startswith("delete_habit:"))
async def delete_habit(callback: CallbackQuery, state: FSMContext):
    logger.info("Удаление привычки")
    try:
        data = callback.data.split(":")
        logger.info(data[2]

                    )
        logger.info("Операция определена")
        user_id = int(data[1])
        name = data[2]
        logger.info(f"{user_id}: {name}")
        await database.delete_habit(user_id, name)
        logger.info("Пользователь удалил привычку!")
        await callback.message.answer(texts["habit_deleted"], reply_markup=menu_keyboard())
        await state.clear()
    except Exception:
        pass
    await callback.answer()
