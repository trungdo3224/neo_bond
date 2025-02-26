from sqlalchemy import Column, ForeignKey, String, Text, TIMESTAMP
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.ext.declarative import declarative_base
import uuid

Base = declarative_base()

class Message(Base):
    __tablename__ = 'messages'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    conversation_id = Column(UUID(as_uuid=True), ForeignKey('conversations.id', ondelete='CASCADE'))
    sender_type = Column(String(10), nullable=False)
    sender_id = Column(UUID(as_uuid=True))
    message_text = Column(Text, nullable=False)
    timestamp = Column(TIMESTAMP, default='now()')
    ai_response_metadata = Column(JSONB)
