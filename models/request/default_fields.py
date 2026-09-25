from dataclasses import dataclass


@dataclass
class EnvConfig:
    title: str = "Новый диалог"
    atkEnabled: bool = False
    tkEnabled: bool = False
    useTestAgent: bool = False
    model: str = "Qwen/Qwen3.8-27B-FP8"
    kits: str = "СБП"
    url_app: str = "https://test-app.local"


DEFAULT_CONVERSATION = EnvConfig()
