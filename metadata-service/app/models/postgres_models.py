from sqlalchemy import Column, Integer, String, JSON
from sqlalchemy.ext.declarative import declarative_base

import uuid

Base = declarative_base()

class StandProperties(Base):
    __tablename__ = "stand_properties"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    location = Column(String, nullable=False)
    attributes = Column(JSON)  # For additional structured data
    

class Brand(Base):
    __tablename__ = "brands"
    brand_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    required_metadata = Column(JSON)  # JSONB for required metadata fields

class Document(Base):
    __tablename__ = "documents"
    
    document_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    file_name = Column(String, nullable=False)
    file_size = Column(BigInteger, nullable=False)
    file_type = Column(String, nullable=False)
    upload_date = Column(DateTime(timezone=True), server_default=func.now())
    last_modified_date = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    user_id = Column(UUID(as_uuid=True), nullable=False)
    tags = Column(ARRAY(String))
    description = Column(String)
    storage_path = Column(String, nullable=False)
    version = Column(Integer, default=1)
    checksum = Column(String, nullable=False)
    acl = Column(JSONB)
    thumbnail_path = Column(String)
    expiration_date = Column(DateTime(timezone=True))
    category = Column(String)
    division = Column(String)
    business_unit = Column(String)
    brand_id = Column(UUID(as_uuid=True), ForeignKey('brands.brand_id'))
    document_type = Column(String, nullable=False)

    __table_args__ = (
        Index('idx_document_user', 'user_id'),
        Index('idx_document_tags', 'tags', postgresql_using='gin'),
        Index('idx_document_upload_date', 'upload_date'),
        Index('idx_document_category', 'category'),
        Index('idx_document_division', 'division'),
        Index('idx_document_business_unit', 'business_unit'),
        Index('idx_document_brand', 'brand_id'),
        Index('idx_document_file_type', 'file_type'),
        Index('idx_document_document_type', 'document_type')
    )
