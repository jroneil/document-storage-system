from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

import pytest

import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

from app.services.document_repository import InMemoryDocumentRepository
from app.services.document_service import DocumentNotFoundError, DocumentService


def _sample_metadata() -> dict:
    now = datetime.now(timezone.utc)
    return {
        "document_id": uuid4(),
        "file_name": "manual.pdf",
        "file_size": 1024,
        "file_type": "application/pdf",
        "upload_date": now,
        "last_modified_date": now,
        "user_id": uuid4(),
        "tags": ["initial"],
        "description": "Original revision",
        "storage_path": "/tmp/manual.pdf",
        "version": 1,
        "checksum": "abc123",
        "acl": {"public": False},
        "thumbnail_path": None,
        "expiration_date": None,
        "category": "Guides",
        "division": "Docs",
        "business_unit": "Docs",
        "brand_id": None,
        "document_type": "Document",
    }


def _service() -> DocumentService:
    return DocumentService(InMemoryDocumentRepository())


def test_create_document_assigns_revision_sequentially():
    service = _service()
    metadata = _sample_metadata()

    created = service.create_document(metadata)
    assert created["revision"] == 1

    created_again = service.create_document(metadata)
    assert created_again["revision"] == 2


def test_update_document_creates_new_revision_without_mutating_history():
    service = _service()
    metadata = _sample_metadata()
    first = service.create_document(metadata)

    updated = service.update_document(first["document_id"], {"description": "Updated"})

    assert updated["revision"] == first["revision"] + 1
    assert updated["description"] == "Updated"

    history = service.list_document_history(first["document_id"])
    assert len(history) == 2
    assert history[0]["description"] == "Updated"
    assert history[1]["description"] == "Original revision"


def test_get_latest_document_excludes_soft_deleted_revision():
    service = _service()
    metadata = _sample_metadata()
    created = service.create_document(metadata)
    service.soft_delete_document(created["document_id"])

    with pytest.raises(DocumentNotFoundError):
        service.get_latest_document(created["document_id"])

    # Including deleted revisions should return the tombstone row.
    latest_deleted = service.get_latest_document(created["document_id"], include_deleted=True)
    assert latest_deleted["is_deleted"] is True


def test_soft_delete_document_generates_new_revision():
    service = _service()
    metadata = _sample_metadata()
    created = service.create_document(metadata)

    deleted = service.soft_delete_document(created["document_id"])

    assert deleted["revision"] == created["revision"] + 1
    assert deleted["is_deleted"] is True

    history = service.list_document_history(created["document_id"])
    assert [item["revision"] for item in history] == [2, 1]
