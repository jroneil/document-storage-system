# storage-service/app/__init__.py

# Expose the main FastAPI app
from .main import app

# Expose services for easier imports
from .services.s3_storage import upload_file_to_s3, delete_file_from_s3

# Optional: Define what should be exposed when the package is imported
__all__ = ["app", "upload_file_to_s3", "delete_file_from_s3"]