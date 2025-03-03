

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from fastapi_backend import database
from fastapi_backend.services.users import UserService
from fastapi_backend.schemas.users import UserSchema
from fastapi_backend.schemas.auth import AuthSchema
from fastapi_backend.utilities.auth import get_current_user
from typing import Annotated
from fastapi_backend.schemas.users import CurrentUserSchema
from fastapi.security import OAuth2PasswordBearer
router = APIRouter()

database_session = Depends(database.get_db)

users_service = UserService()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# --------- Admin routes ---------
@router.get("/admin/users")
def get_users(db: Session = Depends(database.get_db)):
    if not db:
        raise HTTPException(status_code=500, detail="No database connection")
    try:
        users = users_service.get_users(db)
        if not users:
            raise HTTPException(status_code=404, detail="No users found.")
        
        return users
    except Exception as e:
        error_details = str(e) or "Register Failed."
        raise HTTPException(status_code=404, detail=error_details)

@router.get("/admin/users/{id}")
def get_user(id: str, db: Session = Depends(database.get_db)):
    try:
        user = users_service.get_user_by_id(id, db)
        if not user:
            raise HTTPException(status_code=404, detail="User not found.")
        user.pop("password_hash", None)
        return user
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.put("/admin/users/{user_id}")
def update_user(user_id: str, user: UserSchema, db: Session = database_session):
    users_service.update_user(user_id, user, db)
    return user
    

@router.delete("admin/users/{user_id}")
def delete_user(user_id: str, db: Session = database_session):
    users_service.delete_user(user_id, db)
    return {"message": "User deleted successfully."}



#  --------- Auth routes ---------
@router.post("/auth/signup")
def create_user(user: UserSchema, db: Session = Depends(database.get_db)):
    if not user:
        raise HTTPException(status_code=400, detail="No user data provided")
    try:
        result = users_service.create_user(user, db)
        print(result)
        if result:
            # Exclude password_hash from the result
            return result
        else:
            raise HTTPException(status_code=500, detail="Register Failed.")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Register Failed.")

@router.post("/auth/login")
def login_user(user: AuthSchema, db: Session = database_session):
    if not user:
        raise HTTPException(status_code=400, detail="No user data provided")
    try:
        result = users_service.login_user(user, db)
        if result:
            return result
        else:
            raise HTTPException(status_code=500, detail="Login Failed Check Your Email or Password.")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Login Failed.")

@router.get("/me", response_model=str)
async def read_user_me(current_user: Annotated[str, Depends(get_current_user)]):
    return current_user

# @router.get("/me")
# async def user_me():
    
#     current_user = await get_current_user("")
#     print(current_user)
#     return current_user