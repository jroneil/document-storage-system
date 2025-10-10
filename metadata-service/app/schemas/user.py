from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional, List
from datetime import datetime
from uuid import UUID

# Enums
class UserRoleEnum(str):
    ADMIN = "admin"
    MANAGER = "manager"
    MEMBER = "member"
    VIEWER = "viewer"

# Base User Schema
class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=100)
    email: EmailStr
    full_name: Optional[str] = Field(None, max_length=255)
    role: UserRoleEnum = UserRoleEnum.MEMBER
    phone_number: Optional[str] = Field(None, max_length=20)
    department: Optional[str] = Field(None, max_length=100)
    job_title: Optional[str] = Field(None, max_length=100)

# User Creation Schema
class UserCreate(UserBase):
    password: str = Field(..., min_length=8, max_length=100)

# User Update Schema
class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    full_name: Optional[str] = Field(None, max_length=255)
    role: Optional[UserRoleEnum] = None
    is_active: Optional[bool] = None
    phone_number: Optional[str] = Field(None, max_length=20)
    department: Optional[str] = Field(None, max_length=100)
    job_title: Optional[str] = Field(None, max_length=100)
    profile_picture: Optional[str] = Field(None, max_length=500)
    password: Optional[str] = Field(None, min_length=8, max_length=100)

# User Response Schema
class UserResponse(UserBase):
    user_id: UUID
    is_active: bool
    is_verified: bool
    created_at: datetime
    updated_at: datetime
    last_login: Optional[datetime] = None
    profile_picture: Optional[str] = None
    
    model_config = ConfigDict(from_attributes=True)

# User with Projects Response
class UserWithProjectsResponse(UserResponse):
    projects: List['ProjectBriefResponse'] = []
    owned_projects: List['ProjectBriefResponse'] = []

# User Login Schema
class UserLogin(BaseModel):
    username: str
    password: str

# User Login Response
class UserLoginResponse(BaseModel):
    user: UserResponse
    access_token: str
    token_type: str = "bearer"

# Password Change Schema
class PasswordChange(BaseModel):
    old_password: str
    new_password: str = Field(..., min_length=8, max_length=100)

# User List Response
class UserListResponse(BaseModel):
    users: List[UserResponse]
    total: int
    page: int
    page_size: int

# Import for forward references
from metadata_service.app.schemas.project import ProjectBriefResponse
UserWithProjectsResponse.model_rebuild()
