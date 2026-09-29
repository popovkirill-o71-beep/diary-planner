# bot.py — главный файл бота
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.filters import Command

from config import BOT_TOKEN
from evening import router as evening_router  # Импортируем роутер из evening.py

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Подключаем роутер с вечерним опросом к диспетчеру
dp.include_router(evening_router)

@dp.message(Command("start"))
async def cmd_start(message):
    await message.answer("Привет! Я бот для ведения дневника. \nНапиши /evening, чтобы начать.")

async def main():
    print("Бот запущен...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())