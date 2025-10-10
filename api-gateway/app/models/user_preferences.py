from sqlalchemy import Column, String, JSON, DateTime
from sqlalchemy.sql import func
from ..utils.database import Base

class UserPreferences(Base):
    __tablename__ = "user_preferences"

    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, unique=True, index=True, nullable=False)
    search_criteria = Column(JSON, nullable=True)
    display_columns = Column(JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
