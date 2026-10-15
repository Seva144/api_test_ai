from uuid import UUID

from assertions.assertion_base import assert_test_cases_agent_generated
from models.request.default_fields import MESSAGE_WITHOUT_USE_TEST_AGENT
from tests.base_test import TestBase


class TestSendMessageToAgent(TestBase):

    LOG_FILE = "CRUD/test_send_message_to_agent.log"

    def test_create_conversation(self):
        id_conversation = UUID("e43d8905-fd76-4bf3-85f3-56190985646e")

        # 2. Отправить 1 сообщение для генерации тест-кейса

        message_one = "Сделай тест кейсы на отпуск использую данные из файла"
        message_response_one = self.send_message(MESSAGE_WITHOUT_USE_TEST_AGENT, id_conversation, message_one)
        assert_test_cases_agent_generated(message_response_one)
        id_message_one = message_response_one.message_id
        self.logger.info(f"Id первого сообщения {id_message_one}")

        # 3. Отправить 2 сообщение
        message_two = "Сделай тeст кесф с обновленными данными"
        message_response_two = self.send_message(MESSAGE_WITHOUT_USE_TEST_AGENT, id_conversation, message_two)
        assert_test_cases_agent_generated(message_response_two)
        id_message_two = message_response_two.message_id
        self.logger.info(f"Id второго сообщения {id_message_two}")