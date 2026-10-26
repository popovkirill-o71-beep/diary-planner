# scheduler.py — планировщик автоматических напоминаний
import logging
from datetime import date, timedelta
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from storage import get_entry, get_tasks_for_day

logger = logging.getLogger(__name__)

# Создаём планировщик
scheduler = AsyncIOScheduler()


async def send_evening_reminder(bot, chat_id: int):
    """Вечернее напоминание в 21:30."""
    try:
        text = (
            "🌙 Добрый вечер! Пора подвести итоги дня.\n\n"
            "Напиши /evening — я задам 3 вопроса и сохраню ответы.\n"
            "Или /today — посмотреть задачи на сегодня."
        )
        await bot.send_message(chat_id, text)
        logger.info("Вечернее напоминание отправлено")
    except Exception as e:
        logger.error(f"Не удалось отправить вечернее напоминание: {e}")


async def send_morning_reminder(bot, chat_id: int):
    """Утреннее напоминание в 8:00 с задачами на день."""
    try:
        today = date.today()
        tasks = get_tasks_for_day(today)

        # Если задач нет — берём планы на сегодня из вчерашней записи
        if not tasks:
            yesterday = today - timedelta(days=1)
            yesterday_entry = get_entry(yesterday)
            if yesterday_entry:
                tasks = yesterday_entry.get("plans_for_tomorrow", [])

        # Формируем сообщение
        if tasks:
            lines = ["☀️ Доброе утро! Вот твои задачи на сегодня:\n"]
            for i, task in enumerate(tasks, 1):
                lines.append(f"  {i}. {task}")
            lines.append("\nНапиши /done <номер>, когда выполнишь.")
            text = "\n".join(lines)
        else:
            text = (
                "☀️ Доброе утро!\n\n"
                "На сегодня задач пока нет. Добавь через /add <задача>\n"
                "Или напиши /morning — я покажу вчерашний итог."
            )

        await bot.send_message(chat_id, text)
        logger.info("Утреннее напоминание отправлено")
    except Exception as e:
        logger.error(f"Не удалось отправить утреннее напоминание: {e}")


def setup_scheduler(bot, chat_id: int):
    """Настроить расписание напоминаний: 8:00 утром и 21:30 вечером."""
    # Утреннее напоминание в 8:00
    scheduler.add_job(
        send_morning_reminder,
        "cron",
        hour=8,
        minute=0,
        args=[bot, chat_id],
        id="morning_reminder"
    )

    # Вечернее напоминание в 21:30
    scheduler.add_job(
        send_evening_reminder,
        "cron",
        hour=21,
        minute=30,
        args=[bot, chat_id],
        id="evening_reminder"
    )

    scheduler.start()
    logger.info("Планировщик запущен: напоминания в 8:00 и 21:30")

    return scheduler


def shutdown_scheduler():
    """Остановить планировщик при завершении бота."""
    if scheduler.running:
        scheduler.shutdown()
        logger.info("Планировщик остановлен")