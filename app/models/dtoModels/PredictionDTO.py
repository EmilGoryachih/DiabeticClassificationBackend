# app/models/dto/prediction.py
from pydantic import BaseModel, Field
from typing import Optional
import uuid, datetime as dt

from app.models.dtoModels.Entity import SmokingHistoryEnum


class PredictionInDTO(BaseModel):
    bmi:               float = Field(..., gt=5, lt=100)
    HbA1c_level:       float = Field(..., gt=3, lt=15)
    blood_glucose_level: int = Field(..., gt=40, lt=400)
    smoking_history:   SmokingHistoryEnum
    hypertension:      bool
    heart_disease:     bool

class PredictionOutDTO(BaseModel):
    id:          uuid.UUID
    created_at:  dt.datetime
    probability: float
    prediction:  bool
    threshold:   float


