from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from uuid import UUID

class ConversationSchema(BaseModel):
    id: Optional[UUID]
    user_id: UUID
    ai_id: UUID
    start_time: Optional[datetime]
    end_time: Optional[datetime]
    metadata: Optional[dict]

    class Config:
        orm_mode = True
