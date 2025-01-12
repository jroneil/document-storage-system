from datetime import datetime
from typing import Optional, List, Dict
from pydantic import BaseModel

class SearchCriteriaSchema(BaseModel):
    search_terms: List[str]
    filters: Dict[str, List[str]]
    sort_by: Optional[str] = None

class DisplayColumnsSchema(BaseModel):
    columns: List[str]

class UserPreferencesBase(BaseModel):
    user_id: str
    search_criteria: Optional[SearchCriteriaSchema] = None
    display_columns: Optional[DisplayColumnsSchema] = None

class UserPreferencesCreate(UserPreferencesBase):
    pass

class UserPreferencesUpdate(BaseModel):
    search_criteria: Optional[SearchCriteriaSchema] = None
    display_columns: Optional[DisplayColumnsSchema] = None

class UserPreferencesInDB(UserPreferencesBase):
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
