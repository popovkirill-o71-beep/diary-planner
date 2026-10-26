# tasks.py — команды для работы с задачами в течение дня
from datetime import date
from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from storage import add_task, mark_task_done, add_note, get_tasks_for_day

router = Router()


@router.message(Command("add"))
async def cmd_add(message: Message):
    """Добавить задачу на сегодня. Пример: /add Позвонить маме"""
    task_text = message.text.replace("/add", "", 1).strip()

    if not task_text:
        await message.answer("❌ Напиши задачу после команды. Пример: /add Позвонить маме")
        return

    today = date.today()
    success = add_task(today, task_text)

    if success:
        tasks = get_tasks_for_day(today)
        task_list = "\n".join([f"  {i}. {t}" for i, t in enumerate(tasks, 1)])
        await message.answer(f"✅ Добавил задачу:\n\n{task_list}")
    else:
        await message.answer("❌ Не удалось сохранить задачу. Попробуй ещё раз.")


@router.message(Command("done"))
async def cmd_done(message: Message):
    """Отметить задачу выполненной. Пример: /done 1"""
    args = message.text.replace("/done", "", 1).strip()

    if not args:
        await message.answer("❌ Напиши номер задачи. Пример: /done 1")
        return

    try:
        task_number = int(args)
    except ValueError:
        await message.answer(f"❌ '{args}' — это не число. Напиши номер задачи.")
        return

    today = date.today()
    success, msg = mark_task_done(today, task_number)

    if success:
        await message.answer(msg)
    else:
        await message.answer(f"❌ {msg}")


@router.message(Command("note"))
async def cmd_note(message: Message):
    """Добавить заметку. Пример: /note Хороший день был"""
    note_text = message.text.replace("/note", "", 1).strip()

    if not note_text:
        await message.answer("❌ Напиши заметку после команды. Пример: /note Хороший день был")
        return

    today = date.today()
    success = add_note(today, note_text)

    if success:
        await message.answer(f"💭 Заметка сохранена:\n\n{note_text}")
    else:
        await message.answer("❌ Не удалось сохранить заметку.")