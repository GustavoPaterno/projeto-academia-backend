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

    user = await User.find_one({"training.id": training_id})
    if not user:
        raise HTTPException(status_code=404, detail="user não encontrado")
    
    treino = next((t for t in user.training if t.id == training_id), None)
    if not treino:
        raise HTTPException(status_code=404, detail="Treino não encontrado")
    
    user.training = [t for t in user.training if t.id != training_id]
    await user.save()
    return {"message": "treino deletado"}


###########################################

async def add_exercises_user(user_id: str, training_id: str, exercises_data: TrainingExercises):
    try:
        oid = ObjectId(user_id)
    except Exception:
        raise HTTPException(status_code=400, detail="ID de usuário inválido")
    
    user = await User.find_one(User.id == oid)
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    # Encontra o treino dentro da lista de treinos do usuário
    treino = next((t for t in user.training if t.id == training_id), None)
    if not treino:
        raise HTTPException(status_code=404, detail="Treino não encontrado")

    # Gera id se não tiver
    if not exercises_data.id:
        exercises_data.id = str(uuid4())

    # Adiciona o exercício ao treino
    treino.exercises.append(exercises_data)

    # Salva o usuário com a lista de treinos atualizada
    await user.save()

    # Retorna o exercício adicionado como DTO
    return TrainingExercisesDTO(**exercises_data.dict())

async def get_exercises_user(training_id: str, exercise_id: str):

    user = await User.find_one({"training.id": training_id})
    if not user:
        raise HTTPException(status_code=404, detail="Treino não encontrado")

    # 2️⃣ Busca o treino dentro do usuário
    treino = next((t for t in user.training if t.id == training_id), None)
    if not treino:
        raise HTTPException(status_code=404, detail="Treino não encontrado")

    # 3️⃣ Busca o exercício dentro do treino
    exercicio = next((e for e in treino.exercises if e.id == exercise_id), None)
    if not exercicio:
        raise HTTPException(status_code=404, detail="Exercício não encontrado")

    # 4️⃣ Retorna o DTO do exercício encontrado
    return TrainingExercisesDTO(**exercicio.dict())


async def alter_exercises_user(exercise_id: str, training_id: str, exercise_data: TrainingExercises):

    user = await User.find_one({"training.id": training_id})
    if not user:
        raise HTTPException(status_code=404, detail="Treino não encontrado")

    treino = next((t for t in user.training if t.id == training_id), None)
    if not treino:
        raise HTTPException(status_code=404, detail="Treino não encontrado")

    exercicio = next((e for e in treino.exercises if e.id == exercise_id), None)
    if not exercicio:
        raise HTTPException(status_code=404, detail="Exercício não encontrado")

    exercicio.name = exercise_data.name
    exercicio.series = exercise_data.series
    exercicio.type = exercise_data.type
    exercicio.repetitions = exercise_data.repetitions

    await user.save()

    return TrainingExercisesDTO(**exercicio.dict())


async def delete_exercises_user(exercise_id: str ,training_id: str):

    user = await User.find_one({"training.id": training_id})
    if not user:
        raise HTTPException(status_code=404, detail="user não encontrado")
    
    treino = next((t for t in user.training if t.id == training_id), None)
    if not treino:
        raise HTTPException(status_code=404, detail="Treino não encontrado")
    
    exercicio = next((e for e in treino.exercises if e.id == exercise_id), None)
    if not exercicio:
        raise HTTPException(status_code=404, detail="Exercício não encontrado")
    
    treino.exercises = [t for t in treino.exercises if t.id != exercise_id]
    await user.save()
    return {"message": "treino deletado"}
