# processing-service/app/__init__.py

# Expose the main FastAPI app
from .main import app

# Expose services for easier imports
from .services.text_extraction import extract_text_from_pdf
from .services.thumbnail_generation import generate_thumbnail

# Optional: Define what should be exposed when the package is imported
__all__ = ["app", "extract_text_from_pdf", "generate_thumbnail"]