from typing import Optional
from datetime import datetime
from ..models.user_preferences import UserPreferences
from ..schemas.user_preferences import UserPreferencesCreate, UserPreferencesUpdate
from ..utils.database import SessionLocal

class UserPreferencesService:
    def __init__(self):
        self.db = SessionLocal()

    def save_search_criteria(self, user_id: str, criteria: dict) -> Optional[UserPreferences]:
        try:
            # Check if preferences exist for user
            preferences = self.db.query(UserPreferences).filter(
                UserPreferences.user_id == user_id
            ).first()

            if preferences:
                # Update existing preferences
                preferences.search_criteria = criteria
                preferences.updated_at = datetime.utcnow()
            else:
                # Create new preferences
                preferences = UserPreferences(
                    user_id=user_id,
                    search_criteria=criteria,
                    created_at=datetime.utcnow(),
                    updated_at=datetime.utcnow()
                )
                self.db.add(preferences)

            self.db.commit()
            self.db.refresh(preferences)
            return preferences
        except Exception as e:
            self.db.rollback()
            raise e
        finally:
            self.db.close()

    def save_display_columns(self, user_id: str, columns: list) -> Optional[UserPreferences]:
        try:
            preferences = self.db.query(UserPreferences).filter(
                UserPreferences.user_id == user_id
            ).first()

            if preferences:
                preferences.display_columns = columns
                preferences.updated_at = datetime.utcnow()
            else:
                preferences = UserPreferences(
                    user_id=user_id,
                    display_columns=columns,
                    created_at=datetime.utcnow(),
                    updated_at=datetime.utcnow()
                )
                self.db.add(preferences)

            self.db.commit()
            self.db.refresh(preferences)
            return preferences
        except Exception as e:
            self.db.rollback()
            raise e
        finally:
            self.db.close()

    def get_user_preferences(self, user_id: str) -> Optional[UserPreferences]:
        try:
            preferences = self.db.query(UserPreferences).filter(
                UserPreferences.user_id == user_id
            ).first()
            return preferences
        except Exception as e:
            raise e
        finally:
            self.db.close()
