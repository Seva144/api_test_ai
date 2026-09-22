import logging
import os

from dotenv import load_dotenv

from utilities.logger_utils import logger


def pytest_configure(config):
    # устанавливаем текущую диреткорию на корень проекта (это позволит прописывать относительные пути к файлам)
    path_dir = os.path.abspath(__file__)
    os.chdir(os.path.dirname(path_dir))

    # загружаем переменные-параметры из файла /.env
    load_dotenv(dotenv_path=".env")

    # задаем параметры логгера
    path = "logs/"
    os.makedirs(os.path.dirname(path), exist_ok=True)
    file_handler = logging.FileHandler(path + "/info.log", "w")
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(logging.Formatter("%(lineno)d: %(asctime)s %(message)s"))

    # cоздаем кастомный логгер
    custom_logger = logging.getLogger("custom_logger")
    custom_logger.setLevel(logging.INFO)
    custom_logger.addHandler(file_handler)


def pytest_runtest_setup(item):
    logger.info(f"{item.name}:")
