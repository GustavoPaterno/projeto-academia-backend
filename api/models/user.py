from datetime import date, datetime
from typing import List, Optional
from beanie import Document, Indexed
from uuid import uuid4, UUID
from typing import Optional, Annotated

from pydantic import Field

from api.models.historical import Historical
from api.models.historical_training import HistoricalTraining
from api.models.training import Training

class User(Document):
    name: str
    email: Annotated[str, Indexed(unique=True)]
    descricao: Optional[str] = None  
    birthday: str
    password: str
    genero: str
    level: int
    exp: int
    # photo: Optional[str] = None  
    training: List[HistoricalTraining] = Field(default_factory=list)
    historical: List[Historical] = Field(default_factory=list)
