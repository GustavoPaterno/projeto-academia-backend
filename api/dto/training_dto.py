from pydantic import BaseModel

class TrainingDTO(BaseModel):
    nome: str
    type: str
    series: int
    repetitions: int