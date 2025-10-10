from pydantic import BaseModel
from typing import Optional, Dict, List
from datetime import datetime

class UserPreferencesBase(BaseModel):
    user_id: str
    search_criteria: Optional[Dict] = None
    display_columns: Optional[List] = None

class UserPreferencesCreate(UserPreferencesBase):
    pass

class UserPreferencesUpdate(BaseModel):
    search_criteria: Optional[Dict] = None
    display_columns: Optional[List] = None

class UserPreferencesInDB(UserPreferencesBase):
    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
