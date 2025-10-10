from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from app.services.notification import send_email
import datetime
app = FastAPI()

@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring and load balancing"""
    return JSONResponse(
        status_code=200,
        content={
            "status": "healthy",
            "service": "notification-service",
            "timestamp": datetime.datetime.now().isoformat(),
            "version": "1.0.0"
        }
    )
@app.post("/send-email")
async def send_email_endpoint(to: str, subject: str, body: str):
    try:
        send_email(to, subject, body)
        return JSONResponse(
            status_code=200,
            content={"message": "Email sent successfully"}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))