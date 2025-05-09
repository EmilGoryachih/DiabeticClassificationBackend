from datetime import date, datetime
from uuid import UUID
from enum import Enum

from pydantic import BaseModel, EmailStr, Field
from app.models.dtoModels.Entity import Entity as DTO


class FeedbackCreateDTO(DTO):
    prediction_id: UUID
    is_correct:    bool
    comment:       str | None = Field(None, max_length=500)


class FeedbackOutDTO(DTO):
    id:            UUID
    prediction_id: UUID
    is_correct:    bool
    comment:       str | None
    created_at:    datetime