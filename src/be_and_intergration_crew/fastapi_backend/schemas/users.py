from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from uuid import UUID

class UserSchema(BaseModel):
    id: Optional[UUID]
    username: str
    email: EmailStr
    password_hash: str
    created_at: Optional[datetime]
    last_login: Optional[datetime]
    preferences: Optional[dict]

    class Config:
        orm_mode = True