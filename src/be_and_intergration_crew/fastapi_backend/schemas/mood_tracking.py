from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from uuid import UUID

class MoodTrackingSchema(BaseModel):
    id: Optional[UUID]
    user_id: UUID
    mood: str
    timestamp: Optional[datetime]
    suggested_movie_id: Optional[UUID]

    class Config:
        orm_mode = True
