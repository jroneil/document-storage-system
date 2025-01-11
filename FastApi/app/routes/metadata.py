from fastapi import APIRouter, HTTPException
import httpx
from dotenv import load_dotenv
import os

load_dotenv()

METADATA_SERVICE_URL = os.getenv("METADATA_SERVICE_URL")

router = APIRouter()

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