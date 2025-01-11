from fastapi import FastAPI
from app.routes.ingestion import router as ingestion_router
from app.routes.metadata import router as metadata_router
from app.routes.storage import router as storage_router
from app.routes.processing import router as processing_router
from app.routes.search import router as search_router
from app.routes.ai import router as ai_router
from app.routes.notification import router as notification_router

# Customize the OpenAPI schema
app = FastAPI(
    title="API Gateway",
    description="A single entry point for all microservices in the Document Storage System.",
    version="1.0.0",
    contact={
        "name": "Your Name",
        "email": "your.email@example.com",
    },
    license_info={
        "name": "MIT",
    },
)

# Include all routes
app.include_router(ingestion_router, prefix="/ingestion", tags=["ingestion"])
app.include_router(metadata_router, prefix="/metadata", tags=["metadata"])
app.include_router(storage_router, prefix="/storage", tags=["storage"])
app.include_router(processing_router, prefix="/processing", tags=["processing"])
app.include_router(search_router, prefix="/search", tags=["search"])
app.include_router(ai_router, prefix="/ai", tags=["ai"])
app.include_router(notification_router, prefix="/notification", tags=["notification"])