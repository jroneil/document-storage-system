from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from app.services.orchestrator import start_saga, handle_document_uploaded_event
from app.services.message_queue import listen_for_events
import json

app = FastAPI()

@app.post("/start-saga")
async def start_saga_endpoint(payload: dict):
    try:
        saga = start_saga(payload)
        return JSONResponse(
            status_code=200,
            content={"message": "Saga started successfully", "saga": saga.dict()}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def handle_event(ch, method, properties, body):
    try:
        payload = json.loads(body)
        if method.routing_key == "document_uploaded":
            handle_document_uploaded_event(payload)
    except Exception as e:
        print(f"Failed to handle event: {str(e)}")

# Start listening for events
listen_for_events("document_uploaded", handle_event)