-- Create metadata tables for document storage system

-- Create brands table
CREATE TABLE IF NOT EXISTS brands (
    brand_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR NOT NULL,
    required_metadata JSON
);

-- Create documents table
CREATE TABLE IF NOT EXISTS documents (
    document_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    file_name VARCHAR NOT NULL,
    file_size BIGINT NOT NULL,
    file_type VARCHAR NOT NULL,
    upload_date TIMESTAMPTZ DEFAULT NOW(),
    last_modified_date TIMESTAMPTZ DEFAULT NOW(),
    user_id UUID NOT NULL,
    tags TEXT[],
    description TEXT,
    storage_path VARCHAR NOT NULL,
    version INTEGER DEFAULT 1,
    checksum VARCHAR NOT NULL,
    acl JSONB,
    thumbnail_path VARCHAR,
    expiration_date TIMESTAMPTZ,
    category VARCHAR,
    division VARCHAR,
    business_unit VARCHAR,
    brand_id UUID REFERENCES brands(brand_id),
    document_type VARCHAR NOT NULL DEFAULT 'Document'
);

-- Create stand_metadata table
CREATE TABLE IF NOT EXISTS stand_metadata (
    id SERIAL PRIMARY KEY,
    name VARCHAR NOT NULL,
    location VARCHAR NOT NULL,
    attributes JSON
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_document_user ON documents(user_id);
CREATE INDEX IF NOT EXISTS idx_document_tags ON documents USING GIN(tags);
CREATE INDEX IF NOT EXISTS idx_document_upload_date ON documents(upload_date);
CREATE INDEX IF NOT EXISTS idx_document_category ON documents(category);
CREATE INDEX IF NOT EXISTS idx_document_division ON documents(division);
CREATE INDEX IF NOT EXISTS idx_document_business_unit ON documents(business_unit);
CREATE INDEX IF NOT EXISTS idx_document_brand ON documents(brand_id);
CREATE INDEX IF NOT EXISTS idx_document_file_type ON documents(file_type);
CREATE INDEX IF NOT EXISTS idx_document_document_type ON documents(document_type);

-- Print confirmation
SELECT 'Metadata tables created successfully!' as status;
