# evening.py — логика вечернего опроса через FSM
from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command

from states import DiaryStates
from questions import QUESTIONS
from storage import get_entry, save_entry, date

router = Router()


@router.message(Command("evening"))
async def start_evening(message: Message, state: FSMContext):
    """Запуск вечернего опроса."""
    # Сохраняем дату в состоянии, чтобы потом знать, куда писать
    today = date.today()
    await state.update_data(day=today)
    await state.set_state(DiaryStates.q1)
    await message.answer(QUESTIONS[0])


@router.message(DiaryStates.q1)
async def process_q1(message: Message, state: FSMContext):
    """Ответ на первый вопрос: что сделал сегодня."""
    await state.update_data(done_today=message.text)
    await state.set_state(DiaryStates.q2)
    await message.answer(QUESTIONS[1])


@router.message(DiaryStates.q2)
async def process_q2(message: Message, state: FSMContext):
    """Ответ на второй вопрос: сложности."""
    await state.update_data(difficulties=message.text)
    await state.set_state(DiaryStates.q3)
    await message.answer(QUESTIONS[2])


@router.message(DiaryStates.q3)
async def process_q3(message: Message, state: FSMContext):
    """Ответ на третий вопрос: планы на завтра. Сохраняем всё в файл."""
    data = await state.get_data()
    day: date = data.get("day")
    
    # Формируем запись в новом формате
    entry = {
        "tasks_planned": [],          # задачи на сегодня (из утреннего /morning)
        "tasks_done": _parse_list(data.get("done_today", "")),
        "difficulties": data.get("difficulties", ""),
        "thoughts": "",
        "plans_for_tomorrow": _parse_list(message.text)  # то, что написал сейчас
    }
    
    # Если уже была запись за сегодня — не теряем старые данные
    existing = get_entry(day)
    if existing:
        entry["tasks_planned"] = existing.get("tasks_planned", [])
        entry["thoughts"] = existing.get("thoughts", "")
    
    save_entry(day, entry)
    
    await message.answer(
        f"✅ Сохранил итоги дня!\n\n"
        f"Сделал: {data.get('done_today', '')}\n"
        f"Сложности: {data.get('difficulties', '')}\n"
        f"Планы на завтра: {message.text}\n\n"
        f"Хорошего вечера! 🌙"
    )
    await state.clear()


def _parse_list(text: str) -> list[str]:
    """Разобрать текст в список задач.
    
    Принимает: "Задача 1, задача 2" или "1. Задача 1\n2. Задача 2"
    Возвращает: ["Задача 1", "Задача 2"]
    """
    if not text or not text.strip():
        return []
    
    # Разбиваем по запятым, переносам строк или точкам с цифрами
    parts = text.replace("\n", ",").split(",")
    result = []
    for part in parts:
        cleaned = part.strip()
        # Убираем нумерацию в начале ("1. ", "2) " и т.п.)
        if cleaned and cleaned[0].isdigit() and "." in cleaned[:3]:
            cleaned = cleaned.split(".", 1)[1].strip()
        if cleaned:
            result.append(cleaned)
    return result