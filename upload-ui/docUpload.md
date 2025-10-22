Revised spec incorporating your answers + next-step assumptions

I merged your responses into the original spec, added concrete defaults where you said “later,” and flagged decisions as Assumed where needed so we can keep moving. At the end, I list a few remaining decisions to finalize so I can produce message schemas, API contracts, and DB migrations.

Overview
Two upload paths:
Single document uploads (PDF, HTML, Word, etc.)
Bulk uploads (CSV, JSON, XML, Excel)
Core components:
Upload UI (frontend for both flows)
Storage Service (single-file uploads → MinIO + message)
Bulk Upload Service (parses bulk files → messages)
Metadata Service (persists metadata in documents table)
Object Storage (MinIO)
Message Broker: RabbitMQ
Separate queues for single vs bulk
Single Document Upload Flow
Upload UI sends the file and basic metadata to Storage Service.
Storage Service uploads to MinIO.
Object key format: brand/business_unit/document_title-revision (you called out “brand/business unit/document name-revision”).
Assumed: a single bucket; key encodes the path. If you prefer multiple buckets, say so.
Storage Service publishes a JSON message to RabbitMQ (single-upload topic/queue) with:
brand, business_unit, document_title, revision
object_key (as above), bucket (Assumed: “documents”)
content_type, size, checksum (Assumed optional for now)
idempotency_key (required)
uploader_id, upload_timestamp (Assumed optional now)
Metadata Service consumes, then upserts into documents using unique key (brand, document_title, revision, business_unit).
Bulk Upload Flow
Upload UI sends a bulk file (CSV/JSON/XML/Excel) to Bulk Upload Service.
Bulk Upload Service parses to document records (rules exist in C:\docProject\document-storage-system\bulk-upload-service).
For each parsed record, Bulk Upload Service publishes a JSON message to RabbitMQ (bulk-upload topic/queue) with:
transaction_type: "new" (insert) | "update" (update existing)
brand, business_unit, document_title, revision
object_key (if applicable), other metadata fields from bulk
idempotency_key (required)
Metadata Service processes:
Uses transaction_type to choose insert vs update.
Unique key: (brand, document_title, revision, business_unit).
If “new” but record exists: per your note, do a check; for now we will reject to DLQ (Assumed) until sequence/versioning policy is implemented.
Queues and retry/DLQ
RabbitMQ queues
single-upload → metadata
bulk-upload → metadata
Each has its own DLQ with backoff/retry.
Assumed: 3 retries with exponential backoff; then route to DLQ.
Assumed: poison-message detection by idempotency_key and repeated failures.
Uniqueness, versioning, and collisions
Unique key: (brand, document_title, revision, business_unit).
“new” → insert; if exists, reject and put to DLQ (Assumed initial behavior).
“update” → must match existing unique key, then update fields.
Versioning and sequence:
You plan to add a sequence number later that copies records and increments sequence.
For now: revision is accepted as provided; no monotonic enforcement (Assumed).
Assumed: revision is free-form string; we treat it as opaque for matching.
Business unit taxonomy
Will be controlled later. For now accept any string; no mapping; no rejection (Assumed).
Idempotency
Required in all messages.
Assumed strategy: Metadata Service stores processed idempotency_keys with TTL (e.g., 7 days) to ensure at-least-once delivery is safe.
Security and deployment
All services will eventually run in Kubernetes.
For now, minimal auth assumed between services (internal network); signed upload URLs for MinIO can be added later (Assumed later).
Observability
Logging service to be added later. For now:
Log message receipt, success, and error with idempotency_key and unique key.
Basic metrics counters for processed/failed by queue (Assumed).
UI requirements
Upload UI supports both flows.
Bulk uploads should provide per-record results and downloadable error report (Confirmed “yes”).
Assumed: For single uploads, show progress bar and final success/failure; for bulk, show batch status and link to per-record report.
Storage lifecycle
Retention/archival: “yes” to policies later.
Assumed initial: no auto-archival; soft delete supported at metadata level with is_deleted boolean; MinIO object remains until lifecycle rules are defined.
Database model (initial, minimal)
Priority: “basic messaging and inserting for now; develop further later.”
Assumed initial documents table schema:
id (uuid, pk)
brand (text, not null)
business_unit (text, not null)
document_title (text, not null)
revision (text, not null)
bucket (text, not null, default 'documents')
object_key (text, not null)
content_type (text, null)
size_bytes (bigint, null)
checksum (text, null)
uploader_id (text, null)
upload_timestamp (timestamptz, null, default now())
tags (jsonb, null)
is_deleted (boolean, not null, default false)
created_at (timestamptz, not null, default now())
updated_at (timestamptz, not null, default now())
UNIQUE (brand, business_unit, document_title, revision)
Assumed an auxiliary idempotency_keys table:
idempotency_key (text, pk)
processed_at (timestamptz)
outcome (text) // success|failed
related_document_id (uuid, null)
TTL/cleanup handled by scheduled job.
Message formats (initial JSON)
Single-upload message (Storage → Metadata)
Example:
{
  "source": "storage-service",
  "idempotency_key": "uuid-...-1",
  "brand": "Acme",
  "business_unit": "NorthAmerica",
  "document_title": "SafetyManual",
  "revision": "v1",
  "bucket": "documents",
  "object_key": "Acme/NorthAmerica/SafetyManual-v1.pdf",
  "content_type": "application/pdf",
  "size_bytes": 123456,
  "checksum": "sha256:...",
  "uploader_id": "user-123",
  "upload_timestamp": "2025-10-22T12:00:00Z",
  "tags": { "category": "safety" }
}

