from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from services.file_upload import handle_file_upload
from services.metadata_parser import parse_metadata
from services.message_queue import publish_event

app = FastAPI()

@app.post("/bulk-upload")
async def bulk_upload(file: UploadFile = File(...)):
    try:
        # Step 1: Handle file upload
        file_path = handle_file_upload(file)

        # Step 2: Parse metadata from the file
        metadata_list = parse_metadata(file_path)

        # Step 3: Send metadata to the message queue
        for metadata in metadata_list:
            publish_event("metadata_uploaded", metadata)

        return JSONResponse(
            status_code=200,
            content={"message": "Bulk upload completed successfully", "metadata_count": len(metadata_list)}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))