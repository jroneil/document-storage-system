from pydantic import BaseModel
from typing import Optional, List, Dict
from datetime import datetime
import uuid

class DocumentMetadata(BaseModel):
    document_id: uuid.UUID
    file_name: str
    file_size: int
    file_type: str
    upload_date: datetime
    last_modified_date: datetime
    user_id: uuid.UUID
    tags: Optional[List[str]] = None
    description: Optional[str] = None
    storage_path: str
    version: int = 1
    checksum: str
    acl: Optional[Dict] = None
    thumbnail_path: Optional[str] = None
    expiration_date: Optional[datetime] = None
    category: Optional[str] = None
    division: Optional[str] = None
    business_unit: Optional[str] = None
    brand_id: Optional[uuid.UUID] = None
    document_type: str
    region: Optional[str] = None
    country: Optional[str] = None
    languages: List[str] = []
    alternate_part_numbers: List[str] = []

class BrandMetadata(BaseModel):
    document_id: uuid.UUID
    available_countries: List[str]
    languages: List[str]
    brand_colors: List[str]
    brand_logo_path: str
    campaign_name: Optional[str] = None
    product_line: Optional[str] = None
