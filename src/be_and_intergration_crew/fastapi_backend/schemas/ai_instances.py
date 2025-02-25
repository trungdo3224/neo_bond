from pydantic import BaseModel
from typing import Optional, List
from uuid import UUID

class AIInstanceSchema(BaseModel):
    id: Optional[UUID]
    name: str
    description: Optional[str]
    skill_sets: Optional[List[str]]
    personality: Optional[dict]

    class Config:
        orm_mode = True