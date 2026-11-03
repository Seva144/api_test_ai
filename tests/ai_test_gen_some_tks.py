from uuid import UUID

from assertions.assertion_base import assert_test_cases_agent_generated, assert_messages_contains_id
from models.request.default_fields import MESSAGE_TK_SIMPLE
from tests.base_test import TestBase


class TestAiGenSomeTks(TestBase):

    LOG_FILE = "test_ai_gen_some_tks.log"

    def test_ai_gen_some_tks(self):
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
            # assert_test_cases_agent_generated(message_send)
            id_message = message_send.message_id

            # 3. Получение сообщений
            self.logger.info(f"ШАГ 3: Получение сообщений диалога")
            messages = self.get_messages(id_conversation, id_user)
            assistant_msg = assert_messages_contains_id(messages, id_message)

            # 4. Отправка второго сообщения с корректировками
            self.logger.info(f"ШАГ 4: Отправка второго сообщения с корректирвоками")
            message_two = "Сгенерируй негативный тест-кейс по авторизации"
            message_send_two = self.send_message(MESSAGE_TK_SIMPLE, id_conversation, message)
            # assert_test_cases_agent_generated(message_send)
            id_message_two = message_send_two.message_id

            # 5. Получение всех сообщений второй раз
            self.logger.info(f"ШАГ 5: Получение всех сообщений второй раз")
            messages = self.get_messages(id_conversation, id_user)
            assistant_msg = assert_messages_contains_id(messages, id_message_two)
            print(messages)

        finally:
            # 6. удаление диалога
            self.delete_conversation(id_conversation, id_user)

