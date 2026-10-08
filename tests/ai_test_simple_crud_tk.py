from uuid import UUID

from models.request.default_fields import MESSAGE_ATK_SIMPLE, MESSAGE_TK_SIMPLE
from tests.base_test import TestBase


class TestAiSimpleCrudTk(TestBase):

    LOG_FILE = "ai_test_simple_crud_tk.log"

    """
        Простой тест получения в чате шаблона ТК
    """

    def test_ai_simple_crud_tk(self):
        # 1. создание диалога
        create_conversation_response = self.create_conversation()
        id_conversation: UUID = create_conversation_response.id
        id_user: str = create_conversation_response.user_id
        message: str = "Сделай ТК по авторизации"
        try:
            #2. отправка сообщения
            self.send_message(MESSAGE_TK_SIMPLE, id_conversation, message)
            #3. получение всех сообщений диалога
            self.get_messages(id_conversation, id_user)
        finally:
            #4. удаление диалога
            self.delete_conversation(id_conversation, id_user)
