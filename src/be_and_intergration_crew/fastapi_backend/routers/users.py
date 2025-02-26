

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi_backend import database
from fastapi_backend.services.users import UserService
from fastapi_backend.schemas.users import UserSchema
router = APIRouter()

database_session = Depends(database.get_db)

users_service = UserService()

@router.get("/users")
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

@router.get("/users/{id}")
def get_user(id: str, db: Session = Depends(database.get_db)):
    try:
        user = users_service.get_user_by_id(id, db)
        if not user:
            raise HTTPException(status_code=404, detail="User not found.")
        user.pop("password_hash", None)
        return user
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/users/signup")
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



@router.put("/users/{user_id}")
def update_user(user_id: str, user: UserSchema, db: Session = database_session):
    users_service.update_user(user_id, user, db)
    return user
    

@router.delete("/users/{user_id}")
def delete_user(user_id: str, db: Session = database_session):
    users_service.delete_user(user_id, db)
    return {"message": "User deleted successfully."}