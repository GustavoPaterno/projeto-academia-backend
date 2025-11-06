
from typing_extensions import Annotated
from fastapi import APIRouter, Depends, HTTPException

from api.dto.historical_training_dto import HistoricalTrainingDTO
from api.models.historical_training import HistoricalTraining
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