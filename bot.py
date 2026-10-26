# bot.py — главный файл бота с планировщиком напоминаний
import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.filters import Command

from config import BOT_TOKEN, MY_CHAT_ID
from evening import router as evening_router
from morning import router as morning_router
from tasks import router as tasks_router
from weekly import router as weekly_router
from scheduler import setup_scheduler, shutdown_scheduler

# Настройка логирования
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Подключаем все роутеры
dp.include_router(evening_router)
dp.include_router(morning_router)
dp.include_router(tasks_router)
dp.include_router(weekly_router)


@dp.message(Command("start"))
async def cmd_start(message):
    await message.answer(
        "Привет! Я бот для ведения дневника. 📓\n\n"
        "Напиши /help — список всех команд."
    )


async def main():
    print("Бот запущен...")
    
    # Запускаем планировщик напоминаний
    scheduler = setup_scheduler(bot, MY_CHAT_ID)
    
    try:
        await dp.start_polling(bot)
    finally:
        # Останавливаем планировщик при завершении бота
        shutdown_scheduler()


if __name__ == "__main__":
    asyncio.run(main())