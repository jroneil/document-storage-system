from fastapi import APIRouter, HTTPException
import httpx
from dotenv import load_dotenv
import os

load_dotenv()

INGESTION_SERVICE_URL = os.getenv("INGESTION_SERVICE_URL")

router = APIRouter()

@router.post("/upload")
async def upload_file(file: bytes):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{INGESTION_SERVICE_URL}/upload",
                files={"file": file}
            )
            return response.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))