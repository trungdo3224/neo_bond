from sqlalchemy import Column, ForeignKey, String, TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
import uuid

Base = declarative_base()

class MoodTracking(Base):
    __tablename__ = 'mood_tracking'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'))
    mood = Column(String(50))
    timestamp = Column(TIMESTAMP, default='now()')
    suggested_movie_id = Column(UUID(as_uuid=True))
