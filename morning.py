# morning.py — логика утреннего показа задач
from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from storage import get_yesterday_entry  # импортируем функцию из storage.py

router = Router()

@router.message(Command("morning"))
async def show_yesterday(message: Message):
    """Обработчик команды /morning. Показывает задачу на сегодня из вчерашнего дневника."""
    user_id = message.from_user.id
    
    # Пытаемся получить вчерашнюю запись
    entry = get_yesterday_entry(user_id)
    
    # КРАЕВОЙ СЛУЧАЙ: если вчера ты не вел дневник
    if entry is None:
        await message.answer("🤷 Вчера ты не вел дневник, поэтому задачи на сегодня нет. Напиши /evening, чтобы начать!")
        return
    
    # Если запись есть, достаем ответы
    answers = entry["answers"]
    
    # Третий ответ (индекс 2) — это задача на сегодня
    task = answers[2]
    
    # Отправляем пользователю
    await message.answer(
        f"☀️ Доброе утро!\n\n"
        f"Вот твоя главная задача на сегодня (из вчерашнего дневника):\n"
        f"🎯 {task}\n\n"
        f"Удачи! А вечером напиши /evening, чтобы подвести итоги."
    )