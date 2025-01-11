from fastapi import APIRouter, HTTPException
import httpx
from dotenv import load_dotenv
import os

load_dotenv()

PROCESSING_SERVICE_URL = os.getenv("PROCESSING_SERVICE_URL")

router = APIRouter()

@router.post("/extract-text")
async def extract_text(file_path: str):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{PROCESSING_SERVICE_URL}/extract-text",
                json={"file_path": file_path}
            )
            return response.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/generate-thumbnail")
async def generate_thumbnail(image_path: str, output_path: str):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{PROCESSING_SERVICE_URL}/generate-thumbnail",
                json={"image_path": image_path, "output_path": output_path}
            )
            return response.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))