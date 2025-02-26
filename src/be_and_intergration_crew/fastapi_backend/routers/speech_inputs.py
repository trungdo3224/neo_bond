from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from fastapi_backend.schemas.speech_inputs import SpeechInputSchema
from fastapi_backend.models.speech_inputs import SpeechInput
from fastapi_backend.database import get_db

router = APIRouter()
databaseSession = Depends(get_db)

@router.get("/speech-inputs/", response_model=List[SpeechInputSchema])
def read_speech_inputs(skip: int = 0, limit: int = 10, db: Session = databaseSession):
    inputs = db.query(SpeechInput).offset(skip).limit(limit).all()
    return inputs

@router.post("/speech-inputs/", response_model=SpeechInputSchema)
def create_speech_input(speech_input: SpeechInputSchema, db: Session = databaseSession):
    db_speech_input = SpeechInput(**speech_input.dict())
    db.add(db_speech_input)
    db.commit()
    db.refresh(db_speech_input)
    return db_speech_input

@router.get("/speech-inputs/{input_id}", response_model=SpeechInputSchema)
def read_speech_input(input_id: str, db: Session = databaseSession):
    speech_input = db.query(SpeechInput).filter(SpeechInput.id == input_id).first()
    if speech_input is None:
        raise HTTPException(status_code=404, detail="Speech input not found")
    return speech_input

@router.get("/speech-inputs/user/{user_id}", response_model=List[SpeechInputSchema])
def read_user_speech_inputs(user_id: str, db: Session = databaseSession):
    inputs = db.query(SpeechInput).filter(SpeechInput.user_id == user_id).all()
    return inputs

@router.get("/speech-inputs/conversation/{conversation_id}", response_model=List[SpeechInputSchema])
def read_conversation_speech_inputs(conversation_id: str, db: Session = databaseSession):
    inputs = db.query(SpeechInput).filter(SpeechInput.conversation_id == conversation_id).all()
    return inputs

@router.put("/speech-inputs/{input_id}", response_model=SpeechInputSchema)
def update_speech_input(input_id: str, speech_input: SpeechInputSchema, db: Session = databaseSession):
    db_speech_input = db.query(SpeechInput).filter(SpeechInput.id == input_id).first()
    if db_speech_input is None:
        raise HTTPException(status_code=404, detail="Speech input not found")
    for key, value in speech_input.dict(exclude_unset=True).items():
        setattr(db_speech_input, key, value)
    db.commit()
    db.refresh(db_speech_input)
    return db_speech_input

@router.delete("/speech-inputs/{input_id}", response_model=SpeechInputSchema)
def delete_speech_input(input_id: str, db: Session = databaseSession):
    speech_input = db.query(SpeechInput).filter(SpeechInput.id == input_id).first()
    if speech_input is None:
        raise HTTPException(status_code=404, detail="Speech input not found")
    db.delete(speech_input)
    db.commit()
    return speech_input
