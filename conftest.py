import logging
import os
import sys
from pathlib import Path

from dotenv import load_dotenv


def pytest_configure(config):
    # устанавливаем текущую диреткорию на корень проекта (это позволит прописывать относительные пути к файлам)
    path_dir = os.path.abspath(__file__)
    os.chdir(os.path.dirname(path_dir))

    # загружаем переменные-параметры из файла /.env
    load_dotenv(dotenv_path=".env")

    # задаем путь диреткории логгера
    log_dir = "logs/"
    os.makedirs(os.path.dirname(log_dir), exist_ok=True)

    # 4. Настроить root-логгер
    _setup_logging(log_dir)


def _setup_logging(log_dir: Path):
    """Настраивает root-логгер: консоль + файл, единый формат."""
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)

    # формат логгера
    fmt = "%(asctime)s [%(levelname)-8s] %(name)s:%(lineno)d — %(message)s"
    formatter = logging.Formatter(fmt, datefmt="%Y-%m-%d %H:%M:%S")

    # --- консоль ---
    console = logging.StreamHandler(sys.stdout)
    console.setLevel(logging.INFO)
    console.setFormatter(formatter)
    root_logger.addHandler(console)

    # --- файл ---
    file_all = logging.FileHandler(log_dir + "test_run.log", mode="w", encoding="utf-8")
    file_all.setLevel(logging.DEBUG)
    file_all.setFormatter(formatter)
    root_logger.addHandler(file_all)

    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("httpcore").setLevel(logging.WARNING)


def pytest_runtest_setup(item):
    logging.getLogger("pytest").info(f"▶ START  {item.nodeid}")


def pytest_runtest_makereport(item, call):
    if call.when == "call":
        if call.excinfo is None:
            logging.getLogger("pytest").info(f"✔ PASSED {item.nodeid}")
        else:
            logging.getLogger("pytest").error(
                f"✘ FAILED {item.nodeid} — {call.excinfo.type.__name__}: {call.excinfo.value}"
            )


def pytest_runtest_teardown(item):
    logging.getLogger("pytest").debug(f"◆ END    {item.nodeid}")