Bulk-upload message (Bulk → Metadata)
Example:
{
  "source": "bulk-upload-service",
  "idempotency_key": "uuid-...-2",
  "transaction_type": "new",  // "new" | "update"
  "brand": "Acme",
  "business_unit": "NorthAmerica",
  "document_title": "SafetyManual",
  "revision": "v2",
  "bucket": "documents",
  "object_key": "Acme/NorthAmerica/SafetyManual-v2.pdf",
  "content_type": "application/pdf",
  "size_bytes": 234567,
  "checksum": "sha256:...",
  "tags": { "category": "safety" }
}

RabbitMQ setup (initial)
Exchanges:
exchange: uploads.exchange (topic)
Queues:
single-upload.queue bound with routing key single.upload
bulk-upload.queue bound with routing key bulk.upload
single-upload.dlq, bulk-upload.dlq
Retry/backoff:
Assumed: dead-letter exchange pattern with delayed retries (e.g., 5s, 30s, 5m), 3 attempts.
Items you already answered that I’ve captured
Metadata schema location noted: C:\docProject\document-storage-system\metadata-service\app\models
Object key pattern: brand/business unit/document name-revision
Bulk parsing rules exist in: C:\docProject\document-storage-system\bulk-upload-service
Transaction types: new = insert; update = update existing
Collisions: check brand+document_title+revision; later add sequence copy/versioning
Broker: RabbitMQ
Idempotency: yes
UI bulk per-record report: yes
Storage lifecycle and logging service: later
Short-term goal: basic messaging + insert/update; refine later
Remaining decisions to confirm

Bucket strategy

Use a single bucket named “documents” for now? Or separate by environment/brand? I assumed single bucket.

Exact filename in object key

Your format implies adding extension (e.g., “SafetyManual-v1.pdf”). Confirm we should include the original extension in the final object_key.

DLQ behavior for “new” when record exists

I assumed we reject to DLQ for now. Alternative: auto-convert to update. Which do you prefer short term?

Idempotency TTL

Is 7 days retention for processed idempotency keys acceptable for now?

Minimal required fields for messages

For initial validation, I propose required: brand, business_unit, document_title, revision, object_key, idempotency_key, source.
Optional: bucket (default “documents”). OK?

Partial failure handling in bulk

You said bulk rules are in code; for the UI, do you want:
Continue-on-error per record, aggregate a downloadable error CSV/JSON? I’ll implement that as default unless you prefer all-or-nothing.

Content validation now vs later

You said “LATER”. I’ll leave MIME/size/AV as optional, logged if present, not enforced. Confirm.

Database

Postgres assumed. OK?
Do you want a simple upsert on UNIQUE or explicit “new” vs “update” branching with error on collision as described?

Timestamps/timezone

Use UTC ISO-8601 everywhere. OK?

Naming

Do you want “revision” consistently, or “version”? You used “revision” in answers; I’ll standardize on “revision”.

If you confirm these, I will deliver next:

JSON Schemas for both message types (with required/optional fields)
OpenAPI specs for Storage, Bulk Upload, and Metadata endpoints
SQL migration for documents and idempotency_keys
RabbitMQ definitions and retry/DLQ policy examples
Example end-to-end sequence diagrams

only change current scheme to add thing that were missed