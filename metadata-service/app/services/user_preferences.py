from typing import Optional
from datetime import datetime
from fastapi import HTTPException
from .schemas.user_preferences import UserPreferences, SearchCriteria, ColumnPreference
from .models.user_preferences import UserPreferencesModel
from .db.session import SessionLocal

class UserPreferencesService:
    def __init__(self):
        self.db = SessionLocal()

    async def get_user_preferences(self, user_id: str) -> Optional[UserPreferences]:
        preferences = self.db.query(UserPreferencesModel).filter(UserPreferencesModel.user_id == user_id).first()
        if not preferences:
            return None
        return UserPreferences(**preferences.dict())

    async def save_search(self, user_id: str, search: SearchCriteria) -> UserPreferences:
        preferences = self.db.query(UserPreferencesModel).filter(UserPreferencesModel.user_id == user_id).first()
        
        if not preferences:
            preferences = UserPreferencesModel(user_id=user_id)
            self.db.add(preferences)
        
        # Add new search criteria
        preferences.saved_searches.append(search)
        self.db.commit()
        self.db.refresh(preferences)
        return UserPreferences(**preferences.dict())

    async def update_column_preferences(self, user_id: str, columns: List[ColumnPreference]) -> UserPreferences:
        preferences = self.db.query(UserPreferencesModel).filter(UserPreferencesModel.user_id == user_id).first()
        
        if not preferences:
            preferences = UserPreferencesModel(user_id=user_id)
            self.db.add(preferences)
        
        preferences.column_preferences = columns
        self.db.commit()
        self.db.refresh(preferences)
        return UserPreferences(**preferences.dict())

    async def delete_search(self, user_id: str, search_name: str) -> UserPreferences:
        preferences = self.db.query(UserPreferencesModel).filter(UserPreferencesModel.user_id == user_id).first()
        
        if not preferences:
            raise HTTPException(status_code=404, detail="User preferences not found")
        
        # Remove the search criteria
        preferences.saved_searches = [s for s in preferences.saved_searches if s.name != search_name]
        self.db.commit()
        self.db.refresh(preferences)
        return UserPreferences(**preferences.dict())
