from datetime import date, datetime
from uuid import UUID
from enum import Enum

from pydantic import BaseModel, EmailStr, Field, ConfigDict
from app.models.dtoModels.Entity import Entity as DTO


class FeedbackCreateDTO(DTO):
    prediction_id: UUID
    is_correct:    bool
    comment:       str | None = Field(None, max_length=500)


class FeedbackOutDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    prediction_id: UUID
    is_correct: bool
    comment: str
    created_at: datetime

