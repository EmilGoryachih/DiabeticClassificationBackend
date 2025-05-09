from datetime import date, datetime
from uuid import UUID
from enum import Enum

from pydantic import BaseModel, EmailStr, Field
from app.models.dtoModels.Entity import Entity as DTO, SmokingHistoryEnum


class PredictionInputDTO(DTO):
    """То, что фронт отправляет на /predict"""
    age:                     int   = Field(..., ge=0, le=120)
    bmi:                     float = Field(..., ge=10, le=100)
    HbA1c_level:             float = Field(..., ge=3.0, le=15.0)
    blood_glucose_level:     int   = Field(..., ge=50, le=500)
    smoking_history:         SmokingHistoryEnum
    is_male:                 bool
    hypertension:            bool
    heart_disease:           bool


class PredictionOutDTO(DTO):
    """Ответ /predict (/explain)"""
    id:               UUID
    created_at:       datetime
    probability:      float
    prediction:       bool
    threshold_used:   float
    explanation_text: str | None = None
    shap_png:         str | None = None      # base64 (если запрашивали)