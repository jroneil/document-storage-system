from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from services.notification import send_email

app = FastAPI()

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