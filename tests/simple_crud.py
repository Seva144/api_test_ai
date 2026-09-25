from tests.base_test import TestBase


class TestSimpleCRUD(TestBase):

    LOG_FILE = "test_simple_crud.log"

    def test_create_and_delete_conversation(self):
        # создание диалога
        create_conversation = self.create_conversation()
        # удаление диалога
        self.delete_conversation(create_conversation.id, create_conversation.user_id)



