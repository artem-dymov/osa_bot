from aiogram.dispatcher.filters.state import StatesGroup, State


class Registering(StatesGroup):
    group = State()
