from uuid import UUID

from assertions.assertion_base import assert_stream_result, \
    assert_messages_contains_id, assert_check_content_message
from models.request.default_fields import MESSAGE_ATK_BY_PBO
from tests.base_test import TestBase


class TestAiGenAtkByPbo(TestBase):
    LOG_FILE = "test-ai-gen-atk-by-pbo.log"

    def test_ai_gen_atk_by_pbo(self):
        # 1. создание диалога
        self.logger.info(f"ШAГ 1: Создание диалога пользователя")
        create_conversation_response = self.create_conversation()
        # переменные
        id_conversation: UUID = create_conversation_response.id
        id_user: str = create_conversation_response.user_id
        try:
            # 2. Отправка первого сообщения
            self.logger.info(f"ШАГ 2: Отправка первого сообщения")
            message_request_one = "Напиши АТК по авторизации"
            message_response_one = self.send_message_locally(MESSAGE_ATK_BY_PBO, id_conversation, message_request_one)
            assert_stream_result(message_response_one, id_conversation)
            id_message_one = message_response_one.message_id

            # 3. Получить сообщения диалога
            self.logger.info(f"ШАГ 3: Получение сообщений диалога")
            messages = self.get_messages(id_conversation, id_user)
            message_first = assert_messages_contains_id(messages, id_message_one)

            word_one = "WebOperation"
            word_two = "OperationType"

            assert_check_content_message(message_first.content, word_one, word_two)

            #4. Отправить сообщенеи для изменения
            self.logger.info(f"ШАГ 4: Отправка второго сообщения")
            message_request_two = "Напиши АТК по авторизации с переходом на главную страницу"
            message_response_two = self.send_message_locally(MESSAGE_ATK_BY_PBO, id_conversation, message_request_two)
            assert_stream_result(message_response_two, id_conversation)
            id_message_two = message_response_two.message_id

            #5. Получить сообщения диалога
            messages = self.get_messages(id_conversation, id_user)
            message_second = assert_messages_contains_id(messages, id_message_two)
            assert_check_content_message(message_second.content, word_one, word_two)

        finally:
            # 6. удаление диалога
            self.logger.info(f"ШАГ 6: Удаление диалога с id - {id_conversation}")
            self.delete_conversation(id_conversation, id_user)
