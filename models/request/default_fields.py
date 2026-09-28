from dataclasses import dataclass


@dataclass
class ConversationConfigDefault:
    title: str = "Новый диалог"
    atkEnabled: bool = False
    tkEnabled: bool = False
    useTestAgent: bool = False
    model: str = "Qwen/Qwen3.5-4B"
    kits: str = "СБП"
    url_app: str = "https://test-app.local"


DEFAULT_CONVERSATION = ConversationConfigDefault()


@dataclass
class MessageConfigAtkOther:
    atkEnabled: bool = True
    tkEnabled: bool = False
    useTestAgent: bool = False
    model: str = "Qwen/Qwen3.5-4B"
    kits: str = "СБП"
    url_app: str = "https://test-app.local"


MESSAGE_ATK_OTHER = MessageConfigAtkOther()
