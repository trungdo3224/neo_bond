from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from uuid import UUID

class SpeechInputSchema(BaseModel):
    id: Optional[UUID]
    user_id: UUID
    conversation_id: UUID
    transcript: str
    audio_url: Optional[str]
    processed_at: Optional[datetime]

    class Config:
        orm_mode = True
