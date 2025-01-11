import os
from datetime import datetime
from app.models.document import DocumentMetadata, BrandMetadata
import uuid
import hashlib

def extract_metadata(file_path: str, user_id: uuid.UUID, file_type: str, document_type: str) -> dict:
    try:
        file_size = os.path.getsize(file_path)
        file_name = os.path.basename(file_path)
        upload_date = datetime.now()
        last_modified_date = upload_date

        document_id = uuid.uuid4()
        checksum = calculate_checksum(file_path)

        metadata = DocumentMetadata(
            document_id=document_id,
            file_name=file_name,
            file_size=file_size,
            file_type=file_type,
            upload_date=upload_date,
            last_modified_date=last_modified_date,
            user_id=user_id,
            storage_path=f"/documents/{document_id}/{file_name}",
            checksum=checksum,
            document_type=document_type
        )

        return metadata.dict()
    except Exception as e:
        raise Exception(f"Failed to extract metadata: {str(e)}")

def calculate_checksum(file_path: str) -> str:
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()