

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi_backend import database
from fastapi_backend.services import users_service

router = APIRouter()

databaseSession = Depends(database.get_db)

@router.get("/")
async def get_users(db: Session = databaseSession):
    try:
        users = users_service.get_users(db=db)
        if users:
            print(users)
            return users
        else:
            return {"message": "No users found"}
    except Exception as e:
        print(e)
        return {"error_message": str(e)}

@router.get("/{id}")
async def get_user(id: str, db: Session = databaseSession):
    try:
        user = users_service.get_user(id, db)
        if not user:
            raise HTTPException(status_code=404, detail="User not found.")
        return user
    except Exception as e:
        return {"error_message": str(e)}


@router.post("/signup")
async def create_user(user: dict, db: Session = databaseSession):
    if(user):
        try:
            result = users_service.create_user(user, db=db)
            if result:
                return {
                    "message": result["message"],
                    "user: ": result["user"],
                }
            else:
                return {"message": "User not created"}
        except Exception as e:
            return {"error_message": str(e)}
    else:
        return {"message": "No user data"}



# @router.put("/users/{user_id}", response_model=UserSchema)
# def update_user(user_id: str, user: UserSchema, db: Session = Depends(get_db)):
#     db_user = db.query(User).filter(User.id == user_id).first()
#     if db_user is None:
#         raise HTTPException(status_code=404, detail="User not found")
#     for key, value in user.dict().items():
#         setattr(db_user, key, value)
#     db.commit()
#     db.refresh(db_user)
#     return db_user

# @router.delete("/users/{user_id}", response_model=UserSchema)
# def delete_user(user_id: str, db: Session = Depends(get_db)):
#     user = db.query(User).filter(User.id == user_id).first()
#     if user is None:
#         raise HTTPException(status_code=404, detail="User not found")
#     db.delete(user)
#     db.commit()
#     return user