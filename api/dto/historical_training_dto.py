from uuid import uuid4
from pydantic import BaseModel, Field


class HistoricalTrainingDTO(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    name: str
    type: str
    series: int
    repetitions: int