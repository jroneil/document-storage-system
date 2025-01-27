```
├── metadata-service/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── models/
│   │   │   └── document.py
│   │   ├── services/
│   │   │   ├── mongo_service.py
│   │   │   ├── postgres_service.py
│   │   │   └── message_queue.py
│   │   ├── utils/
│   │   │   └── db_utils.py
│   │   └── tests/
│   │       └── test_metadata.py
│   ├── requirements.txt
│   └── Dockerfile
├── docker-compose.yml
```
# Project documentation
# Metadata Service

This service manages metadata objects using a hybrid database approach:
- PostgreSQL for structured data (stand properties).
- MongoDB for flexible, document-specific metadata.

## Setup
1. Install dependencies:
   ```bash
   pip install -r requirements.txt# API Documentation

The Metadata Service API allows you to manage **stand properties**, **dynamic metadata**, and **branding configurations**. Below are the available endpoints and examples of how to use them.

---

## Base URL

All API endpoints are relative to the base URL:
http://localhost:8000

---

## 1. Stand Properties

### Create Stand Properties

- **Endpoint**: `POST /stand-properties/`
- **Description**: Create a new stand property.
- **Request Body**:

json
```
  {

    "name": "Stand 1",
    "location": "Hall A",
    "attributes": {
      "size": "large",
      "theme": "modern"
    }
  }
  ```
  - Response
```json
{
  "id": 1,
  "name": "Stand 1",
  "location": "Hall A",
  "attributes": {
    "size": "large",
    "theme": "modern"
  }
}
```
  
 
# Get Stand Properties
- Endpoint: GET /stand-properties/{stand_id}

- Description: Retrieve stand properties by ID.

- Response:
```
{
  "id": 1,
  "name": "Stand 1",
  "location": "Hall A",
  "attributes": {
    "size": "large",
    "theme": "modern"
  }
}
```
2. Dynamic Metadata
Create Dynamic Metadata
 Endpoint: POST /dynamic-metadata/

- Description: Create new dynamic metadata. 
- Optionally, specify a brand_id to enforce   brand-specific metadata requirements.

Request Body:
```
{
  "document_id": "doc123",
  "metadata": {
    "product_name": "Widget X",
    "price": 29.99,
    "release_date": "2023-10-01"
  }
}
```
- Query Parameter:

   - brand_id (optional): UUID of the brand to validate metadata against.

- Response:
```
{
  "id": "650d4f5e8f1b2c3d4e5f6a7b"
}
```
Get Dynamic Metadata
- Endpoint: GET /dynamic-metadata/{document_id}

- Description: Retrieve dynamic metadata by document ID.

Response:
```
{
  "document_id": "doc123",
  "metadata": {
    "product_name": "Widget X",
    "price": 29.99,
    "release_date": "2023-10-01"
  }
}
```
3. Branding
Create Brand
Endpoint: POST /brands/

- Description: Create a new brand with required metadata fields.

Request Body:
```
{
  "name": "Example Brand",
  "required_metadata": {
    "product_name": "string",
    "price": "number",
    "release_date": "string"
  }
}
```
- Response:
```
{
  "brand_id": "a1b2c3d4-e5f6-7890-1234-567890abcdef",
  "name": "Example Brand",
  "required_metadata": {
    "product_name": "string",
    "price": "number",
    "release_date": "string"
  }
}
```
Get Brand
- Endpoint: GET /brands/{brand_id}

- Description: Retrieve brand details by ID.

- Response:
```
{
  "brand_id": "a1b2c3d4-e5f6-7890-1234-567890abcdef",
  "name": "Example Brand",
  "required_metadata": {
    "product_name": "string",
    "price": "number",
    "release_date": "string"
  }
}
```
Example Workflow
1. Create a Brand
```
curl -X POST "http://localhost:8000/brands/" \
-H "Content-Type: application/json" \
-d '{
  "name": "Example Brand",
  "required_metadata": {
    "product_name": "string",
    "price": "number",
    "release_date": "string"
  }
}'
```
2. Create Dynamic Metadata with Brand Validation
```
curl -X POST "http://localhost:8000/dynamic-metadata/?brand_id=a1b2c3d4-e5f6-7890-1234-567890abcdef" \
-H "Content-Type: application/json" \
-d '{
  "document_id": "doc123",
  "metadata": {
    "product_name": "Widget X",
    "price": 29.99,
    "release_date": "2023-10-01"
  }
}'
```
3. Retrieve Dynamic Metadata
```
curl -X GET "http://localhost:8000/dynamic-metadata/doc123"

```
Error Responses
Validation Error
If required metadata fields are missing or invalid:
```
{
  "detail": "Field product_name must be of type string"
}
```
Not Found Error
If a resource (e.g., stand, metadata, or brand) is not found:
```
{
  "detail": "Resource not found"
}
```
Running the Service
1. Install dependencies:

```
pip install -r requirements.txt
```
2 .Start the FastAPI app:
```
uvicorn app.main:app --reload
```
3. Use the API endpoints as described above.


6. Running the Services
Build and start the services using Docker Compose:

```
bash
Copy
docker-compose up --build
Access the Metadata Service API at:
```
```
http://localhost:8000
```
Access PostgreSQL at:
```

Host: localhost
Port: 5432
User: user
Password: password
Database: metadata_db
```
Access MongoDB at:

```
Host: localhost
Port: 27017
User: admin
Password: admin
```
7. Environment Variables
The docker-compose.yml file sets the following environment variables:
```
PostgreSQL:

POSTGRES_USER: Database user.

POSTGRES_PASSWORD: Database password.

POSTGRES_DB: Database name.

POSTGRES_HOST: Hostname of the PostgreSQL service.

MongoDB:

MONGO_HOST: Hostname of the MongoDB service.

MONGO_PORT: Port of the MongoDB service.
```
Metadata Service:

These variables are passed to the service to connect to the databases.

8. Persistent Data Storage
PostgreSQL: Data is stored in the postgres_data volume.

MongoDB: Data is stored in the mongo_data volume.

These volumes ensure that data persists even if the containers are stopped or removed.

9. Stopping the Services
To stop the services, run:
```
docker-compose down
```
To remove volumes as well, use:
```
docker-compose down --volumes
```
This setup provides a complete development environment for the Metadata Service, including PostgreSQL and MongoDB. Let me know if you need further assistance!


