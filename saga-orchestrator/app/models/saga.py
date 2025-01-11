from pydantic import BaseModel
from typing import Optional, List, Dict
from datetime import datetime
import uuid

class SagaStep(BaseModel):
    step_id: uuid.UUID
    saga_id: uuid.UUID
    service_name: str
    status: str  # e.g., "pending", "completed", "failed"
    payload: Dict
    created_at: datetime
    updated_at: datetime

class Saga(BaseModel):
    saga_id: uuid.UUID
    steps: List[SagaStep]
    status: str  # e.g., "in_progress", "completed", "failed"
    created_at: datetime
    updated_at: datetime