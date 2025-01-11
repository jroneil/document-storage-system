from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from app.models.document import DocumentMetadata, BrandMetadata
from app.services.postgres_service import save_document_metadata, delete_document_metadata
from app.services.mongo_service import save_brand_metadata, delete_brand_metadata
from app.services.message_queue import listen_for_events
import json

app = FastAPI()

@app.post("/save-metadata")
async def save_metadata(payload: dict):
    try:
        # Save document metadata to PostgreSQL
        save_document_metadata(payload["document"])

        # Save brand metadata to MongoDB
        save_brand_metadata(payload["brand"])

        return JSONResponse(
            status_code=200,
            content={"message": "Metadata saved successfully"}
        )
    except Exception as e:
        # Trigger compensation action
        delete_document_metadata(payload["document"]["document_id"])
        delete_brand_metadata(payload["brand"]["document_id"])
        raise HTTPException(status_code=500, detail=str(e))

def handle_document_uploaded_event(ch, method, properties, body):
    try:
        payload = json.loads(body)
        # Handle the event (e.g., trigger indexing in Elasticsearch)
        print(f"Handling document_uploaded event: {payload}")
    except Exception as e:
        print(f"Failed to handle document_uploaded event: {str(e)}")

# Start listening for events
listen_for_events("document_uploaded", handle_document_uploaded_event)