from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List, Dict, Any
from datetime import datetime
from uuid import UUID

# Enums
class ProjectStatusEnum(str):
    ACTIVE = "active"
    ARCHIVED = "archived"
    DELETED = "deleted"

class ProjectRoleEnum(str):
    OWNER = "owner"
    ADMIN = "admin"
    EDITOR = "editor"
    VIEWER = "viewer"

# Base Project Schema
class ProjectBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    status: ProjectStatusEnum = ProjectStatusEnum.ACTIVE
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    tags: Optional[List[str]] = []
    properties: Optional[Dict[str, Any]] = {}
    storage_quota: Optional[int] = None  # In bytes
    is_public: bool = False

# Project Creation Schema
class ProjectCreate(ProjectBase):
    owner_id: Optional[UUID] = None  # Will be set from authenticated user if not provided

# Project Update Schema
class ProjectUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    status: Optional[ProjectStatusEnum] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    tags: Optional[List[str]] = None
    properties: Optional[Dict[str, Any]] = None
    storage_quota: Optional[int] = None
    is_public: Optional[bool] = None

# Project Response Schema
class ProjectResponse(ProjectBase):
    project_id: UUID
    owner_id: Optional[UUID] = None
    created_at: datetime
    updated_at: datetime
    storage_used: int = 0
    document_count: int = 0
    
    model_config = ConfigDict(from_attributes=True)

# Brief Project Response (for listings)
class ProjectBriefResponse(BaseModel):
    project_id: UUID
    name: str
    description: Optional[str] = None
    status: ProjectStatusEnum
    owner_id: Optional[UUID] = None
    created_at: datetime
    document_count: int = 0
    
    model_config = ConfigDict(from_attributes=True)

# Project with Owner Response
class ProjectWithOwnerResponse(ProjectResponse):
    owner: Optional['UserBriefResponse'] = None

# Project with Users Response
class ProjectWithUsersResponse(ProjectResponse):
    owner: Optional['UserBriefResponse'] = None
    users: List['ProjectUserResponse'] = []

# User-Project Association Schema
class UserProjectAssociation(BaseModel):
    user_id: UUID
    project_id: UUID
    role: ProjectRoleEnum = ProjectRoleEnum.VIEWER

# User Project Response (with role)
class ProjectUserResponse(BaseModel):
    user_id: UUID
    username: str
    email: str
    full_name: Optional[str] = None
    role: ProjectRoleEnum
    joined_at: datetime
    is_active: bool
    
    model_config = ConfigDict(from_attributes=True)

# Add User to Project Schema
class AddUserToProject(BaseModel):
    user_id: UUID
    role: ProjectRoleEnum = ProjectRoleEnum.VIEWER

# Update User Role in Project Schema
class UpdateUserRoleInProject(BaseModel):
    role: ProjectRoleEnum

# Project List Response
class ProjectListResponse(BaseModel):
    projects: List[ProjectResponse]
    total: int
    page: int
    page_size: int

# Project Statistics
class ProjectStatistics(BaseModel):
    project_id: UUID
    total_documents: int
    storage_used: int
    storage_quota: Optional[int]
    total_users: int
    active_users: int
    recent_uploads: int  # Last 7 days

# Import for forward references
from properties_service.app.schemas.user import UserBriefResponse

# User Brief Response (for project owner)
class UserBriefResponse(BaseModel):
    user_id: UUID
    username: str
    email: str
    full_name: Optional[str] = None
    
    model_config = ConfigDict(from_attributes=True)

ProjectWithOwnerResponse.model_rebuild()
ProjectWithUsersResponse.model_rebuild()
