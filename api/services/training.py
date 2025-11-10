from bson import ObjectId
from fastapi import HTTPException
from api.dto.historical_training_dto import HistoricalTrainingDTO
from api.dto.training_exercises_dto import TrainingExercisesDTO
from api.models.training_exercises import TrainingExercises
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

async def alter_training_user(user_id: str, training_data: HistoricalTraining):
    user = await User.find_one({"training.id": user_id})
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    treino = next((t for t in user.training if t.id == user_id), None)
    if not treino:
        raise HTTPException(status_code=404, detail="Treino não encontrado")

    treino.name = training_data.name
    treino.type = training_data.type
    treino.exercises = training_data.exercises

    await user.save()

    return HistoricalTrainingDTO(**treino.dict())

async def delete_training_user(training_id: str):
    # 1️⃣ Achar o usuário que contém o treino
    user = await User.find_one({"training.id": training_id})
    if not user:
        raise HTTPException(status_code=404, detail="Treino não encontrado")

    # 2️⃣ Filtrar o treino fora da lista
    original_count = len(user.training)
    user.training = [t for t in user.training if t.id != training_id]

    # 3️⃣ Se nada foi removido, treino não existia
    if len(user.training) == original_count:
        raise HTTPException(status_code=404, detail="Treino não encontrado")

    # 4️⃣ Salvar o usuário com a lista atualizada
    await user.save()

    # 5️⃣ Retornar mensagem de sucesso
    return {"message": "Treino removido com sucesso"}

###########################################

# async def add_exercises_user(user_id: str, training_data: TrainingExercises):
#     try:
#         oid = ObjectId(user_id)
#     except Exception:
#         return {"message": "ID inválido"}
    
#     user = await User.find_one(User.id == oid)
#     if not user:
#         raise HTTPException(status_code=404, detail="Usuário não encontrado")

#     # Forçar geração se o id estiver ausente
#     if not training_data.id:
#         training_data.id = str(uuid4())

#     user.training.append(training_data)
#     await user.save()

#     return HistoricalTrainingDTO(**training_data.dict())

# async def get_exercises_user(training_id: str):
#     # Busca o usuário que contém esse treino
#     user = await User.find_one({"training.id": training_id})
#     if not user:
#         raise HTTPException(status_code=404, detail="Treino não encontrado")

#     # Busca o treino dentro do array do usuário
#     treino = next((t for t in user.training if t.id == training_id), None)
#     if not treino:
#         raise HTTPException(status_code=404, detail="Treino não encontrado")

#     return HistoricalTrainingDTO(**treino.dict())

# async def alter_exercises_user(user_id: str, training_data: TrainingExercises):
#     user = await User.find_one({"training.id": user_id})
#     if not user:
#         raise HTTPException(status_code=404, detail="Usuário não encontrado")

#     treino = next((t for t in user.training if t.id == user_id), None)
#     if not treino:
#         raise HTTPException(status_code=404, detail="Treino não encontrado")

#     treino.name = training_data.name
#     treino.series = training_data.series
#     treino.type = training_data.type
#     treino.repetitions = training_data.repetitions

#     await user.save()

#     return TrainingExercisesDTO(**treino.dict())

# async def delete_exercises_user(training_id: str):
#     # 1️⃣ Achar o usuário que contém o treino
#     user = await User.find_one({"training.id": training_id})
#     if not user:
#         raise HTTPException(status_code=404, detail="Treino não encontrado")

#     # 2️⃣ Filtrar o treino fora da lista
#     original_count = len(user.training)
#     user.training = [t for t in user.training if t.id != training_id]

#     # 3️⃣ Se nada foi removido, treino não existia
#     if len(user.training) == original_count:
#         raise HTTPException(status_code=404, detail="Treino não encontrado")

#     # 4️⃣ Salvar o usuário com a lista atualizada
#     await user.save()

#     # 5️⃣ Retornar mensagem de sucesso
#     return {"message": "Treino removido com sucesso"}
