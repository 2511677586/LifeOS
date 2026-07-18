from __future__ import annotations

from dataclasses import replace
import json
import re
import uuid
from datetime import datetime
from typing import Iterable

from app.models.knowledge_metadata import KnowledgeMetadata
from app.services.knowledge_type_service import KnowledgeTypeService

TITLE_LIMIT = 60
HEADING_PATTERN = re.compile(r"^#{1,6}\s*")


class MetadataService:
    """Builds, validates, and evolves knowledge metadata for Markdown records."""

    def __init__(self, knowledge_type_service: KnowledgeTypeService | None = None) -> None:
        self._knowledge_type_service = knowledge_type_service or KnowledgeTypeService()

    def generate_knowledge_id(self, created: datetime | None = None) -> str:
        timestamp = (created or datetime.now().astimezone()).astimezone()
        timestamp_part = timestamp.strftime("%Y%m%d-%H%M%S")
        suffix = uuid.uuid4().hex[:6]
        return f"knowledge-{timestamp_part}-{suffix}"

    def generate_timestamp(self) -> datetime:
        return datetime.now().astimezone()

    def generate_title(self, content: str) -> str:
        for line in content.splitlines():
            candidate = self._clean_title_candidate(line)
            if candidate:
                return self._limit_title(candidate)
        return "Untitled Memory"

    def create_metadata(
        self,
        content: str,
        *,
        title: str | None = None,
        knowledge_type: str | None = None,
        tags: Iterable[str] | None = None,
        source: str = "manual",
    ) -> KnowledgeMetadata:
        created = self.generate_timestamp()
        metadata = KnowledgeMetadata(
            id=self.generate_knowledge_id(created),
            title=title.strip() if title else self.generate_title(content),
            type=self._knowledge_type_service.validate_type(knowledge_type)
            if knowledge_type is not None
            else self._knowledge_type_service.default_type(),
            created=created,
            updated=created,
            tags=[tag.strip() for tag in (tags or []) if tag and tag.strip()],
            source=source.strip() if source.strip() else "manual",
            version=1,
        )
        self.validate_metadata(metadata)
        return metadata

    def update_metadata(
        self,
        metadata: KnowledgeMetadata,
        *,
        title: str | None = None,
        knowledge_type: str | None = None,
        tags: Iterable[str] | None = None,
        source: str | None = None,
    ) -> KnowledgeMetadata:
        updated_metadata = replace(
            metadata,
            title=title.strip() if title is not None else metadata.title,
            type=self._knowledge_type_service.validate_type(knowledge_type)
            if knowledge_type is not None
            else self._knowledge_type_service.validate_type(metadata.type),
            tags=[tag.strip() for tag in tags if tag and tag.strip()] if tags is not None else metadata.tags,
            source=(source.strip() if source is not None and source.strip() else metadata.source),
            updated=self.generate_timestamp(),
            version=metadata.version + 1,
        )
        self.validate_metadata(updated_metadata)
        return updated_metadata

    def validate_metadata(self, metadata: KnowledgeMetadata) -> None:
        if not metadata.id.strip():
            raise ValueError("Metadata id cannot be empty.")
        if not metadata.title.strip():
            raise ValueError("Metadata title cannot be empty.")
        if metadata.created.tzinfo is None or metadata.updated.tzinfo is None:
            raise ValueError("Metadata timestamps must be timezone-aware.")
        if metadata.updated < metadata.created:
            raise ValueError("Metadata updated timestamp cannot be earlier than created.")
        if metadata.version < 1:
            raise ValueError("Metadata version must be >= 1.")
        metadata.type = self._knowledge_type_service.validate_type(metadata.type)

    def build_markdown_document(self, content: str, metadata: KnowledgeMetadata) -> str:
        front_matter = self.serialize_front_matter(metadata)
        return f"{front_matter}\n\n{content}"

    def serialize_front_matter(self, metadata: KnowledgeMetadata) -> str:
        self.validate_metadata(metadata)
        lines = ["---"]
        lines.append(f'id: {self._quote_string(metadata.id)}')
        created_text = self._format_datetime(metadata.created)
        updated_text = self._format_datetime(metadata.updated)
        lines.append(f'created: {self._quote_string(created_text)}')
        lines.append(f'updated: {self._quote_string(updated_text)}')
        # Legacy aliases keep compatibility for downstream readers expecting old keys.
        lines.append(f'created_at: {self._quote_string(created_text)}')
        lines.append(f'updated_at: {self._quote_string(updated_text)}')
        lines.append(f'type: {self._quote_string(metadata.type)}')
        lines.append(f'title: {self._quote_string(metadata.title)}')
        lines.append(f"tags: {self._serialize_tags(metadata.tags)}")
        lines.append(f'source: {self._quote_string(metadata.source)}')
        lines.append(f'version: {metadata.version}')
        lines.append("---")
        return "\n".join(lines)

    def _clean_title_candidate(self, line: str) -> str:
        candidate = line.strip()
        if not candidate:
            return ""
        candidate = HEADING_PATTERN.sub("", candidate).strip()
        return candidate

    def _limit_title(self, title: str) -> str:
        if len(title) <= TITLE_LIMIT:
            return title
        shortened = title[: TITLE_LIMIT - 3].rstrip()
        if not shortened:
            return title[: TITLE_LIMIT - 3]
        return f"{shortened}..."

    def _format_datetime(self, value: datetime) -> str:
        return value.astimezone().isoformat(timespec="seconds")

    def _quote_string(self, value: str) -> str:
        return json.dumps(value, ensure_ascii=False)

    def _serialize_tags(self, tags: Iterable[str]) -> str:
        serialized_tags = [self._quote_string(tag) for tag in tags]
        return f"[{', '.join(serialized_tags)}]" if serialized_tags else "[]"
