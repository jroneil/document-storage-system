from fastapi import APIRouter, HTTPException
import httpx
from dotenv import load_dotenv
import os
from fastapi.responses import JSONResponse

load_dotenv()

NOTIFICATION_SERVICE_URL = os.getenv("NOTIFICATION_SERVICE_URL")

router = APIRouter()

@router.get("/health")
async def health():
    async with httpx.AsyncClient() as client:
        r = await client.get(f"{NOTIFICATION_SERVICE_URL}/health", timeout=10)
    return JSONResponse(status_code=r.status_code, content=r.json())



@router.post("/send-email")
async def send_email(to: str, subject: str, body: str):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{NOTIFICATION_SERVICE_URL}/send-email",
                json={"to": to, "subject": subject, "body": body}
            )
            return response.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))