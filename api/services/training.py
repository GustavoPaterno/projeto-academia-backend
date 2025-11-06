from bson import ObjectId
from fastapi import HTTPException
from api.dto.historical_training_dto import HistoricalTrainingDTO
from api.models.historical_training import HistoricalTraining

from api.models.user import User
from uuid import uuid4

async def add_training_user(user_id: str, training_data: HistoricalTraining):
    try:
        oid = ObjectId(user_id)
    except Exception:
        return {"message": "ID inválido"}
    
    user = await User.find_one(User.id == oid)
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    # Forçar geração se o id estiver ausente
    if not training_data.id:
        training_data.id = str(uuid4())

    user.training.append(training_data)
    await user.save()

    return HistoricalTrainingDTO(**training_data.dict())

async def get_training_user(training_id: str):
    # Busca o usuário que contém esse treino
    user = await User.find_one({"training.id": training_id})
    if not user:
        raise HTTPException(status_code=404, detail="Treino não encontrado")

    # Busca o treino dentro do array do usuário
    treino = next((t for t in user.training if t.id == training_id), None)
    if not treino:
        raise HTTPException(status_code=404, detail="Treino não encontrado")

    return HistoricalTrainingDTO(**treino.dict())