# evening.py — логика вечернего опроса
from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command

from states import DiaryStates
from questions import QUESTIONS

router = Router()  # Создаём роутер — он будет принимать сообщения

# Словарь для временного хранения ответов (пока в памяти, потом перенесём в файл)
# Ключ - ID пользователя, Значение - список ответов
temp_answers = {} 

@router.message(Command("evening"))
async def start_evening(message: Message, state: FSMContext):
    """Запуск вечернего опроса по команде /evening"""
    user_id = message.from_user.id
    
    # Очищаем старые данные, если они были
    temp_answers[user_id] = []
    
    # Устанавливаем бота в первое состояние (ждёт ответ на 1 вопрос)
    await state.set_state(DiaryStates.q1)
    
    # Отправляем первый вопрос
    await message.answer(QUESTIONS[0])

@router.message(DiaryStates.q1)
async def process_q1(message: Message, state: FSMContext):
    """Обработка ответа на первый вопрос"""
    user_id = message.from_user.id
    temp_answers[user_id].append(message.text)  # Сохраняем ответ
    
    # Переходим ко второму состоянию
    await state.set_state(DiaryStates.q2)
    await message.answer(QUESTIONS[1])

@router.message(DiaryStates.q2)
async def process_q2(message: Message, state: FSMContext):
    """Обработка ответа на второй вопрос"""
    user_id = message.from_user.id
    temp_answers[user_id].append(message.text)
    
    # Переходим к третьему состоянию
    await state.set_state(DiaryStates.q3)
    await message.answer(QUESTIONS[2])

@router.message(DiaryStates.q3)
async def process_q3(message: Message, state: FSMContext):
    """Обработка ответа на третий вопрос и завершение"""
    user_id = message.from_user.id
    temp_answers[user_id].append(message.text)
    
    # Показываем, что сохранили (пока просто выводим)
    answers = temp_answers[user_id]
    await message.answer(
        f"✅ Отлично! Записал:\n"
        f"1. {answers[0]}\n"
        f"2. {answers[1]}\n"
        f"3. {answers[2]}"
    )
    
    # Сбрасываем состояние, бот снова обычный
    await state.clear()
    # Очищаем временные данные
    del temp_answers[user_id]