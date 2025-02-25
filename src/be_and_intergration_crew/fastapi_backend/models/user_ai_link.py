from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID

class UserAILink(Base):
    __tablename__ = 'user_ai_link'
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'), primary_key=True)
    ai_id = Column(UUID(as_uuid=True), ForeignKey('ai_instances.id', ondelete='CASCADE'), primary_key=True)