from sqlalchemy.orm import Session
from typing import List, Optional
from fastapi_backend.models.ai_responses import AIResponse
from fastapi_backend.schemas.ai_responses import AIResponseSchema

class AIResponseService:
    def __init__(self, db: Session):
        self.db = db

    def get_ai_responses(self, skip: int = 0, limit: int = 10) -> List[AIResponse]:
        return self.db.query(AIResponse).offset(skip).limit(limit).all()

    def get_ai_response_by_id(self, response_id: str) -> Optional[AIResponse]:
        return self.db.query(AIResponse).filter(AIResponse.id == response_id).first()

    def get_conversation_ai_responses(self, conversation_id: str) -> List[AIResponse]:
        return self.db.query(AIResponse)\
            .filter(AIResponse.conversation_id == conversation_id)\
            .order_by(AIResponse.generated_at.asc())\
            .all()

    def create_ai_response(self, response: AIResponseSchema) -> AIResponse:
        db_response = AIResponse(**response.dict())
        self.db.add(db_response)
        self.db.commit()
        self.db.refresh(db_response)
        return db_response

    def update_ai_response(self, response_id: str, response: AIResponseSchema) -> Optional[AIResponse]:
        db_response = self.get_ai_response_by_id(response_id)
        if not db_response:
            return None
        
        # Update AI response fields
        for key, value in response.dict(exclude_unset=True).items():
            setattr(db_response, key, value)
        
        self.db.commit()
        self.db.refresh(db_response)
        return db_response

    def delete_ai_response(self, response_id: str) -> Optional[AIResponse]:
        response = self.get_ai_response_by_id(response_id)
        if not response:
            return None
        
        self.db.delete(response)
        self.db.commit()
        return response

    def get_latest_ai_response(self, conversation_id: str) -> Optional[AIResponse]:
        return self.db.query(AIResponse)\
            .filter(AIResponse.conversation_id == conversation_id)\
            .order_by(AIResponse.generated_at.desc())\
            .first()
