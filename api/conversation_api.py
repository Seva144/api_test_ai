from typing import Any, Iterator
from uuid import UUID

from httpx import Response

from api import routes
from api.client import ApiClient


def post_conversation(client: ApiClient, **kwargs) -> Response:
    return client.post(routes.Routes.CONVERSATION, **kwargs)


def delete_conversation(client: ApiClient, id_conversation: UUID) -> Response:
    return client.delete(routes.Routes.CONVERSATION_BY_ID.format(id_conversation))


def stream_message(client: ApiClient, id_conversation: UUID, **kwargs: Any) -> Iterator[Response]:
    return client.stream("POST", routes.Routes.MESSAGE_SEND.format(id_conversation), **kwargs)
