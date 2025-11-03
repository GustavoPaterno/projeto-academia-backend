from beanie import Document

class HistoricalTraining(Document):
    name: str
    series: int
    repetitions: int