# bot.py — главный файл бота для ведения дневника
# Этот файл запускает бота и обрабатывает команду /start

import asyncio  # библиотека для асинхронной работы (нужна для aiogram)
from aiogram import Bot, Dispatcher  # Bot — сам бот, Dispatcher — обрабатывает сообщения
from aiogram.filters import Command  # Command — фильтр для команд вроде /start

# Создаём бота с токеном из config.py
from config import BOT_TOKEN
bot = Bot(token=BOT_TOKEN)

# Создаём диспетчер — он решает, какой функции передать сообщение
dp = Dispatcher()

# Эта функция срабатывает, когда пользователь пишет /start
@dp.message(Command("start"))  # декоратор: "вызови эту функцию на команду /start"
async def cmd_start(message):  # message — объект с информацией о сообщении
    """Обработчик команды /start. Отвечает приветствием."""
    await message.answer("Привет! Я бот для ведения дневника. 📓")

# Главная функция — запускает бота
async def main():
    """Запускает бота в режиме polling (он сам проверяет новые сообщения)."""
    print("Бот запущен...")
    await dp.start_polling(bot)  # бот начинает слушать сообщения

# Точка входа — отсюда начинается выполнение программы
if __name__ == "__main__":
    asyncio.run(main())  # запускаем асинхронную функцию main()