from http import HTTPStatus

import pytest

from api.api_client import ApiClient
from api.objects_api import post_object
from api.routes import Routes
from assertions.assertion_base import assert_status_code, assert_schema
from models.conversation_dto import ConversationDTO
import logging

from utilities.json_utils import read_json_conversation_request

logger = logging.getLogger(__name__)

class TestObjects:


    # фикстура один экзмепляр на все тесты
    @pytest.fixture(scope='class')
    def client(self):
        return ApiClient()

    def default_chat_values(self):
        return

    def test_create_conversation(self, client):
        exp_obj = read_json_conversation_request("post_conversation_default")
        logger.info(f"payload: {exp_obj}")
        response = post_object(client, Routes.CONVERSATIONS, json=exp_obj)

        assert_status_code(response, HTTPStatus.OK)
        assert_schema(response, ConversationDTO)

        logger.info(f"created conversation id={response.json()['id']}")



