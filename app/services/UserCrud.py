# app/services/user_service.py
from uuid import uuid4
from datetime import datetime

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.repositories.UserRepository import UserRepository
from app.models.dbModels.UserEntity import UserEntity
from app.models.dtoModels.UserDTO import UserCreateDTO, UserOutDTO
from app.services.AuthorizationService import AuthService


async def add_user(dto: UserCreateDTO, session: AsyncSession) -> UserOutDTO:

    repo = UserRepository(session)

    if await repo.find_by_email(str(dto.email)):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with given email already exists",
        )

    auth = AuthService()
    hashed_pw = auth.get_password_hash(dto.password)

    entity = UserEntity(
        id=uuid4(),
        first_name=dto.first_name,
        last_name=dto.last_name,
        email=dto.email,
        hashed_password=hashed_pw,
        birth_date=dto.birth_date,
        gender=dto.gender,
        created_at=datetime.utcnow(),
    )

    saved = await repo.add_user(entity)

    return UserOutDTO(**saved)
