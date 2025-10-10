from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_, or_, func
from typing import Optional, List
from uuid import UUID
from datetime import datetime, timedelta

from app.models.postgres_models import Project, User, ProjectStatus, ProjectRole, user_projects
from app.schemas.project import ProjectCreate, ProjectUpdate


def create_project(db: Session, project: ProjectCreate, owner_id: UUID) -> Project:
    """Create a new project."""
    db_project = Project(
        name=project.name,
        description=project.description,
        status=ProjectStatus(project.status),
        owner_id=owner_id,
        start_date=project.start_date,
        end_date=project.end_date,
        tags=project.tags,
        project_metadata=project.properties,
        storage_quota=project.storage_quota,
        is_public=project.is_public
    )
    
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    
    # Add owner to project users with OWNER role
    add_user_to_project(db, db_project.project_id, owner_id, ProjectRole.OWNER)
    
    return db_project


def get_project(db: Session, project_id: UUID) -> Optional[Project]:
    """Get a project by ID."""
    return db.query(Project).filter(Project.project_id == project_id).first()


def get_project_with_owner(db: Session, project_id: UUID) -> Optional[Project]:
    """Get a project with owner details."""
    return db.query(Project).options(
        joinedload(Project.owner)
    ).filter(Project.project_id == project_id).first()


def get_project_with_users(db: Session, project_id: UUID) -> Optional[Project]:
    """Get a project with all users."""
    return db.query(Project).options(
        joinedload(Project.owner),
        joinedload(Project.users)
    ).filter(Project.project_id == project_id).first()


def get_projects(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    owner_id: Optional[UUID] = None,
    status: Optional[str] = None,
    is_public: Optional[bool] = None,
    search: Optional[str] = None
) -> tuple[List[Project], int]:
    """Get a list of projects with filters."""
    query = db.query(Project)
    
    # Apply filters
    if owner_id:
        query = query.filter(Project.owner_id == owner_id)
    
    if status:
        query = query.filter(Project.status == ProjectStatus(status))
    
    if is_public is not None:
        query = query.filter(Project.is_public == is_public)
    
    if search:
        search_filter = or_(
            Project.name.ilike(f"%{search}%"),
            Project.description.ilike(f"%{search}%")
        )
        query = query.filter(search_filter)
    
    # Get total count
    total = query.count()
    
    # Apply pagination and order by creation date (newest first)
    projects = query.order_by(Project.created_at.desc()).offset(skip).limit(limit).all()
    
    return projects, total


def get_user_projects(
    db: Session,
    user_id: UUID,
    skip: int = 0,
    limit: int = 100,
    status: Optional[str] = None
) -> tuple[List[Project], int]:
    """Get all projects a user is part of."""
    query = db.query(Project).join(
        user_projects, Project.project_id == user_projects.c.project_id
    ).filter(user_projects.c.user_id == user_id)
    
    if status:
        query = query.filter(Project.status == ProjectStatus(status))
    
    # Get total count
    total = query.count()
    
    # Apply pagination
    projects = query.order_by(Project.created_at.desc()).offset(skip).limit(limit).all()
    
    return projects, total


def update_project(db: Session, project_id: UUID, project_update: ProjectUpdate) -> Optional[Project]:
    """Update a project."""
    db_project = get_project(db, project_id)
    if not db_project:
        return None
    
    # Update fields
    update_data = project_update.model_dump(exclude_unset=True)
    
    for field, value in update_data.items():
        if field == 'status' and value:
            value = ProjectStatus(value)
        setattr(db_project, field, value)
    
    db_project.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_project)
    return db_project


def delete_project(db: Session, project_id: UUID) -> bool:
    """Delete a project (soft delete by setting status to DELETED)."""
    db_project = get_project(db, project_id)
    if not db_project:
        return False
    
    db_project.status = ProjectStatus.DELETED
    db_project.updated_at = datetime.utcnow()
    db.commit()
    return True


def hard_delete_project(db: Session, project_id: UUID) -> bool:
    """Permanently delete a project."""
    db_project = get_project(db, project_id)
    if not db_project:
        return False
    
    db.delete(db_project)
    db.commit()
    return True


def archive_project(db: Session, project_id: UUID) -> Optional[Project]:
    """Archive a project."""
    db_project = get_project(db, project_id)
    if not db_project:
        return None
    
    db_project.status = ProjectStatus.ARCHIVED
    db_project.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_project)
    return db_project


def restore_project(db: Session, project_id: UUID) -> Optional[Project]:
    """Restore an archived or deleted project."""
    db_project = get_project(db, project_id)
    if not db_project:
        return None
    
    db_project.status = ProjectStatus.ACTIVE
    db_project.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_project)
    return db_project


