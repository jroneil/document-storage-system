from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from services.s3_storage import upload_file_to_s3, delete_file_from_s3

app = FastAPI()

@app.post("/upload")
async def upload_file(file_path: str, bucket_name: str, s3_key: str):
    try:
        s3_url = upload_file_to_s3(file_path, bucket_name, s3_key)
        return JSONResponse(
            status_code=200,
            content={"message": "File uploaded successfully", "s3_url": s3_url}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/delete")
async def delete_file(bucket_name: str, s3_key: str):
    try:
        delete_file_from_s3(bucket_name, s3_key)
        return JSONResponse(
            status_code=200,
            content={"message": "File deleted successfully"}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))