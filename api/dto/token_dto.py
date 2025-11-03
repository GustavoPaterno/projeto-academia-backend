from pydantic import BaseModel

# Modelo de token
class Token(BaseModel):
    access_token: str
    token_type: str

# Modelo de dados de token
class TokenData(BaseModel):
    name: str | None = None