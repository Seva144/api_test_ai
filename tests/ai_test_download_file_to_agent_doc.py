from uuid import UUID

from assertions.assertion_base import assert_messages_contains_id, assert_stream_result, \
    assert_test_cases_agent_generated
from models.request.default_fields import MESSAGE_SEND_AGENT
from tests.base_test import TestBase


class TestAiDownloadFileToAgentDoc(TestBase):


    LOG_FILE = "test-ai-download-file-to-agent-doc.log"

    def test_ai_download_file_to_agent_doc(self):
        # 1. создание диалога
        self.logger.info(f"ШAГ 1: Создание диалога пользователя")
        create_conversation_response = self.create_conversation()
        # переменные
        id_conversation: UUID = create_conversation_response.id
        id_user: str = create_conversation_response.user_id

        try:
            # 2. Загрузка файла на агент
            self.logger.info(f"ШАГ 2: Загружаем файл на агент")
            file_path = "resources/Doc_rest.docx"
            self.upload_file(id_conversation, file_path)

            # 3. Отправить сообщение для генерации тест-кейса
            self.logger.info(f"ШАГ 3: Написать сообщение для генерации ТК")
            message = "Сделай тест кейсы на отпуск использую данные из файла"
            message_send = self.send_message_agent(MESSAGE_SEND_AGENT, id_conversation, message)
            assert_test_cases_agent_generated(message_send)
            id_message = message_send.message_id

            # 4. Получить сообщения диалога
            self.logger.info(f"ШАГ 3: Получение сообщений диалога")
            messages = self.get_messages(id_conversation, id_user)
            assert_messages_contains_id(messages, id_message)

        finally:
            # 5. удаление диалога
            self.logger.info("Удаление ")
            self.delete_conversation(id_conversation, id_user)