def add_user_to_project(
    db: Session,
    project_id: UUID,
    user_id: UUID,
    role: ProjectRole = ProjectRole.VIEWER
) -> bool:
    """Add a user to a project."""
    # Check if association already exists
    existing = db.execute(
        user_projects.select().where(
            and_(
                user_projects.c.project_id == project_id,
                user_projects.c.user_id == user_id
            )
        )
    ).first()
    
    if existing:
        # Update role if association exists
        db.execute(
            user_projects.update().where(
                and_(
                    user_projects.c.project_id == project_id,
                    user_projects.c.user_id == user_id
                )
            ).values(role=role, is_active=True)
        )
    else:
        # Create new association
        db.execute(
            user_projects.insert().values(
                project_id=project_id,
                user_id=user_id,
                role=role,
                is_active=True
            )
        )
    
    db.commit()
    return True


def remove_user_from_project(db: Session, project_id: UUID, user_id: UUID) -> bool:
    """Remove a user from a project."""
    result = db.execute(
        user_projects.delete().where(
            and_(
                user_projects.c.project_id == project_id,
                user_projects.c.user_id == user_id
            )
        )
    )
    db.commit()
    return result.rowcount > 0


def update_user_role_in_project(
    db: Session,
    project_id: UUID,
    user_id: UUID,
    role: ProjectRole
) -> bool:
    """Update a user's role in a project."""
    result = db.execute(
        user_projects.update().where(
            and_(
                user_projects.c.project_id == project_id,
                user_projects.c.user_id == user_id
            )
        ).values(role=role)
    )
    db.commit()
    return result.rowcount > 0


def get_project_users(db: Session, project_id: UUID) -> List[dict]:
    """Get all users in a project with their roles."""
    result = db.execute(
        user_projects.select().where(
            user_projects.c.project_id == project_id
        )
    ).fetchall()
    
    users_data = []
    for row in result:
        user = db.query(User).filter(User.user_id == row.user_id).first()
        if user:
            users_data.append({
                'user_id': user.user_id,
                'username': user.username,
                'email': user.email,
                'full_name': user.full_name,
                'role': row.role,
                'joined_at': row.joined_at,
                'is_active': row.is_active
            })
    
    return users_data


def get_user_role_in_project(db: Session, project_id: UUID, user_id: UUID) -> Optional[ProjectRole]:
    """Get a user's role in a project."""
    result = db.execute(
        user_projects.select().where(
            and_(
                user_projects.c.project_id == project_id,
                user_projects.c.user_id == user_id
            )
        )
    ).first()
    
    return ProjectRole(result.role) if result else None


def update_project_storage(db: Session, project_id: UUID, size_delta: int) -> Optional[Project]:
    """Update project storage used."""
    db_project = get_project(db, project_id)
    if not db_project:
        return None
    
    db_project.storage_used = (db_project.storage_used or 0) + size_delta
    db.commit()
    db.refresh(db_project)
    return db_project


def increment_document_count(db: Session, project_id: UUID) -> Optional[Project]:
    """Increment project document count."""
    db_project = get_project(db, project_id)
    if not db_project:
        return None
    
    db_project.document_count = (db_project.document_count or 0) + 1
    db.commit()
    db.refresh(db_project)
    return db_project


def decrement_document_count(db: Session, project_id: UUID) -> Optional[Project]:
    """Decrement project document count."""
    db_project = get_project(db, project_id)
    if not db_project:
        return None
    
    db_project.document_count = max((db_project.document_count or 0) - 1, 0)
    db.commit()
    db.refresh(db_project)
    return db_project


def get_project_statistics(db: Session, project_id: UUID) -> Optional[dict]:
    """Get project statistics."""
    db_project = get_project(db, project_id)
    if not db_project:
        return None
    
    # Get total users
    total_users = db.execute(
        func.count(user_projects.c.user_id).select().where(
            user_projects.c.project_id == project_id
        )
    ).scalar()
    
    # Get active users (users who are is_active)
    active_users = db.execute(
        func.count(user_projects.c.user_id).select().where(
            and_(
                user_projects.c.project_id == project_id,
                user_projects.c.is_active == True
            )
        )
    ).scalar()
    
    return {
        'project_id': project_id,
        'total_documents': db_project.document_count or 0,
        'storage_used': db_project.storage_used or 0,
        'storage_quota': db_project.storage_quota,
        'total_users': total_users or 0,
        'active_users': active_users or 0,
        'recent_uploads': 0  # This would need document upload tracking
    }
