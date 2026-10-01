from dataclasses import dataclass
from typing import Any
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from models.response.message_agent_dto import TestCaseDTO


class MessageMetadataDTO(BaseModel):
    """metadata-блок в чанке агента."""
    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    assistant_id: str | None = Field(default=None, alias="assistantId")
    sender_id: str | None = Field(default=None, alias="senderId")
    test_cases: list[TestCaseDTO] = Field(default_factory=list, alias="testCases")
    user_text: str | None = Field(default=None, alias="userText")
    workflow_status: str | None = Field(default=None, alias="workflowStatus")
    source: str | None = None
    sent_at: str | None = Field(default=None, alias="sentAt")
    type: str | None = None


class MessageChunkDTO(BaseModel):

    model_config = ConfigDict(
        populate_by_name=True,
        extra="ignore",
        str_strip_whitespace=False
    )

    conversation_id: UUID = Field(alias="conversationId")
    message_id: UUID | None = Field(default=None, alias="messageId")
    role: str | None = None  # USER / ASSISTANT / SYSTEM
    content: str
    seq: int

    metadata: MessageMetadataDTO | None = None

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

