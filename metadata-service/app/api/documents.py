from __future__ import annotations

from typing import List
from uuid import UUID

from fastapi import APIRouter, HTTPException, status

from app.schemas.document_metadata import (
    DocumentMetadataHistoryResponse,
    DocumentMetadataResponse,
    DocumentMetadataUpdate,
)
from app.services.postgres_service import (
    DocumentNotFoundError,
    delete_document_metadata,
    get_document_service,
    list_document_history,
    update_document_metadata,
)


router = APIRouter(prefix="/documents", tags=["documents"])


@router.get("/{document_id}", response_model=DocumentMetadataResponse)
def read_document(document_id: UUID, include_deleted: bool = False) -> DocumentMetadataResponse:
    try:
        record = get_document_service().get_latest_document(document_id, include_deleted=include_deleted)
    except DocumentNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    return DocumentMetadataResponse.model_validate(record)


@router.get("/{document_id}/history", response_model=DocumentMetadataHistoryResponse)
def read_document_history(document_id: UUID) -> DocumentMetadataHistoryResponse:
    history = list_document_history(document_id)
    if not history:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document not found")
    items: List[DocumentMetadataResponse] = [
        DocumentMetadataResponse.model_validate(record) for record in history
    ]
    return DocumentMetadataHistoryResponse(items=items)


@router.put("/{document_id}", response_model=DocumentMetadataResponse)
def update_document(document_id: UUID, payload: DocumentMetadataUpdate) -> DocumentMetadataResponse:
    try:
        record = update_document_metadata(document_id, payload.model_dump(exclude_unset=True))
    except DocumentNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    return DocumentMetadataResponse.model_validate(record)


@router.delete("/{document_id}", response_model=DocumentMetadataResponse)
def delete_document(document_id: UUID) -> DocumentMetadataResponse:
    try:
        record = delete_document_metadata(document_id)
    except DocumentNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    return DocumentMetadataResponse.model_validate(record)
