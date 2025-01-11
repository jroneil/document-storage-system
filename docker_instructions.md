# How to Use the Docker Compose File
- Save the docker-compose.yml file in the root directory of your project.

- Ensure each service has a Dockerfile in its respective directory (e.g., ingestion-service/Dockerfile, metadata-service/Dockerfile, etc.).

- Run the following command to start all services:
```
docker-compose up --build
```
# Access the services:

- API Gateway: http://localhost:8000

- Swagger UI: http://localhost:8000/docs

- RabbitMQ Management: http://localhost:15672

- MinIO Console: http://localhost:9001

- MailHog (SMTP Testing): http://localhost:8025

# Explanation of Services
## API Gateway:

- Acts as the single entry point for all client requests.

- Routes requests to the appropriate microservices.

## Ingestion Service:

Handles file uploads and metadata extraction.

Sends metadata to the Metadata Service via RabbitMQ.

## Metadata Service:

Manages metadata in PostgreSQL and MongoDB.

Listens for events from RabbitMQ.

# Storage Service:

# Stores files in MinIO (S3-compatible object storage).

# Processing Service:

Processes files (e.g., text extraction, thumbnail generation).

# Search Service:

Indexes documents and metadata in Elasticsearch.

# AI Service:

Performs AI-related tasks (e.g., content analysis, classification).

# Notification Service:

Sends notifications (e.g., emails) using an SMTP server.

# Databases:

- PostgreSQL: Stores structured metadata.

- MongoDB: Stores flexible metadata.

- Elasticsearch: Indexes documents for search functionality.

# Message Queue:

- RabbitMQ: Handles event-driven communication between services.

- Object Storage:

- MinIO: Provides S3-compatible object storage for file uploads.

# SMTP Server:

MailHog: A local SMTP server for testing email notifications.

## Conclusion
This docker-compose.yml file sets up all the services, databases, and the API Gateway for your Document Storage System. It uses Docker volumes to persist data and ensures all services are connected and ready to use.


