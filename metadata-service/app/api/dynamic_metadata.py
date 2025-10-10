# app/api/dynamic_metadata.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.dynamic_metadata import DynamicMetadataCreate, DynamicMetadataResponse
from app.crud.dynamic_metadata import create_dynamic_metadata, get_dynamic_metadata
from app.models.postgres_models import SessionLocal

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/dynamic-metadata/", response_model=DynamicMetadataResponse)
def create_metadata(metadata: DynamicMetadataCreate, brand_id: uuid.UUID = None, db: Session = Depends(get_db)):
    return create_dynamic_metadata(db, metadata.dict(), brand_id)

@router.get("/dynamic-metadata/{document_id}", response_model=DynamicMetadataResponse)
def read_metadata(document_id: str):
    dynamic_metadata = get_dynamic_metadata(document_id)
    if dynamic_metadata is None:
        raise HTTPException(status_code=404, detail="Metadata not found")
    return dynamic_metadata