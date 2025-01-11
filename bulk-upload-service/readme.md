bulk-upload-service/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── services/
│   │   ├── file_upload.py
│   │   ├── metadata_parser.py
│   │   └── metadata_client.py
│   ├── utils/
│   │   └── file_utils.py
│   └── tests/
│       └── test_bulk_upload.py
├── requirements.txt
└── Dockerfile
10. Running the Service
Build the Docker image:

```
docker build -t bulk-upload-service .
```
# Run the service using Docker Compose:

```
# docker-compose.yml
version: '3.8'
services:
  bulk-upload-service:
    build: ./bulk-upload-service
    ports:
      - "5008:5008"
    environment:
      - METADATA_SERVICE_URL=http://metadata-service:5001
    depends_on:
      - metadata-service
```
# Start the service:

```
docker-compose up
```

11. Example API Request
You can test the bulk upload endpoint using curl or Postman.

CSV File
```
curl -X POST -F "file=@test_metadata.csv" http://localhost:5008/bulk-upload
```
Excel File
```
curl -X POST -F "file=@test_metadata.xlsx" http://localhost:5008/bulk-upload
```
Conclusion
The Bulk Upload Service allows users to upload metadata in CSV or Excel format. It parses the files and sends the metadata to the Metadata Service for storage. This service is modular, scalable, and integrates seamlessly with the rest of your Document Storage System.

Let me know if you need further assistance!