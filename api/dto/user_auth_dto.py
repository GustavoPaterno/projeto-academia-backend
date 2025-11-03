from pydantic import BaseModel

# Modelo de user data transfer object
class UserAuthDto(BaseModel):
    username: str
    password: str