from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.schemas.user import UserCreate, UserResponse, UserLogin
from app.schemas.auth import Token, TokenData
from app.repositories.user_repository import UserRepository
from app.services.auth_service import (
    hash_password, authenticate_user, create_access_token, verify_token
)
from app.utils.exceptions import AuthenticationException
from psycopg2.errors import UniqueViolation

router = APIRouter(prefix="/auth")
user_repo = UserRepository()
security = HTTPBearer()

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(user: UserCreate):
    if not user.password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password is required for registration"
        )
    
    try:
        password_hash = hash_password(user.password)
        result = user_repo.create(user.name, user.email, password_hash)
        return UserResponse(**result)
    except UniqueViolation:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Email {user.email} already exists"
        )

@router.post("/login", response_model=Token)
def login(credentials: UserLogin):
    try:
        user = authenticate_user(credentials.email, credentials.password)
        access_token = create_access_token(user['user_id'])
        return Token(access_token=access_token, token_type="bearer")
    except AuthenticationException as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"}
        )

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> int:
    try:
        user_id = verify_token(credentials.credentials)
        return user_id
    except AuthenticationException as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"}
        )

@router.get("/me", response_model=UserResponse)
def get_current_user_info(user_id: int = Depends(get_current_user)):
    user = user_repo.get_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return UserResponse(**user)
