from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func

import sys
import os

# Add the root directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from fastapi_backend.schemas import Base

class AIResponseLog(Base):
    __tablename__ = 'ai_response_logs'

    id = Column(Integer, primary_key=True, index=True)
    response_content = Column(Text)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
