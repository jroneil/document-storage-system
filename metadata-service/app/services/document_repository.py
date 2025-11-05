from __future__ import annotations

from copy import deepcopy
from typing import Any, Dict, List, Optional, Protocol
from uuid import UUID, uuid4


class DocumentRepository(Protocol):
    """Protocol describing persistence operations for document metadata."""

    def persist(self, metadata: Dict[str, Any]) -> Dict[str, Any]:
        """Persist a metadata record and return the stored row."""

    def fetch_latest(self, document_id: UUID, include_deleted: bool = False) -> Optional[Dict[str, Any]]:
        """Return the latest revision for the given document id."""

    def fetch_history(self, document_id: UUID) -> List[Dict[str, Any]]:
        """Return all revisions for the given document id ordered from newest to oldest."""


class InMemoryDocumentRepository(DocumentRepository):
    """Lightweight repository used for unit tests."""

    def __init__(self) -> None:
        self._records: List[Dict[str, Any]] = []

    def persist(self, metadata: Dict[str, Any]) -> Dict[str, Any]:
        stored = deepcopy(metadata)
        stored.setdefault("id", uuid4())
        self._records.append(stored)
        return deepcopy(stored)

    def fetch_latest(self, document_id: UUID, include_deleted: bool = False) -> Optional[Dict[str, Any]]:
        candidates = [
            record
            for record in self._records
            if record.get("document_id") == document_id
            and (include_deleted or not record.get("is_deleted", False))
        ]
        if not candidates:
            return None
        candidates.sort(key=lambda record: record.get("revision", 0), reverse=True)
        return deepcopy(candidates[0])

    def fetch_history(self, document_id: UUID) -> List[Dict[str, Any]]:
        history = [
            deepcopy(record)
            for record in self._records
            if record.get("document_id") == document_id
        ]
        history.sort(key=lambda record: record.get("revision", 0), reverse=True)
        return history
