# storage.py — работа с файлом дневника (сохранение и чтение)
import json
from datetime import date
from pathlib import Path

# Путь к файлу, где храним все записи
DATA_FILE = Path("diary.json")


def load_diary():
    """Загрузить весь дневник из файла. Если файла нет — вернуть пустой словарь."""
    if DATA_FILE.exists():
        # Читаем файл и превращаем JSON-текст обратно в словарь Python
        text = DATA_FILE.read_text(encoding="utf-8")
        return json.loads(text)
    return {}


def save_entry(user_id: int, answers: list[str]):
    """Сохранить одну запись дневника в файл.
    
    user_id — ID пользователя (чтобы поддерживать нескольких пользователей)
    answers — список из 3 ответов на вопросы
    """
    diary = load_diary()  # загружаем то, что уже есть
    
    # Ключ записи: "user_id_дата" (например, "12345_2026-09-29")
    # Это нужно, чтобы один пользователь не перезаписал запись другого дня
    today = date.today().isoformat()  # "2026-09-29"
    key = f"{user_id}_{today}"
    
    # Записываем в словарь
    diary[key] = {
        "date": today,
        "answers": answers
    }
    
    # Сохраняем весь словарь обратно в файл
    # ensure_ascii=False — чтобы русские буквы не превращались в \u0441\u0442...
    # indent=2 — для красивого форматирования (можно читать глазами)
    DATA_FILE.write_text(
        json.dumps(diary, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )


def get_yesterday_entry(user_id: int) -> dict | None:
    """Получить вчерашнюю запись пользователя. Вернёт None, если её нет."""
    diary = load_diary()
    from datetime import timedelta
    yesterday = (date.today() - timedelta(days=1)).isoformat()
    key = f"{user_id}_{yesterday}"
    return diary.get(key)  # вернёт запись или None, если ключа нет