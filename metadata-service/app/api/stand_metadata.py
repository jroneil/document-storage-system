from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.stand_properties import StandPropertiesCreate, StandPropertiesResponse
from app.crud.stand_properties import create_stand_properties, get_stand_properties
from app.models.postgres_models import Base, engine, SessionLocal

router = APIRouter()

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/stand-properties/", response_model=StandPropertiesResponse)
def create_stand(stand: StandPropertiesCreate, db: Session = Depends(get_db)):
    return create_stand_properties(db, stand)

@router.get("/stand-properties/{stand_id}", response_model=StandPropertiesResponse)
def read_stand(stand_id: int, db: Session = Depends(get_db)):
    db_stand = get_stand_properties(db, stand_id)
    if db_stand is None:
        raise HTTPException(status_code=404, detail="Stand not found")
    return db_stand