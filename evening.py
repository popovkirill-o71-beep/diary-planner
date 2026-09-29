# evening.py — логика вечернего опроса
from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command

from states import DiaryStates
from questions import QUESTIONS
from storage import save_entry  # импортируем функцию сохранения

router = Router()

@router.message(Command("evening"))
async def start_evening(message: Message, state: FSMContext):
    """Запуск вечернего опроса по команде /evening"""
    # Устанавливаем бота в первое состояние
    await state.set_state(DiaryStates.q1)
    await message.answer(QUESTIONS[0])

@router.message(DiaryStates.q1)
async def process_q1(message: Message, state: FSMContext):
    """Обработка ответа на первый вопрос"""
    # Сохраняем ответ в состоянии бота (а не в словаре!)
    await state.update_data(q1=message.text)
    await state.set_state(DiaryStates.q2)
    await message.answer(QUESTIONS[1])

@router.message(DiaryStates.q2)
async def process_q2(message: Message, state: FSMContext):
    """Обработка ответа на второй вопрос"""
    await state.update_data(q2=message.text)
    await state.set_state(DiaryStates.q3)
    await message.answer(QUESTIONS[2])

@router.message(DiaryStates.q3)
async def process_q3(message: Message, state: FSMContext):
    """Обработка ответа на третий вопрос и сохранение в файл"""
    # Получаем все ответы из состояния бота
    data = await state.get_data()
    answers = [data.get("q1", ""), data.get("q2", ""), message.text]
    
    # Сохраняем в файл через нашу функцию
    user_id = message.from_user.id
    save_entry(user_id, answers)
    
    # Показываем сводку
    await message.answer(
        f"✅ Записал в дневник:\n"
        f"1. {answers[0]}\n"
        f"2. {answers[1]}\n"
        f"3. {answers[2]}"
    )
    
    # Сбрасываем состояние
    await state.clear()