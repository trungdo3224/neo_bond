import os
from dotenv import load_dotenv
# auth.py
from datetime import datetime, timedelta
from typing import Optional
from jose import jwt
from typing import Annotated
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from fastapi_backend.schemas.auth import TokenData
from sqlalchemy.orm import Session
from fastapi_backend.schemas.users import CurrentUserSchema
from fastapi_backend.models.users import User
from fastapi_backend import database



database_session = Depends(database.get_db)
load_dotenv()

# Secret key to encode the JWT token
SECRET_KEY = os.getenv('SECRET_KEY')
SECURITY_ALGORITHM = os.getenv('SECURITY_ALGORITHM')
ACCESS_TOKEN_EXPIRE_MINUTES = 600

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_user(db: Session, username: str):
    if not username:
        raise HTTPException(404, detail="User not found")
    try:
        user = db.query(User).filter(User.username == username).first()
        return user
    except:
        raise HTTPException(404, detail="User not found")
# Function to verify password
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# Function to hash password
def get_password_hash(password):
    return pwd_context.hash(str(password))

# Function to create access token
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=SECURITY_ALGORITHM)
    return encoded_jwt

# Function to get current user
async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    print("Getting current user")
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    # db = database_session
    print(f"Token: {token}")
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[SECURITY_ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
        print(token_data)
        # user_in_db: User = get_user(db, username=token_data.username)
        # print(user_in_db)
        # user = CurrentUserSchema(
        #     username=user_in_db.username,
        #     email=user_in_db.email
        # )
        
        # if user is None:
        #     raise credentials_exception
        # return user
        return ""
    except:
        raise credentials_exception

