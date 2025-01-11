# app/schemas/branding.py
from pydantic import BaseModel
from typing import Dict
import uuid

class BrandCreate(BaseModel):
    name: str
    required_metadata: Dict

class BrandResponse(BaseModel):
    brand_id: uuid.UUID
    name: str
    required_metadata: Dict