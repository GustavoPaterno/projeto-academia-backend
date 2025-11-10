from typing import List
from uuid import uuid4
from pydantic import BaseModel, Field

from api.models.training_exercises  import TrainingExercises

class HistoricalTraining(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    name: str
    type: str
    exercises: List[TrainingExercises] = Field(default_factory=list)



