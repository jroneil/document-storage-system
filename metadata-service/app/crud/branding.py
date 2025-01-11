# app/crud/branding.py
from sqlalchemy.orm import Session
from app.models.postgres_models import Brand
from app.schemas.branding import BrandCreate

def create_brand(db: Session, brand: BrandCreate):
    db_brand = Brand(**brand.dict())
    db.add(db_brand)
    db.commit()
    db.refresh(db_brand)
    return db_brand

def get_brand(db: Session, brand_id: uuid.UUID):
    return db.query(Brand).filter(Brand.brand_id == brand_id).first()