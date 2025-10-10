from fastapi import APIRouter, HTTPException
import httpx
from dotenv import load_dotenv
import os
from fastapi.responses import JSONResponse
load_dotenv()

STORAGE_SERVICE_URL = os.getenv("STORAGE_SERVICE_URL")

router = APIRouter()
@router.get("/health")
async def health():
    async with httpx.AsyncClient() as client:
        r = await client.get(f"{STORAGE_SERVICE_URL}/health", timeout=10)
    return JSONResponse(status_code=r.status_code, content=r.json())

@router.post("/upload")
async def upload_file(file: bytes):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{STORAGE_SERVICE_URL}/upload",
                files={"file": file}
            )
            return response.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/delete")
async def delete_file(s3_key: str):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.delete(
                f"{STORAGE_SERVICE_URL}/delete",
                params={"s3_key": s3_key}
            )
            return response.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))