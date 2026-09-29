from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class TkDTO(BaseModel):
    """
    DTO ответа с TK (тест-кейсом).
    Соответствует ru.cbr.msk.lunohod.aiTest.dto.ui.response.tk.TKResponseDTO.
    """

    model_config = ConfigDict(
        populate_by_name=True,
        extra="ignore",
        str_strip_whitespace=False,
    )

    id: UUID
    business_uid: str = Field(alias="businessUid")
    name: str | None = None
    user_id: str = Field(alias="userId")
    kits: str
    cipher: str

    version: int | None = None
    status: str | None = None
    steps: int | None = None
    content: str

    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
