# storage.py — работа с файлом diary.json
# Все функции принимают данные и возвращают результат, не печатают напрямую

import json
import logging
from datetime import date, timedelta
from pathlib import Path

# Настройка логирования (ошибки не проглатываем молча!)
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

DATA_FILE = Path("diary.json")


def load_diary() -> dict:
    """Загрузить весь дневник из файла.
    
    Если файла нет — вернуть пустой словарь (первый запуск).
    Если файл повреждён — залогировать ошибку и вернуть пустой словарь.
    """
    if not DATA_FILE.exists():
        logger.info("Файл diary.json не найден, создаём новый")
        return {}
    
    try:
        text = DATA_FILE.read_text(encoding="utf-8")
        return json.loads(text)
    except json.JSONDecodeError as e:
        # Краевой случай: файл повреждён
        logger.error(f"Файл diary.json повреждён: {e}")
        return {}
    except OSError as e:
        # Краевой случай: нет прав на чтение
        logger.error(f"Не удалось прочитать diary.json: {e}")
        return {}


def save_diary(diary: dict) -> bool:
    """Сохранить весь дневник в файл. Возвращает True при успехе."""
    try:
        DATA_FILE.write_text(
            json.dumps(diary, ensure_ascii=False, indent=2),
            encoding="utf-8"
        )
        return True
    except OSError as e:
        logger.error(f"Не удалось записать diary.json: {e}")
        return False


def get_entry(day: date) -> dict | None:
    """Получить запись за конкретный день. Вернёт None, если записи нет."""
    diary = load_diary()
    key = day.isoformat()  # "2026-10-26"
    return diary.get(key)


def save_entry(day: date, entry: dict) -> bool:
    """Сохранить запись за день. Перезаписывает, если уже была."""
    diary = load_diary()
    key = day.isoformat()
    diary[key] = entry
    return save_diary(diary)


def get_tasks_for_day(day: date) -> list[str]:
    """Получить список запланированных задач на день."""
    entry = get_entry(day)
    if entry is None:
        return []
    return entry.get("tasks_planned", [])


def mark_task_done(day: date, task_index: int) -> tuple[bool, str]:
    """Отметить задачу выполненной по индексу (с 1).
    
    Возвращает (успех: bool, сообщение: str).
    """
    entry = get_entry(day)
    if entry is None:
        return False, "На этот день ещё нет записей"
    
    tasks = entry.get("tasks_planned", [])
    done = entry.get("tasks_done", [])
    
    # Проверка: индекс в пределах списка
    if task_index < 1 or task_index > len(tasks):
        return False, f"Нет задачи с номером {task_index}. Всего задач: {len(tasks)}"
    
    task = tasks[task_index - 1]
    
    # Краевой случай: задача уже выполнена
    if task in done:
        return False, f"Задача '{task}' уже отмечена выполненной"
    
    done.append(task)
    entry["tasks_done"] = done
    return save_entry(day, entry), f"✅ Отметил выполненной: {task}"


def add_task(day: date, task: str) -> bool:
    """Добавить задачу на день."""
    entry = get_entry(day) or {
        "tasks_planned": [],
        "tasks_done": [],
        "difficulties": "",
        "thoughts": "",
        "plans_for_tomorrow": []
    }
    entry["tasks_planned"].append(task)
    return save_entry(day, entry)


def add_note(day: date, note: str) -> bool:
    """Добавить заметку/мысль на день."""
    entry = get_entry(day) or {
        "tasks_planned": [],
        "tasks_done": [],
        "difficulties": "",
        "thoughts": "",
        "plans_for_tomorrow": []
    }
    # Добавляем через разделитель, если уже есть текст
    if entry["thoughts"]:
        entry["thoughts"] += "\n" + note
    else:
        entry["thoughts"] = note
    return save_entry(day, entry)


def get_entries_for_period(start: date, end: date) -> list[tuple[str, dict]]:
    """Получить все записи за период [start, end].
    
    Возвращает список кортежей (дата_строка, запись).
    """
    diary = load_diary()
    result = []
    current = start
    while current <= end:
        key = current.isoformat()
        if key in diary:
            result.append((key, diary[key]))
        current += timedelta(days=1)
    return result


def generate_weekly_report(days: int = 7) -> str:
    """Сгенерировать текстовый отчёт за последние N дней."""
    today = date.today()
    start = today - timedelta(days=days - 1)
    entries = get_entries_for_period(start, today)
    
    if not entries:
        return " За последние 7 дней записей нет. Начни вести дневник командой /evening!"
    
    total_planned = 0
    total_done = 0
    difficulties = []
    thoughts = []
    
    for day_str, entry in entries:
        tasks = entry.get("tasks_planned", [])
        done = entry.get("tasks_done", [])
        total_planned += len(tasks)
        total_done += len(done)
        
        diff = entry.get("difficulties", "")
        if diff:
            difficulties.append(f"• {day_str}: {diff}")
        
        thought = entry.get("thoughts", "")
        if thought:
            thoughts.append(f"• {day_str}: {thought}")
    
    # Считаем процент выполнения
    if total_planned > 0:
        percent = round(total_done / total_planned * 100)
    else:
        percent = 0
    
    report = f"📊 Отчёт за последние {days} дней\n\n"
    report += f" Запланировано задач: {total_planned}\n"
    report += f"✅ Выполнено: {total_done} ({percent}%)\n\n"
    
    if difficulties:
        report += "🌧️ Сложности:\n" + "\n".join(difficulties) + "\n\n"
    
    if thoughts:
        report += "💭 Мысли:\n" + "\n".join(thoughts)
    
    return report