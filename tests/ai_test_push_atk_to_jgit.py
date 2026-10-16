from uuid import UUID

from assertions.assertion_base import assert_stream_result, assert_messages_contains_id, assert_failure_zero
from models.request.default_fields import MESSAGE_ATK_SIMPLE
from tests.base_test import TestBase


class TestAiPushToAtkJgit(TestBase):

    def test_ai_push_atk_to_jgit(self):
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
            message_response = self.send_message_locally(MESSAGE_ATK_SIMPLE, id_conversation, message)
            assert_stream_result(message_response, id_conversation)
            id_message_response = message_response.message_id

            # 3. Получение сообщений
            self.logger.info(f"ШАГ 3: Получение сообщений диалога")
            messages = self.get_messages(id_conversation, id_user)
            assistant_msg = assert_messages_contains_id(messages, id_message_response)

            #  4. Сохранение АТК
            self.logger.info(f"ШАГ 4: Сохранение АТК")
            project_uuid = UUID('1f865f5b-4b8a-4caa-a66f-1cec318750e9')
            atk_save = self.atk_create(id_conversation, id_user, assistant_msg.content, project_uuid)
            id_atk = atk_save.id

            # 5. Отправка АТК на jgit
            self.logger.info(f"ШАГ 5: Отправка АТК на на Jgit")
            sender = self.push_atk([id_atk])
            assert_failure_zero(sender)

        finally:
            # 6. удаление диалога
            self.logger.info(f"ШАГ 5: Удаление диалога")
            self.delete_conversation(id_conversation, id_user)


