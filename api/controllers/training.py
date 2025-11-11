
from typing_extensions import Annotated
from fastapi import APIRouter, Depends, HTTPException

from api.dto.historical_training_dto import HistoricalTrainingDTO
from api.dto.training_exercises_dto import TrainingExercisesDTO
from api.models.historical_training import HistoricalTraining
from api.models.training_exercises import TrainingExercises
from api.services import training as training_service
from api.dto.training_dto import TrainingDTO
from api.dto.user_dto import UserDTO
from api.middleware.authentication import token_required


router = APIRouter()

@router.post("/user/{user_id}/training", response_model=HistoricalTrainingDTO)
async def add_training(current_user: Annotated[UserDTO, Depends(token_required)], user_id: str, training_data: HistoricalTraining):
   result = await training_service.add_training_user(user_id, training_data)
   return result

@router.get("/user/{user_id}/training", response_model=HistoricalTrainingDTO)
async def get_training(current_user: Annotated[UserDTO, Depends(token_required)], user_id: str):
   return await training_service.get_training_user(user_id)

@router.post("/user/{user_id}/training/update", response_model=HistoricalTrainingDTO)
async def alter_training(current_user: Annotated[UserDTO, Depends(token_required)], user_id: str, training_data: HistoricalTraining):
   result = await training_service.alter_training_user(user_id, training_data)
   return result

@router.delete("/user/{training_id}/training", response_model=dict)
async def delete_training(training_id: str):
   return await training_service.delete_training_user(training_id)

#################################################################################

@router.post("/user/{user_id}/training/{training_id}/exercise", response_model=TrainingExercisesDTO)
async def add_exercise(user_id: str, training_id: str, exercise: TrainingExercises):
    return await training_service.add_exercises_user(user_id, training_id, exercise)


@router.get("/training/{training_id}/exercises/{exercise_id}", response_model=TrainingExercisesDTO)
async def get_exercise(training_id: str, exercise_id: str):
    return await training_service.get_exercises_user(training_id, exercise_id)


@router.post("/training/{training_id}/exercises/{exercise_id}", response_model=TrainingExercisesDTO)
async def alter_exercise(exercise_id: str, training_id: str, exercise: TrainingExercises):
    return await training_service.alter_exercises_user(exercise_id, training_id, exercise)

@router.delete("/training/{training_id}/exercises/{exercise_id}", response_model=dict)
async def delete_exercises(exercise_id: str, training_id: str):
   return await training_service.delete_exercises_user(exercise_id, training_id)