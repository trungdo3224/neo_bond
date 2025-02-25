from sqlalchemy import Column, String, Text
from sqlalchemy.dialects.postgresql import UUID, JSONB, ARRAY
from fastapi_backend.database import Base
import uuid

class AIInstance(Base):
    __tablename__ = 'ai_instances'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text)
    skill_sets = Column(ARRAY(Text))  # Assuming you're using PostgreSQL
    personality = Column(JSONB)