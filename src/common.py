import jwt
from jose import jwt
from typing import Optional
from fastapi import HTTPException
from datetime import datetime, timedelta
from passlib.context import CryptContext
from src.config import (
    SECRET_KEY, 
    ALGORITHM
    )

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Hashing function
def hash_password(password: str):
    return pwd_context.hash(password)

# Validate and decode access token
def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))

# Function to create access token
async def create_jwt_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    print(f"DEBUG: encoded_jwt: {encoded_jwt}")
    return encoded_jwt
