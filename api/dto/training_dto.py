from pydantic import BaseModel

class TrainingDTO(BaseModel):
    id: int
    nome: str
    type: str
    series: int
    repetitions: int