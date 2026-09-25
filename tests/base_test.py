import logging
from http import HTTPStatus
from pathlib import Path
from typing import Any
from uuid import UUID

import pytest

from api.client import ApiClient
from api.conversation_api import post_conversation, delete_conversation
from assertions.assertion_base import assert_status_code, assert_schema
from config.logging_config import build_logger, LoggingConfig
from models.response.conversation_dto import ConversationDTO
from utilities.json_utils import read_json_conversation_request


class TestBase:
    LOG_DIR: Path = Path("logs")
    LOG_FILE: str = "default_test_run.log"
    LOGGING_CONFIG: LoggingConfig | None = None

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

    def create_conversation(self,  **overrides: Any) -> ConversationDTO:
        self.logger.info(f"Создание нового диалога диалога")
        post_obj = read_json_conversation_request("post_conversation_default", overrides)
        self.logger.info(f"payload: {post_obj}")
        response = post_conversation(self.client, json=post_obj)
        assert_status_code(response, HTTPStatus.OK)
        assert_schema(response, ConversationDTO)
        dto = ConversationDTO.model_validate(response.json())
        self.logger.info(f"Создан диалог id={dto.id}")
        return dto

    def delete_conversation(self, id_conversation: UUID, user: str) -> ConversationDTO:
        self.logger.info(f"Удаляем диалог {id_conversation} пользователя c id {user} ")
        response = delete_conversation(self.client, id_conversation)
        self.logger.info(response)
        assert_status_code(response, HTTPStatus.OK)
        assert_schema(response, ConversationDTO)
        self.logger.info(f"Диалог с id - {id_conversation} удален")
        dto = ConversationDTO.model_validate(response.json())
        return dto












