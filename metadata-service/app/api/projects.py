from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import Optional
from uuid import UUID

from app.models.postgres_models import ProjectRole
from app.schemas.project import (
    ProjectCreate, ProjectUpdate, ProjectResponse, ProjectListResponse,
    ProjectWithOwnerResponse, ProjectWithUsersResponse, ProjectStatistics,
    AddUserToProject, UpdateUserRoleInProject, ProjectUserResponse
)
from app.crud import project as crud_project
from app.services.postgres_service import get_db

router = APIRouter(prefix="/projects", tags=["projects"])


@router.post("/", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
def create_project(
    project: ProjectCreate,
    db: Session = Depends(get_db)
):
    """Create a new project."""
    # For now, using a dummy owner_id. In production, this should come from authenticated user
    # owner_id = current_user.user_id
    if not project.owner_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Owner ID is required"
        )
    
    db_project = crud_project.create_project(db, project, project.owner_id)
    return db_project


@router.get("/", response_model=ProjectListResponse)
def list_projects(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    owner_id: Optional[UUID] = None,
    status: Optional[str] = None,
    is_public: Optional[bool] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get a list of projects with optional filters."""
    projects, total = crud_project.get_projects(
        db, skip=skip, limit=limit, owner_id=owner_id,
        status=status, is_public=is_public, search=search
    )
    
    page = skip // limit + 1 if limit > 0 else 1
    
    return {
        "projects": projects,
        "total": total,
        "page": page,
        "page_size": limit
    }


@router.get("/user/{user_id}", response_model=ProjectListResponse)
def list_user_projects(
    user_id: UUID,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    status: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get all projects a user is part of."""
    projects, total = crud_project.get_user_projects(
        db, user_id, skip=skip, limit=limit, status=status
    )
    
    page = skip // limit + 1 if limit > 0 else 1
    
    return {
        "projects": projects,
        "total": total,
        "page": page,
        "page_size": limit
    }


@router.get("/{project_id}", response_model=ProjectResponse)
def get_project(project_id: UUID, db: Session = Depends(get_db)):
    """Get a specific project by ID."""
    db_project = crud_project.get_project(db, project_id)
    if not db_project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    return db_project


@router.get("/{project_id}/with-owner", response_model=ProjectWithOwnerResponse)
def get_project_with_owner(project_id: UUID, db: Session = Depends(get_db)):
    """Get a project with owner details."""
    db_project = crud_project.get_project_with_owner(db, project_id)
    if not db_project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    return db_project


@router.get("/{project_id}/with-users", response_model=ProjectWithUsersResponse)
def get_project_with_users(project_id: UUID, db: Session = Depends(get_db)):
    """Get a project with all users."""
    db_project = crud_project.get_project_with_users(db, project_id)
    if not db_project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    # Get user roles
    users_data = crud_project.get_project_users(db, project_id)
    
    # Convert to response format
    db_project.users = users_data
    return db_project


@router.put("/{project_id}", response_model=ProjectResponse)
def update_project(
    project_id: UUID,
    project_update: ProjectUpdate,
    db: Session = Depends(get_db)
):
    """Update a project."""
    db_project = crud_project.update_project(db, project_id, project_update)
    if not db_project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    return db_project


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(project_id: UUID, db: Session = Depends(get_db)):
    """Delete a project (soft delete)."""
    success = crud_project.delete_project(db, project_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    return None


@router.post("/{project_id}/archive", response_model=ProjectResponse)
def archive_project(project_id: UUID, db: Session = Depends(get_db)):
    """Archive a project."""
    db_project = crud_project.archive_project(db, project_id)
    if not db_project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    return db_project


@router.post("/{project_id}/restore", response_model=ProjectResponse)
def restore_project(project_id: UUID, db: Session = Depends(get_db)):
    """Restore an archived or deleted project."""
    db_project = crud_project.restore_project(db, project_id)
    if not db_project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    return db_project


@router.post("/{project_id}/users", status_code=status.HTTP_201_CREATED)
def add_user_to_project(
    project_id: UUID,
    user_data: AddUserToProject,
    db: Session = Depends(get_db)
):
    """Add a user to a project."""
    # Check if project exists
    db_project = crud_project.get_project(db, project_id)
    if not db_project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    success = crud_project.add_user_to_project(
        db, project_id, user_data.user_id, ProjectRole(user_data.role)
    )
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to add user to project"
        )
    
    return {"message": "User added to project successfully"}


@router.delete("/{project_id}/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_user_from_project(
    project_id: UUID,
    user_id: UUID,
    db: Session = Depends(get_db)
):
    """Remove a user from a project."""
    success = crud_project.remove_user_from_project(db, project_id, user_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found in project"
        )
    return None


@router.put("/{project_id}/users/{user_id}/role")
def update_user_role(
    project_id: UUID,
    user_id: UUID,
    role_update: UpdateUserRoleInProject,
    db: Session = Depends(get_db)
):
    """Update a user's role in a project."""
    success = crud_project.update_user_role_in_project(
        db, project_id, user_id, ProjectRole(role_update.role)
    )
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found in project"
        )
    
    return {"message": "User role updated successfully"}


@router.get("/{project_id}/users")
def get_project_users(project_id: UUID, db: Session = Depends(get_db)):
    """Get all users in a project."""
    # Check if project exists
    db_project = crud_project.get_project(db, project_id)
    if not db_project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    users = crud_project.get_project_users(db, project_id)
    return {"users": users}


@router.get("/{project_id}/users/{user_id}/role")
def get_user_role(
    project_id: UUID,
    user_id: UUID,
    db: Session = Depends(get_db)
):
    """Get a user's role in a project."""
    role = crud_project.get_user_role_in_project(db, project_id, user_id)
    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found in project"
        )
    return {"role": role}


@router.get("/{project_id}/statistics", response_model=ProjectStatistics)
def get_project_statistics(project_id: UUID, db: Session = Depends(get_db)):
    """Get project statistics."""
    stats = crud_project.get_project_statistics(db, project_id)
    if not stats:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    return stats
