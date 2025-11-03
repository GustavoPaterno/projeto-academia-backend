from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from typing_extensions import Annotated

from api.services.user import create_user, get_user
from api.dto.user_dto import UserRegisterDto
from api.dto.token_dto import Token
from api.middleware.authentication import authenticate_user
from api.middleware.authentication import get_password_hash
from api.middleware.authentication import create_access_token
from config import Config

router = APIRouter()


# ✅ Registrar usuário
@router.post("/auth/register", response_model=dict)
async def register_user(user_data: UserRegisterDto):
    result = await create_user(
        name=user_data.username,
        password=get_password_hash(user_data.password),
        email=user_data.email,
        birthday=user_data.birthday,
        genero=user_data.genero,
        level=0,
        exp=0
    )

    if isinstance(result, dict) and "message" in result:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result["message"]
        )

    return {"message": "Usuário criado com sucesso"}


# ✅ Login
@router.post("/token", response_model=Token)
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> Token:
    user = await authenticate_user(form_data.username, form_data.password)
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
