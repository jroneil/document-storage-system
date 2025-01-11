CREATE TABLE documents (
    document_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    file_name TEXT NOT NULL,
    file_size BIGINT NOT NULL,
    file_type TEXT NOT NULL, -- File format (e.g., PDF, HTML, Video, DOC, Excel)
    upload_date TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    last_modified_date TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    user_id UUID NOT NULL,
    tags TEXT[],
    description TEXT,
    storage_path TEXT NOT NULL,
    version INTEGER DEFAULT 1,
    checksum TEXT NOT NULL,
    acl JSONB,
    thumbnail_path TEXT,
    expiration_date TIMESTAMP WITH TIME ZONE,
    category TEXT,
    division TEXT,
    business_unit TEXT,
    brand_id UUID,
    document_type TEXT NOT NULL -- Document type (e.g., Technical, User, etc.)
);

-- Indexes for faster querying
CREATE INDEX idx_document_user ON documents (user_id);
CREATE INDEX idx_document_tags ON documents USING GIN (tags);
CREATE INDEX idx_document_upload_date ON documents (upload_date);
CREATE INDEX idx_document_category ON documents (category);
CREATE INDEX idx_document_division ON documents (division);
CREATE INDEX idx_document_business_unit ON documents (business_unit);
CREATE INDEX idx_document_brand ON documents (brand_id);
CREATE INDEX idx_document_file_type ON documents (file_type);
CREATE INDEX idx_document_document_type ON documents (document_type);