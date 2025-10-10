from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import (
    ingestion,
    metadata,
    storage,
    processing,
    search,
    ai,
    notification,
    auth,
    user_preferences
)

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

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include all routes
app.include_router(ingestion.router, prefix="/ingestion", tags=["ingestion"])
app.include_router(metadata.router, prefix="/metadata", tags=["metadata"])
app.include_router(storage.router, prefix="/storage", tags=["storage"])
app.include_router(processing.router, prefix="/processing", tags=["processing"])
app.include_router(search.router, prefix="/search", tags=["search"])
app.include_router(ai.router, prefix="/ai", tags=["ai"])
app.include_router(notification.router, prefix="/notification", tags=["notification"])
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(user_preferences.router, prefix="/user-preferences", tags=["user-preferences"])
