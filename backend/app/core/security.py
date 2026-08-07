from datetime import datetime
import os
import bcrypt
from jose import jwt
from dotenv import load_dotenv
from app.core.constants import ALGORITHM

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")


def get_password_hash(password: str) -> str:
    pwd_bytes = password.encode("utf-8")
    hashed = bcrypt.hashpw(pwd_bytes, bcrypt.gensalt())
    return hashed.decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    pwd_bytes = plain_password.encode("utf-8")
    hashed_bytes = hashed_password.encode("utf-8")
    return bcrypt.checkpw(pwd_bytes, hashed_bytes)


def create_access_token(data: dict, expires_at: datetime):
    to_encode = data.copy()
    to_encode.update({"exp": expires_at})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
