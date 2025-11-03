from pydantic import BaseModel


class HistoricalTrainingDTO(BaseModel):
    name: str
    series: int
    repetitions: int