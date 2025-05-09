from enum import Enum

from pydantic import BaseModel

class SmokingHistoryEnum(str, Enum):
    NO_INFO = "No Info"
    NEVER = "never"
    FORMER = "former"
    CURRENT = "current"
    EVER = "ever"
    NOT_CURRENT = "not current"

class Entity(BaseModel):

    class Config:
        orm_mode = True