from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from services.text_extraction import extract_text_from_pdf
from services.thumbnail_generation import generate_thumbnail
import datetime

app = FastAPI()

@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring and load balancing"""
    return JSONResponse(
        status_code=200,
        content={
            "status": "healthy",
            "service": "processing-service",
            "timestamp": datetime.datetime.now().isoformat(),
            "version": "1.0.0"
        }
    )

@app.post("/extract-text")
async def extract_text(file_path: str):
    try:
        text = extract_text_from_pdf(file_path)
        return JSONResponse(
            status_code=200,
            content={"message": "Text extracted successfully", "text": text}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate-thumbnail")
async def generate_thumbnail_endpoint(image_path: str, output_path: str):
    try:
        thumbnail_path = generate_thumbnail(image_path, output_path)
        return JSONResponse(
            status_code=200,
            content={"message": "Thumbnail generated successfully", "thumbnail_path": thumbnail_path}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
