# schemas/message.py
from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field



class MessageDTO(BaseModel):
    """DTO полного сообщения чата."""

    model_config = ConfigDict(
        populate_by_name=True,
        extra="ignore",
        str_strip_whitespace=True
    )

    id: str
    conversation_id: str = Field(alias="conversationId")
    role: str                        # USER / ASSISTANT / SYSTEM
    content: str
    cipher: str
    created_at: datetime = Field(alias="createdAt")
    metadata: dict[str, Any] = Field(default_factory=dict)

    # опциональные
    error: str | None = None
    error_message: str | None = Field(default=None, alias="errorMessage")

