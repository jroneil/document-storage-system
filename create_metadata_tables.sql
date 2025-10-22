-- Create table for document metadata
CREATE TABLE IF NOT EXISTS documents (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    brand TEXT NOT NULL,
    business_unit TEXT NOT NULL,
    document_title TEXT NOT NULL,
    revision TEXT NOT NULL,
    bucket TEXT NOT NULL DEFAULT 'documents',
    object_key TEXT NOT NULL,
    content_type TEXT,
    size_bytes BIGINT,
    checksum TEXT,
    uploader_id TEXT,
    upload_timestamp TIMESTAMPTZ,
    tags JSONB,
    description TEXT,
    category TEXT,
    division TEXT,
    document_type TEXT,
    region TEXT,
    country TEXT,
    languages JSONB,
    alternate_part_numbers JSONB,
    thumbnail_path TEXT,
    expiration_date DATE, -- YYYY-MM-DD
    acl JSONB,
    is_deleted BOOLEAN NOT NULL DEFAULT false,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    -- Unique constraint as per docUpload.md
    UNIQUE (brand, business_unit, document_title, revision)
);

-- Create index for faster lookups on the unique key components
CREATE INDEX IF NOT EXISTS idx_documents_unique_composite ON documents (brand, business_unit, document_title, revision);

-- Create table for idempotency keys
CREATE TABLE IF NOT EXISTS idempotency_keys (
    idempotency_key TEXT PRIMARY KEY,
    processed_at TIMESTAMPTZ NOT NULL,
    outcome TEXT NOT NULL, -- 'success' or 'failed'
    related_document_id UUID REFERENCES documents(id) ON DELETE SET NULL
);

-- Create index for faster lookups on idempotency_key
CREATE INDEX IF NOT EXISTS idx_idempotency_keys_key ON idempotency_keys (idempotency_key);

-- Create index for TTL/cleanup logic (e.g., delete entries older than 7 days)
CREATE INDEX IF NOT EXISTS idx_idempotency_keys_processed_at ON idempotency_keys (processed_at);

-- Optional: Add a trigger to automatically update updated_at timestamp
CREATE OR REPLACE FUNCTION trigger_set_timestamp()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS set_timestamp ON documents;
CREATE TRIGGER set_timestamp
BEFORE UPDATE ON documents
FOR EACH ROW
EXECUTE PROCEDURE trigger_set_timestamp();

-- Add comments for clarity
COMMENT ON TABLE documents IS 'Stores metadata for all uploaded documents.';
COMMENT ON COLUMN documents.id IS 'Primary key for the document record.';
COMMENT ON COLUMN documents.brand IS 'Brand identifier for the document.';
COMMENT ON COLUMN documents.business_unit IS 'Business unit associated with the document.';
COMMENT ON COLUMN documents.document_title IS 'Title of the document.';
COMMENT ON COLUMN documents.revision IS 'Revision or version of the document.';
COMMENT ON COLUMN documents.bucket IS 'Object storage bucket name.';
COMMENT ON COLUMN documents.object_key IS 'Key/path to the file in object storage.';
COMMENT ON COLUMN documents.content_type IS 'MIME type of the file.';
COMMENT ON COLUMN documents.size_bytes IS 'Size of the file in bytes.';
COMMENT ON COLUMN documents.checksum IS 'Checksum of the file (e.g., SHA256).';
COMMENT ON COLUMN documents.uploader_id IS 'Identifier of the user who uploaded the file.';
COMMENT ON COLUMN documents.upload_timestamp IS 'Timestamp when the file was uploaded.';
COMMENT ON COLUMN documents.tags IS 'JSONB array of tags associated with the document.';
COMMENT ON COLUMN documents.description IS 'Textual description of the document.';
COMMENT ON COLUMN documents.category IS 'Category of the document.';
COMMENT ON COLUMN documents.division IS 'Organizational division.';
COMMENT ON COLUMN documents.document_type IS 'Type of document (e.g., Manual, Brochure).';
COMMENT ON COLUMN documents.region IS 'Geographical region applicability.';
COMMENT ON COLUMN documents.country IS 'Country applicability.';
COMMENT ON COLUMN documents.languages IS 'JSONB array of language codes (e.g., ["en", "de"]).';
COMMENT ON COLUMN documents.alternate_part_numbers IS 'JSONB array of alternate part numbers.';
COMMENT ON COLUMN documents.thumbnail_path IS 'Path to a thumbnail image for the document.';
COMMENT ON COLUMN documents.expiration_date IS 'Date when the document expires (YYYY-MM-DD).';
COMMENT ON COLUMN documents.acl IS 'JSONB object for Access Control List (e.g., {"read": ["user1"], "write": ["user1"]}).';
COMMENT ON COLUMN documents.is_deleted IS 'Soft delete flag. True if document is considered deleted.';
COMMENT ON COLUMN documents.created_at IS 'Timestamp when the record was created.';
COMMENT ON COLUMN documents.updated_at IS 'Timestamp when the record was last updated.';

COMMENT ON TABLE idempotency_keys IS 'Ensures at-least-once processing by tracking processed message keys.';
COMMENT ON COLUMN idempotency_keys.idempotency_key IS 'The unique key from the message payload.';
COMMENT ON COLUMN idempotency_keys.processed_at IS 'Timestamp when the key was processed.';
COMMENT ON COLUMN idempotency_keys.outcome IS 'Outcome of the processing (success or failed).';
COMMENT ON COLUMN idempotency_keys.related_document_id IS 'Optional link to the document record this key pertains to.';
