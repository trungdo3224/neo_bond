from sqlalchemy.orm import Session
from typing import List, Optional
from fastapi_backend.models.messages import Message
from fastapi_backend.schemas.messages import MessageSchema

class MessageService:
    def __init__(self, db: Session):
        self.db = db

    def get_messages(self, skip: int = 0, limit: int = 10) -> List[Message]:
        return self.db.query(Message).offset(skip).limit(limit).all()

    def get_message_by_id(self, message_id: str) -> Optional[Message]:
        return self.db.query(Message).filter(Message.id == message_id).first()

    def get_conversation_messages(self, conversation_id: str) -> List[Message]:
        return self.db.query(Message)\
            .filter(Message.conversation_id == conversation_id)\
            .order_by(Message.timestamp.asc())\
            .all()

    def create_message(self, message: MessageSchema) -> Message:
        db_message = Message(**message.dict())
        self.db.add(db_message)
        self.db.commit()
        self.db.refresh(db_message)
        return db_message

    def update_message(self, message_id: str, message: MessageSchema) -> Optional[Message]:
        db_message = self.get_message_by_id(message_id)
        if not db_message:
            return None
        
        # Update message fields
        for key, value in message.dict(exclude_unset=True).items():
            setattr(db_message, key, value)
        
        self.db.commit()
        self.db.refresh(db_message)
        return db_message

    def delete_message(self, message_id: str) -> Optional[Message]:
        message = self.get_message_by_id(message_id)
        if not message:
            return None
        
        self.db.delete(message)
        self.db.commit()
        return message

    def get_latest_messages(self, conversation_id: str, limit: int = 10) -> List[Message]:
        return self.db.query(Message)\
            .filter(Message.conversation_id == conversation_id)\
            .order_by(Message.timestamp.desc())\
            .limit(limit)\
            .all()
