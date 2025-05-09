from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

from app.infrastructure.db.session import fastapi_get_db
from app.services.authorization import AuthService, get_current_user_service
from app.models.dtoModels.TockenDTO import TokenDTO
from app.models.dtoModels.UserDTO import UserOutDTO

router = APIRouter()


@router.post("/get-token", response_model=TokenDTO)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session:    AsyncSession = Depends(fastapi_get_db),
    auth:       AuthService  = Depends(),
):
    return await auth.login_for_access_token(form_data, session)


@router.get("/current-user", response_model=UserOutDTO)
async def read_users_me(
    current_user: Annotated[UserOutDTO, Depends(get_current_user_service)]
):
    return current_user
