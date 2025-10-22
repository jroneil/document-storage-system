Got it — here’s how Cline should handle this CSV sample

Your upload service should:

Stream-parse the CSV.
Validate and normalize fields into a canonical JSON shape.
Batch and publish to the queue.

Below are:

Canonical schema
CSV-to-canonical mapping rules (including complex fields)
Validation rules
Example normalized JSON output for your sample rows
Batch message payload example
Canonical record schema
{
  "record_id": "string",                // sha256 over stable fields (see below)
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

CSV → canonical mapping rules
file_name → asset.file_name
file_size → asset.file_size (int)
file_type → asset.file_type
user_id → ownership.uploader_user_id
tags → metadata.tags (split on comma, trim)
description → metadata.description
storage_path → asset.storage_path
version → asset.version (int)
checksum → asset.checksum
acl → ownership.acl (parse JSON string)
thumbnail_path → asset.thumbnail_path (nullable if empty)
expiration_date → asset.expiration_date (validate YYYY-MM-DD; nullable)
category → metadata.category
division → metadata.division
business_unit → metadata.business_unit
brand_id → metadata.brand_id
document_type → metadata.document_type
region → metadata.region
country → metadata.country
languages → metadata.languages (split on comma, trim, lowercase ISO codes)
alternate_part_numbers → metadata.alternate_part_numbers (split on comma, trim)

Record ID:

record_id = sha256(lowercase(file_name) + '|' + checksum + '|' + storage_path)
Deterministic and stable across retries.
Validation rules
Required: file_name, file_size (>=0), file_type, user_id, storage_path, version (>=1), checksum, acl
Types:
file_size: integer
version: integer
expiration_date: date YYYY-MM-DD or blank
acl: JSON with arrays read, write
Sets:
tags, languages, alternate_part_numbers: split by comma, trim empties
Max sizes:
tags <= 50, languages <= 20, alt part numbers <= 50
file_type must be a valid MIME type pattern type/subtype
Paths must start with /
On validation error: collect per-row error; don’t drop job.
Example normalized JSON for your sample (first two rows)

Row 1

{
  "record_id": "sha256(technical_manual_v1.pdf|abc123def456|/documents/tech/manual_v1.pdf)",
  "source": {
    "job_id": "<uuid>",
    "batch_id": 1,
    "row_num": 2,
    "filename": "input.csv",
    "schema_version": "v1"
  },
  "asset": {
    "file_name": "technical_manual_v1.pdf",
    "file_size": 5242880,
    "file_type": "application/pdf",
    "version": 1,
    "checksum": "abc123def456",
    "storage_path": "/documents/tech/manual_v1.pdf",
    "thumbnail_path": "/thumbnails/tech_manual_v1.jpg",
    "expiration_date": "2026-12-31"
  },
  "ownership": {
    "uploader_user_id": "user-001",
    "acl": {
      "read": ["user-001", "user-002"],
      "write": ["user-001"]
    }
  },
  "metadata": {
    "tags": ["technical", "manual", "engineering"],
    "description": "Technical manual for product X",
    "category": "Technical Documentation",
    "division": "Engineering",
    "business_unit": "Product Development",
    "brand_id": "brand-001",
    "document_type": "Manual",
    "region": "EMEA",
    "country": "Germany",
    "languages": ["en", "de"],
    "alternate_part_numbers": ["PN-001-A", "PN-001-B"]
  }
}


Row 2

{
  "record_id": "sha256(marketing_brochure.pdf|def456ghi789|/documents/marketing/brochure.pdf)",
  "source": {
    "job_id": "<uuid>",
    "batch_id": 1,
    "row_num": 3,
    "filename": "input.csv",
    "schema_version": "v1"
  },
  "asset": {
    "file_name": "marketing_brochure.pdf",
    "file_size": 2097152,
    "file_type": "application/pdf",
    "version": 1,
    "checksum": "def456ghi789",
    "storage_path": "/documents/marketing/brochure.pdf",
    "thumbnail_path": "/thumbnails/marketing_brochure.jpg",
    "expiration_date": "2025-06-30"
  },
  "ownership": {
    "uploader_user_id": "user-002",
    "acl": {
      "read": ["user-002", "user-003"],
      "write": ["user-002"]
    }
  },
  "metadata": {
    "tags": ["marketing", "sales", "brochure"],
    "description": "Marketing brochure for product launch",
    "category": "Marketing Materials",
    "division": "Marketing",
    "business_unit": "Sales",
    "brand_id": "brand-002",
    "document_type": "Brochure",
    "region": "NA",
    "country": "USA",
    "languages": ["en", "es"],
    "alternate_part_numbers": ["PN-002-A"]
  }
}


Row 3 (partial, truncated in your sample)

Same mapping; ensure file_type is the Excel MIME.
languages: ["en", "ja"].
If expiration_date is “2024-12-31”, accept as valid.
Batch message payload sent to queue (inline variant)
{
  "job_id": "<uuid>",
  "batch_id": 1,
  "total_batches": 1,             // fill when known, else omit and set later
  "schema_version": "v1",
  "source_file": "input.csv",
  "records": [
    { /* normalized row 1 as above */ },
    { /* normalized row 2 as above */ }
    // ...
  ]
}

Notes for Cline (implementation checklist)
Use a streaming CSV parser (e.g., Node: csv-parse with from: fs.createReadStream).
For acl, parse the JSON string (double-escaped) safely; if parse fails, log validation error.
Normalize lists: split by ,, trim, filter empty, languages to lowercase.
Compute record_id using crypto.createHash('sha256').update(key).digest('hex').
Batch size: env BATCH_SIZE=500 or cap by size MAX_MESSAGE_BYTES=4MB.
Publish to chosen queue with key/partition = job_id.
On parse/validation error per row: add to errors store tied to job_id and row_num.
Return { job_id } from the upload endpoint; expose GET /jobs/:job_id for progress.

If you want, I can generate concrete code for your stack (Node/TypeScript with SQS/Kafka, or Python/FastAPI with Pub/Sub/RabbitMQ).