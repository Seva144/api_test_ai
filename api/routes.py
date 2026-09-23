from enum import Enum


class Routes(str, Enum):
    OBJECTS = '/objects'
    OBJECTS_ITEM = '/objects/{}'
    CONVERSATION = '/chat/conversations'
    CONVERSATION_BY_ID = '/chat/conversations/{}'

    def __str__(self) -> str:
        return self.value
