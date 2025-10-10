from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import Optional
from uuid import UUID

from app.models.postgres_models import Base
from app.schemas.user import (
    UserCreate, UserUpdate, UserResponse, UserListResponse,
    UserWithProjectsResponse, UserLogin, PasswordChange
)
from app.crud import user as crud_user
from app.services.postgres_service import get_db

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """Create a new user."""
    # Check if username already exists
    existing_user = crud_user.get_user_by_username(db, user.username)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    
    # Check if email already exists
    existing_email = crud_user.get_user_by_email(db, user.email)
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    db_user = crud_user.create_user(db, user)
    return db_user


@router.get("/", response_model=UserListResponse)
def list_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    role: Optional[str] = None,
    is_active: Optional[bool] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get a list of users with optional filters."""
    users, total = crud_user.get_users(
        db, skip=skip, limit=limit, role=role,
        is_active=is_active, search=search
    )
    
    page = skip // limit + 1 if limit > 0 else 1
    
    return {
        "users": users,
        "total": total,
        "page": page,
        "page_size": limit
    }


@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: UUID, db: Session = Depends(get_db)):
    """Get a specific user by ID."""
    db_user = crud_user.get_user(db, user_id)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return db_user


@router.get("/{user_id}/with-projects", response_model=UserWithProjectsResponse)
def get_user_with_projects(user_id: UUID, db: Session = Depends(get_db)):
    """Get a user with their projects."""
    db_user = crud_user.get_user(db, user_id)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return db_user


@router.put("/{user_id}", response_model=UserResponse)
def update_user(
    user_id: UUID,
    user_update: UserUpdate,
    db: Session = Depends(get_db)
):
    """Update a user."""
    db_user = crud_user.update_user(db, user_id, user_update)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return db_user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: UUID, db: Session = Depends(get_db)):
    """Delete a user (soft delete)."""
    success = crud_user.delete_user(db, user_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return None


@router.post("/{user_id}/verify", response_model=UserResponse)
def verify_user(user_id: UUID, db: Session = Depends(get_db)):
    """Mark a user as verified."""
    db_user = crud_user.verify_user(db, user_id)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return db_user


@router.post("/{user_id}/change-password", response_model=UserResponse)
def change_password(
    user_id: UUID,
    password_change: PasswordChange,
    db: Session = Depends(get_db)
):
    """Change user password."""
    db_user = crud_user.get_user(db, user_id)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Verify old password
    if not crud_user.verify_password(password_change.old_password, db_user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect password"
        )
    
    # Update to new password
    user_update = UserUpdate(password=password_change.new_password)
    updated_user = crud_user.update_user(db, user_id, user_update)
    
    return updated_user


@router.post("/authenticate", response_model=UserResponse)
def authenticate(login: UserLogin, db: Session = Depends(get_db)):
    """Authenticate a user."""
    db_user = crud_user.authenticate_user(db, login.username, login.password)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )
    return db_user


@router.get("/username/{username}", response_model=UserResponse)
def get_user_by_username(username: str, db: Session = Depends(get_db)):
    """Get a user by username."""
    db_user = crud_user.get_user_by_username(db, username)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return db_user


@router.get("/email/{email}", response_model=UserResponse)
def get_user_by_email(email: str, db: Session = Depends(get_db)):
    """Get a user by email."""
    db_user = crud_user.get_user_by_email(db, email)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return db_user
