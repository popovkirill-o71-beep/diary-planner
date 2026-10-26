# morning.py — утренняя сводка
from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from storage import get_entry, get_tasks_for_day, date
from datetime import timedelta

router = Router()

# Мотивирующие цитаты (выбираем случайно по дню)
QUOTES = [
    "«Начни делать то, что нужно. Потом делай то, что возможно. И вдруг ты делаешь невозможное.» — Франциск Ассизский",
    "«Маленькие шаги каждый день приводят к большим результатам.»",
    "«Лучшее время начать — сейчас.»",
    "«Дисциплина — это мост между целями и достижениями.»"
]


@router.message(Command("morning"))
async def show_morning(message: Message):
    """Показать планы на сегодня и вчерашний итог."""
    today = date.today()
    yesterday = today - timedelta(days=1)
    
    # Получаем задачи на сегодня (их мог поставить пользователь вчера вечером)
    tasks_today = get_tasks_for_day(today)
    
    # Если задач на сегодня нет — берём планы на завтра из вчерашней записи
    if not tasks_today:
        yesterday_entry = get_entry(yesterday)
        if yesterday_entry:
            tasks_today = yesterday_entry.get("plans_for_tomorrow", [])
    
    # Формируем сообщение
    lines = ["☀️ Доброе утро!\n"]
    
    if tasks_today:
        lines.append("📋 Твои задачи на сегодня:")
        for i, task in enumerate(tasks_today, 1):
            lines.append(f"  {i}. {task}")
    else:
        lines.append("📋 На сегодня задач пока нет. Добавь через /add <задача>")
    
    # Вчерашний итог
    yesterday_entry = get_entry(yesterday)
    if yesterday_entry:
        difficulties = yesterday_entry.get("difficulties", "")
        done = yesterday_entry.get("tasks_done", [])
        lines.append(f"\n📝 Вчера ты сделал: {len(done)} задач")
        if difficulties:
            lines.append(f"🌧️ Сложности: {difficulties}")
    
    # Цитата дня (выбираем по номеру дня в году, чтобы не повторялась)
    quote = QUOTES[today.timetuple().tm_yday % len(QUOTES)]
    lines.append(f"\n💬 {quote}")
    
    await message.answer("\n".join(lines))