from datetime import datetime, timedelta
from typing import Optional
import bcrypt
import jwt
from app.config import settings
from app.repositories.user_repository import UserRepository
from app.utils.exceptions import AuthenticationException

user_repo = UserRepository()

def hash_password(password: str) -> str:
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password_bytes, salt).decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    password_bytes = plain_password.encode('utf-8')
    hashed_bytes = hashed_password.encode('utf-8')
    return bcrypt.checkpw(password_bytes, hashed_bytes)

def create_access_token(user_id: int) -> str:
    expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)
    payload = {
        "user_id": user_id,
        "exp": expire
    }
    return jwt.encode(payload, settings.secret_key, algorithm=settings.algorithm)

def verify_token(token: str) -> int:
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        user_id: int = payload.get("user_id")
        if user_id is None:
            raise AuthenticationException("Invalid token")
        return user_id
    except jwt.ExpiredSignatureError:
        raise AuthenticationException("Token expired")
    except jwt.InvalidTokenError:
        raise AuthenticationException("Invalid token")

def authenticate_user(email: str, password: str):
    user = user_repo.get_by_email(email)
    if not user:
        raise AuthenticationException("Invalid credentials")
    
    if not user.get('password_hash'):
        raise AuthenticationException("User has no password set")
    
    if not verify_password(password, user['password_hash']):
        raise AuthenticationException("Invalid credentials")
    
    return user
