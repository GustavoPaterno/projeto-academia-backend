from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from typing_extensions import Annotated

from api.dto.user_dto import UserDTO
from api.middleware.authentication import token_required
from api.services import user as user_service

router = APIRouter()


# ✅ Usuário logado (já está feito)
@router.get("/user/me", response_model=UserDTO)
async def get_current_user(current_user: Annotated[UserDTO, Depends(token_required)]):
    return current_user


@router.post("/user", status_code=status.HTTP_201_CREATED)
async def create_user(user_dto: UserDTO):
    created = await user_service.create_user(
        name=user_dto.name,
        password=user_dto.password,
        email=user_dto.email,
        birthday=user_dto.birthday,
        genero=user_dto.genero,
        level=user_dto.level,
        exp=user_dto.exp,
    )

    # if isinstance(created, dict) and "message" in created:
    #     raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=created["message"])

    return created


# ✅ Buscar usuário por nome
@router.get("/user/{name}", response_model=UserDTO)
async def get_user(name: str):
    user = await user_service.get_user(name)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado")
    return user


# ✅ Atualizar usuário
@router.put("/user", response_model=dict)
async def update_user(user_dto: UserDTO):
    result = await user_service.update_user(user_dto)
    if "message" in result and result["message"] == "Usuário não encontrado":
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=result["message"])
    return result


# ✅ Deletar usuário
@router.delete("/user", response_model=dict)
async def delete_user(user_dto: Annotated[UserDTO, Depends(token_required)]):
    return await user_service.delete_user(user_dto)