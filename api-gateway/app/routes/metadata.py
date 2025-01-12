from fastapi import APIRouter, HTTPException, Depends
import httpx
from dotenv import load_dotenv
import os
from typing import List
from metadata_service.services.user_preferences import UserPreferencesService
from metadata_service.schemas.user_preferences import UserPreferences, SearchCriteria, ColumnPreference

load_dotenv()

METADATA_SERVICE_URL = os.getenv("METADATA_SERVICE_URL")

router = APIRouter()
preferences_service = UserPreferencesService()

@router.post("/save-metadata")
async def save_metadata(metadata: dict):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{METADATA_SERVICE_URL}/save-metadata",
                json=metadata
            )
            return response.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/user-preferences/{user_id}", response_model=UserPreferences)
async def get_user_preferences(user_id: str):
    preferences = await preferences_service.get_user_preferences(user_id)
    if not preferences:
        raise HTTPException(status_code=404, detail="Preferences not found")
    return preferences

@router.post("/user-preferences/{user_id}/save-search", response_model=UserPreferences)
async def save_search(user_id: str, search: SearchCriteria):
    return await preferences_service.save_search(user_id, search)

@router.put("/user-preferences/{user_id}/columns", response_model=UserPreferences)
async def update_columns(user_id: str, columns: List[ColumnPreference]):
    return await preferences_service.update_column_preferences(user_id, columns)

@router.delete("/user-preferences/{user_id}/search/{search_name}", response_model=UserPreferences)
async def delete_search(user_id: str, search_name: str):
    return await preferences_service.delete_search(user_id, search_name)
