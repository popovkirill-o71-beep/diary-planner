# bot.py — главный файл бота
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.filters import Command

from config import BOT_TOKEN
from evening import router as evening_router
from morning import router as morning_router  # <-- ДОБАВИЛИ ЭТУ СТРОКУ

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Подключаем оба роутера
dp.include_router(evening_router)
dp.include_router(morning_router)  # <-- ДОБАВИЛИ ЭТУ СТРОКУ

@dp.message(Command("start"))
async def cmd_start(message):
    await message.answer(
        "Привет! Я бот для ведения дневника. 📓\n\n"
        "Вечером пиши /evening — я задам вопросы и сохраню задачу на завтра.\n"
        "Утром пиши /morning — я напомню, что ты себе запланировал."
    )

async def main():
    print("Бот запущен...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())