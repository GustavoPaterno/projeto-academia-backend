from bson import ObjectId
from fastapi import HTTPException
from api.dto.historical_dto import HistoricalDTO
from api.dto.historical_training_dto import HistoricalTrainingDTO
from api.dto.training_exercises_dto import TrainingExercisesDTO
from api.models.historical import Historical
from api.models.training_exercises import TrainingExercises
from api.models.historical_training import HistoricalTraining

from api.models.user import User
from uuid import uuid4

async def add_historical_user(user_id: str, historical_data: Historical):
    try:
        oid = ObjectId(user_id)
    except Exception:
        return {"message": "ID inválido"}
    
    user = await User.find_one(User.id == oid)
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    # Forçar geração se o id estiver ausente
    if not historical_data.id:
        historical_data.id = str(uuid4())

    user.historical.append(historical_data)
    await user.save()

    return HistoricalDTO(**historical_data.dict())

async def get_historical_user(historical_id: str):
    user = await User.find_one({"historical.id": historical_id})
    if not user:
        raise HTTPException(status_code=404, detail="usuario não encontrado")

    historical = next((t for t in user.historical if t.id == historical_id), None)
    if not historical:
        raise HTTPException(status_code=404, detail="historico não encontrado")

    return HistoricalDTO(**historical.dict())

async def alter_historical_user(user_id: str, historical_data: Historical):
    user = await User.find_one({"historical.id": user_id})
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    historical = next((t for t in user.historical if t.id == user_id), None)
    if not historical:
        raise HTTPException(status_code=404, detail="historico não encontrado")

    historical.name = historical_data.name
    historical.type = historical_data.type
    historical.dia = historical_data.dia
    historical.exercises = historical_data.exercises

    await user.save()

    return HistoricalDTO(**historical.dict())


async def delete_historical_user(historico_id: str):

    user = await User.find_one({"historico.id": historico_id})
    if not user:
        raise HTTPException(status_code=404, detail="user não encontrado")
    
    historical = next((t for t in user.historical if t.id == historico_id), None)
    if not historical:
        raise HTTPException(status_code=404, detail="historico não encontrado")
    
    user.historical = [t for t in user.historical if t.id != historico_id]
    await user.save()
    return {"message": "historico deletado"}


###########################################

async def add_exercises_historical(user_id: str, historico_id: str, exercises_data: TrainingExercises):
    try:
        oid = ObjectId(user_id)
    except Exception:
        raise HTTPException(status_code=400, detail="ID de usuário inválido")
    
    user = await User.find_one(User.id == oid)
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    historical = next((t for t in user.historical if t.id == historico_id), None)
    if not historical:
        raise HTTPException(status_code=404, detail="historico não encontrado")

    # Gera id se não tiver
    if not exercises_data.id:
        exercises_data.id = str(uuid4())

    historical.exercises.append(exercises_data)

    await user.save()

    # Retorna o exercício adicionado como DTO
    return TrainingExercisesDTO(**exercises_data.dict())

async def get_exercises_historical(historical_id: str, exercise_id: str):

    user = await User.find_one({"historical.id": historical_id})
    if not user:
        raise HTTPException(status_code=404, detail="user não encontrado")

    historical = next((t for t in user.historical if t.id == historical_id), None)
    if not historical:
        raise HTTPException(status_code=404, detail="historico não encontrado")

    exercicio = next((e for e in historical.exercises if e.id == exercise_id), None)
    if not exercicio:
        raise HTTPException(status_code=404, detail="Exercício não encontrado")

    # 4️⃣ Retorna o DTO do exercício encontrado
    return TrainingExercisesDTO(**exercicio.dict())


async def alter_exercises_historical(exercise_id: str, historical_id: str, exercise_data: TrainingExercises):

    user = await User.find_one({"historical.id": historical_id})
    if not user:
        raise HTTPException(status_code=404, detail="user não encontrado")

    historical = next((t for t in user.historical if t.id == historical_id), None)
    if not historical:
        raise HTTPException(status_code=404, detail="historico não encontrado")

    exercicio = next((e for e in historical.exercises if e.id == exercise_id), None)
    if not exercicio:
        raise HTTPException(status_code=404, detail="Exercício não encontrado")

    exercicio.name = exercise_data.name
    exercicio.series = exercise_data.series
    exercicio.type = exercise_data.type
    exercicio.repetitions = exercise_data.repetitions

    await user.save()

    return TrainingExercisesDTO(**exercicio.dict())


async def delete_exercises_historical(exercise_id: str , historical_id: str):

    user = await User.find_one({"historical.id": historical_id})
    if not user:
        raise HTTPException(status_code=404, detail="user não encontrado")
    
    historical = next((t for t in user.historical if t.id == historical_id), None)
    if not historical:
        raise HTTPException(status_code=404, detail="historico não encontrado")
    
    exercicio = next((e for e in historical.exercises if e.id == exercise_id), None)
    if not exercicio:
        raise HTTPException(status_code=404, detail="Exercício não encontrado")
    
    historical.exercises = [t for t in historical.exercises if t.id != exercise_id]
    await user.save()
    return {"message": "historico deletado"}
