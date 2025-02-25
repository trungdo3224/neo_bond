from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from fastapi_backend.schemas.ai_instances import AIInstanceSchema
from fastapi_backend.models.ai_instances import AIInstance
from fastapi_backend.database import get_db

router = APIRouter()

@router.get("/ai-instances/", response_model=List[AIInstanceSchema])
def read_ai_instances(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    instances = db.query(AIInstance).offset(skip).limit(limit).all()
    return instances

@router.post("/ai-instances/", response_model=AIInstanceSchema)
def create_ai_instance(instance: AIInstanceSchema, db: Session = Depends(get_db)):
    db_instance = AIInstance(**instance.dict())
    db.add(db_instance)
    db.commit()
    db.refresh(db_instance)
    return db_instance

@router.get("/ai-instances/{instance_id}", response_model=AIInstanceSchema)
def read_ai_instance(instance_id: str, db: Session = Depends(get_db)):
    instance = db.query(AIInstance).filter(AIInstance.id == instance_id).first()
    if instance is None:
        raise HTTPException(status_code=404, detail="AI Instance not found")
    return instance

@router.put("/ai-instances/{instance_id}", response_model=AIInstanceSchema)
def update_ai_instance(instance_id: str, instance: AIInstanceSchema, db: Session = Depends(get_db)):
    db_instance = db.query(AIInstance).filter(AIInstance.id == instance_id).first()
    if db_instance is None:
        raise HTTPException(status_code=404, detail="AI Instance not found")
    for key, value in instance.dict(exclude_unset=True).items():
        setattr(db_instance, key, value)
    db.commit()
    db.refresh(db_instance)
    return db_instance

@router.delete("/ai-instances/{instance_id}", response_model=AIInstanceSchema)
def delete_ai_instance(instance_id: str, db: Session = Depends(get_db)):
    instance = db.query(AIInstance).filter(AIInstance.id == instance_id).first()
    if instance is None:
        raise HTTPException(status_code=404, detail="AI Instance not found")
    db.delete(instance)
    db.commit()
    return instance
