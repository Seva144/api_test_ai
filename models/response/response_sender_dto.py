from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class SenderDTO(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    message: str | None = None
    success_uids: list[UUID] | None = Field(default=None, alias="successUids")
    failed_uids: list[UUID] | None = Field(default=None, alias="failedUids")
    total_count: int | None = Field(default=None, alias="totalCount")
    success_count: int | None = Field(default=None, alias="successCount")
    failed_count: int | None = Field(default=None, alias="failedCount")