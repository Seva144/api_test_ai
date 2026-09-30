from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class FileDTO(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        extra="ignore",
        str_strip_whitespace=False,
    )

    id: str
    conversation_id: str = Field(alias="conversationId")
    filename: str
    original_filename: str = Field(alias="originalFilename")

    file_size: int | None = Field(default=None, alias="fileSize")
    mime_type: str | None = Field(default=None, alias="mimeType")
    processing_status: str | None = Field(default=None, alias="processingStatus")

    content: str | None = None
    summary: str | None = None

    created_at: datetime = Field(alias="createdAt")
    metadata: dict[str, Any] | None = None
