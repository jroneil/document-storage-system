from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from typing import Optional, List
from uuid import UUID
from datetime import datetime
import bcrypt

from app.models.postgres_models import User, UserRole
from app.schemas.user import UserCreate, UserUpdate


def hash_password(password: str) -> str:
    """Hash a password using bcrypt."""
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash."""
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))


def create_user(db: Session, user: UserCreate) -> User:
    """Create a new user."""
    # Hash the password
    hashed_password = hash_password(user.password)
    
    # Create user instance
    db_user = User(
        username=user.username,
        email=user.email,
        full_name=user.full_name,
        password_hash=hashed_password,
        role=UserRole(user.role),
        phone_number=user.phone_number,
        department=user.department,
        job_title=user.job_title
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user(db: Session, user_id: UUID) -> Optional[User]:
    """Get a user by ID."""
    return db.query(User).filter(User.user_id == user_id).first()


def get_user_by_username(db: Session, username: str) -> Optional[User]:
    """Get a user by username."""
    return db.query(User).filter(User.username == username).first()


def get_user_by_email(db: Session, email: str) -> Optional[User]:
    """Get a user by email."""
    return db.query(User).filter(User.email == email).first()


def get_users(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    role: Optional[str] = None,
    is_active: Optional[bool] = None,
    search: Optional[str] = None
) -> tuple[List[User], int]:
    """Get a list of users with filters."""
    query = db.query(User)
    
    # Apply filters
    if role:
        query = query.filter(User.role == UserRole(role))
    
    if is_active is not None:
        query = query.filter(User.is_active == is_active)
    
    if search:
        search_filter = or_(
            User.username.ilike(f"%{search}%"),
            User.email.ilike(f"%{search}%"),
            User.full_name.ilike(f"%{search}%")
        )
        query = query.filter(search_filter)
    
    # Get total count
    total = query.count()
    
    # Apply pagination
    users = query.offset(skip).limit(limit).all()
    
    return users, total


def update_user(db: Session, user_id: UUID, user_update: UserUpdate) -> Optional[User]:
    """Update a user."""
    db_user = get_user(db, user_id)
    if not db_user:
        return None
    
    # Update fields
    update_data = user_update.model_dump(exclude_unset=True)
    
    # Handle password update separately
    if 'password' in update_data:
        update_data['password_hash'] = hash_password(update_data.pop('password'))
    
    for field, value in update_data.items():
        if field == 'role' and value:
            value = UserRole(value)
        setattr(db_user, field, value)
    
    db_user.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: UUID) -> bool:
    """Delete a user (soft delete by setting is_active to False)."""
    db_user = get_user(db, user_id)
    if not db_user:
        return False
    
    db_user.is_active = False
    db_user.updated_at = datetime.utcnow()
    db.commit()
    return True


def hard_delete_user(db: Session, user_id: UUID) -> bool:
    """Permanently delete a user."""
    db_user = get_user(db, user_id)
    if not db_user:
        return False
    
    db.delete(db_user)
    db.commit()
    return True


def update_last_login(db: Session, user_id: UUID) -> Optional[User]:
    """Update user's last login timestamp."""
    db_user = get_user(db, user_id)
    if not db_user:
        return None
    
    db_user.last_login = datetime.utcnow()
    db.commit()
    db.refresh(db_user)
    return db_user


def verify_user(db: Session, user_id: UUID) -> Optional[User]:
    """Mark a user as verified."""
    db_user = get_user(db, user_id)
    if not db_user:
        return None
    
    db_user.is_verified = True
    db_user.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_user)
    return db_user


def authenticate_user(db: Session, username: str, password: str) -> Optional[User]:
    """Authenticate a user by username and password."""
    user = get_user_by_username(db, username)
    if not user:
        return None
    
    if not verify_password(password, user.password_hash):
        return None
    
    if not user.is_active:
        return None
    
    # Update last login
    update_last_login(db, user.user_id)
    
    return user
