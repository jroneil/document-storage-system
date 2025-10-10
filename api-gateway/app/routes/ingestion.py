from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
import httpx
from dotenv import load_dotenv
import os

load_dotenv()

INGESTION_SERVICE_URL = os.getenv("INGESTION_SERVICE_URL")

router = APIRouter()
@router.get("/health")
async def health():
    async with httpx.AsyncClient() as client:
        r = await client.get(f"{INGESTION_SERVICE_URL}/health", timeout=10)
    return JSONResponse(status_code=r.status_code, content=r.json())


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