# app/api/routes/prediction_router.py
import uuid
from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.db.session import fastapi_get_db
from app.models.dtoModels.FeedbackDTO import FeedbackOutDTO
from app.models.dtoModels.PredictionDTO import PredictionOutDTO
from app.models.dtoModels.UserDTO import UserOutDTO
from app.services.AuthorizationService import get_current_user_service
from app.models.dtoModels import PredictionDTO, FeedbackDTO
from app.services.PredictionService import (
    create as create_pred,
    explain, explain_text,
    add_feedback,
    list_predictions, list_feedbacks
)

router = APIRouter()

@router.post(
    "",
    response_model=PredictionDTO.PredictionOutDTO,
    status_code=status.HTTP_201_CREATED,
)
async def make_prediction(
    data: PredictionDTO.PredictionInDTO,
    session: AsyncSession = Depends(fastapi_get_db),
    user   = Depends(get_current_user_service),
):
    return await create_pred(data, user, session)

@router.get("/{pred_id}/explain")
async def explain_prediction(
    pred_id: UUID,
    session: AsyncSession = Depends(fastapi_get_db),
    user   = Depends(get_current_user_service),
):
    return await explain(pred_id, user, session)

@router.get("/{pred_id}/explain_text")
async def explain_prediction_text(
    pred_id: UUID,
    session: AsyncSession = Depends(fastapi_get_db),
    user   = Depends(get_current_user_service),
):
    return await explain_text(pred_id, user, session)

@router.post("/{pred_id}/feedback", status_code=status.HTTP_201_CREATED)
async def leave_feedback(
    pred_id: UUID,
    fb: FeedbackDTO.FeedbackCreateDTO,
    session: AsyncSession = Depends(fastapi_get_db),
    user   = Depends(get_current_user_service),
):
    return await add_feedback(pred_id, fb, user, session)
## Routes in app/api/routes/PredictionRout.py
from typing import List
from app.services.PredictionService import (
    create, explain, explain_text, add_feedback,
    list_predictions, list_feedbacks
)
from app.models.dtoModels.FeedbackDTO import FeedbackOutDTO

@router.get("/predictions", response_model=List[PredictionOutDTO])
async def get_all_predictions(
    user: UserOutDTO = Depends(get_current_user_service),
    session: AsyncSession = Depends(fastapi_get_db),
):
    return await list_predictions(user, session)

@router.get(
    "/prediction/{pred_id}/feedbacks",
    response_model=List[FeedbackOutDTO]
)
async def get_feedbacks_for_prediction(
    pred_id: uuid.UUID,
    user:   UserOutDTO = Depends(get_current_user_service),
    session: AsyncSession = Depends(fastapi_get_db),
):
    return await list_feedbacks(pred_id, user, session)
