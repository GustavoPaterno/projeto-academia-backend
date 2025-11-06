from bson import ObjectId
from fastapi import HTTPException
from api.dto.historical_training_dto import HistoricalTrainingDTO
from api.models.historical_training import HistoricalTraining

from api.models.user import User

# async def add_training_user(user_id: str, training_dto: HistoricalTraining):
#     try:
#         oid = ObjectId(user_id)
#     except Exception:
#         return {"message": "ID inválido"}
    
#     user = await User.find_one(User.id == oid)
#     if not user:
#         raise HTTPException(status_code=404, detail="Usuário não encontrado")

#     user.training.append(training_dto)
#     await user.save()
#     return training_dto


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
