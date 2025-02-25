from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from uuid import UUID

class AIResponseSchema(BaseModel):
    id: Optional[UUID]
    conversation_id: UUID
    response_text: str
    audio_url: Optional[str]
    generated_at: Optional[datetime]

    class Config:
        orm_mode = True
