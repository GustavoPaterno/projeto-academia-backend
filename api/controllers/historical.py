
from typing_extensions import Annotated
from fastapi import APIRouter, Depends, HTTPException


from api.dto.historical_dto import HistoricalDTO
from api.dto.training_exercises_dto import TrainingExercisesDTO
from api.models.historical import Historical
from api.models.historical_training import HistoricalTraining
from api.models.training_exercises import TrainingExercises
from api.services import historical as historical_service
from api.dto.training_dto import TrainingDTO
from api.dto.user_dto import UserDTO
from api.middleware.authentication import token_required


router = APIRouter()

@router.post("/user/{user_id}/historical", response_model=HistoricalDTO)
async def add_training(user_id: str, current_user: Annotated[UserDTO, Depends(token_required)], training_data: Historical):
    result = await historical_service.add_historical_user(user_id, training_data)
    return result

@router.get("/user/{user_id}/historical", response_model=HistoricalDTO)
async def get_training(current_user: Annotated[UserDTO, Depends(token_required)], user_id: str):
   return await historical_service.get_historical_user(user_id)

@router.post("/user/{user_id}/historical/update", response_model=HistoricalDTO)
async def alter_training(current_user: Annotated[UserDTO, Depends(token_required)], user_id: str, training_data: Historical):
   result = await historical_service.alter_historical_user(user_id, training_data)
   return result

@router.delete("/user/{training_id}/historical", response_model=dict)
async def delete_training(training_id: str):
   return await historical_service.delete_historical_user(training_id)

#################################################################################

@router.post("/user/{user_id}/historical/{training_id}/exercise", response_model=TrainingExercisesDTO)
async def add_exercise(user_id: str, training_id: str, exercise: TrainingExercises):
    return await historical_service.add_exercises_historical(user_id, training_id, exercise)

@router.get("/training/{training_id}/historical/{exercise_id}", response_model=TrainingExercisesDTO)
async def get_exercise_historical(training_id: str, exercise_id: str):
    return await historical_service.get_exercises_historical(training_id, exercise_id)

@router.post("/training/{training_id}/historical/{exercise_id}", response_model=TrainingExercisesDTO)
async def alter_exercise_historical(exercise_id: str, training_id: str, exercise: TrainingExercises):
    return await historical_service.alter_exercises_historical(exercise_id, training_id, exercise)

@router.delete("/training/{training_id}/historical/{exercise_id}", response_model=dict)
async def delete_exercises_historical(exercise_id: str, training_id: str):
   return await historical_service.delete_exercises_historical(exercise_id, training_id)