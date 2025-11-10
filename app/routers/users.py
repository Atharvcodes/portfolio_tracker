from fastapi import APIRouter, HTTPException, status
from app.schemas.user import UserCreate, UserResponse
from app.repositories.user_repository import UserRepository
from app.utils.exceptions import DuplicateEmailException
from psycopg2.errors import UniqueViolation

router = APIRouter(prefix="/users")
user_repo = UserRepository()

@router.post("/create_user", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate):
    try:
        result = user_repo.create(user.name, user.email, None)
        return UserResponse(**result)
    except UniqueViolation:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Email {user.email} already exists"
        )

@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int):
    user = user_repo.get_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User {user_id} not found"
        )
    return UserResponse(**user)
