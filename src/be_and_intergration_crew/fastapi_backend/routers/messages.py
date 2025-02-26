from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from fastapi_backend.schemas.messages import MessageSchema
from fastapi_backend.models.messages import Message
from fastapi_backend.database import get_db

router = APIRouter()

@router.get("/messages/", response_model=List[MessageSchema])
def read_messages(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    messages = db.query(Message).offset(skip).limit(limit).all()
    return messages

@router.post("/messages/", response_model=MessageSchema)
def create_message(message: MessageSchema, db: Session = Depends(get_db)):
    db_message = Message(**message.dict())
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message

@router.get("/messages/{message_id}", response_model=MessageSchema)
def read_message(message_id: str, db: Session = Depends(get_db)):
    message = db.query(Message).filter(Message.id == message_id).first()
    if message is None:
        raise HTTPException(status_code=404, detail="Message not found")
    return message

@router.get("/messages/conversation/{conversation_id}", response_model=List[MessageSchema])
def read_conversation_messages(conversation_id: str, db: Session = Depends(get_db)):
    messages = db.query(Message).filter(Message.conversation_id == conversation_id).all()
    return messages

@router.put("/messages/{message_id}", response_model=MessageSchema)
def update_message(message_id: str, message: MessageSchema, db: Session = Depends(get_db)):
    db_message = db.query(Message).filter(Message.id == message_id).first()
    if db_message is None:
        raise HTTPException(status_code=404, detail="Message not found")
    for key, value in message.dict(exclude_unset=True).items():
        setattr(db_message, key, value)
    db.commit()
    db.refresh(db_message)
    return db_message

@router.delete("/messages/{message_id}", response_model=MessageSchema)
def delete_message(message_id: str, db: Session = Depends(get_db)):
    message = db.query(Message).filter(Message.id == message_id).first()
    if message is None:
        raise HTTPException(status_code=404, detail="Message not found")
    db.delete(message)
    db.commit()
    return message
