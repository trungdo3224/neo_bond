import sys
import os
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from fastapi_backend.models.users import User

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_users(db: Session):
    if not db:
        return {"message": "No database connection"}
    try:
        users = db.query(User).all()
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
        return {"error_message": str(e)}

def get_user(id: str, db: Session):
    try:
        print("GEtting user info")
        user = db.query(User).filter(User.id == id).first()
        if user:
            print("User found.")
            return user
        else:
            return {"message": "User not found."}
    except Exception as e:
        return {"error_message": str(e)}

def create_user(user: dict, db: Session):
    if not user:
        return {"message": "No user data provided"}
    try:
        user_data = user.get("user")
        # Check if the user already exists

        existing_user = db.query(User).filter(User.username == user_data["username"]).first()
        if existing_user:
            raise ValueError("User already exists")

        # Hash the password

        hashed_password = pwd_context.hash(str(user_data["password"]))

        # Create a new user instance

        new_user = User(
            username=user_data["username"],
            email=user_data["email"],
            password_hash=hashed_password,  # Ensure this matches the model definition
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
            "message": "User created successfully",
            "user": new_user
        }
    except Exception as e:
        print(e)
        return {"error_message": str(e)}