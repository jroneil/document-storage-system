import os
from minio import Minio
from minio.error import S3Error
from dotenv import load_dotenv
import uuid
from datetime import datetime

load_dotenv()

# Initialize MinIO client
minio_client = Minio(
    os.getenv("MINIO_ENDPOINT", "minio:9000"),
    access_key=os.getenv("MINIO_ACCESS_KEY", "minioadmin"),
    secret_key=os.getenv("MINIO_SECRET_KEY", "minioadmin"),
    secure=False  # Set to True if using HTTPS
)

def ensure_bucket_exists(bucket_name: str):
    """Ensure the bucket exists, create it if it doesn't"""
    try:
        if not minio_client.bucket_exists(bucket_name):
            minio_client.make_bucket(bucket_name)
            print(f"Created bucket: {bucket_name}")
    except S3Error as e:
        raise Exception(f"Error ensuring bucket exists: {str(e)}")

def upload_file_to_minio(file_path: str, bucket_name: str, object_name: str, metadata: dict = None) -> str:
    """
    Upload a file to MinIO with metadata
    
    Args:
        file_path: Path to the local file
        bucket_name: MinIO bucket name
        object_name: Object name in MinIO (folder structure)
        metadata: Optional metadata dictionary
    
    Returns:
        URL of the uploaded file
    """
    try:
        # Ensure bucket exists
        ensure_bucket_exists(bucket_name)
        
        # Prepare metadata
        minio_metadata = {}
        if metadata:
            for key, value in metadata.items():
                minio_metadata[key] = str(value)
        
        # Upload file
        minio_client.fput_object(
            bucket_name,
            object_name,
            file_path,
            metadata=minio_metadata
        )
        
        # Return the object URL
        return f"http://{os.getenv('MINIO_ENDPOINT', 'minio:9000')}/{bucket_name}/{object_name}"
        
    except S3Error as e:
        raise Exception(f"Failed to upload file to MinIO: {str(e)}")

def delete_file_from_minio(bucket_name: str, object_name: str) -> bool:
    """
    Delete a file from MinIO
    
    Args:
        bucket_name: MinIO bucket name
        object_name: Object name in MinIO
    
    Returns:
        True if successful
    """
    try:
        minio_client.remove_object(bucket_name, object_name)
        return True
    except S3Error as e:
        raise Exception(f"Failed to delete file from MinIO: {str(e)}")

def generate_object_path(brand: str, business_unit: str, document_name: str, revision: str, file_extension: str) -> str:
    """
    Generate object path in the format: <brand>/<business unit>/<document name>-<revision>.<extension>
    
    Args:
        brand: Brand name
        business_unit: Business unit name
        document_name: Document name
        revision: Revision number
        file_extension: File extension
    
    Returns:
        Object path string
    """
    # Clean and format the components
    clean_brand = brand.lower().replace(' ', '-')
    clean_business_unit = business_unit.lower().replace(' ', '-')
    clean_document_name = document_name.lower().replace(' ', '-')
    clean_extension = file_extension.lower().lstrip('.')
    
    return f"{clean_brand}/{clean_business_unit}/{clean_document_name}-{revision}.{clean_extension}"

def get_file_metadata(file_path: str) -> dict:
    """
    Get basic file metadata
    
    Args:
        file_path: Path to the file
    
    Returns:
        Dictionary with file metadata
    """
    try:
        stat = os.stat(file_path)
        return {
            "file_size": stat.st_size,
            "last_modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
            "created": datetime.fromtimestamp(stat.st_ctime).isoformat()
        }
    except Exception as e:
        raise Exception(f"Failed to get file metadata: {str(e)}")
