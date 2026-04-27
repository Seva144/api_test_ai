import os
import logging
import pytest
from dotenv import load_dotenv

from src.api_client import ApiClient
from src.pom.api_object import ObjectsApi


# === Настройка логгера (выполняется один раз при старте pytest) ===
@pytest.fixture(scope="session", autouse=True)
def setup_logging():
    # Загружаем .env
    load_dotenv()

    # Создаем папку для логов
    log_path = "logs"
    os.makedirs(log_path, exist_ok=True)

    # Настраиваем файловый хендлер
    file_handler = logging.FileHandler(f"{log_path}/info.log", mode="a", encoding="utf-8")
    file_handler.setLevel(logging.INFO)
    formatter = logging.Formatter("%(lineno)d: %(asctime)s %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
    file_handler.setFormatter(formatter)

    # Настраиваем корневой логгер (чтобы ловить логи от httpx, api_client и т.д.)
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)

    # Очищаем старые хендлеры, чтобы не дублировать логи при повторных прогонах
    if root_logger.hasHandlers():
        root_logger.handlers.clear()

    root_logger.addHandler(file_handler)

    # Опционально: вывод в консоль
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)


# === Фикстуры для внедрения зависимостей ===
@pytest.fixture(scope="session")
def api_client():
    """Создает один клиент на всю сессию тестов"""
    return ApiClient()


@pytest.fixture
def objects_api(api_client):
    """Создает сервис для работы с объектами (функция на каждый тест)"""
    return ObjectsApi(api_client)


# === Хук: логирование начала каждого теста ===
def pytest_runtest_setup(item):
    logging.info(f"🧪 START TEST: {item.name}")