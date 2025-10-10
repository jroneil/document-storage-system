from sqlalchemy.orm import Session
from app.models.postgres_models import StandMetadata

def create_stand_metadata(db: Session, stand: StandMetadataCreate):
    db_stand =  StandMetadata(**stand.dict())
    db.add(db_stand)
    db.commit()
    db.refresh(db_stand)
    return db_stand

def get_stand_metadata(db: Session, stand_id: int):
    return db.query(StandMetadata).filter(StandMetadata.id == stand_id).first()