# Docker Quick Start - User Portal Only

This guide helps you run just the User Portal and Metadata Service using Docker, without needing to start all microservices.

## What Gets Started

- **PostgreSQL**: Database for users and projects
- **Metadata Service**: Backend API (port 8000)
- **User Portal**: Frontend UI (port 3000)

## Prerequisites

- Docker Desktop installed and running
- Docker Compose v2.0 or higher

## Quick Start

### 1. Start the Services

```bash
docker-compose -f docker-compose.user-portal.yml up --build
```

This will:
- Pull PostgreSQL image
- Build metadata-service
- Build user-portal
- Run database migrations automatically
- Start all services

### 2. Access the Application

- **User Portal**: http://localhost:3000
- **API Documentation**: http://localhost:8000/docs
- **PostgreSQL**: localhost:5432

### 3. Create Your First User

1. Navigate to http://localhost:3000
2. Click on "Register" or go to http://localhost:3000/register
3. Fill in the form:
   - Username: `testuser`
   - Email: `test@example.com`
   - Password: `password123` (min 8 characters)
   - Full Name: `Test User`
4. Click "Create account"
5. You'll be redirected to the login page
6. Login with your credentials
7. Start creating projects!

## Stopping the Services

```bash
# Stop and remove containers
docker-compose -f docker-compose.user-portal.yml down

# Stop and remove containers + volumes (clears database)
docker-compose -f docker-compose.user-portal.yml down -v
```

## Viewing Logs

```bash
# All services
docker-compose -f docker-compose.user-portal.yml logs -f

# Specific service
docker-compose -f docker-compose.user-portal.yml logs -f metadata-service
docker-compose -f docker-compose.user-portal.yml logs -f user-portal
```

## Troubleshooting

### Port Already in Use

If ports 3000, 8000, or 5432 are already in use, you can modify the docker-compose file:

```yaml
ports:
  - "3001:3000"  # Change host port
```

### Database Connection Issues

If the metadata-service can't connect to PostgreSQL:

```bash
# Restart services
docker-compose -f docker-compose.user-portal.yml restart metadata-service
```

### Clear Everything and Start Fresh

```bash
# Stop and remove everything
docker-compose -f docker-compose.user-portal.yml down -v

# Remove images
docker rmi dms2project-metadata-service dms2project-user-portal

# Start again
docker-compose -f docker-compose.user-portal.yml up --build
```

### Can't Access User Portal

If the user portal shows a blank page:

1. Check if Next.js is running:
   ```bash
   docker logs dms-user-portal
   ```

2. Wait for "Ready in X ms" message

3. Refresh browser at http://localhost:3000

### API Connection Error

If the UI can't connect to the API:

1. Check if metadata-service is running:
   ```bash
   docker logs dms-metadata-service
   ```

2. Verify API is accessible:
   ```bash
   curl http://localhost:8000/docs
   ```

3. Check browser console for CORS errors

## Development Mode

The docker-compose setup uses volume mounts, so changes to your code will be reflected:

- **User Portal**: Hot reload enabled
- **Metadata Service**: Auto-reload enabled

Just edit files in your IDE and see changes immediately!

## Database Access

Connect to PostgreSQL directly:

```bash
docker exec -it dms-postgres psql -U postgres -d metadata_db
```

Useful SQL commands:

```sql
-- List tables
\dt

-- View users
SELECT * FROM users;

-- View projects
SELECT * FROM projects;

-- Exit
\q
```

## API Testing

Use the built-in API documentation:

1. Go to http://localhost:8000/docs
2. Try out endpoints directly
3. No authentication required for testing

## Next Steps

After running the user portal:

1. Create multiple users
2. Create projects for each user
3. Test user-project associations
4. Try the project management features

To integrate with other services later, use the full `docker-compose.yml` file.

## Support

For issues:
- Check logs: `docker-compose -f docker-compose.user-portal.yml logs`
- Verify containers: `docker ps`
- Check network: `docker network ls`
You have an old PostgreSQL 13 volume that's incompatible with the new PostgreSQL 15 image. Here's how to fix it:

## 🔧 Quick Fix

Run this command to remove the old volume and start fresh:

```bash
docker-compose -f docker-compose.user-portal.yml down -v
docker-compose -f docker-compose.user-portal.yml up --build
```

The `-v` flag removes the old database volume, allowing PostgreSQL 15 to initialize a fresh database.

## ⚠️ Important Note

This will **delete all existing data** in your PostgreSQL database. Since you're just setting up the user portal for the first time, this is fine. All your users and projects will be gone, but you can recreate them.

## 🎯 Step-by-Step Solution

1. **Stop and remove everything** (including the incompatible volume):
   ```bash
   docker-compose -f docker-compose.user-portal.yml down -v
   ```

2. **Start fresh**:
   ```bash
   docker-compose -f docker-compose.user-portal.yml up --build
   ```

3. **Verify it's working**:
   - Wait for "Running migrations..." message
   - Look for "Starting server..." message
   - Access http://localhost:3000

## 🔍 What Happened?

- You had an old PostgreSQL 13 database from a previous Docker setup
- The new compose file uses PostgreSQL 15
- PostgreSQL can't upgrade databases automatically between major versions
- Solution: Remove the old volume and let PostgreSQL 15 create a new one

## ✅ After the Fix

Once it's running, you'll have:
- Fresh PostgreSQL 15 database
- All tables created automatically via migrations
- Clean slate to create users and projects

The error won't happen again unless you switch PostgreSQL versions in the future!