from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from fastapi_backend.schemas.emotions import EmotionSchema
from fastapi_backend.models.emotions import Emotion
from ..database import get_db

router = APIRouter()

@router.get("/emotions/", response_model=List[EmotionSchema])
def read_emotions(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    emotions = db.query(Emotion).offset(skip).limit(limit).all()
    return emotions

@router.post("/emotions/", response_model=EmotionSchema)
def create_emotion(emotion: EmotionSchema, db: Session = Depends(get_db)):
    db_emotion = Emotion(**emotion.dict())
    db.add(db_emotion)
    db.commit()
    db.refresh(db_emotion)
    return db_emotion

@router.get("/emotions/{emotion_id}", response_model=EmotionSchema)
def read_emotion(emotion_id: str, db: Session = Depends(get_db)):
    emotion = db.query(Emotion).filter(Emotion.id == emotion_id).first()
    if emotion is None:
        raise HTTPException(status_code=404, detail="Emotion not found")
    return emotion

@router.get("/emotions/user/{user_id}", response_model=List[EmotionSchema])
def read_user_emotions(user_id: str, db: Session = Depends(get_db)):
    emotions = db.query(Emotion).filter(Emotion.user_id == user_id).all()
    return emotions

@router.get("/emotions/conversation/{conversation_id}", response_model=List[EmotionSchema])
def read_conversation_emotions(conversation_id: str, db: Session = Depends(get_db)):
    emotions = db.query(Emotion).filter(Emotion.conversation_id == conversation_id).all()
    return emotions

@router.put("/emotions/{emotion_id}", response_model=EmotionSchema)
def update_emotion(emotion_id: str, emotion: EmotionSchema, db: Session = Depends(get_db)):
    db_emotion = db.query(Emotion).filter(Emotion.id == emotion_id).first()
    if db_emotion is None:
        raise HTTPException(status_code=404, detail="Emotion not found")
    for key, value in emotion.dict(exclude_unset=True).items():
        setattr(db_emotion, key, value)
    db.commit()
    db.refresh(db_emotion)
    return db_emotion

@router.delete("/emotions/{emotion_id}", response_model=EmotionSchema)
def delete_emotion(emotion_id: str, db: Session = Depends(get_db)):
    emotion = db.query(Emotion).filter(Emotion.id == emotion_id).first()
    if emotion is None:
        raise HTTPException(status_code=404, detail="Emotion not found")
    db.delete(emotion)
    db.commit()
    return emotion
