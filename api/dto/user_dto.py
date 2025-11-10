from datetime import date, datetime
from typing import List, Optional
from pydantic import BaseModel
from uuid import uuid4, UUID

from pydantic import Field

from api.dto.historical_dto import HistoricalDTO
from api.dto.historical_training_dto import HistoricalTrainingDTO
from api.dto.training_dto import TrainingDTO

class UserDTO(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    name: str
    email: str
    descricao: Optional[str] = None  # Biografia
    birthday: str
    password: str
    genero: str
    level: int
    exp: int
    training: List[HistoricalTrainingDTO] = []
    historical: List[HistoricalDTO] = []

    class Config:
        allow_population_by_field_name = True
    
class UserRegisterDto(BaseModel):
    name: str
    email: str
    descricao: Optional[str] = None  # Biografia
    birthday: str
    password: str
    genero: str
    level: int
    exp: int
    # photo: Optional[str] = None  # pode guardar caminho/URL
    training: List[HistoricalTrainingDTO] = []
    historical: List[HistoricalDTO] = []

    