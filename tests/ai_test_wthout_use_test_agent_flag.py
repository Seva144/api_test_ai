from uuid import UUID

from assertions.assertion_base import assert_test_cases_agent_generated, assert_messages_contains_id, \
    assert_check_content_message
from models.request.default_fields import MESSAGE_TK_SIMPLE, MESSAGE_WITHOUT_USE_TEST_AGENT
from tests.base_test import TestBase


class TestAiWithoutUseTestAgentFlag(TestBase):
    LOG_FILE = "ai-test-without-use-test-agent-flag.log"

    """
        Тест для проверки неиспользвания use-test-agent флага
        """

    def test_ai_without_use_test_agent_flag(self):
        # 1. создание диалога
        self.logger.info(f"ШAГ 1: Создание диалога пользователя")
        create_conversation_response = self.create_conversation()
        # переменные
        id_conversation: UUID = create_conversation_response.id
        id_user: str = create_conversation_response.user_id

        try:
            # 2. Загрузка файла на агент
            self.logger.info(f"ШАГ 2: Загружаем файл на агент")
            file_path = "resources/Authorized.txt"
            self.file_upload(id_conversation, file_path)

            # 3. Отправить сообщение для генерации тест-кейса
            self.logger.info(f"ШАГ 3: Написать сообщение для генерации ТК")
            message_request_one = "Сделай тест-кейсы на авторизацию использую данные из файла"
            message_response_one = self.send_message(MESSAGE_WITHOUT_USE_TEST_AGENT, id_conversation, message_request_one)
            assert_test_cases_agent_generated(message_response_one)
            id_message_one = message_response_one.message_id

            # 4. Получить сообщения диалога
            self.logger.info(f"ШАГ 4: Получение сообщений диалога")
            messages = self.get_messages(id_conversation, id_user)
            message_first = assert_messages_contains_id(messages, id_message_one)
            word_one = "Vova_P"
            word_two = "Dima_M"
            assert_check_content_message(message_first.content, word_one, word_two)



        finally:
            # 5. удаление диалога
            self.logger.info(f"ШАГ 7: Удаление диалога с id - {id_conversation}")
            self.delete_conversation(id_conversation, id_user)



