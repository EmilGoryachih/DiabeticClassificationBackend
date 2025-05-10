import enum
import uuid
from datetime import datetime

from sqlalchemy import (
    Column,
    String,
    UUID,
    DateTime,
    Integer,
    Float,
    Boolean,
    Enum,
    ForeignKey, JSON,
)
from sqlalchemy.orm import relationship

from app.models.dbModels.EntityDB import EntityDB


class SmokingHistoryEnum(str, enum.Enum):
    NO_INFO = "No Info"
    NEVER = "never"
    FORMER = "former"
    CURRENT = "current"
    EVER = "ever"
    NOT_CURRENT = "not current"

    def __str__(self) -> str:
        return str(self.value)


class PredictionEntity(EntityDB):

    __tablename__ = "predictions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    user = relationship("UserEntity", back_populates="predictions")

    created_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)

    probability = Column(Float, nullable=False)
    prediction = Column(Boolean, nullable=False)
    threshold_used = Column(Float, nullable=False)

    input_json = Column(JSON)
    explain_json = Column(JSON, nullable=True)

    input_age = Column(Integer, nullable=False)
    input_bmi = Column(Float, nullable=False)
    input_hba1c_level = Column(Float, nullable=False)
    input_blood_glucose_level = Column(Float, nullable=False)
    input_smoking_history = Column(Enum(SmokingHistoryEnum), nullable=False)
    input_is_male = Column(Boolean, nullable=False)
    input_hypertension = Column(Boolean, nullable=False)
    input_heart_disease = Column(Boolean, nullable=False)

    explanation_text = Column(String, nullable=True)
    shap_png = Column(String, nullable=True)

    feedback = relationship(
        "FeedbackEntity",
        back_populates="prediction",
        uselist=False,
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    def __init__(
        self,
        *,
        user_id: uuid.UUID,
        probability: float,
        prediction: bool,
        threshold_used: float,
        input_age: int,
        input_bmi: float,
        input_hba1c_level: float,
        input_blood_glucose_level: float,
        input_smoking_history: SmokingHistoryEnum,
        input_is_male: bool,
        input_hypertension: bool,
        input_heart_disease: bool,
        explanation_text: str | None = None,
        shap_png: str | None = None,
        created_at: datetime | None = None,
        input_json: dict | None = None,
        explain_json: dict | None = None,
        id: uuid.UUID | None = None,

    ) -> None:
        self.id = id or uuid.uuid4()
        self.created_at = created_at or datetime.utcnow()

        self.user_id = user_id

        self.probability = probability
        self.prediction = prediction
        self.threshold_used = threshold_used

        self.input_age = input_age
        self.input_bmi = input_bmi
        self.input_hba1c_level = input_hba1c_level
        self.input_blood_glucose_level = input_blood_glucose_level
        self.input_smoking_history = input_smoking_history
        self.input_is_male = input_is_male
        self.input_hypertension = input_hypertension
        self.input_heart_disease = input_heart_disease

        self.explanation_text = explanation_text
        self.shap_png = shap_png

        self.input_json = input_json or {}
        self.explain_json = explain_json

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "user_id": str(self.user_id),
            "created_at": self.created_at.isoformat(),
            "probability": self.probability,
            "prediction": self.prediction,
            "threshold_used": self.threshold_used,
            "input_age": self.input_age,
            "input_bmi": self.input_bmi,
            "input_hba1c_level": self.input_hba1c_level,
            "input_blood_glucose_level": self.input_blood_glucose_level,
            "input_smoking_history": str(self.input_smoking_history),
            "input_is_male": self.input_is_male,
            "input_hypertension": self.input_hypertension,
            "input_heart_disease": self.input_heart_disease,
            "explanation_text": self.explanation_text,
            "shap_png": self.shap_png,
        }
