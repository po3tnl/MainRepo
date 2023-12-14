from aiogram.fsm.state import StatesGroup, State


class CreateState(StatesGroup):
    place = State()
    date = State()
    time = State()
    minplayer = State()
    maxplayer = State()
    price = State()
