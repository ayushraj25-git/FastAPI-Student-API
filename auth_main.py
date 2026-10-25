from fastapi import FastAPI, HTTPException,Depends
from pydantic import BaseModel, Field
from pwdlib import PasswordHash
from database import get_connection
import sqlite3
import jwt
from datetime import datetime, timedelta, timezone
from config import SECRET_KEY, ALGORITHM
app = FastAPI()
password_hash = PasswordHash.recommended()


class SignupData(BaseModel):
    username: str = Field(min_length=3)
    password: str = Field(min_length=8)

class LoginData(BaseModel):
    username: str
    password: str    


@app.post("/signup", status_code=201)
def signup(data: SignupData):
    hashed_password = password_hash.hash(data.password)

    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO users (username, hashed_password) VALUES (?, ?)",
            (data.username, hashed_password)
        )
        conn.commit()
    except sqlite3.IntegrityError:
        conn.close()
        raise HTTPException(
            status_code=409,
            detail="Username already exists"
        )

    conn.close()

    return {"message": "Signup successful"}


@app.post("/login")
def login(data: LoginData):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE username = ?",
        (data.username,)
    )

    user = cursor.fetchone()
    conn.close()

    if user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    if not password_hash.verify(
        data.password,
        user["hashed_password"]
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    access_token = jwt.encode(
        {
            "sub": user["username"],
            "exp": datetime.now(timezone.utc) + timedelta(minutes=30)
        },
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    token = credentials.credentials

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )
        username = payload["sub"]

    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )

    return username


@app.get("/protected")
def protected_route(username: str = Depends(get_current_user)):
    return {
        "message": "You accessed a protected route",
        "username": username
    }
