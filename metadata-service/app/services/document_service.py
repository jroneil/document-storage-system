from __future__ import annotations

from copy import deepcopy
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from uuid import UUID, uuid4

from .document_repository import DocumentRepository


class DocumentNotFoundError(Exception):
    """Raised when the requested document metadata cannot be located."""


class DocumentService:
    """High level operations for document metadata revisions."""

    _ALLOWED_FIELDS = {
        "id",
        "document_id",
        "revision",
        "is_deleted",
        "file_name",
        "file_size",
        "file_type",
        "upload_date",
        "last_modified_date",
        "user_id",
        "tags",
        "description",
        "storage_path",
        "version",
        "checksum",
        "acl",
        "thumbnail_path",
        "expiration_date",
        "category",
        "division",
        "business_unit",
        "brand_id",
        "document_type",
    }

    _REQUIRED_FIELDS = {
        "file_name",
        "file_size",
        "file_type",
        "upload_date",
        "last_modified_date",
        "user_id",
        "storage_path",
        "version",
        "checksum",
        "document_type",
    }

    def __init__(self, repository: DocumentRepository) -> None:
        self._repository = repository

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------
    def create_document(self, metadata: Dict[str, Any]) -> Dict[str, Any]:
        record = self._normalize_new_metadata(metadata)
        return self._repository.persist(record)

    def update_document(self, document_id: Any, updates: Dict[str, Any]) -> Dict[str, Any]:
        doc_id = self._to_uuid(document_id)
        current = self._repository.fetch_latest(doc_id, include_deleted=False)
        if not current:
            raise DocumentNotFoundError(f"Document {doc_id} not found")

        base_record = self._prepare_base_record(current)
        normalized_updates = self._normalize_updates(updates)
        base_record.update(normalized_updates)
        base_record["revision"] = current.get("revision", 0) + 1
        base_record["is_deleted"] = False
        base_record["document_id"] = doc_id
        base_record["upload_date"] = current.get("upload_date")
        base_record["last_modified_date"] = normalized_updates.get(
            "last_modified_date",
            datetime.now(timezone.utc),
        )

        self._ensure_required_fields(base_record)
        return self._repository.persist(base_record)

    def get_latest_document(self, document_id: Any, *, include_deleted: bool = False) -> Dict[str, Any]:
        doc_id = self._to_uuid(document_id)
        if include_deleted:
            record = self._repository.fetch_latest(doc_id, include_deleted=True)
            if not record:
                raise DocumentNotFoundError(f"Document {doc_id} not found")
            return deepcopy(record)

        latest_any = self._repository.fetch_latest(doc_id, include_deleted=True)
        if not latest_any or latest_any.get("is_deleted"):
            raise DocumentNotFoundError(f"Document {doc_id} not found")
        return deepcopy(latest_any)

    def list_document_history(self, document_id: Any) -> List[Dict[str, Any]]:
        doc_id = self._to_uuid(document_id)
        return [deepcopy(item) for item in self._repository.fetch_history(doc_id)]

    def soft_delete_document(self, document_id: Any) -> Dict[str, Any]:
        doc_id = self._to_uuid(document_id)
        current = self._repository.fetch_latest(doc_id, include_deleted=True)
        if not current:
            raise DocumentNotFoundError(f"Document {doc_id} not found")

        if current.get("is_deleted"):
            return deepcopy(current)

        record = self._prepare_base_record(current)
        record["revision"] = current.get("revision", 0) + 1
        record["is_deleted"] = True
        record["document_id"] = doc_id
        record["upload_date"] = current.get("upload_date")
        record["last_modified_date"] = datetime.now(timezone.utc)

        self._ensure_required_fields(record)
        return self._repository.persist(record)

    # ------------------------------------------------------------------
    # Normalisation helpers
    # ------------------------------------------------------------------
    def _normalize_new_metadata(self, metadata: Dict[str, Any]) -> Dict[str, Any]:
        record = self._prepare_base_record(metadata)
        doc_id = record.get("document_id")
        record["document_id"] = self._to_uuid(doc_id) if doc_id else uuid4()

        latest = self._repository.fetch_latest(record["document_id"], include_deleted=True)
        next_revision = latest.get("revision", 0) + 1 if latest else 1
        record["revision"] = next_revision

        if "is_deleted" not in record:
            record["is_deleted"] = False
        else:
            record["is_deleted"] = bool(record["is_deleted"])

        record["upload_date"] = record.get("upload_date") or datetime.now(timezone.utc)
        record["last_modified_date"] = record.get("last_modified_date") or datetime.now(timezone.utc)

        self._ensure_required_fields(record)
        return record

    def _normalize_updates(self, updates: Dict[str, Any]) -> Dict[str, Any]:
        record = self._prepare_base_record(updates, allow_missing_required=True)
        for forbidden in ("document_id", "revision", "is_deleted"):
            record.pop(forbidden, None)
        return record

    def _prepare_base_record(
        self,
        payload: Dict[str, Any],
        *,
        allow_missing_required: bool = False,
    ) -> Dict[str, Any]:
        record = {
            key: deepcopy(value)
            for key, value in payload.items()
            if key in self._ALLOWED_FIELDS
        }

        for key in ("document_id", "user_id", "brand_id"):
            if key in record and record[key] is not None:
                record[key] = self._to_uuid(record[key])

        for key in ("upload_date", "last_modified_date", "expiration_date"):
            if key in record and record[key] is not None:
                record[key] = self._to_datetime(record[key])

        if record.get("tags") is None:
            record["tags"] = []
        elif not isinstance(record["tags"], list):
            record["tags"] = list(record["tags"])

        if record.get("acl") is not None and not isinstance(record["acl"], dict):
            raise ValueError("ACL metadata must be a JSON object")

        if not allow_missing_required:
            self._ensure_required_fields(record)

        record.pop("id", None)
        return record

    # ------------------------------------------------------------------
    # Utility helpers
    # ------------------------------------------------------------------
    @staticmethod
    def _to_uuid(value: Any) -> Optional[UUID]:
        if value is None or isinstance(value, UUID):
            return value
        return UUID(str(value))

    @staticmethod
    def _to_datetime(value: Any) -> Optional[datetime]:
        if value is None or isinstance(value, datetime):
            return value
        return datetime.fromisoformat(str(value))

    def _ensure_required_fields(self, record: Dict[str, Any]) -> None:
        missing = [field for field in self._REQUIRED_FIELDS if record.get(field) is None]
        if missing:
            raise ValueError(f"Missing required metadata fields: {', '.join(missing)}")
