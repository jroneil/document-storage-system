from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class DocumentMetadataBase(BaseModel):
    file_name: str
    file_size: int
    file_type: str
    upload_date: datetime
    last_modified_date: datetime
    user_id: UUID
    tags: List[str] = Field(default_factory=list)
    description: Optional[str] = None
    storage_path: str
    version: int
    checksum: str
    acl: Optional[Dict[str, Any]] = None
    thumbnail_path: Optional[str] = None
    expiration_date: Optional[datetime] = None
    category: Optional[str] = None
    division: Optional[str] = None
    business_unit: Optional[str] = None
    brand_id: Optional[UUID] = None
    document_type: str
    is_deleted: bool = False


class DocumentMetadataResponse(DocumentMetadataBase):
    id: Optional[UUID] = None
    document_id: UUID
    revision: int

    model_config = ConfigDict(from_attributes=True)


class DocumentMetadataHistoryResponse(BaseModel):
    items: List[DocumentMetadataResponse]


class DocumentMetadataUpdate(BaseModel):
    file_name: Optional[str] = None
    file_size: Optional[int] = None
    file_type: Optional[str] = None
    last_modified_date: Optional[datetime] = None
    user_id: Optional[UUID] = None
    tags: Optional[List[str]] = None
    description: Optional[str] = None
    storage_path: Optional[str] = None
    version: Optional[int] = None
    checksum: Optional[str] = None
    acl: Optional[Dict[str, Any]] = None
    thumbnail_path: Optional[str] = None
    expiration_date: Optional[datetime] = None
    category: Optional[str] = None
    division: Optional[str] = None
    business_unit: Optional[str] = None
    brand_id: Optional[UUID] = None
    document_type: Optional[str] = None

    model_config = ConfigDict(extra="forbid")
