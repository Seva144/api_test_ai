from uuid import UUID

from assertions.assertion_base import assert_test_cases_agent_generated, assert_messages_contains_id
from models.request.default_fields import MESSAGE_TK_SIMPLE
from tests.base_test import TestBase


class TestAiSendToTkControl(TestBase):
    LOG_FILE = "ai-test-send-to-tk-control.log"

    def test_ai_send_to_tk_control(self):
        # 1. создание диалога
        self.logger.info(f"ШAГ 1: Создание диалога пользователя")
        create_conversation_response = self.create_conversation()
        # переменные
        id_conversation: UUID = create_conversation_response.id
        id_user: str = create_conversation_response.user_id

        message = "Сгенерируй тест-кейс по авторизации"

        try:
            # 2. Отправка сообщения
            self.logger.info(f"ШAГ 2: отправка сообщения на получение ТК")
            message_send = self.send_message(MESSAGE_TK_SIMPLE, id_conversation, message)
            assert_test_cases_agent_generated(message_send)
            id_message = message_send.message_id

            # 3. Получение сообщений
            self.logger.info(f"ШАГ 3: Получение сообщений диалога")
            messages = self.get_messages(id_conversation, id_user)
            assistant_msg = assert_messages_contains_id(messages, id_message)

            #  4. Сохранение ТК
            self.logger.info(f"ШАГ 4: Сохранение ТК")
            testing_type = "4a494142-2c18-4efd-9ec8-b92ca7d7e9d8"
            tks = self.tks_create(id_conversation, id_user, id_message, assistant_msg.content, testing_type)
            self.logger.info(f"Сгенерировано {len(tks)} TK")


        finally:
            # 6. удаление диалога
            self.delete_conversation(id_conversation, id_user)


