from fastapi import APIRouter

from app.api.routes import UserRout
from app.api.routes import token
from app.api.routes import PredictionRout

api_router = APIRouter()

api_router.include_router(UserRout.router, prefix="/user", tags=["user"])
api_router.include_router(token.router, prefix="/token", tags=["tocken"])
api_router.include_router(PredictionRout.router, prefix="/prediction", tags=["prediction"])
