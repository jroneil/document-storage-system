from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import asyncio
import threading

def run_event_listener():
    """Run the event listener in a separate thread"""
    listen_for_events("document_uploaded", handle_document_uploaded_event)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Start event listener in background thread
    listener_thread = threading.Thread(target=run_event_listener, daemon=True)
    listener_thread.start()
    print("Event listener started")
    yield
    # Shutdown: Clean up if needed
    print("Shutting down")

app = FastAPI(lifespan=lifespan)

@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring service status"""
    return JSONResponse(
        status_code=200,
        content={"status": "healthy", "service": "metadata-service"}
    )

# ... rest of your endpoints remain the same

def handle_document_uploaded_event(ch, method, properties, body):
    try:
        payload = json.loads(body)
        print(f"Handling document_uploaded event: {payload}")
    except Exception as e:
        print(f"Failed to handle document_uploaded event: {str(e)}") 