from uuid import UUID

from tests.base_test import TestBase


class TestAiSimpleCrudAtk(TestBase):

    LOG_FILE = "ai_test_simple_crud_atk.log"

    def test_ai_simple_crud_atk(self):
        # 1. создание диалога
        create_conversation_response = self.create_conversation()
        id_conversation: UUID = create_conversation_response.id
        id_user: str = create_conversation_response.user_id
        message: str = "Сделай АТК по авторизации"
        try:
            #2. отправка сообщения
            self.send_message(id_conversation, message)
            #3. получение всех сообщений диалога
            self.get_messages(id_conversation, id_user)
        finally:
            #4. удаление диалога
            self.delete_conversation(id_conversation, id_user)




