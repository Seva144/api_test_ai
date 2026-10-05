from uuid import UUID

from assertions.assertion_base import assert_test_cases_agent_generated
from models.request.default_fields import MESSAGE_SEND_AGENT
from tests.base_test import TestBase


class TestSendMessageToAgent(TestBase):

    LOG_FILE = "CRUD/test_send_message_to_agent.log"

    def test_create_conversation(self):
        id_conversation = UUID("e43d8905-fd76-4bf3-85f3-56190985646e")

        # 3. Отправить сообщение для генерации тест-кейса

        message = "Сделай тест кейсы на отпуск использую данные из файла"
        message_send = self.send_message(MESSAGE_SEND_AGENT, id_conversation, message)
        assert_test_cases_agent_generated(message_send)
        id_message = message_send.message_id