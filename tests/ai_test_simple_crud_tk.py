from uuid import UUID

from models.request.default_fields import MESSAGE_ATK_SIMPLE
from tests.base_test import TestBase


class AiTestSimpleCrudAtk(TestBase):

    LOG_FILE = "ai_test_simple_crud_atk.log"

    def ai_test_simple_crud_atk(self):
        try:
            #1. создание диалога
            create_conversation_response = self.create_conversation()
            id_conversation: UUID = create_conversation_response.id
            id_user: str = create_conversation_response.user_id
            message: str = "Сделай ТК по авторизации"
            #2. отправка сообщения

            self.send_message(MESSAGE_ATK_SIMPLE, id_conversation, message)
            #3. получение всех сообщений диалога
            self.get_messages(id_conversation, id_user)
        finally:
            #4. удаление диалога
            self.delete_conversation(id_conversation, id_user)
