from __future__ import annotations

import uuid, datetime
from datetime import datetime as dt
from typing import List

import numpy as np
import pandas as pd
import shap
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.ml.runtime import clf, THRESHOLD as THRESH
from app.infrastructure.repositories.PredictionRepository import (
    PredictionRepository,
)
from app.models.dbModels.FeedbackEntity import FeedbackEntity
from app.models.dtoModels.PredictionDTO import PredictionInDTO, PredictionOutDTO
from app.models.dtoModels.FeedbackDTO import FeedbackCreateDTO, FeedbackOutDTO
from app.models.dtoModels.UserDTO       import UserOutDTO
from app.models.dbModels.PredictionEntity import PredictionEntity

def _calc_age(birth_date: dt.date) -> int:
    today = datetime.date.today()
    return today.year - birth_date.year - (
        (today.month, today.day) < (birth_date.month, birth_date.day)
    )


def _proba(model, X):
    if hasattr(model, "predict_proba"):
        try:
            return model.predict_proba(X)[:, 1]
        except ValueError:
            pass

    return model.predict(X)




_FEATURES = [
    "age", "bmi", "HbA1c_level", "blood_glucose_level",
    "smoking_history", "is_male", "hypertension", "heart_disease",
]

_SMOKING_MAP = {"No Info": 0, "never": 1, "former": 2, "current": 3, "ever": 4, "not current": 5}
_INV_SMOKING_MAP = {v:k for k,v in _SMOKING_MAP.items()}

_N_FEATURES = len(_FEATURES)
_bg_numeric = np.zeros((1, _N_FEATURES), dtype=float)

from shap.maskers import Independent

masker = Independent(_bg_numeric)


def _shap_predict(X: np.ndarray) -> np.ndarray:
    df = pd.DataFrame(X, columns=_FEATURES)
    df["smoking_history"] = df["smoking_history"].map(_INV_SMOKING_MAP)
    return _proba(clf, df)
explainer = shap.Explainer(_shap_predict, masker)
async def create(
    pred_in: PredictionInDTO,
    user,
    session: AsyncSession,
) -> PredictionOutDTO:
    repo = PredictionRepository(session)

    record = {
        "age":              _calc_age(user.birth_date),
        "is_male":          user.gender == 1,
        **pred_in.model_dump(),
    }
    X = pd.DataFrame([record])

    proba = float(_proba(clf, X)[0])
    pred  = int(proba > THRESH)

    row = PredictionEntity(
        user_id=user.id,
        probability=proba,
        prediction=pred,
        threshold_used=THRESH,
        input_json=record,

        input_age=record["age"],
        input_bmi=record["bmi"],
        input_hba1c_level=record["HbA1c_level"],
        input_blood_glucose_level=record["blood_glucose_level"],
        input_smoking_history=record["smoking_history"],
        input_is_male=record["is_male"],
        input_hypertension=record["hypertension"],
        input_heart_disease=record["heart_disease"],
    )

    await repo.add(row)

    return PredictionOutDTO(
        id=row.id,
        created_at=row.created_at,
        probability=proba,
        prediction=pred,
        threshold=THRESH,
    )


_SMOKING_MAP = {"No Info": 0, "never": 1, "former": 2, "current": 3, "ever": 4, "not current": 5}

async def _calc_shap(input_json: dict) -> dict[str, float]:
    df = pd.DataFrame([input_json])
    df["smoking_history"] = df["smoking_history"].map(_SMOKING_MAP)

    arr = df[_FEATURES].astype(float).values
    sv = explainer(arr)


    return dict(zip(_FEATURES, sv.values[0]))



async def explain(
    pred_id: uuid.UUID,
    user:    UserOutDTO,
    session: AsyncSession,
) -> dict[str, float]:

    repo = PredictionRepository(session)
    row  = await repo.get_by_id(pred_id, user.id)
    if not row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    if row.explain_json is None:
        row.explain_json = await _calc_shap(row.input_json)
        await repo.update(row)

    return row.explain_json



async def explain_text(
    pred_id: uuid.UUID,
    user:    UserOutDTO,
    session: AsyncSession,
) -> dict[str, str]:
    feat_imp = await explain(pred_id, user, session)

    top3 = sorted(feat_imp.items(),
                  key=lambda kv: abs(kv[1]),
                  reverse=True)[:3]

    phrases = [
        f"Feature “{f}” {'increases' if v > 0 else 'decreases'} risk by {abs(v):.2f}"
        for f, v in top3
    ]
    return {"explanation": "; ".join(phrases) + "."}



async def add_feedback(
    pred_id:    uuid.UUID,
    fb_in:      FeedbackCreateDTO,
    user:       UserOutDTO,
    session:    AsyncSession,
) -> dict[str, str]:
    repo = PredictionRepository(session)

    if not await repo.get_by_id(pred_id, user.id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    fb_row = FeedbackEntity(
        id             = uuid.uuid4(),
        prediction_id  = pred_id,
        created_at     = dt.utcnow(),
        is_correct     = fb_in.is_correct,
        comment        = fb_in.comment,
    )
    await repo.add_feedback(fb_row)
    return {"status": "ok"}


async def list_predictions(
    user: UserOutDTO,
    session: AsyncSession,
) -> List[PredictionOutDTO]:
    repo = PredictionRepository(session)
    rows = await repo.list_by_user(user.id)
    return [
        PredictionOutDTO(
            id=row.id,
            created_at=row.created_at,
            probability=row.probability,
            prediction=row.prediction,
            threshold=row.threshold_used,
        ) for row in rows
    ]

async def list_feedbacks(
    pred_id: uuid.UUID,
    user: UserOutDTO,
    session: AsyncSession,
) -> List[FeedbackOutDTO]:
    # ensure prediction belongs to user
    repo = PredictionRepository(session)
    if not await repo.get_by_id(pred_id, user.id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    fbs = await repo.list_feedbacks_by_prediction(pred_id)
    return [FeedbackOutDTO.from_orm(fb) for fb in fbs]
