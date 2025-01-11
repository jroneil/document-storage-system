from app.models.saga import Saga, SagaStep
from app.services.message_queue import publish_event
import uuid
from datetime import datetime

def start_saga(payload: dict):
    try:
        # Create a new saga
        saga_id = uuid.uuid4()
        saga = Saga(
            saga_id=saga_id,
            steps=[],
            status="in_progress",
            created_at=datetime.now(),
            updated_at=datetime.now()
        )

        # Step 1: Document Uploaded
        step1 = SagaStep(
            step_id=uuid.uuid4(),
            saga_id=saga_id,
            service_name="ingestion-service",
            status="pending",
            payload=payload,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        saga.steps.append(step1)

        # Publish event: document_uploaded
        publish_event("document_uploaded", payload)

        return saga
    except Exception as e:
        raise Exception(f"Failed to start saga: {str(e)}")

def handle_document_uploaded_event(payload: dict):
    try:
        # Step 2: Save Metadata
        step2 = SagaStep(
            step_id=uuid.uuid4(),
            saga_id=payload["saga_id"],
            service_name="metadata-service",
            status="pending",
            payload=payload,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )

        # Publish event: save_metadata
        publish_event("save_metadata", payload)

        return step2
    except Exception as e:
        raise Exception(f"Failed to handle document_uploaded event: {str(e)}")