import logging

from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

logger = logging.getLogger("HabitBot")


class HabitsDeletion(CallbackData, prefix='delete_habit', sep=':'):
    user_id: int
    habit_name: str


add_button = InlineKeyboardButton(text="Добавить привычку", callback_data="add_button")
remove_button = InlineKeyboardButton(text="Удалить привычку", callback_data="remove_button")
get_button = InlineKeyboardButton(text="Мои привычки", callback_data="get_button")
help_button = InlineKeyboardButton(text="Помощь", callback_data="help_button")
cancel_button = InlineKeyboardButton(text="Отмена", callback_data="cancel_button")


def menu_keyboard():
    builder = InlineKeyboardBuilder()

    builder.row(add_button)
    builder.row(remove_button)
    builder.row(get_button)
    builder.row(help_button)

    return builder.as_markup(resize_keyboard=True)


def cancel_keyboard():
    builder = InlineKeyboardBuilder()

    builder.row(cancel_button)

    return builder.as_markup(resize_keyboard=True)


def delete_habits_keyboard(habits: tuple):
    logger.info("Удаление привычек")
    builder = InlineKeyboardBuilder()
    for habit in habits:
        builder.add(InlineKeyboardButton(text=f"{habit[1]}", callback_data=HabitsDeletion(
            user_id=habit[0],
            habit_name=habit[1]
        ).pack()))
    builder.row(cancel_button)
    logger.info("Клавиатура для удаление привычек построена")
    return builder.as_markup(resize_keyboard=True)
