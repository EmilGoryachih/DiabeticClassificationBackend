# app/infrastructure/repositories/prediction_repository.py
import uuid
from typing import Optional, Sequence
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update, delete

from app.models.dbModels.PredictionEntity import PredictionEntity
from app.models.dbModels.FeedbackEntity   import FeedbackEntity

class PredictionRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    # ─────────────────── PREDICTIONS ─────────────────── #
    async def add(self, row: PredictionEntity) -> None:
        self.session.add(row)
        await self.session.commit()

    async def get_by_id(self, pred_id: UUID, user_id: UUID) -> Optional[PredictionEntity]:
        q = select(PredictionEntity).where(
            PredictionEntity.id == pred_id,
            PredictionEntity.user_id == user_id,
        )
        res = await self.session.execute(q)
        return res.scalars().first()

    async def list_for_user(self, user_id: UUID) -> Sequence[PredictionEntity]:
        q = (
            select(PredictionEntity)
            .where(PredictionEntity.user_id == user_id)
            .order_by(PredictionEntity.created_at.desc())
        )
        res = await self.session.execute(q)
        return res.scalars().all()

    async def update(self, row: PredictionEntity) -> None:
        # row уже изменён в сервисе → просто flush/commit
        await self.session.commit()

    # ─────────────────── FEEDBACK ─────────────────── #
    async def add_feedback(self, fb: FeedbackEntity) -> None:
        self.session.add(fb)
        await self.session.commit()

    async def list_by_user(self, user_id: uuid.UUID):
        result = await self.session.execute(
            select(PredictionEntity).where(PredictionEntity.user_id == user_id)
        )
        return result.scalars().all()

    async def list_feedbacks_by_prediction(self, pred_id: uuid.UUID):
        result = await self.session.execute(
            select(FeedbackEntity).where(FeedbackEntity.prediction_id == pred_id)
        )
        return result.scalars().all()