from aiogram.dispatcher.filters.state import StatesGroup, State


class PollStates(StatesGroup):
    minor_state = State()
    open_micro_question = State()
    anonymous_question = State()


