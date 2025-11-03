from datetime import date, datetime
from typing import List, Optional
from pydantic import BaseModel
from uuid import uuid4, UUID

from pydantic import Field

from api.dto.historical_dto import HistoricalDTO
from api.dto.training_dto import TrainingDTO

class UserDTO(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    name: str
    email: str
    descricao: Optional[str] = None  # Biografia
    birthday: str
    password: str
    genero: str
    level: int
    exp: int
    # photo: Optional[str] = None  # pode guardar caminho/URL
    training: List[TrainingDTO] = []
    historical: List[HistoricalDTO] = []
    
class UserRegisterDto(BaseModel):
    username: str
    password: str
    email: str
    birthday: str
    genero: str
