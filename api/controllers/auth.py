from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from typing_extensions import Annotated

from api.dto.user_auth_dto import UserAuthDto
from api.services.user import create_user, get_user
from api.dto.user_dto import UserRegisterDto
from api.dto.token_dto import Token
from api.middleware.authentication import authenticate_user
from api.middleware.authentication import create_access_token
from config import Config

router = APIRouter()

# ✅ Login
@router.post("/token", response_model=Token)
async def login(login_data: UserAuthDto) -> Token:
    user = await authenticate_user(login_data.username, login_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário ou senha incorretos.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=Config.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.name},  # ou user.username se existir
        expires_delta=access_token_expires
    )

    return Token(access_token=access_token, token_type="bearer")
