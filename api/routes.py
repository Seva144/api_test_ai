from enum import Enum


class Routes(str, Enum):

    CONVERSATION = 'chat/conversations'
    CONVERSATION_BY_ID = 'chat/conversations/{}'
    MESSAGE_SEND = 'chat/conversations/{}/messages'
    MESSAGES_GET = 'chat/conversations/{}/messages'
    ATK_POST = '/atk/save'
    ATK_DELETE = '/atk/{}'
    TK_POST = '/tk/save'
    TK_DELETE = '/tk/{}'
    FILE_UPLOAD = 'chat/{}/files/upload'
    FILE_DELETE = 'chat/{}/files/{}'
    FILES_GET = 'chat/{}/files'
    TESTING_TYPE = 'testing-type/get-all'
    SEND_TKS = 'tk/send-control'
    PUSH_ATKS = 'atk/save-jgit'

    def __str__(self) -> str:
        return self.value
