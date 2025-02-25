from sqlalchemy import Column, ForeignKey, Text, TIMESTAMP, UUID
from sqlalchemy.ext.declarative import declarative_base
import uuid

Base = declarative_base()

class AIResponse(Base):
    __tablename__ = 'ai_responses'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    conversation_id = Column(UUID(as_uuid=True), ForeignKey('conversations.id', ondelete='CASCADE'))
    response_text = Column(Text, nullable=False)
    audio_url = Column(Text)
    generated_at = Column(TIMESTAMP, default='now()')
