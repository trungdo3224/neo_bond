from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from fastapi_backend.schemas.conversations import ConversationSchema
from fastapi_backend.models.conversations import Conversation
from ..database import get_db

router = APIRouter()

@router.get("/conversations/", response_model=List[ConversationSchema])
def read_conversations(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    conversations = db.query(Conversation).offset(skip).limit(limit).all()
    return conversations

@router.post("/conversations/", response_model=ConversationSchema)
def create_conversation(conversation: ConversationSchema, db: Session = Depends(get_db)):
    db_conversation = Conversation(**conversation.dict())
    db.add(db_conversation)
    db.commit()
    db.refresh(db_conversation)
    return db_conversation

@router.get("/conversations/{conversation_id}", response_model=ConversationSchema)
def read_conversation(conversation_id: str, db: Session = Depends(get_db)):
    conversation = db.query(Conversation).filter(Conversation.id == conversation_id).first()
    if conversation is None:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return conversation

@router.get("/conversations/user/{user_id}", response_model=List[ConversationSchema])
def read_user_conversations(user_id: str, db: Session = Depends(get_db)):
    conversations = db.query(Conversation).filter(Conversation.user_id == user_id).all()
    return conversations

@router.put("/conversations/{conversation_id}", response_model=ConversationSchema)
def update_conversation(conversation_id: str, conversation: ConversationSchema, db: Session = Depends(get_db)):
    db_conversation = db.query(Conversation).filter(Conversation.id == conversation_id).first()
    if db_conversation is None:
        raise HTTPException(status_code=404, detail="Conversation not found")
    for key, value in conversation.dict(exclude_unset=True).items():
        setattr(db_conversation, key, value)
    db.commit()
    db.refresh(db_conversation)
    return db_conversation

@router.delete("/conversations/{conversation_id}", response_model=ConversationSchema)
def delete_conversation(conversation_id: str, db: Session = Depends(get_db)):
    conversation = db.query(Conversation).filter(Conversation.id == conversation_id).first()
    if conversation is None:
        raise HTTPException(status_code=404, detail="Conversation not found")
    db.delete(conversation)
    db.commit()
    return conversation
