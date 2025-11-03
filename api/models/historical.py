from datetime import date, datetime
from typing import List
from beanie import Document
from api.models.historical_training import HistoricalTraining


class Historical(Document):
    id: int
    type: str
    dia: str
    training: List[HistoricalTraining]

    
