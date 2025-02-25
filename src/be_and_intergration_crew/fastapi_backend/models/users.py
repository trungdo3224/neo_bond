from sqlalchemy import Column, String, Text, DateTime, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.sql import func
from fastapi_backend.database import Base
import uuid

class User(Base):
    __tablename__ = 'users'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    last_login = Column(DateTime(timezone=True))
    preferences = Column(JSONB)
    __table_args__ = (UniqueConstraint('username', 'email', name='uix_1'),)

class UserInteraction(Base):
    __tablename__ = 'user_interactions'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), index=True)
    interaction_type = Column(String)
    interaction_content = Column(Text)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
