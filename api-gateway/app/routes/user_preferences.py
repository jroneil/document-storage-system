from fastapi import APIRouter, Depends, HTTPException
from typing import Optional
from ..services.user_preferences import UserPreferencesService
from ..utils.auth import get_current_user
from ..schemas.user_preferences import (
    UserPreferencesCreate,
    UserPreferencesUpdate,
    UserPreferencesInDB
)

router = APIRouter(prefix="/api/user-preferences", tags=["user-preferences"])

@router.post("/save-search", response_model=UserPreferencesInDB)
async def save_search_criteria(
    criteria: dict,
    current_user: str = Depends(get_current_user)
):
    service = UserPreferencesService()
    try:
        preferences = service.save_search_criteria(current_user, criteria)
        return preferences
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/save-columns", response_model=UserPreferencesInDB)
async def save_display_columns(
    columns: list,
    current_user: str = Depends(get_current_user)
):
    service = UserPreferencesService()
    try:
        preferences = service.save_display_columns(current_user, columns)
        return preferences
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=Optional[UserPreferencesInDB])
async def get_user_preferences(
    current_user: str = Depends(get_current_user)
):
    service = UserPreferencesService()
    try:
        preferences = service.get_user_preferences(current_user)
        return preferences
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
