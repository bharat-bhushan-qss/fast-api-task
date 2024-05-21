import jwt
import psycopg2
from jose import jwt, JWTError
from typing import Optional
from datetime import timedelta
from fastapi import HTTPException, status, Depends, Header
from fastapi.security import OAuth2PasswordBearer
from src.models.auth import UserBase, UserOut
from src.config import (
    SECRET_KEY, 
    ALGORITHM, 
    ACCESS_TOKEN_EXPIRE_MINUTES
    )
from src.common import hash_password, decode_access_token, create_jwt_access_token


# OAuth2PasswordBearer instance for token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


################################################## Auth0 handling functions ######################################################################

def authenticate(token: Optional[str] = Header(None)):
    if token is None:
        raise HTTPException(status_code=401, detail="Access token missing")
    payload = decode_access_token(token)
    print(f"payload: {payload}")
    user_id = payload.get("sub")
    return user_id


################################################## JWT auth handling functions ######################################################################

async def create_user(db, user: UserBase):
    try:
        usr_q = f"""
        SELECT * FROM users WHERE username = '{user.username}'
        """
        print(f"usr_q: {usr_q}")
        user_exist = await db.fetch_one(query=usr_q)
        
        print(f"user_exist: {user_exist}")
        if user_exist:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already registered",
            )

        hashed_password = hash_password(user.password)
        query = f"""INSERT INTO users (username, password) VALUES ('{user.username}', '{hashed_password}')"""
        await db.execute(query)
        access_token_expires = timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))
        access_token = await create_jwt_access_token(
            data={"sub": user.username}, expires_delta=access_token_expires
        )
        await db.disconnect()
        return UserOut(access_token=access_token)
    except psycopg2.Error as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(err)
        )


async def authenticate_user(db, username: str, password: str):
    usr_q = f"""
        SELECT * FROM USER WEHERE username = '{username}'
        """
    user_exist = await db.fetch_one(query=usr_q)
    return user_exist


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    return username
