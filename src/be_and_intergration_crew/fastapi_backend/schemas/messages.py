from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from uuid import UUID

class MessageSchema(BaseModel):
    id: Optional[UUID]
    conversation_id: UUID
    sender_type: str
    sender_id: Optional[UUID]
    message_text: str
    timestamp: Optional[datetime]
    ai_response_metadata: Optional[dict]

    class Config:
        orm_mode = True
