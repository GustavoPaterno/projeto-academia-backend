from pydantic import BaseModel, Field
from beanie import Document
from typing import Optional


class Training(Document):
    nome: str
    type: str
    series: int
    repetitions: int