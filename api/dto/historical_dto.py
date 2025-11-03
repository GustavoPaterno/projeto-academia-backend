from datetime import date, datetime
from typing import List
from pydantic import BaseModel

from api.dto.historical_training_dto import HistoricalTrainingDTO


class HistoricalDTO(BaseModel):
    id: int
    type: str
    dia: str
    training: List[HistoricalTrainingDTO]

    
