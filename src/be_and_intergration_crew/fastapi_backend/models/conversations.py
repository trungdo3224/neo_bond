from sqlalchemy import Column, ForeignKey, TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID
from fastapi_backend.database import Base
import uuid


class Conversation(Base):
    __tablename__ = 'conversations'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'))
    ai_id = Column(UUID(as_uuid=True), ForeignKey('ai_instances.id', ondelete='CASCADE'))
    start_time = Column(TIMESTAMP, default='now()')
    end_time = Column(TIMESTAMP)
