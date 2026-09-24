import logging
from pathlib import Path

import pytest

from api.client import ApiClient
from config.logging_config import build_logger, LoggingConfig


class TestBase:
    LOG_DIR: Path = Path("logs")
    LOG_FILE: str = "default_test_run.log"
    LOGGING_CONFIG: LoggingConfig | None

    logger: logging.Logger = None
    client: ApiClient = None

    @pytest.fixture(scope="class")
    def client(self) -> ApiClient:
        return type(self).client

    @classmethod
    def get_logger_config(cls) -> LoggingConfig:
        if cls.LOGGING_CONFIG is not None:
            return cls.LOGGING_CONFIG
        return LoggingConfig(
            log_dir=cls.LOG_DIR,
            file_name=cls.LOG_FILE,
        )

    @classmethod
    def setup_class(cls) -> None:
        config_log = cls.get_logger_config()
        cls.logger = build_logger(cls.__name__, config_log)

        cls.client = ApiClient(logger=cls.logger)
        cls.logger.info("ApiClient инициализирован")

        cls.logger.info("=" * 60)
        cls.logger.info(f"START {cls.__name__}  (log: {config_log.log_dir / config_log.file_name})")
        cls.logger.info("=" * 60)

    @classmethod
    def teardown_class(cls) -> None:
        cls.logger.info("=" * 60)
        cls.logger.info(f"END {cls.__name__}")
        cls.logger.info("=" * 60)

        # закрыть HTTP-соединения
        if cls.client is not None:
            cls.client.close()
