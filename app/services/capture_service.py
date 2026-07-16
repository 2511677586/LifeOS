from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from app.models.knowledge_metadata import KnowledgeMetadata
from app.services.metadata_service import MetadataService
from app.services.storage_service import StoredRecord, StorageService


@dataclass(slots=True)
class SavedRecord:
    metadata: KnowledgeMetadata
    path: Path
    document: str


class CaptureService:
    def __init__(self, metadata_service: MetadataService | None = None, storage_service: StorageService | None = None) -> None:
        self._metadata_service = metadata_service or MetadataService()
        self._storage_service = storage_service or StorageService()

    def save_content(self, content: str) -> SavedRecord:
        cleaned_content = content.strip()
        if not cleaned_content:
            raise ValueError("Content cannot be empty.")

        metadata = self._metadata_service.create_metadata(content)
        document = self._metadata_service.build_markdown_document(content, metadata)
        path = self._storage_service.save_markdown(metadata.id, document)
        return SavedRecord(metadata=metadata, path=path, document=document)

    def list_recent_records(self, limit: int = 20) -> list[StoredRecord]:
        return self._storage_service.list_recent_records(limit=limit)
