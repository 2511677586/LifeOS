from __future__ import annotations

import json
import re
import uuid
from datetime import datetime
from typing import Iterable

from app.models.knowledge_metadata import KnowledgeMetadata

TITLE_LIMIT = 60
HEADING_PATTERN = re.compile(r"^#{1,6}\s*")


class MetadataService:
    def generate_knowledge_id(self, created_at: datetime | None = None) -> str:
        timestamp = (created_at or datetime.now().astimezone()).astimezone()
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

    def create_metadata(self, content: str) -> KnowledgeMetadata:
        created_at = self.generate_timestamp()
        return KnowledgeMetadata(
            id=self.generate_knowledge_id(created_at),
            created_at=created_at,
            updated_at=created_at,
            type="memory",
            title=self.generate_title(content),
            tags=[],
            source="manual",
            version=1,
        )

    def build_markdown_document(self, content: str, metadata: KnowledgeMetadata) -> str:
        front_matter = self.serialize_front_matter(metadata)
        return f"{front_matter}\n\n{content}"

    def serialize_front_matter(self, metadata: KnowledgeMetadata) -> str:
        lines = ["---"]
        lines.append(f'id: {self._quote_string(metadata.id)}')
        lines.append(f'created_at: {self._quote_string(self._format_datetime(metadata.created_at))}')
        lines.append(f'updated_at: {self._quote_string(self._format_datetime(metadata.updated_at))}')
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
