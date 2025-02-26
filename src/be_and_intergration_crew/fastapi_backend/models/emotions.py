from sqlalchemy import Column, ForeignKey, String, DECIMAL, TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
import uuid

Base = declarative_base()

class Emotion(Base):
    __tablename__ = 'emotions'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'))
    conversation_id = Column(UUID(as_uuid=True), ForeignKey('conversations.id', ondelete='CASCADE'))
    detected_emotion = Column(String(50))
    confidence = Column(DECIMAL(5, 2))
    detected_at = Column(TIMESTAMP, default='now()')
