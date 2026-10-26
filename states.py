# states.py — состояния FSM для вечернего опроса
from aiogram.fsm.state import State, StatesGroup


class DiaryStates(StatesGroup):
    """Состояния вечернего диалога."""
    q1 = State()  # ждём ответ на вопрос 1
    q2 = State()  # ждём ответ на вопрос 2
    q3 = State()  # ждём ответ на вопрос 3