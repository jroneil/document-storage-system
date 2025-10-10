from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from app.services.orchestrator import start_saga, handle_document_uploaded_event
from app.services.message_queue import listen_for_events
import json
import datetime

app = FastAPI()

@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring service status"""
    return JSONResponse(
        status_code=200,
        content={
            "status": "healthy",
            "service": "saga-orchestrator",
            "timestamp": datetime.datetime.now().isoformat(),
            "version": "1.0.0"
        }
    )

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

# Start listening for events with retry logic
def start_event_listener():
    """Start event listener with retry logic for RabbitMQ connection"""
    import time
    max_retries = 10
    retry_delay = 5
    
    for attempt in range(max_retries):
        try:
            listen_for_events("document_uploaded", handle_event)
            print("Successfully connected to RabbitMQ and started event listener")
            return
        except Exception as e:
            print(f"Failed to connect to RabbitMQ (attempt {attempt + 1}/{max_retries}): {str(e)}")
            if attempt < max_retries - 1:
                print(f"Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
            else:
                print("Max retries reached. Event listener will not start.")
                # Don't crash the service, just log the error
                break

# Start the event listener in the background
import threading
listener_thread = threading.Thread(target=start_event_listener, daemon=True)
listener_thread.start()
