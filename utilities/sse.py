from typing import Iterator


def iter_sse(response) -> Iterator[tuple[str, str]]:
    """
    Парсит SSE из httpx.Response через iter_lines().
    Yield-ит (event, data) для каждого события.

    SSE-формат:
        event: <тип>        — опционально
        data: <строка>      — может быть несколько подряд
                            — пустая строка = конец события
    """
    event: str | None = None
    data_lines: list[str] = []

    for raw in response.iter_lines():
        line = raw.rstrip("\r\n")

        # пустая строка = конец события
        if line == "":
            if data_lines:
                yield event or "message", "\n".join(data_lines)
            event = None
            data_lines = []
            continue

        # строки-комментарии начинаются с ":"
        if line.startswith(":"):
            continue

        # поле: значение
        field, sep, value = line.partition(":")
        if sep and value.startswith(" "):
            value = value[1:]      # SSE: один ведущий пробел отбрасывается

        if field == "event":
            event = value
        elif field == "data":
            data_lines.append(value)
        # id/retry нам не нужны