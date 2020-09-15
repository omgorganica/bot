from aiogram.dispatcher.filters.state import StatesGroup, State


class States(StatesGroup):
    shift_start = State()
    add_user = State()