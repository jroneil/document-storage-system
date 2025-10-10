# app/crud/dynamic_metadata.py
from app.models.mongo_models import metadata_collection
from app.utils.validators import validate_metadata
from app.crud.branding import get_brand
from sqlalchemy.orm import Session

def create_dynamic_metadata(db: Session, dynmetadata: Dict, brand_id: uuid.UUID = None):
    if brand_id:
        brand = get_brand(db, brand_id)
        if brand:
            validate_metadata(dynmetadata, brand.required_metadata)
    result = metadata_collection.insert_one(dynmetadata)
    return {"id": str(result.inserted_id)}