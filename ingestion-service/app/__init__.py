# ingestion-service/app/__init__.py

# Expose the main FastAPI app
from .main import app

# Expose services for easier imports
from .services.file_upload import handle_file_upload
from .services.metadata_extraction import extract_metadata
from .services.message_queue import publish_event

# Optional: Define what should be exposed when the package is imported
__all__ = ["app", "handle_file_upload", "extract_metadata", "publish_event"]