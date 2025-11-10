from bson import ObjectId
from fastapi import Depends

from datetime import date

from fastapi.encoders import jsonable_encoder
from pymongo.errors import DuplicateKeyError

from api.dto.user_dto import UserDTO
from api.models.user import User

from typing_extensions import Annotated

async def create_user(name: str, password: str, email: str, birthday: str, genero: str, level: int, exp: int):
    user = User(
        name=name,
        password=password,
        email=email,
        birthday=birthday,
        genero=genero,
        level=level,
        exp=exp,
    )
    try:
        await user.insert()
        return user  # ✅ retorna o documento inserido
    except DuplicateKeyError:
        return {
            "message": "Email já está em uso."
        }

async def get_all_user():
    users = await User.find_all().to_list()
    return [
        UserDTO(
            _id=str(user.id),
            **user.dict(exclude={"id"})
        )
        for user in users
    ]

async def get_user(user_id: str):
    try:
        oid = ObjectId(user_id)
    except Exception:
        return {"message": "ID inválido"}

    user = await User.find_one(User.id == oid)
    if not user:
        return None
    
    return jsonable_encoder(user)

async def get_user_name(user_name: str):
    user = await User.find_one({"name": user_name})
    if not user:
        return None
    return user

async def update_user(user_dto: UserDTO, user_id: str):
    try:
        oid = ObjectId(user_id)
    except Exception:
        return {"message": "ID inválido"}

    user = await User.find_one(User.id == oid)
    if not user:
        return {"message": "Usuário não encontrado"}

    # atualiza os campos
    user.name = user_dto.name
    user.password = user_dto.password
    user.email = user_dto.email
    user.birthday = user_dto.birthday
    user.genero = user_dto.genero
    user.level = user_dto.level
    user.exp = user_dto.exp

    # ⚠️ ATENÇÃO: aqui usamos save() em vez de insert()
    await user.save()
    return {"message": "Usuário atualizado com sucesso"}


async def delete_user(user_id: str):
    try:
        oid = ObjectId(user_id)
    except Exception:
        return {"message": "ID inválido"}
    user = await User.find_one(User.id == oid)
    if not user:
        return
    
    await user.delete()

    return {"message": "Usuário deletado com sucesso"}