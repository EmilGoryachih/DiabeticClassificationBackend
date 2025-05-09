import uuid
from datetime import datetime

from sqlalchemy import (
    Column,
    UUID,
    DateTime,
    Boolean,
    Text,
    ForeignKey,
)
from sqlalchemy.orm import relationship

from app.models.dbModels.EntityDB import EntityDB


class FeedbackEntity(EntityDB):

    __tablename__ = "feedback"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)

    prediction_id = Column(
        UUID(as_uuid=True),
        ForeignKey("predictions.id", ondelete="CASCADE"),
        nullable=False,
    )
    prediction = relationship("PredictionEntity", back_populates="feedback")

    is_correct = Column(Boolean, nullable=False)
    comment = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)

    def __init__(
        self,
        *,
        prediction_id: uuid.UUID,
        is_correct: bool,
        comment: str | None = None,
        created_at: datetime | None = None,
        id: uuid.UUID | None = None,
    ) -> None:
        self.id = id or uuid.uuid4()
        self.prediction_id = prediction_id
        self.is_correct = is_correct
        self.comment = comment
        self.created_at = created_at or datetime.utcnow()

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "prediction_id": str(self.prediction_id),
            "is_correct": self.is_correct,
            "comment": self.comment,
            "created_at": self.created_at.isoformat(),
        }
