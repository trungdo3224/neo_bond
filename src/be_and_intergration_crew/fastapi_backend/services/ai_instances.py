from sqlalchemy.orm import Session
from typing import List, Optional
from fastapi_backend.models.ai_instances import AIInstance
from fastapi_backend.schemas.ai_instances import AIInstanceSchema
from fastapi import HTTPException

class AIInstanceService:
    def __init__(self, db: Session):
        self.db = db

    def get_ai_instances(self, skip: int = 0, limit: int = 10) -> List[AIInstance]:
        return self.db.query(AIInstance).offset(skip).limit(limit).all()

    def get_ai_instance_by_id(self, instance_id: str) -> Optional[AIInstance]:
        return self.db.query(AIInstance).filter(AIInstance.id == instance_id).first()

    def get_ai_instance_by_name(self, name: str) -> Optional[AIInstance]:
        return self.db.query(AIInstance).filter(AIInstance.name == name).first()

    def create_ai_instance(self, instance: AIInstanceSchema) -> AIInstance:
        # Check if name already exists
        if self.get_ai_instance_by_name(instance.name):
            raise HTTPException(status_code=400, detail="AI Instance name already exists")
        
        db_instance = AIInstance(**instance.dict())
        self.db.add(db_instance)
        self.db.commit()
        self.db.refresh(db_instance)
        return db_instance

    def update_ai_instance(self, instance_id: str, instance: AIInstanceSchema) -> Optional[AIInstance]:
        db_instance = self.get_ai_instance_by_id(instance_id)
        if not db_instance:
            return None
        
        # Update instance fields
        for key, value in instance.dict(exclude_unset=True).items():
            setattr(db_instance, key, value)
        
        self.db.commit()
        self.db.refresh(db_instance)
        return db_instance

    def delete_ai_instance(self, instance_id: str) -> Optional[AIInstance]:
        instance = self.get_ai_instance_by_id(instance_id)
        if not instance:
            return None
        
        self.db.delete(instance)
        self.db.commit()
        return instance
