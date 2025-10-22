# pgAdmin Setup for Document Management System

## Overview

This document explains how to set up and use pgAdmin to view and manage the PostgreSQL database in the Document Management System.

## Accessing pgAdmin

1. **Start the services**:
   ```bash
   docker-compose up -d
   ```

2. **Access pgAdmin**:
   - Open your web browser and go to: `http://localhost:5050`
   - Login credentials:
     - **Email**: `admin@dms.com`
     - **Password**: `admin`

## Connecting to PostgreSQL Database

### Step 1: Add a New Server

1. In pgAdmin, right-click on **Servers** in the left sidebar
2. Select **Register** → **Server**

### Step 2: Configure Server Connection

Fill in the following details in the **General** tab:
- **Name**: `DMS PostgreSQL` (or any name you prefer)

In the **Connection** tab:
- **Host name/address**: `postgres` (this is the Docker service name)
- **Port**: `5432`
- **Maintenance database**: `document_storage`
- **Username**: `admin`
- **Password**: `password`
- **Save password?**: ☑ Yes

### Step 3: Test Connection

Click **Save** to test the connection. You should see the server appear in the left sidebar.

## Database Structure

Once connected, you can explore the following:

### Main Tables

1. **documents** - Contains document metadata
   - `document_id` (UUID, Primary Key)
   - `file_name`, `file_size`, `file_type`
   - `upload_date`, `last_modified_date`
   - `user_id`, `tags`, `description`
   - `storage_path`, `version`, `checksum`
   - `category`, `division`, `business_unit`
   - `document_type`, `brand_id`

2. **brands** - Contains brand information
   - `brand_id` (UUID, Primary Key)
   - `name`, `required_metadata`

3. **stand_metadata** - Contains stand metadata
   - `id` (Integer, Primary Key)
   - `name`, `location`, `attributes`

### Useful Queries

#### View All Documents
```sql
SELECT * FROM documents ORDER BY upload_date DESC;
```

#### Count Documents by Type
```sql
SELECT document_type, COUNT(*) as count 
FROM documents 
GROUP BY document_type 
ORDER BY count DESC;
```

#### Find Documents by Category
```sql
SELECT document_id, file_name, category, upload_date 
FROM documents 
WHERE category IS NOT NULL 
ORDER BY category, upload_date DESC;
```

#### Check Database Size
```sql
SELECT 
    pg_size_pretty(pg_database_size('document_storage')) as database_size;
```

## Common Operations

### View Table Data
1. Expand the server → Databases → `document_storage` → Schemas → `public` → Tables
2. Right-click on any table and select **View/Edit Data** → **All Rows**

### Run Custom Queries
1. Click on **Tools** → **Query Tool**
2. Write your SQL query and click **Execute** (F5)

### Export Data
1. Right-click on a table
2. Select **Import/Export**
3. Choose export format (CSV, JSON, etc.)

## Troubleshooting

### Connection Issues
- **Error**: "Could not connect to server"
  - Ensure PostgreSQL container is running: `docker ps | grep postgres`
  - Check if PostgreSQL is healthy: `docker logs postgres`

### Permission Issues
- **Error**: "Permission denied"
  - Verify username and password match the docker-compose.yml configuration
  - Check that the database name is `document_storage`

### Network Issues
- **Error**: "Host not found"
  - Ensure pgAdmin and PostgreSQL are on the same Docker network
  - Use `postgres` as the hostname (Docker service name)

## Security Notes

- Change the default pgAdmin password in production
- Consider using environment variables for sensitive data
- Regularly backup the pgAdmin configuration volume

## Useful Links

- [pgAdmin Documentation](https://www.pgadmin.org/docs/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
