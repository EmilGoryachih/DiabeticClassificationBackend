from datetime import date, datetime
from uuid import UUID
from enum import Enum

from pydantic import BaseModel, EmailStr, Field
from app.models.dtoModels.Entity import Entity as DTO

class UserCreateDTO(DTO):
    first_name: str = Field(..., max_length=50)
    last_name:  str = Field(..., max_length=50)
    email:      EmailStr
    password:   str  = Field(..., min_length=6)           # plain password
    birth_date: date
    gender:     int = Field(..., ge=0, le=1)              # 0=F, 1=M


class UserOutDTO(DTO):
    id:         UUID
    first_name: str
    last_name:  str
    email:      EmailStr
    birth_date: date
    gender:     int
    created_at: datetime

