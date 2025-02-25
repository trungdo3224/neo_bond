from sqlalchemy.orm import Session
from typing import List, Optional
from fastapi_backend.models.emotions import Emotion
from fastapi_backend.schemas.emotions import EmotionSchema

class EmotionService:
    def __init__(self, db: Session):
        self.db = db

    def get_emotions(self, skip: int = 0, limit: int = 10) -> List[Emotion]:
        return self.db.query(Emotion).offset(skip).limit(limit).all()

    def get_emotion_by_id(self, emotion_id: str) -> Optional[Emotion]:
        return self.db.query(Emotion).filter(Emotion.id == emotion_id).first()

    def get_user_emotions(self, user_id: str) -> List[Emotion]:
        return self.db.query(Emotion)\
            .filter(Emotion.user_id == user_id)\
            .order_by(Emotion.detected_at.desc())\
            .all()

    def get_conversation_emotions(self, conversation_id: str) -> List[Emotion]:
        return self.db.query(Emotion)\
            .filter(Emotion.conversation_id == conversation_id)\
            .order_by(Emotion.detected_at.asc())\
            .all()

    def create_emotion(self, emotion: EmotionSchema) -> Emotion:
        db_emotion = Emotion(**emotion.dict())
        self.db.add(db_emotion)
        self.db.commit()
        self.db.refresh(db_emotion)
        return db_emotion

    def update_emotion(self, emotion_id: str, emotion: EmotionSchema) -> Optional[Emotion]:
        db_emotion = self.get_emotion_by_id(emotion_id)
        if not db_emotion:
            return None
        
        # Update emotion fields
        for key, value in emotion.dict(exclude_unset=True).items():
            setattr(db_emotion, key, value)
        
        self.db.commit()
        self.db.refresh(db_emotion)
        return db_emotion

    def delete_emotion(self, emotion_id: str) -> Optional[Emotion]:
        emotion = self.get_emotion_by_id(emotion_id)
        if not emotion:
            return None
        
        self.db.delete(emotion)
        self.db.commit()
        return emotion

    def get_user_latest_emotion(self, user_id: str) -> Optional[Emotion]:
        return self.db.query(Emotion)\
            .filter(Emotion.user_id == user_id)\
            .order_by(Emotion.detected_at.desc())\
            .first()
