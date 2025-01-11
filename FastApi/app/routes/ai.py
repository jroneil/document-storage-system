from fastapi import APIRouter, HTTPException
import httpx
from dotenv import load_dotenv
import os

load_dotenv()

AI_SERVICE_URL = os.getenv("AI_SERVICE_URL")

router = APIRouter()

@router.post("/analyze-content")
async def analyze_content(text: str):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{AI_SERVICE_URL}/analyze-content",
                json={"text": text}
            )
            return response.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))