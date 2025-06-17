from aiogram.fsm.state import State, StatesGroup


class AddHabit(StatesGroup):
    waiting_for_name = State()
    waiting_for_times = State()
    waiting_for_reminder = State()


class DeleteHabit(StatesGroup):
    waiting_for_name = State()
