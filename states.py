# states.py — здесь мы описываем "состояния" (уровни) нашего бота
from aiogram.fsm.state import State, StatesGroup

class DiaryStates(StatesGroup):
    """Состояния для ведения вечернего дневника."""
    q1 = State()  # Бот задал первый вопрос и ждёт ответ
    q2 = State()  # Бот задал второй вопрос и ждёт ответ
    q3 = State()  # Бот задал третий вопрос и ждёт ответ