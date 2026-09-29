
from uuid import UUID

from assertions.assertion_base import assert_stream_result, assert_messages_contains_id
from models.request.default_fields import MESSAGE_ATK_SIMPLE
from tests.base_test import TestBase


class TestAiSaveAtk(TestBase):

    def test_ai_save_atk(self):
        # 1. создание диалога
        self.logger.info(f"ШAГ 1: Создание диалога пользователя")
        create_conversation_response = self.create_conversation()
        # переменные
        id_conversation: UUID = create_conversation_response.id
        id_user: str = create_conversation_response.user_id

        message = "Сгенерируй авто тест-кейс по авторизации"
        try:
            # 2. Отправка сообщения
            self.logger.info(f"ШAГ 2: отправка сообщения на получение АТК")
            message_send = self.send_message(MESSAGE_ATK_SIMPLE, id_conversation, message)
            assert_stream_result(message_send, id_conversation)
            id_message = message_send.message_id

            # 3.  Получение сообщения
            self.logger.info(f"ШАГ 3: Получение сообщений диалога")
            messages = self.get_messages(id_conversation, id_user)
            assistant_msg = assert_messages_contains_id(messages, id_message)

            # 4. Сохранение АТК
            self.logger.info(f"ШАГ 4: Сохранение АТК")
            project_uuid = UUID('1f865f5b-4b8a-4caa-a66f-1cec318750e9')
            atk_save = self.atk_create(id_conversation, id_user, assistant_msg.content, project_uuid)
            id_atk = atk_save.id

            # 5. Удаление АТК
            self.logger.info(f"ШАГ 5: Удаление АТК")
            atk_delete = self.atk_delete(id_user, id_atk)

        finally:
            # 6. удаление диалога
            self.delete_conversation(id_conversation, id_user)

