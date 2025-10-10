from fastapi import APIRouter, HTTPException, Depends
import httpx
from dotenv import load_dotenv
import os
from typing import List
from fastapi.responses import JSONResponse

load_dotenv()

METADATA_SERVICE_URL = os.getenv("METADATA_SERVICE_URL")

router = APIRouter()
@router.get("/health")
async def health():
    async with httpx.AsyncClient() as client:
        r = await client.get(f"{METADATA_SERVICE_URL}/health", timeout=10)
    return JSONResponse(status_code=r.status_code, content=r.json())

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

@router.get("/user-preferences/{user_id}")
async def get_user_preferences(user_id: str):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{METADATA_SERVICE_URL}/user-preferences/{user_id}"
            )
            if response.status_code == 404:
                raise HTTPException(status_code=404, detail="Preferences not found")
            return response.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/user-preferences/{user_id}/save-search")
async def save_search(user_id: str, search: dict):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{METADATA_SERVICE_URL}/user-preferences/{user_id}/save-search",
                json=search
            )
            return response.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/user-preferences/{user_id}/columns")
async def update_columns(user_id: str, columns: List[dict]):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.put(
                f"{METADATA_SERVICE_URL}/user-preferences/{user_id}/columns",
                json=columns
            )
            return response.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/user-preferences/{user_id}/search/{search_name}")
async def delete_search(user_id: str, search_name: str):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.delete(
                f"{METADATA_SERVICE_URL}/user-preferences/{user_id}/search/{search_name}"
            )
            return response.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
