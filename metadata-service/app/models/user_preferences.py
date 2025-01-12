from sqlalchemy import Column, String, JSON, DateTime
from sqlalchemy.sql import func
from .base import Base

class UserPreferences(Base):
    __tablename__ = "user_preferences"
    
    user_id = Column(String, primary_key=True, index=True)
    search_criteria = Column(JSON, nullable=True)
    display_columns = Column(JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return f"<UserPreferences(user_id={self.user_id}, search_criteria={self.search_criteria}, display_columns={self.display_columns})>"
