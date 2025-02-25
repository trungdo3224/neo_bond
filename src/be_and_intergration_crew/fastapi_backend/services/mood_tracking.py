from sqlalchemy.orm import Session
from typing import List, Optional
from fastapi_backend.models.mood_tracking import MoodTracking
from fastapi_backend.schemas.mood_tracking import MoodTrackingSchema

class MoodTrackingService:
    def __init__(self, db: Session):
        self.db = db

    def get_mood_trackings(self, skip: int = 0, limit: int = 10) -> List[MoodTracking]:
        return self.db.query(MoodTracking).offset(skip).limit(limit).all()

    def get_mood_tracking_by_id(self, mood_id: str) -> Optional[MoodTracking]:
        return self.db.query(MoodTracking).filter(MoodTracking.id == mood_id).first()

    def get_user_mood_trackings(self, user_id: str) -> List[MoodTracking]:
        return self.db.query(MoodTracking)\
            .filter(MoodTracking.user_id == user_id)\
            .order_by(MoodTracking.timestamp.desc())\
            .all()

    def create_mood_tracking(self, mood: MoodTrackingSchema) -> MoodTracking:
        db_mood = MoodTracking(**mood.dict())
        self.db.add(db_mood)
        self.db.commit()
        self.db.refresh(db_mood)
        return db_mood

    def update_mood_tracking(self, mood_id: str, mood: MoodTrackingSchema) -> Optional[MoodTracking]:
        db_mood = self.get_mood_tracking_by_id(mood_id)
        if not db_mood:
            return None
        
        # Update mood tracking fields
        for key, value in mood.dict(exclude_unset=True).items():
            setattr(db_mood, key, value)
        
        self.db.commit()
        self.db.refresh(db_mood)
        return db_mood

    def delete_mood_tracking(self, mood_id: str) -> Optional[MoodTracking]:
        mood = self.get_mood_tracking_by_id(mood_id)
        if not mood:
            return None
        
        self.db.delete(mood)
        self.db.commit()
        return mood

    def get_user_latest_mood(self, user_id: str) -> Optional[MoodTracking]:
        return self.db.query(MoodTracking)\
            .filter(MoodTracking.user_id == user_id)\
            .order_by(MoodTracking.timestamp.desc())\
            .first()

    def get_user_mood_history(self, user_id: str, limit: int = 10) -> List[MoodTracking]:
        return self.db.query(MoodTracking)\
            .filter(MoodTracking.user_id == user_id)\
            .order_by(MoodTracking.timestamp.desc())\
            .limit(limit)\
            .all()
