from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from uuid import UUID

class EmotionSchema(BaseModel):
    id: Optional[UUID]
    user_id: UUID
    conversation_id: UUID
    detected_emotion: str
    confidence: float
    detected_at: Optional[datetime]

    class Config:
        orm_mode = True
