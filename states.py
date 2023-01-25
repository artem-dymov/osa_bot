from aiogram.dispatcher.filters.state import StatesGroup, State


class Registering(StatesGroup):
    group = State()
    confirm_group = State()


class PollStates(StatesGroup):
    minor_state = State()
    open_micro_question = State()
    anonymous_question = State()


