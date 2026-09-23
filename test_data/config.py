from dataclasses import dataclass


@dataclass
class EnvConfig:
    model: str = "Qwen/Qwen3.8-27B-FP8"
    kits: str = "СБП"
    url_app: str = "https://test-app.local"


DEFAULT_CONVERSATION = EnvConfig()
