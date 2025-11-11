from datetime import date, datetime
from typing import List
from uuid import uuid4
from beanie import Document
from pydantic import BaseModel, Field
from api.dto.training_exercises_dto import TrainingExercisesDTO
from api.models.historical_training import HistoricalTraining
from api.models.training_exercises import TrainingExercises


class Historical(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    name: str
    type: str
    dia: str
    exercises: List[TrainingExercises] = Field(default_factory=list)

    
