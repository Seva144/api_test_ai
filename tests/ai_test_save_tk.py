from uuid import UUID

from assertions.assertion_base import assert_stream_result, assert_messages_contains_id, \
    assert_test_cases_agent_generated
from models.request.default_fields import MESSAGE_TK_SIMPLE
from tests.base_test import TestBase


class TestAiSaveTk(TestBase):

    LOG_FILE = "test_ai_save_tk.log"

    def test_ai_save_tk(self):
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
            tks = self.tks_create(id_conversation, id_user, id_message, assistant_msg.content)
            self.logger.info(f"Сгенерировано {len(tks)} TK")

            # 5. Удаление ТК
            self.tks_delete(id_user, tks)

        finally:
            # 6. удаление диалога
            self.delete_conversation(id_conversation, id_user)









