# search-service/app/__init__.py

# Expose the main FastAPI app
from .main import app

# Expose services for easier imports
from .services.elasticsearch_client import index_document, search_documents

# Optional: Define what should be exposed when the package is imported
__all__ = ["app", "index_document", "search_documents"]