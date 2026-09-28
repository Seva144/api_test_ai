from uuid import UUID

from tests.base_test import TestBase


class TestCreateOtherAtk(TestBase):

    LOG_FILE = "test_simple_crud.log"

    def test_create_atk_other(self):
        try:
            # 1. создание диалога
            create_conversation_response = self.create_conversation()
            id_conversation: UUID = create_conversation_response.id
            id_user: str = create_conversation_response.user_id
            message: str = "Сделай АТК по авторизации"
            #2. отправка сообщения
            self.send_message_atk_other(id_conversation, message)
            #3. получение всех сообщений диалога
            self.get_messages(id_conversation, id_user)
        finally:
            #3. удаление диалога
            self.delete_conversation(id_conversation, id_user)




