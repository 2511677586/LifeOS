from __future__ import annotations

from datetime import datetime, timezone
import json
from pathlib import Path

from app.repositories.knowledge_repository import KnowledgeRepository
from app.services.knowledge_type_service import KnowledgeTypeService
from app.services.storage_service import StoredRecord


class KnowledgeQueryService:
    """Query layer for Knowledge Object retrieval and filtering.

    This service is responsible for read-oriented operations only. It uses
    KnowledgeRepository as the persistence boundary and avoids direct access to
    StorageService.

    The implementation is Markdown-first and backward compatible with legacy
    Markdown files that may not contain front matter metadata.
    """

    def __init__(
        self,
        knowledge_repository: KnowledgeRepository,
        knowledge_type_service: KnowledgeTypeService | None = None,
    ) -> None:
        self._knowledge_repository = knowledge_repository
        self._knowledge_type_service = knowledge_type_service or KnowledgeTypeService()

    def list_all(self) -> list[StoredRecord]:
        """Return all known records in repository order (most recent first)."""
        return self._knowledge_repository.list(limit=None)

    def get_by_id(self, knowledge_id: str) -> StoredRecord | None:
        """Get a single knowledge record by stable ID.

        Returns None when the record does not exist.
        """
        for record in self.list_all():
            if self._record_id(record) == knowledge_id:
                return record
        return None

    def filter_by_type(self, knowledge_type: str) -> list[StoredRecord]:
        """Filter records by metadata type value."""
        normalized_type = self._knowledge_type_service.canonicalize_type(knowledge_type)
        if not normalized_type:
            return []

        matches: list[StoredRecord] = []
        for record in self.list_all():
            metadata = self._parse_front_matter(record.content)
            record_type = self._knowledge_type_service.canonicalize_type(str(metadata.get("type", "")))
            if record_type == normalized_type:
                matches.append(record)
        return matches

    def filter_by_tag(self, tag: str) -> list[StoredRecord]:
        """Filter records containing a metadata tag (case-insensitive)."""
        normalized_tag = tag.strip().lower()
        if not normalized_tag:
            return []

        matches: list[StoredRecord] = []
        for record in self.list_all():
            metadata = self._parse_front_matter(record.content)
            tags = metadata.get("tags", [])
            normalized_tags = {str(item).strip().lower() for item in tags if str(item).strip()}
            if normalized_tag in normalized_tags:
                matches.append(record)
        return matches

    def filter_by_date_range(self, start_date: datetime, end_date: datetime) -> list[StoredRecord]:
        """Filter records by created timestamp within an inclusive range."""
        start = self._normalize_datetime(start_date)
        end = self._normalize_datetime(end_date)
        if end < start:
            return []

        matches: list[StoredRecord] = []
        for record in self.list_all():
            metadata = self._parse_front_matter(record.content)
            created_value = metadata.get("created") or metadata.get("created_at")
            created = self._parse_datetime(created_value)
            if created is None:
                continue
            normalized_created = self._normalize_datetime(created)
            if start <= normalized_created <= end:
                matches.append(record)
        return matches

    def _record_id(self, record: StoredRecord) -> str:
        metadata = self._parse_front_matter(record.content)
        metadata_id = metadata.get("id")
        if isinstance(metadata_id, str) and metadata_id.strip():
            return metadata_id.strip()
        return Path(record.path).stem

    def _parse_front_matter(self, content: str) -> dict[str, object]:
        lines = content.splitlines()
        if len(lines) < 3 or lines[0].strip() != "---":
            return {}

        metadata: dict[str, object] = {}
        for line in lines[1:]:
            if line.strip() == "---":
                break
            if ":" not in line:
                continue
            key, raw_value = line.split(":", 1)
            key = key.strip()
            value = raw_value.strip()
            metadata[key] = self._parse_scalar(value)
        return metadata

    def _parse_scalar(self, value: str) -> object:
        if not value:
            return ""
        if value.startswith('"') and value.endswith('"'):
            try:
                return json.loads(value)
            except json.JSONDecodeError:
                return value.strip('"')
        if value.startswith("[") and value.endswith("]"):
            try:
                parsed = json.loads(value)
                return parsed if isinstance(parsed, list) else []
            except json.JSONDecodeError:
                return []
        if value.isdigit():
            return int(value)
        return value

    def _parse_datetime(self, value: object) -> datetime | None:
        if not isinstance(value, str) or not value.strip():
            return None
        try:
            return datetime.fromisoformat(value)
        except ValueError:
            return None

    def _normalize_datetime(self, value: datetime) -> datetime:
        if value.tzinfo is None:
            return value.replace(tzinfo=timezone.utc)
        return value.astimezone(timezone.utc)
