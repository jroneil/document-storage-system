# User-Project Structure Documentation

## Overview

This document describes the user-project management system implemented in the metadata service. The system provides comprehensive user authentication, authorization, and project collaboration features.

## Database Schema

### Users Table

The `users` table stores user account information:

| Column | Type | Description |
|--------|------|-------------|
| user_id | UUID | Primary key |
| username | String(100) | Unique username |
| email | String(255) | Unique email address |
| full_name | String(255) | User's full name |
| password_hash | String(255) | Bcrypt hashed password |
| role | Enum | User role (admin, manager, member, viewer) |
| is_active | Boolean | Account active status |
| is_verified | Boolean | Email verification status |
| created_at | DateTime | Account creation timestamp |
| updated_at | DateTime | Last update timestamp |
| last_login | DateTime | Last login timestamp |
| profile_picture | String(500) | Profile picture URL |
| phone_number | String(20) | Contact number |
| department | String(100) | Department name |
| job_title | String(100) | Job title |
| metadata | JSONB | Additional user metadata |

### Projects Table

The `projects` table stores project information:

| Column | Type | Description |
|--------|------|-------------|
| project_id | UUID | Primary key |
| name | String(255) | Project name |
| description | Text | Project description |
| status | Enum | Project status (active, archived, deleted) |
| owner_id | UUID | Foreign key to users table |
| created_at | DateTime | Project creation timestamp |
| updated_at | DateTime | Last update timestamp |
| start_date | DateTime | Project start date |
| end_date | DateTime | Project end date |
| tags | Array[String] | Project tags |
| metadata | JSONB | Additional project metadata |
| storage_quota | BigInteger | Storage quota in bytes |
| storage_used | BigInteger | Storage used in bytes |
| document_count | Integer | Number of documents |
| is_public | Boolean | Public visibility flag |

### User-Projects Association Table

The `user_projects` table manages many-to-many relationships between users and projects:

| Column | Type | Description |
|--------|------|-------------|
| id | Integer | Primary key |
| user_id | UUID | Foreign key to users table |
| project_id | UUID | Foreign key to projects table |
| role | Enum | User role in project (owner, admin, editor, viewer) |
| joined_at | DateTime | When user joined project |
| is_active | Boolean | Active membership status |

## User Roles

### System-Level Roles
- **Admin**: Full system access and management
- **Manager**: Can manage teams and projects
- **Member**: Regular user with standard permissions
- **Viewer**: Read-only access

### Project-Level Roles
- **Owner**: Full project control
- **Admin**: Can manage project settings and users
- **Editor**: Can create and edit content
- **Viewer**: Read-only project access

## API Endpoints

### User Endpoints

#### Create User
```http
POST /users/
Content-Type: application/json

{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "securepassword123",
  "full_name": "John Doe",
  "role": "member"
}
```

#### List Users
```http
GET /users/?skip=0&limit=100&role=member&is_active=true&search=john
```

#### Get User
```http
GET /users/{user_id}
```

#### Update User
```http
PUT /users/{user_id}
Content-Type: application/json

{
  "full_name": "John Smith",
  "department": "Engineering"
}
```

#### Delete User
```http
DELETE /users/{user_id}
```

#### Authenticate User
```http
POST /users/authenticate
Content-Type: application/json

{
  "username": "john_doe",
  "password": "securepassword123"
}
```

#### Change Password
```http
POST /users/{user_id}/change-password
Content-Type: application/json

{
  "old_password": "oldpassword123",
  "new_password": "newpassword456"
}
```

### Project Endpoints

#### Create Project
```http
POST /projects/
Content-Type: application/json

{
  "name": "My Project",
  "description": "Project description",
  "owner_id": "user-uuid-here",
  "tags": ["important", "client-work"],
  "storage_quota": 10737418240,
  "is_public": false
}
```

#### List Projects
```http
GET /projects/?skip=0&limit=100&status=active&search=project
```

#### Get Project
```http
GET /projects/{project_id}
```

#### Update Project
```http
PUT /projects/{project_id}
Content-Type: application/json

{
  "name": "Updated Project Name",
  "description": "Updated description"
}
```

#### Delete Project
```http
DELETE /projects/{project_id}
```

#### Archive Project
```http
POST /projects/{project_id}/archive
```

#### Add User to Project
```http
POST /projects/{project_id}/users
Content-Type: application/json

{
  "user_id": "user-uuid-here",
  "role": "editor"
}
```

#### Remove User from Project
```http
DELETE /projects/{project_id}/users/{user_id}
```

#### Update User Role
```http
PUT /projects/{project_id}/users/{user_id}/role
Content-Type: application/json

{
  "role": "admin"
}
```

#### Get Project Statistics
```http
GET /projects/{project_id}/statistics
```

## Setup Instructions

### 1. Install Dependencies

```bash
cd metadata-service
pip install -r requirements.txt
```

### 2. Configure Environment

Create or update `.env` file:

```env
POSTGRES_URL=postgresql://postgres:postgres@localhost:5432/metadata_db
```

### 3. Run Database Migrations

```bash
# Create tables
python -m app.migrations.create_user_project_tables

# To drop tables (use with caution)
python -m app.migrations.create_user_project_tables --drop
```

### 4. Start the Service

```bash
python run.py
```

The service will be available at `http://localhost:8000`

## Usage Examples

### Creating a User and Project

```python
import requests

# Create a user
user_response = requests.post(
    "http://localhost:8000/users/",
    json={
        "username": "jane_smith",
        "email": "jane@example.com",
        "password": "securepass123",
        "full_name": "Jane Smith",
        "role": "member"
    }
)
user_id = user_response.json()["user_id"]

# Create a project
project_response = requests.post(
    "http://localhost:8000/projects/",
    json={
        "name": "Client Project",
        "description": "Important client work",
        "owner_id": user_id,
        "storage_quota": 10737418240  # 10 GB
    }
)
project_id = project_response.json()["project_id"]

# Add another user to the project
requests.post(
    f"http://localhost:8000/projects/{project_id}/users",
    json={
        "user_id": "another-user-id",
        "role": "editor"
    }
)
```

## Security Considerations

1. **Password Hashing**: All passwords are hashed using bcrypt
2. **Authentication**: Implement JWT or session-based auth in production
3. **Authorization**: Verify user permissions before allowing operations
4. **Input Validation**: All inputs are validated using Pydantic schemas
5. **SQL Injection**: Protected by SQLAlchemy ORM

## Future Enhancements

- [ ] Implement JWT authentication
- [ ] Add OAuth2 support
- [ ] Email verification system
- [ ] Password reset functionality
- [ ] Audit logging
- [ ] Role-based access control (RBAC) middleware
- [ ] Project templates
- [ ] User groups/teams
- [ ] Project sharing and permissions

## Testing

Run the service and test using the FastAPI interactive docs:

```
http://localhost:8000/docs
```

## Troubleshooting

### Database Connection Issues
- Verify PostgreSQL is running
- Check database credentials in `.env`
- Ensure database exists

### Import Errors
- Verify all dependencies are installed
- Check Python path includes the project root

### Migration Fails
- Check database permissions
- Verify no existing tables with same names
- Review error messages for specific issues

## Support

For issues or questions, please refer to the main project documentation or contact the development team.
