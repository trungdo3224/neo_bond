from sqlalchemy.orm import Session
from typing import List, Optional
from fastapi_backend.models.conversations import Conversation
from fastapi_backend.schemas.conversations import ConversationSchema
from datetime import datetime

class ConversationService:
    def __init__(self, db: Session):
        self.db = db

    def get_conversations(self, skip: int = 0, limit: int = 10) -> List[Conversation]:
        return self.db.query(Conversation).offset(skip).limit(limit).all()

    def get_conversation_by_id(self, conversation_id: str) -> Optional[Conversation]:
        return self.db.query(Conversation).filter(Conversation.id == conversation_id).first()

    def get_user_conversations(self, user_id: str) -> List[Conversation]:
        return self.db.query(Conversation).filter(Conversation.user_id == user_id).all()

    def create_conversation(self, conversation: ConversationSchema) -> Conversation:
        db_conversation = Conversation(**conversation.dict())
        self.db.add(db_conversation)
        self.db.commit()
        self.db.refresh(db_conversation)
        return db_conversation

    def update_conversation(self, conversation_id: str, conversation: ConversationSchema) -> Optional[Conversation]:
        db_conversation = self.get_conversation_by_id(conversation_id)
        if not db_conversation:
            return None
        
        # Update conversation fields
        for key, value in conversation.dict(exclude_unset=True).items():
            setattr(db_conversation, key, value)
        
        self.db.commit()
        self.db.refresh(db_conversation)
        return db_conversation

    def end_conversation(self, conversation_id: str) -> Optional[Conversation]:
        db_conversation = self.get_conversation_by_id(conversation_id)
        if not db_conversation:
            return None
        
        db_conversation.end_time = datetime.now()
        self.db.commit()
        self.db.refresh(db_conversation)
        return db_conversation

    def delete_conversation(self, conversation_id: str) -> Optional[Conversation]:
        conversation = self.get_conversation_by_id(conversation_id)
        if not conversation:
            return None
        
        self.db.delete(conversation)
        self.db.commit()
        return conversation
