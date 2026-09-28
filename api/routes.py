from enum import Enum


class Routes(str, Enum):
    CONVERSATION = '/chat/conversations'
    CONVERSATION_BY_ID = '/chat/conversations/{}'
    MESSAGE_SEND = 'chat/conversations/{}/messages'
    MESSAGES_GET = 'chat/conversations/{}/messages'

    def __str__(self) -> str:
        return self.value
