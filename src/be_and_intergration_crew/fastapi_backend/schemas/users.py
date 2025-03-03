from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from uuid import UUID
from typing import Union

class UserSchema(BaseModel):
    id: Optional[UUID]
    email: EmailStr
    username: str
    password: str
    created_at: Optional[datetime]
    last_login: Optional[datetime]
    preferences: Optional[dict]

    class Config:
        orm_mode = True

class CurrentUserSchema(BaseModel):
    username: Optional[str]
    email: Optional[str]