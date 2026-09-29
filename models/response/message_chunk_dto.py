from dataclasses import dataclass
from typing import Any
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class MessageChunkDTO(BaseModel):

    model_config = ConfigDict(
        populate_by_name=True,
        extra="ignore",
        str_strip_whitespace=False
    )

    conversation_id: UUID = Field(alias="conversationId")
    message_id: UUID = Field(alias="messageId")
    role: str | None = None  # USER / ASSISTANT / SYSTEM
    content: str
    seq: int

    metadata: dict[str, Any] | None = None

    event_type: str | None = Field(default=None, exclude=True)


@dataclass
class MessageStreamResult:
    """Результат сборки SSE-стрима: чанки + склеенный текст + метаданные."""
    conversation_id: UUID
    message_id: UUID
    chunks: list[MessageChunkDTO]
    full_text: str
    event_count: int
    finished: bool = False

    @property
    def last_seq(self) -> int:
        return max((c.seq for c in self.chunks), default=0)

