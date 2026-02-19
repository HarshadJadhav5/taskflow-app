from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from database import get_db
from models import User
import os
from dotenv import load_dotenv

load_dotenv()

# ──────────────────────────────────────────────────────────────
# CONFIGURATION
# ──────────────────────────────────────────────────────────────

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

# This is used to hash passwords (turn "password123" into random gibberish)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# This tells FastAPI: "look for the token in the Authorization header"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


# ──────────────────────────────────────────────────────────────
# PASSWORD FUNCTIONS
# ──────────────────────────────────────────────────────────────

def hash_password(password: str) -> str:
    """
    Converts plain password into hashed password
    Example: "mypassword" → "$2b$12$KIX..."
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Checks if the plain password matches the hashed one
    Used during login
    """
    return pwd_context.verify(plain_password, hashed_password)


# ──────────────────────────────────────────────────────────────
# TOKEN FUNCTIONS
# ──────────────────────────────────────────────────────────────

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """
    Creates a JWT token (the thing we give to users after login)
    Token contains user info and expiration time
    """
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    
    # This creates the actual token string
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str, credentials_exception):
    """
    Decodes the JWT token and extracts the user email
    If token is invalid/expired, raises an exception
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        
        if email is None:
            raise credentials_exception
        
        return email
    
    except JWTError:
        raise credentials_exception


# ──────────────────────────────────────────────────────────────
# GET CURRENT USER (Used to protect routes)
# ──────────────────────────────────────────────────────────────

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """
    This function runs automatically on protected routes
    It extracts the token, verifies it, and returns the logged-in user
    If token is invalid, user gets 401 Unauthorized
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    email = verify_token(token, credentials_exception)
    
    # Find the user in database
    user = db.query(User).filter(User.email == email).first()
    
    if user is None:
        raise credentials_exception
    
    return user