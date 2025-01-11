from pymongo import MongoClient
from pydantic import BaseModel
from typing import List
import uuid

client = MongoClient("mongodb://localhost:27017/")
db = client["metadata_db"]
metadata_collection = db["dynamic_metadata"]

class DocumentMetadata(BaseModel):
    document_id: uuid.UUID
    available_countries: List[str]
    languages: List[str]
    brand_colors: List[str]
    brand_logo_path: str
    campaign_name: str
    product_line: str

    class Config:
        json_schema_extra = {
            "example": {
                "document_id": "uuid-from-postgresql",
                "available_countries": ["US", "CA", "GB"],
                "languages": ["en", "fr", "es"],
                "brand_colors": ["#FF0000", "#00FF00"],
                "brand_logo_path": "/path/to/logo.png",
                "campaign_name": "Summer Sale 2023",
                "product_line": "Electronics"
            }
        }
