from http import HTTPStatus

from api.conversation_api import post_conversation, delete_conversation
from assertions.assertion_base import assert_status_code, assert_schema
from models.response.conversation_dto import ConversationDTO

from tests.base_test import TestBase
from utilities.json_utils import read_json_conversation_request


class TestSimpleCRUD(TestBase):

    LOG_FILE = "test_simple_crud.log"

    def test_create_and_delete_conversation(self):
        # создание диалога
        self.logger.info(f"Создание диалога - test_create_and_delete_conversation")
        post_obj = read_json_conversation_request("post_conversation_default")
        self.logger.info(f"payload: {post_obj}")
        response_post = post_conversation(self.client, json=post_obj)
        assert_status_code(response_post, HTTPStatus.OK)
        assert_schema(response_post, ConversationDTO)

        # удаление диалога
        id_conversation = response_post.json()['id']
        self.logger.info(f"Создан диалог с id={id_conversation}")
        self.logger.info(f"Удаление диалога")
        response_delete = delete_conversation(self.client, id_conversation)
        self.logger.info(response_delete)
        assert_status_code(response_delete, HTTPStatus.OK)
        assert_schema(response_delete, ConversationDTO)


