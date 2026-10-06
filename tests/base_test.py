import logging
from http import HTTPStatus
from pathlib import Path
from typing import Any
from uuid import UUID

import pytest

from api.client import ApiClient
from api.ai_test_api import post_conversation, delete_conversation, stream_message, get_messages, post_atk, delete_atk, \
    post_tk, delete_tk, upload_file
from assertions.assertion_base import assert_status_code, assert_schema, assert_schema_list, assert_file_uploaded
from config.logging_config import build_logger, LoggingConfig
from models.request.default_fields import *
from models.response.atk_dto import AtkDTO
from models.response.conversation_dto import ConversationDTO
from models.response.file_dto import FileDTO
from models.response.message_chunk_dto import MessageChunkDTO, MessageStreamResult
from models.response.message_dto import MessageDTO
from models.response.tk_dto import TkDTO
from utilities.json_utils import create_request
from utilities.log_utils import pretty_json
from utilities.sse import iter_sse


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

    def create_conversation(self) -> ConversationDTO:
        self.logger.info(f"Создание нового диалога диалога")

        request = create_request(DEFAULT_CONVERSATION, "post_conversation")
        self.logger.info(f"payload: {request}")

        response = post_conversation(self.client, json=request)

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

    def _log_stream_result(self, result: MessageStreamResult, finished: bool) -> None:
        sep = "=" * 60

        self.logger.info(sep)
        self.logger.info("РЕЗУЛЬТАТ SSE-СТРИМА")
        self.logger.info(sep)
        self.logger.info(f"conversationId: {result.conversation_id}")
        self.logger.info(f"messageId:      {result.message_id}")
        self.logger.info(f"событий всего:  {result.event_count}")
        self.logger.info(f"чанков:         {len(result.chunks)}")
        self.logger.info(f"последний seq:  {result.last_seq}")
        self.logger.info(f"finish получен: {finished}")
        self.logger.info(f"длина текста:   {len(result.full_text)} символов")
        self.logger.info(sep)
        self.logger.info("СОБРАННЫЙ ОТВЕТ МОДЕЛИ:")
        self.logger.info(sep)
        self.logger.info(result.full_text)
        self.logger.info(sep)

    def send_message_locally(self, config: Any, id_conversation: UUID, message: str) -> MessageStreamResult:
        self.logger.info(f"Отправляем сообщение {message!r} в диалог {id_conversation}")

        request = create_request(config, "send_message", message=message)

        chunks: list[MessageChunkDTO] = []
        event_count = 0
        finished = False

        with stream_message(self.client, id_conversation, json=request) as response:
            response.raise_for_status()
            for event, data in iter_sse(response):
                event_count += 1
                # print(f"event={event} data={data}")

                if event == "finish":
                    finished = True
                    break

                if not data:
                    continue

                chunk = MessageChunkDTO.model_validate_json(data)
                chunk.event_type = event
                chunks.append(chunk)

        if not chunks:
            raise AssertionError("SSE не вернул ни одного чанка")

        ordered = sorted(chunks, key=lambda c: c.seq)
        full_text = "".join(c.content for c in ordered)

        result = MessageStreamResult(
            conversation_id=ordered[0].conversation_id,
            message_id=ordered[0].message_id,
            chunks=ordered,
            full_text=full_text,
            event_count=event_count,
            finished=finished
        )

        self._log_stream_result(result, finished=finished)
        return result

    def send_message(self, config: Any, id_conversation: UUID, message: str) -> MessageStreamResult:
        """
            Отправляет сообщение агенту (useTestAgent=true).
            Агент возвращает ОДИН finish-чанк с metadata.testCases.
            """
        self.logger.info(f"→ SEND MESSAGE (agent) в диалог {id_conversation}: {message!r}")

        request = create_request(config, "send_message", message=message)
        chunks: list[MessageChunkDTO] = []
        event_count = 0

        with stream_message(self.client, id_conversation, json=request) as response:
            response.raise_for_status()

            for event, data in iter_sse(response):
                event_count += 1
                self.logger.debug("event=%s data=%s", event, pretty_json(data))

                if not data:
                    continue

                chunk = MessageChunkDTO.model_validate_json(data)
                chunk.event_type = event
                chunks.append(chunk)

        if not chunks:
            raise AssertionError("Агент не вернул ни одного сообщения")

        # у агента обычно один финальный чанк с testCases
        last = chunks[-1]
        full_text = last.content

        result = MessageStreamResult(
            conversation_id=last.conversation_id,
            message_id=last.message_id,
            chunks=chunks,
            full_text=full_text,
            event_count=event_count,
        )

        self._log_stream_result(result, finished=True)
        return result

    def get_messages(self, id_conversation: UUID, user_id: str) -> dict[UUID, MessageDTO]:
        self.logger.info(f"Получение всех сообщений пользователя {user_id} из диалога - {id_conversation}")
        response = get_messages(self.client, id_conversation)
        assert_status_code(response, HTTPStatus.OK)
        assert_schema_list(response, MessageDTO)
        messages = [MessageDTO.model_validate(item) for item in response.json()]
        self.logger.info(f"Получено {len(messages)} сообщений")
        by_id: dict[UUID, MessageDTO] = {m.id: m for m in messages}
        return by_id

    def atk_create(self, id_conversation: UUID,
                   user_id: str,
                   message: str,
                   project_id: UUID) -> AtkDTO:
        self.logger.info(f"Отправка АТК пользователя {user_id} id сообщения - {id_conversation}")
        request = create_request(ATK_MESSAGE_DEFAULT, "post_atk", message=message)
        response = post_atk(self.client, project_id, json=request)
        assert_status_code(response, HTTPStatus.OK)
        assert_schema(response, AtkDTO)
        dto = AtkDTO.model_validate(response.json())
        self.logger.info(f"Создан АТК с id={dto.id}")
        return dto

    def atk_delete(self, user_id: str, atk_id: UUID) -> AtkDTO:
        self.logger.info(f"Удаление АТК с id - {atk_id}, пользователем id - {user_id}")
        response = delete_atk(self.client, atk_id)
        assert_status_code(response, HTTPStatus.OK)
        assert_schema(response, AtkDTO)
        dto = AtkDTO.model_validate(response.json())
        self.logger.info(f"Удален АТК с id={dto.id}")
        return dto

    def tks_create(self, id_conversation: UUID,
                   user_id: str,
                   message_id: UUID,
                   message: str
                   ) -> list[TkDTO]:
        self.logger.info(f"Отправка ТК пользователя {user_id} id сообщения - {id_conversation}")
        request = create_request(TK_MESSAGE_DEFAULT, "post_tk", message=message)
        response = post_tk(self.client, message_id, json=request)
        assert_status_code(response, HTTPStatus.OK)
        assert_schema_list(response, TkDTO)
        tks = [TkDTO.model_validate(item) for item in response.json()]
        self.logger.info(f"Создано TK: {len(tks)}")
        return tks

    def tks_delete(self, user_id: str, tks: list[TkDTO]):
        self.logger.info(f"Удаление сгенерированных ТК пользователем - {user_id}")
        for tk in tks:
            self.logger.info(f" Удаляем TK id - {tk.id}")
            response = delete_tk(self.client, tk.id)
            assert_status_code(response, HTTPStatus.OK)
            assert_schema(response, TkDTO)
            self.logger.info(f" TK id - {tk.id} удалён")

    def upload_file(
            self,
            id_conversation: UUID,
            file_path: Path | str,
            *,
            filename: str | None = None,
            mime_type: str = "application/octet-stream",
            use_test_agent: bool = False,
    ) -> FileDTO:
        path = Path(file_path)
        self.logger.info(f"Загрузка файла {path.name} ({path.stat().st_size} байт) в диалог {id_conversation}")

        with path.open("rb") as f:
            file_tuple = (filename or path.name, f, mime_type)

            response = upload_file(
                self.client,
                id_conversation,
                file_tuple,
                use_test_agent=use_test_agent,
            )

        assert_status_code(response, HTTPStatus.OK)
        assert_schema(response, FileDTO)
        dto = FileDTO.model_validate(response.json())
        assert_file_uploaded(dto, id_conversation)

        self.logger.info(
            f"Файл загружен: id={dto.id}, filename={dto.filename}, "
            f"size={dto.file_size}, status={dto.processing_status}"
        )

        return dto
