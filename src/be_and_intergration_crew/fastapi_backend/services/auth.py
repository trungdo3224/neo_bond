from sqlalchemy.orm import Session
from typing import Optional
from fastapi_backend.auth.auth import verify_password
from fastapi_backend.models.users import User
from fastapi import HTTPException

class AuthService:
  def __init__(self):
    pass
  def login(self, db: Session, email: str, password: str) -> Optional[User]:
    if not email or not password:
      raise HTTPException(status_code=400, detail="Invalid email or password")
    try:
      user = db.query(User).filter(User.email == email).first()
      if not user:
        raise HTTPException(status_code=404, detail="User not found")
      if not verify_password(password, user.password_hash):
        raise HTTPException(status_code=400, detail="Incorrect password")
      return user
    except Exception as e:
      raise HTTPException(status_code=404, detail=str(e))
  
  def logout(self):
    pass