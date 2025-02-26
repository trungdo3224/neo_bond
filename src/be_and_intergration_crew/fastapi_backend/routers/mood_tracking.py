from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from fastapi_backend.schemas.mood_tracking import MoodTrackingSchema
from fastapi_backend.models.mood_tracking import MoodTracking
from fastapi_backend.database import get_db

router = APIRouter()

@router.get("/mood-tracking/", response_model=List[MoodTrackingSchema])
def read_mood_trackings(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    moods = db.query(MoodTracking).offset(skip).limit(limit).all()
    return moods

@router.post("/mood-tracking/", response_model=MoodTrackingSchema)
def create_mood_tracking(mood: MoodTrackingSchema, db: Session = Depends(get_db)):
    db_mood = MoodTracking(**mood.dict())
    db.add(db_mood)
    db.commit()
    db.refresh(db_mood)
    return db_mood

@router.get("/mood-tracking/{mood_id}", response_model=MoodTrackingSchema)
def read_mood_tracking(mood_id: str, db: Session = Depends(get_db)):
    mood = db.query(MoodTracking).filter(MoodTracking.id == mood_id).first()
    if mood is None:
        raise HTTPException(status_code=404, detail="Mood tracking not found")
    return mood

@router.get("/mood-tracking/user/{user_id}", response_model=List[MoodTrackingSchema])
def read_user_mood_trackings(user_id: str, db: Session = Depends(get_db)):
    moods = db.query(MoodTracking).filter(MoodTracking.user_id == user_id).all()
    return moods

@router.put("/mood-tracking/{mood_id}", response_model=MoodTrackingSchema)
def update_mood_tracking(mood_id: str, mood: MoodTrackingSchema, db: Session = Depends(get_db)):
    db_mood = db.query(MoodTracking).filter(MoodTracking.id == mood_id).first()
    if db_mood is None:
        raise HTTPException(status_code=404, detail="Mood tracking not found")
    for key, value in mood.dict(exclude_unset=True).items():
        setattr(db_mood, key, value)
    db.commit()
    db.refresh(db_mood)
    return db_mood

@router.delete("/mood-tracking/{mood_id}", response_model=MoodTrackingSchema)
def delete_mood_tracking(mood_id: str, db: Session = Depends(get_db)):
    mood = db.query(MoodTracking).filter(MoodTracking.id == mood_id).first()
    if mood is None:
        raise HTTPException(status_code=404, detail="Mood tracking not found")
    db.delete(mood)
    db.commit()
    return mood
