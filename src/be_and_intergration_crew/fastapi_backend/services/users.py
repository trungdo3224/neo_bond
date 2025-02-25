
from sqlalchemy.orm import Session
from typing import List, Optional
from fastapi_backend.models.users import User
from fastapi_backend.schema.users import UserSchema
from fastapi import HTTPException


class UserService:
    def __init__(self, db: Session):
        self.db = db

    def get_users(self, skip: int = 0, limit: int = 10) -> List[User]:
        return self.db.query(User).offset(skip).limit(limit).all()

    def get_user_by_id(self, user_id: str) -> Optional[User]:
        return self.db.query(User).filter(User.id == user_id).first()

    def get_user_by_email(self, email: str) -> Optional[User]:
        return self.db.query(User).filter(User.email == email).first()

    def create_user(self, user: UserSchema) -> User:
        # Check if email already exists
        if self.get_user_by_email(user.email):
            raise HTTPException(status_code=400, detail="Email already registered")
        
        db_user = User(**user.dict())
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def update_user(self, user_id: str, user: UserSchema) -> Optional[User]:
        db_user = self.get_user_by_id(user_id)
        if not db_user:
            return None
        
        # Update user fields
        for key, value in user.dict(exclude_unset=True).items():
            setattr(db_user, key, value)
        
        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def delete_user(self, user_id: str) -> Optional[User]:
        user = self.get_user_by_id(user_id)
        if not user:
            return None
        
        self.db.delete(user)
        self.db.commit()
        return user
