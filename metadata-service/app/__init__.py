# metadata-service/app/__init__.py

# Expose the main FastAPI app
from .main import app

# Expose services for easier imports
from .services.mongo_service import save_brand_metadata, delete_brand_metadata
from .services.postgres_service import save_document_metadata, delete_document_metadata
from .services.message_queue import listen_for_events

# Optional: Define what should be exposed when the package is imported
__all__ = ["app", "save_brand_metadata", "delete_brand_metadata", "save_document_metadata", "delete_document_metadata", "listen_for_events"]