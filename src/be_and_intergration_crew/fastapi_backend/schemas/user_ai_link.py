from pydantic import BaseModel
from uuid import UUID

class UserAILinkSchema(BaseModel):
    user_id: UUID
    ai_id: UUID

    class Config:
        orm_mode = True