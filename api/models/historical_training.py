from uuid import uuid4
from pydantic import BaseModel, Field

class HistoricalTraining(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    name: str
    series: int
    type: str
    repetitions: int
