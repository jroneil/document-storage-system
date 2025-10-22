# Bulk Upload Service Implementation Summary

## Overview
The bulk upload service has been enhanced to support parsing records in CSV, JSON, XML, and Excel formats. The parsed data is normalized according to the canonical schema and sent to the metadata service via RabbitMQ for database storage.

## Key Features Implemented

### 1. Multi-Format File Parsing
- **CSV**: Stream parsing with validation
- **JSON**: Support for both array of objects and single object formats
- **XML**: Flexible parsing with support for various XML structures
- **Excel**: Support for both .xlsx and .xls formats

### 2. Canonical Schema Compliance
All parsed records are normalized to the following canonical schema:

```json
{
  "record_id": "string",                // SHA256 hash of stable fields
  "source": {
    "job_id": "uuid",
    "batch_id": "integer",
    "row_num": "integer",
    "filename": "string",
    "schema_version": "v1"
  },
  "asset": {
    "file_name": "string",
    "file_size": "integer",
    "file_type": "string",
    "version": "integer",
    "checksum": "string",
    "storage_path": "string",
    "thumbnail_path": "string|null",
    "expiration_date": "string|null"    // ISO 8601 date YYYY-MM-DD
  },
  "ownership": {
    "uploader_user_id": "string",
    "acl": {
      "read": ["string"],
      "write": ["string"]
    }
  },
  "metadata": {
    "tags": ["string"],
    "description": "string|null",
    "category": "string|null",
    "division": "string|null",
    "business_unit": "string|null",
    "brand_id": "string|null",
    "document_type": "string|null",
    "region": "string|null",
    "country": "string|null",
    "languages": ["string"],
    "alternate_part_numbers": ["string"]
  }
}
```

### 3. Validation and Error Handling
- **Required Fields**: file_name, file_size, file_type, user_id, storage_path, version, checksum, acl
- **Type Validation**: Integer validation for file_size and version
- **Date Validation**: ISO 8601 format (YYYY-MM-DD) for expiration_date
- **ACL Validation**: JSON parsing with read/write arrays
- **List Processing**: Comma-separated values for tags, languages, alternate_part_numbers
- **Error Collection**: Per-row validation errors without job failure

### 4. Batch Processing
- Records are processed in batches (default: 500 records)
- Job tracking with unique job_id
- Validation errors are collected and reported
- Batch messages sent to RabbitMQ queue "bulk_metadata_upload"

## API Endpoints

### POST /bulk-upload
Upload and process bulk metadata files.

**Request:**
- Multipart form data with file
- Supported file types: CSV, JSON, XML, Excel (.xlsx, .xls)

**Response:**
```json
{
  "message": "Bulk upload processing started",
  "job_id": "uuid-string",
  "records_processed": 10,
  "validation_errors": 0,
  "source_file": "input.csv"
}
```

### GET /jobs/{job_id}
Get job status and processing results (placeholder implementation).

### GET /health
Health check endpoint for monitoring.

## File Format Examples

### CSV Format
```csv
transaction_type,file_name,file_size,file_type,user_id,tags,description,storage_path,version,checksum,acl,thumbnail_path,expiration_date,category,division,business_unit,brand_id,document_type,region,country,languages,alternate_part_numbers
new,technical_manual_v1.pdf,5242880,application/pdf,user-001,"technical,manual,engineering","Technical manual for product X","/documents/tech/manual_v1.pdf",1,abc123def456,"{""read"": [""user-001"", ""user-002""], ""write"": [""user-001""]}","/thumbnails/tech_manual_v1.jpg",2026-12-31,Technical Documentation,Engineering,Product Development,brand-001,Manual,EMEA,Germany,"en,de","PN-001-A,PN-001-B"
```

### JSON Format
```json
[
  {
    "transaction_type": "new",
    "file_name": "technical_manual_v1.pdf",
    "file_size": 5242880,
    "file_type": "application/pdf",
    "user_id": "user-001",
    "tags": "technical,manual,engineering",
    "description": "Technical manual for product X",
    "storage_path": "/documents/tech/manual_v1.pdf",
    "version": 1,
    "checksum": "abc123def456",
    "acl": "{\"read\": [\"user-001\", \"user-002\"], \"write\": [\"user-001\"]}",
    "thumbnail_path": "/thumbnails/tech_manual_v1.jpg",
    "expiration_date": "2026-12-31",
    "category": "Technical Documentation",
    "division": "Engineering",
    "business_unit": "Product Development",
    "brand_id": "brand-001",
    "document_type": "Manual",
    "region": "EMEA",
    "country": "Germany",
    "languages": "en,de",
    "alternate_part_numbers": "PN-001-A,PN-001-B"
  }
]
```

### XML Format
```xml
<?xml version="1.0" encoding="UTF-8"?>
<records>
  <record>
    <transaction_type>new</transaction_type>
    <file_name>technical_manual_v1.pdf</file_name>
    <file_size>5242880</file_size>
    <file_type>application/pdf</file_type>
    <user_id>user-001</user_id>
    <tags>technical,manual,engineering</tags>
    <description>Technical manual for product X</description>
    <storage_path>/documents/tech/manual_v1.pdf</storage_path>
    <version>1</version>
    <checksum>abc123def456</checksum>
    <acl>{"read": ["user-001", "user-002"], "write": ["user-001"]}</acl>
    <thumbnail_path>/thumbnails/tech_manual_v1.jpg</thumbnail_path>
    <expiration_date>2026-12-31</expiration_date>
    <category>Technical Documentation</category>
    <division>Engineering</division>
    <business_unit>Product Development</business_unit>
    <brand_id>brand-001</brand_id>
    <document_type>Manual</document_type>
    <region>EMEA</region>
    <country>Germany</country>
    <languages>en,de</languages>
    <alternate_part_numbers>PN-001-A,PN-001-B</alternate_part_numbers>
  </record>
</records>
```

## Dependencies Added
- `xmltodict`: For XML parsing
- `pandas`: For enhanced data processing (future use)

## Testing
The implementation includes comprehensive test files:
- `sample_document_metadata.csv` - Original CSV sample
- `sample_document_metadata.json` - JSON format sample
- `sample_document_metadata.xml` - XML format sample
- `test_parser.py` - Parser testing script
- `test_app.py` - FastAPI app testing script

## Integration with Metadata Service
- Parsed records are sent to RabbitMQ queue "bulk_metadata_upload"
- The metadata service should listen to this queue for processing
- Batch messages include job tracking and validation error information

## Next Steps
1. **Metadata Service Integration**: Ensure metadata service is listening to "bulk_metadata_upload" queue
2. **Job Status Tracking**: Implement persistent job status tracking
3. **Error Handling**: Enhanced error reporting and retry mechanisms
4. **Performance Optimization**: Streaming processing for large files
5. **Authentication**: Add authentication to API endpoints

## Usage Example
Files can be uploaded from the bulk-upload page in the upload-ui, which will send them to the `/bulk-upload` endpoint for processing.
