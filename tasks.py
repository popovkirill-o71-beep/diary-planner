# tasks.py — команды для работы с задачами в течение дня
from datetime import date
from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from storage import (
    add_task, mark_task_done, delete_task,
    add_note, get_tasks_for_day, get_entry
)

router = Router()


# ========== СТАРЫЕ КОМАНДЫ ==========

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


# ========== НОВЫЕ КОМАНДЫ ==========

@router.message(Command("today"))
async def cmd_today(message: Message):
    """Показать задачи на сегодня со статусами."""
    today = date.today()
    tasks = get_tasks_for_day(today)
    entry = get_entry(today)
    done = entry.get("tasks_done", []) if entry else []

    if not tasks:
        await message.answer("📋 На сегодня задач нет. Добавь через /add <задача>")
        return

    lines = ["📋 Задачи на сегодня:"]
    for i, t in enumerate(tasks, 1):
        status = "✅" if t in done else "⬜"
        lines.append(f"  {status} {i}. {t}")

    # Показываем прогресс
    done_count = len(done)
    total = len(tasks)
    lines.append(f"\nПрогресс: {done_count}/{total}")

    await message.answer("\n".join(lines))


@router.message(Command("delete"))
async def cmd_delete(message: Message):
    """Удалить задачу по номеру. Пример: /delete 2"""
    args = message.text.replace("/delete", "", 1).strip()

    if not args:
        await message.answer("❌ Напиши номер задачи. Пример: /delete 2")
        return

    try:
        task_number = int(args)
    except ValueError:
        await message.answer(f"❌ '{args}' — это не число. Напиши номер задачи.")
        return

    today = date.today()
    success, msg = delete_task(today, task_number)

    if success:
        # Показываем обновлённый список
        tasks = get_tasks_for_day(today)
        if tasks:
            task_list = "\n".join([f"  {i}. {t}" for i, t in enumerate(tasks, 1)])
            await message.answer(f"{msg}\n\nОсталось:\n{task_list}")
        else:
            await message.answer(f"{msg}\n\nСписок задач пуст.")
    else:
        await message.answer(f"❌ {msg}")


@router.message(Command("help"))
async def cmd_help(message: Message):
    """Список всех команд бота."""
    text = (
        "📖 Команды бота:\n\n"
        "/start — приветствие\n"
        "/evening — вечерний опрос (итоги дня + планы на завтра)\n"
        "/morning — утренняя сводка с задачами и цитатой\n"
        "/today — задачи на сегодня со статусами\n"
        "/add <задача> — добавить задачу\n"
        "/done <номер> — отметить задачу выполненной\n"
        "/delete <номер> — удалить задачу\n"
        "/note <текст> — добавить заметку\n"
        "/weekly — отчёт за последние 7 дней\n"
        "/help — эта справка"
    )
    await message.answer(text)