from http import HTTPStatus

import pytest

from api.api_client import ApiClient
from api.objects_api import post_object
from assertions.assertion_base import assert_status_code, assert_schema
from models.conversation_dto import ConversationDTO
from utilities.json_utils import *


class TestObjects:


    # фикстура один экзмепляр на все тесты
    @pytest.fixture(scope='class')
    def client(self):
        return ApiClient()

    def default_chat_values(self):
        return

    def test_create_conversation(self, client, request):
        exp_obj = read_json_conversation_request("post_conversation_default")
        response = post_object(client, json=exp_obj)

        assert_status_code(response, HTTPStatus.OK)
        assert_schema(response, ConversationDTO)



