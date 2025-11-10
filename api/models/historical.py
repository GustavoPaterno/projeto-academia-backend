from datetime import date, datetime
from typing import List
from uuid import uuid4
from beanie import Document
from pydantic import BaseModel, Field
from api.models.historical_training import HistoricalTraining


class Historical(Document):
    type: str
    dia: str
    training: List[HistoricalTraining]

    
