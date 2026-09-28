import logging
import sys
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class LoggingConfig:
    log_dir: Path = Path("logs")
    file_name: str = "test_run.log"

    fmt: str = "%(asctime)s - || %(name)s:%(lineno)d || %(message)s"
    datefmt: str = "%Y-%m-%d %H:%M:%S"

    console_level: int = logging.INFO
    file_level: int = logging.DEBUG
    root_level: int = logging.DEBUG

    # мьютит логи httpx и httpcore осталяя только логи пользователя
    muted_loggers: list[str] = field(
        default_factory=lambda: ["httpx", "httpcore"]
    )


def build_logger(name: str, config: LoggingConfig) -> logging.Logger:
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

    return logger


def setup_root_logging(cfg: LoggingConfig) -> None:
    """Настраивает root-логгер: консоль + общий файл."""
    root_logger = logging.getLogger()
    root_logger.setLevel(cfg.root_level)

    if root_logger.handlers:
        root_logger.handlers.clear()

    formatter = logging.Formatter(cfg.fmt, datefmt=cfg.datefmt)

    console = logging.StreamHandler(sys.stdout)
    console.setLevel(cfg.console_level)
    console.setFormatter(formatter)
    root_logger.addHandler(console)

    cfg.log_dir.mkdir(parents=True, exist_ok=True)
    file_all = logging.FileHandler(
        cfg.log_dir / cfg.file_name, mode="w", encoding="utf-8"
    )
    file_all.setLevel(cfg.file_level)
    file_all.setFormatter(formatter)
    root_logger.addHandler(file_all)

    for muted in cfg.muted_loggers:
        logging.getLogger(muted).setLevel(logging.WARNING)










