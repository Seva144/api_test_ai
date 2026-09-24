import logging
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class LoggingConfig:
    log_dir: Path = Path("logs")
    file_name: str = "test_run.log"

    fmt: str = "%(asctime)s [%(levelname)-8s] %(name)s:%(lineno)d — %(message)s"
    datefmt: str = "%Y-%m-%d %H:%M:%S"

    console_level: int = logging.INFO
    file_level: int = logging.DEBUG
    root_level: int = logging.DEBUG

    # мьютит логи httpx и httpcore осталяя только логи пользователя
    muted_loggers: list[str] = field(
        default_factory=lambda: ["httpx", "httpcore"]
    )


def build_logger(name: str, config: LoggingConfig) -> logging.Logger:
    """Создаёт логгер с FileHandler по cfg. Дублирование handlers исключено."""
    logger = logging.getLogger(name)
    logger.setLevel(config.root_level)
    logger.propagate = False

    if logger.handlers:
        return logger

    config.log_dir.mkdir(parents=True, exist_ok=True)
    formatter = logging.Formatter(config.fmt, datefmt=config.datefmt)

    handler = logging.FileHandler(
        config.log_dir / config.file_name,
        mode="w",
        encoding="utf-8",
    )
    handler.setLevel(config.file_level)
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    for muted_name in config.muted_loggers:
        logging.getLogger(muted_name).setLevel(logging.WARNING)

    return logger











