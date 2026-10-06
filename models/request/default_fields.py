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
class MessageConfigAtkSimple:
    atkEnabled: bool = True
    tkEnabled: bool = False
    useTestAgent: bool = False
    model: str = "Qwen/Qwen3.5-4B"
    kits: str = "СБП"
    url_app: str = "https://test-app.local"


MESSAGE_ATK_SIMPLE = MessageConfigAtkSimple()


@dataclass
class MessageConfigTkSimple:
    atkEnabled: bool = False
    tkEnabled: bool = True
    useTestAgent: bool = False
    model: str = "Qwen/Qwen3.5-4B"
    kits: str = "СБП"
    url_app: str = "https://test-app.local"


MESSAGE_TK_SIMPLE = MessageConfigTkSimple()


@dataclass
class MessageConfigAtkByPbo:
    atkEnabled: bool = True
    tkEnabled: bool = False
    useTestAgent: bool = False
    model: str = "Qwen/Qwen3.5-4B"
    kits: str = "ПБО"
    url_app: str = "https://test-app.local"


MESSAGE_ATK_BY_PBO = MessageConfigAtkByPbo()


# Объекты для сохранения ТК и АТК
@dataclass
class ATKMessageConfig:
    name: str = "АТК"
    kits: str = "СБП"


ATK_MESSAGE_DEFAULT = ATKMessageConfig()


@dataclass
class TKMessageConfig:
    name: str = "ТК"
    kits: str = "СБП"


TK_MESSAGE_DEFAULT = ATKMessageConfig()




