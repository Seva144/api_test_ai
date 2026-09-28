import json
from typing import Any


def pretty_json(data: Any, indent: int = 2) -> str:
    """
    Приводит данные к красиво отформатированной JSON-строке.

    Понимает:
      - dict / list — сериализует через json.dumps;
      - bytes — декодирует utf-8 и парсит как JSON;
      - str — парсит как JSON, если валидный, иначе возвращает как есть;
      - прочее — возвращает str(data).

    Никогда не падает: если данные не JSON, вернёт их как строку.
    """
    if data is None:
        return ""

    # bytes → str
    if isinstance(data, (bytes, bytearray)):
        try:
            data = data.decode("utf-8")
        except UnicodeDecodeError:
            return f"<binary {len(data)} bytes>"

    # str → попробовать распарсить
    if isinstance(data, str):
        stripped = data.strip()
        if not stripped:
            return ""
        try:
            parsed = json.loads(stripped)
            return json.dumps(parsed, ensure_ascii=False, indent=indent)
        except (json.JSONDecodeError, ValueError):
            return data

    # dict / list → сериализовать
    try:
        return json.dumps(data, ensure_ascii=False, indent=indent)
    except (TypeError, ValueError):
        return str(data)