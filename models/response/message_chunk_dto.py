from typing import Any
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class MessageChunkDto(BaseModel):

    model_config = ConfigDict(
        populate_by_name=True,
        extra="ignore",
        str_strip_whitespace=True
    )

    conversation_id: UUID = Field(alias="conversationId")
    message_id: UUID = Field(alias="messageId")
    role: str | None = None  # USER / ASSISTANT / SYSTEM
    content: str
    seq: int
    event_type: str = Field(default="", exclude=True)
    metadata: dict[str, Any] | None = None

