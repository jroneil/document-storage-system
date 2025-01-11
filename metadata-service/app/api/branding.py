# app/api/branding.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.branding import BrandCreate, BrandResponse
from app.crud.branding import create_brand, get_brand
from app.models.postgres_models import Base, engine, SessionLocal

router = APIRouter()

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/brands/", response_model=BrandResponse)
def create_brand_endpoint(brand: BrandCreate, db: Session = Depends(get_db)):
    return create_brand(db, brand)

@router.get("/brands/{brand_id}", response_model=BrandResponse)
def read_brand(brand_id: uuid.UUID, db: Session = Depends(get_db)):
    db_brand = get_brand(db, brand_id)
    if db_brand is None:
        raise HTTPException(status_code=404, detail="Brand not found")
    return db_brand