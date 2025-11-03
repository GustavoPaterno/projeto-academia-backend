import jwt
from jwt.exceptions import InvalidTokenError, ExpiredSignatureError

from fastapi import status, Depends
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordBearer

from passlib.context import CryptContext

from api.dto.user_dto import UserDTO 
from api.dto.token_dto import TokenData
from api.services.user import get_user

from datetime import timedelta, datetime, timezone

from config import Config

from typing_extensions import Annotated

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')

def verify_password(password, hashed_password):
    return pwd_context.verify(password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode,
        Config.SECRET_KEY,
        Config.ALGORITHM
    )
    return encoded_jwt

async def authenticate_user(name: str, password: str):
    user = await get_user(name)
    
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    
    return user

async def token_required(token: Annotated[str, Depends(oauth2_scheme)]): # get_current_user
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não foi possível validar credenciais.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token,
            Config.SECRET_KEY,
            algorithms=Config.ALGORITHM
        )
        name = payload.get("sub")
        if name is None:
            raise credentials_exception
        token_data = TokenData(name=name)
    except InvalidTokenError:
        raise credentials_exception
    user = await get_user(token_data.name)
    if user is None:
        raise credentials_exception
    return name