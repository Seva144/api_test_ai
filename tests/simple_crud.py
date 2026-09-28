from uuid import UUID

from tests.base_test import TestBase


class TestSimpleCRUD(TestBase):

    LOG_FILE = "test_simple_crud.log"

    def test_create_and_delete_conversation(self):
        # создание диалога
        create_conversation = self.create_conversation()

        id_conversation: UUID = create_conversation.id
        id_user: str = create_conversation.user_id

        message: str = "Сделай АТК по авторизации"

        # отправка сообщения
        self.send_message_atk_other(id_conversation, message)

        # удаление диалога
        self.delete_conversation(id_conversation, id_user)




