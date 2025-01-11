import os
from fastapi import UploadFile
from datetime import datetime

UPLOAD_DIR = "uploads"

def handle_file_upload(file: UploadFile) -> str:
    try:
        if not os.path.exists(UPLOAD_DIR):
            os.makedirs(UPLOAD_DIR)

        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        file_path = os.path.join(UPLOAD_DIR, f"{timestamp}_{file.filename}")

        with open(file_path, "wb") as buffer:
            buffer.write(file.file.read())

        return file_path
    except Exception as e:
        raise Exception(f"Failed to upload file: {str(e)}")