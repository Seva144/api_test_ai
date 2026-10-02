from uuid import UUID

from tests.base_test import TestBase


class TestCreateConversation(TestBase):

    LOG_FILE = "CRUD/test-ai-download-file-to-agent-doc.log"

    def test_create_conversation(self):
        # 1. создание диалога
        self.logger.info(f"ШAГ 1: Создание диалога пользователя")
        create_conversation_response = self.create_conversation()
        # переменные
        id_conversation: UUID = create_conversation_response.id
        id_user: str = create_conversation_response.user_id
        print(f"id диалога {id_conversation}")
        print(f"id_user {id_user}")

