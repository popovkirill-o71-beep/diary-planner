# weekly.py — отчёт за последние 7 дней
from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from storage import generate_weekly_report

router = Router()


@router.message(Command("weekly"))
async def cmd_weekly(message: Message):
    """Сгенерировать отчёт за последние 7 дней."""
    report = generate_weekly_report(days=7)
    await message.answer(report)