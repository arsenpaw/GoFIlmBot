from aiogram.fsm.state import State, StatesGroup

class BotStates(StatesGroup):
    url = State()
    qality = State()
    sound = State()
    season = State()
    episod = State()
    s_sound =State()
    s_quality = State()
    s_final = State()
    download = State()
    final = State()
