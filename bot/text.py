# text.py

texts = {
    "start": "Привет, {name}! Я помогу тебе с привычками.",
    "already_registered": "Мы уже знакомы!",
    "help": (
        "Этот бот создан для отслеживания привычек.\n"
        "/add <название> <кол-во> — добавить привычку\n"
        "/del <название> — удалить привычку\n"
        "/list — посмотреть список привычек\n"
        "/cancel — отменить ввод или действие\n"
        "Также доступен интерфейс через кнопки."
    ),
    "add_success": "Привычка '{name}' добавлена!",
    "add_duplicate": "Привычка '{name}' уже существует!",
    "add_bad_format": "Формат: /add <название> <количество>",
    "del_success": "Привычка '{name}' удалена.",
    "del_fail": "Не удалось найти привычку '{name}'.",
    "del_bad_format": "Формат: /del <название>",
    "list_empty": "У тебя пока нет привычек.",
    "list": "Твои привычки:\n",
    "cancelled": "Действие отменено.",
    "input_habit_name": "Отправьте название привычки!",
    "input_habit_times": "Введите количество повторений!",
    "bad_number": "Давай-ка нормальное число!",
    "habit_exists": "Такая привычка уже есть!",
    "prompt_remove": "Введите название привычки из списка!",
    "habit_deleted": "Привычка удалена!",
    "menu": "Меню",
    "no_habits": "У вас нет привычек!",
    "dog_api_fail": "Не удалось получить картинку с собачкой.",
    "unknown_command": "Неизвестная команда. Используйте /help.",
    "add_habit_error": "Ошибка при добавлении привычки",
    "remind_fail": "Неверно! Формат: /remind <час>:<минута>",
    "remind_success": "Напоминание установлено!",
}
