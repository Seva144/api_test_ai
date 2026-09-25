from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class ConversationDTO(BaseModel):
    model_config = ConfigDict(
        # разрешает создавать и по alias, и по имени поля
        populate_by_name=True,
        # лишние поля не ломают парсинг
        extra="ignore",
        # опционально: неизменяемость, как record в Java
    )

    id: UUID
    business_uid: str = Field(alias="businessUid")
    user_id: str = Field(alias="userId")
    current_model: str = Field(alias="currentModel")
    atk_enabled: bool = Field(alias="atkEnabled")
    tk_enabled: bool = Field(alias="tkEnabled")
    use_test_agent: bool = Field(alias="useTestAgent")
    url_app: str = Field(alias="urlApp")
    kits_component: str = Field(alias="kitsComponent")
    title: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    cipher: str

    # для того чтобы парсинг не упал
    description: str | None = None
    error: str | None = None
    error_message: str | None = Field(default=None, alias="errorMessage")


