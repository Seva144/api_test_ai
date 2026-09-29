from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field, ConfigDict


class AtkDTO(BaseModel):
    """
    DTO ответа с ATK (авто-тест-кейсом).
    Соответствует ru.cbr.msk.lunohod.aiTest.dto.ui.response.atk.ATKResponseDto.
    """

    model_config = ConfigDict(
        populate_by_name=True,      # принимает и camelCase, и snake_case
        extra="ignore",
        str_strip_whitespace=False
    )

    id: UUID
    business_uid: str = Field(alias="businessUid")
    name: str | None = None
    user_id: str = Field(alias="userId")
    content: str
    kits: str
    cipher: str

    project_uuid: UUID = Field(alias="projectUUID")
    name_class: str = Field(alias="nameClass")

    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
