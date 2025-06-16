from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def get_main_keyboard():
    """Основная клавиатура"""
    builder = ReplyKeyboardBuilder()
    buttons = [
        KeyboardButton(text="Добавить привычку"),
        KeyboardButton(text="Мои привычки"),
        KeyboardButton(text="Удалить привычку"),
        KeyboardButton(text="Отмена")
    ]
    builder.row(*buttons)
    return builder.as_markup(resize_keyboard=True)


def get_cancel_keyboard():
    builder = ReplyKeyboardBuilder()
    builder.add(KeyboardButton(text="Отмена"))
    return builder.as_markup(resize_keyboard=True)
