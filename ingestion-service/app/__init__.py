# ingestion-service/app/__init__.py
from .services.file_upload import handle_file_upload
from .services.metadata_extraction import extract_metadata
from .services.message_queue import publish_event

__all__ = ["app", "handle_file_upload", "extract_metadata", "publish_event"]

# Optional: Add type hints (recommended)
from fastapi import FastAPI
from typing import Callable

app: FastAPI
handle_file_upload: Callable
extract_metadata: Callable
publish_event: Callable
