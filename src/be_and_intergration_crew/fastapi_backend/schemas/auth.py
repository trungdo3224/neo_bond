from pydantic import BaseModel

class AuthSchema(BaseModel):
    email: str
    password: str

class TokenData(BaseModel):
    username: str | None = None