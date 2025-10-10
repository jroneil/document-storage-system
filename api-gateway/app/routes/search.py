from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
import httpx
import os

router = APIRouter()
SEARCH_SERVICE_URL = os.getenv("SEARCH_SERVICE_URL", "http://search-service:5005")

@router.get("/test")
async def test():
    return {"message": "api-gateway: search proxy up"}

@router.get("/health")
async def health():
    async with httpx.AsyncClient() as client:
        r = await client.get(f"{SEARCH_SERVICE_URL}/health", timeout=10)
    return JSONResponse(status_code=r.status_code, content=r.json())

@router.post("/index-document")
async def index_document(document_id: str, metadata: dict):
    try:
        async with httpx.AsyncClient() as client:
            r = await client.post(
                f"{SEARCH_SERVICE_URL}/index-document",
                params={"document_id": document_id},
                json={"metadata": metadata},
                timeout=30,
            )
        return JSONResponse(status_code=r.status_code, content=r.json())
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Search service error: {e}")

@router.get("")
async def search(query: str):
    try:
        async with httpx.AsyncClient() as client:
            r = await client.get(
                f"{SEARCH_SERVICE_URL}/search",
                params={"query": query},
                timeout=30,
            )
        return JSONResponse(status_code=r.status_code, content=r.json())
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Search service error: {e}")