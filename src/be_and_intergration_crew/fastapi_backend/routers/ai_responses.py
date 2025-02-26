from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from fastapi_backend.schemas.ai_responses import AIResponseSchema
from fastapi_backend.models.ai_responses import AIResponse
from fastapi_backend.database import get_db

router = APIRouter()

@router.get("/ai-responses/", response_model=List[AIResponseSchema])
def read_ai_responses(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    responses = db.query(AIResponse).offset(skip).limit(limit).all()
    return responses

@router.post("/ai-responses/", response_model=AIResponseSchema)
def create_ai_response(response: AIResponseSchema, db: Session = Depends(get_db)):
    db_response = AIResponse(**response.dict())
    db.add(db_response)
    db.commit()
    db.refresh(db_response)
    return db_response

@router.get("/ai-responses/{response_id}", response_model=AIResponseSchema)
def read_ai_response(response_id: str, db: Session = Depends(get_db)):
    response = db.query(AIResponse).filter(AIResponse.id == response_id).first()
    if response is None:
        raise HTTPException(status_code=404, detail="AI Response not found")
    return response

@router.get("/ai-responses/conversation/{conversation_id}", response_model=List[AIResponseSchema])
def read_conversation_ai_responses(conversation_id: str, db: Session = Depends(get_db)):
    responses = db.query(AIResponse).filter(AIResponse.conversation_id == conversation_id).all()
    return responses

@router.put("/ai-responses/{response_id}", response_model=AIResponseSchema)
def update_ai_response(response_id: str, response: AIResponseSchema, db: Session = Depends(get_db)):
    db_response = db.query(AIResponse).filter(AIResponse.id == response_id).first()
    if db_response is None:
        raise HTTPException(status_code=404, detail="AI Response not found")
    for key, value in response.dict(exclude_unset=True).items():
        setattr(db_response, key, value)
    db.commit()
    db.refresh(db_response)
    return db_response

@router.delete("/ai-responses/{response_id}", response_model=AIResponseSchema)
def delete_ai_response(response_id: str, db: Session = Depends(get_db)):
    response = db.query(AIResponse).filter(AIResponse.id == response_id).first()
    if response is None:
        raise HTTPException(status_code=404, detail="AI Response not found")
    db.delete(response)
    db.commit()
    return response
