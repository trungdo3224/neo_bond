from sqlalchemy.orm import Session
from typing import List, Optional
from fastapi_backend.auth.auth import get_password_hash
from fastapi_backend.models.users import User
from fastapi_backend.schemas.users import UserSchema
from fastapi import HTTPException
from sqlalchemy import func

class UserService:
    def __init__(self):
        pass

    def get_users(self, db: Session) -> List[User]:
        if not db:
            raise HTTPException(status_code=500, detail="No database connection")
        try:
            users = db.query(User).all()
            if not users:
                raise HTTPException(status_code=404, detail="No users found")
            result_users = []
            for user in users:
                user = {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "preferences": user.preferences
                }
                result_users.append(user)
            return result_users
        except Exception as e:
            error_details = str(e) or "An error occurred"
            raise HTTPException(status_code=404, detail=error_details)

    def get_user_by_id(self, user_id: str, db: Session) -> Optional[User]:
        try:
            user = db.query(User).filter(User.id == user_id).first()
            user_data = {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "preferences": user.preferences,
                "created_at": user.created_at,
                "last_login": user.last_login
            }
            if user_data:
                return user_data
            else:
                raise HTTPException(status_code=404, detail="User not found.")
        except Exception as e:
            raise HTTPException(status_code=404, detail=str(e))

    def get_user_by_email(self, email: str, db: Session) -> Optional[User]:
        if not email:
            raise HTTPException(status_code=400, detail="No email provided")
        try:
            user = db.query(User).filter(User.email == email).first()
            user_data = {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "preferences": user.preferences,
                "created_at": user.created_at,
                "last_login": user.last_login
            }
            if user_data:
                return user_data
            else:
                raise HTTPException(status_code=404, detail="User not found.")
        except Exception as e:
            raise HTTPException(status_code=404, detail=str(e))

    def create_user(self, user: UserSchema, db: Session) -> User:
        if not user:
            raise HTTPException(status_code=400, detail="No user data provided")
        
        # Check if email already exists
        user_found = db.query(User).filter(User.email == user.email).first()
        if user_found:
            return {
                "message": "User already exists",
            }
        try:
            # Hash the password
            hashed_password = get_password_hash(str(user.password))

            # Create a new user instance
            new_user = User(
                username=user.username,
                email=user.email,
                password_hash=hashed_password,  # Ensure this matches the model definition
                last_login=func.now(),
                created_at=func.now(),
                preferences={
                    "theme": "light",
                    "language": "en"
                }
            )

            # Add the new user to the database
            db.add(new_user)
            db.commit()
            db.refresh(new_user)

            return {
                "user": new_user
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    

    def update_user(self, user_id: str, db: Session) -> Optional[User]:
        db_user = db.query(User).filter(User.id == user_id).first()
        if db_user is None:
            raise HTTPException(status_code=404, detail="User not found")
        try:
            for key, value in db_user.dict().items():
                setattr(db_user, key, value)
            db.commit()
            db.refresh(db_user)
            return db_user
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    def delete_user(self, user_id: str, db: Session) -> Optional[User]:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return None
        
        try:
            db.delete(user)
            db.commit()
            return user
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
