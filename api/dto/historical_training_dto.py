from typing import List
from uuid import uuid4
from pydantic import BaseModel, Field

from api.dto.training_exercises_dto import TrainingExercisesDTO

class HistoricalTrainingDTO(BaseModel):
    # id: str = Field(default_factory=lambda: str(uuid4()))
    name: str
    type: str
    exercises: List[TrainingExercisesDTO] = Field(default_factory=list)



