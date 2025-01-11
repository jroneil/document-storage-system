from sqlalchemy.orm import Session
from app.models.postgres_models import StandProperties

def create_stand_properties(db: Session, stand: StandPropertiesCreate):
    db_stand = StandProperties(**stand.dict())
    db.add(db_stand)
    db.commit()
    db.refresh(db_stand)
    return db_stand

def get_stand_properties(db: Session, stand_id: int):
    return db.query(StandProperties).filter(StandProperties.id == stand_id).first()