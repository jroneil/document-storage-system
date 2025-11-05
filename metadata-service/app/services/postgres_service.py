from __future__ import annotations

import logging
import os
from typing import Any, Dict, List, Optional
from uuid import UUID

import psycopg2
from psycopg2.extras import Json, RealDictCursor
from dotenv import load_dotenv

from .document_repository import DocumentRepository
from .document_service import DocumentNotFoundError, DocumentService

load_dotenv()

logger = logging.getLogger(__name__)


def _connection_kwargs() -> Dict[str, Any]:
    return {
        "host": os.getenv("POSTGRES_HOST"),
        "database": os.getenv("POSTGRES_DB"),
        "user": os.getenv("POSTGRES_USER"),
        "password": os.getenv("POSTGRES_PASSWORD"),
    }


def _get_connection() -> psycopg2.extensions.connection:
    return psycopg2.connect(**_connection_kwargs())


class PostgresDocumentRepository(DocumentRepository):
    """Concrete repository that persists metadata revisions in Postgres."""

    _INSERT_COLUMNS = [
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
    ]

    _RETURNING_COLUMNS = ["id", *_INSERT_COLUMNS]

    def persist(self, metadata: Dict[str, Any]) -> Dict[str, Any]:
        placeholders = ", ".join(["%s"] * len(self._INSERT_COLUMNS))
        query = (
            f"INSERT INTO documents ({', '.join(self._INSERT_COLUMNS)})"
            f" VALUES ({placeholders}) RETURNING {', '.join(self._RETURNING_COLUMNS)}"
        )

        values = [
            metadata.get("document_id"),
            metadata.get("revision"),
            metadata.get("is_deleted", False),
            metadata.get("file_name"),
            metadata.get("file_size"),
            metadata.get("file_type"),
            metadata.get("upload_date"),
            metadata.get("last_modified_date"),
            metadata.get("user_id"),
            metadata.get("tags"),
            metadata.get("description"),
            metadata.get("storage_path"),
            metadata.get("version"),
            metadata.get("checksum"),
            Json(metadata["acl"]) if metadata.get("acl") is not None else None,
            metadata.get("thumbnail_path"),
            metadata.get("expiration_date"),
            metadata.get("category"),
            metadata.get("division"),
            metadata.get("business_unit"),
            metadata.get("brand_id"),
            metadata.get("document_type"),
        ]

        logger.debug("Persisting document metadata with values: %s", values)

        with _get_connection() as connection:
            with connection.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(query, values)
                row = cursor.fetchone()
                return self._convert_row(row)

    def fetch_latest(self, document_id: UUID, include_deleted: bool = False) -> Optional[Dict[str, Any]]:
        conditions = ["document_id = %s"]
        params: List[Any] = [document_id]
        if not include_deleted:
            conditions.append("is_deleted = FALSE")

        query = (
            f"SELECT {', '.join(self._RETURNING_COLUMNS)} FROM documents "
            f"WHERE {' AND '.join(conditions)} ORDER BY revision DESC LIMIT 1"
        )

        with _get_connection() as connection:
            with connection.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(query, params)
                row = cursor.fetchone()
                return self._convert_row(row) if row else None

    def fetch_history(self, document_id: UUID) -> List[Dict[str, Any]]:
        query = (
            f"SELECT {', '.join(self._RETURNING_COLUMNS)} FROM documents "
            "WHERE document_id = %s ORDER BY revision DESC"
        )

        with _get_connection() as connection:
            with connection.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(query, (document_id,))
                rows = cursor.fetchall()
                return [self._convert_row(row) for row in rows]

    @staticmethod
    def _convert_row(row: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        if not row:
            return {}
        # RealDictCursor returns dict-like rows which we copy to avoid mutation.
        record = dict(row)
        # psycopg2 already converts UUID/JSON/ARRAY types, only ensure empty tags default.
        if record.get("tags") is None:
            record["tags"] = []
        return record


_repository = PostgresDocumentRepository()
_document_service = DocumentService(_repository)


# ----------------------------------------------------------------------
# Convenience wrappers used across the codebase
# ----------------------------------------------------------------------
def get_document_service() -> DocumentService:
    return _document_service


def save_document_metadata(document_metadata: Dict[str, Any]) -> Dict[str, Any]:
    logger.info("Saving document metadata for %s", document_metadata.get("document_id"))
    return _document_service.create_document(document_metadata)


def update_document_metadata(document_id: Any, updates: Dict[str, Any]) -> Dict[str, Any]:
    logger.info("Creating new revision for document %s", document_id)
    return _document_service.update_document(document_id, updates)


def get_latest_document_metadata(document_id: Any, *, include_deleted: bool = False) -> Dict[str, Any]:
    logger.debug("Fetching latest metadata for document %s", document_id)
    return _document_service.get_latest_document(document_id, include_deleted=include_deleted)


def list_document_history(document_id: Any) -> List[Dict[str, Any]]:
    logger.debug("Fetching metadata history for document %s", document_id)
    return _document_service.list_document_history(document_id)


def delete_document_metadata(document_id: Any) -> Dict[str, Any]:
    logger.info("Soft deleting document %s", document_id)
    return _document_service.soft_delete_document(document_id)


__all__ = [
    "DocumentNotFoundError",
    "PostgresDocumentRepository",
    "delete_document_metadata",
    "get_document_service",
    "get_latest_document_metadata",
    "list_document_history",
    "save_document_metadata",
    "update_document_metadata",
]
