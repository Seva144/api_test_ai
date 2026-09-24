from http import HTTPStatus

import pytest

from api.client import ApiClient
from api.conversation_api import post_conversation, delete_conversation
from assertions.assertion_base import assert_status_code, assert_schema
from models.conversation_dto import ConversationDTO

from tests.base_test import TestBase
from utilities.json_utils import read_json_conversation_request


class TestSimpleCRUD(TestBase):

    LOG_FILE = "test_simple_crud.log"

    def test_create_and_delete_conversation(self, start):
        # создание диалога
        self.logger.info(f"Создание диалога")
        post_obj = read_json_conversation_request("post_conversation_default")
        logger.info(f"payload: {post_obj}")
        response_post = post_conversation(start, json=post_obj)
        assert_status_code(response_post, HTTPStatus.OK)
        assert_schema(response_post, ConversationDTO)

        # удаление диалога
        id_conversation = response_post.json()['id']
        logger.info(f"Создан диалог с id={id_conversation}")
        logger.info(f"Удаление диалога")
        response_delete = delete_conversation(start, id_conversation)
        logger.info(response_delete)
        assert_status_code(response_delete, HTTPStatus.OK)
        assert_schema(response_delete, ConversationDTO)


