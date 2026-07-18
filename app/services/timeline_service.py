from __future__ import annotations

from collections import defaultdict
from datetime import datetime, timezone
import json
from pathlib import Path

from app.services.knowledge_query_service import KnowledgeQueryService
from app.services.storage_service import StoredRecord


class TimelineService:
    """Timeline foundation for temporal retrieval over Knowledge Objects.

    This service is read-oriented and depends on KnowledgeQueryService for
    record access. It does not interact with StorageService directly and does
    not include UI responsibilities.

    Fallback precedence for resolved event time:
    occurred_at -> created -> created_at -> file timestamp

    TODO: Add repository-backed timeline indexing only after Markdown-compatible
    timeline persistence rules are finalized.
    """

    def __init__(self, knowledge_query_service: KnowledgeQueryService) -> None:
        self._knowledge_query_service = knowledge_query_service

    def normalize_datetime(self, value: str | datetime) -> datetime:
        """Normalize ISO 8601 datetime values into timezone-aware UTC datetimes."""
        parsed: datetime
        if isinstance(value, datetime):
            parsed = value
        elif isinstance(value, str):
            try:
                parsed = datetime.fromisoformat(value)
            except ValueError as exc:
                raise ValueError(f"Invalid datetime value: {value}") from exc
        else:
            raise ValueError(f"Unsupported datetime value type: {type(value)!r}")

        if parsed.tzinfo is None:
            raise ValueError("Naive datetime values are not allowed. Use timezone-aware ISO 8601 values.")
        return parsed.astimezone(timezone.utc)

    def resolve_occurred_at(self, record: StoredRecord) -> datetime:
        """Resolve canonical event time for a record using compatibility fallbacks."""
        metadata = self._parse_front_matter(record.content)
        for key in ("occurred_at", "created", "created_at"):
            raw_value = metadata.get(key)
            if isinstance(raw_value, str) and raw_value.strip():
                return self.normalize_datetime(raw_value)

        # Safe fallback: file timestamp is available from repository-backed path.
        modified_at = datetime.fromtimestamp(record.path.stat().st_mtime, tz=timezone.utc)
        return modified_at

    def sort_chronologically(
        self,
        records: list[StoredRecord] | None = None,
        *,
        descending: bool = False,
    ) -> list[StoredRecord]:
        """Sort records by resolved occurred_at semantics."""
        resolved = self._resolve_records(records)
        return sorted(resolved, key=self.resolve_occurred_at, reverse=descending)

    def filter_by_time_range(
        self,
        start: datetime,
        end: datetime,
        records: list[StoredRecord] | None = None,
    ) -> list[StoredRecord]:
        """Filter records whose resolved occurred_at falls within [start, end]."""
        start_utc = self.normalize_datetime(start)
        end_utc = self.normalize_datetime(end)
        if end_utc < start_utc:
            return []

        filtered: list[StoredRecord] = []
        for record in self._resolve_records(records):
            occurred = self.resolve_occurred_at(record)
            if start_utc <= occurred <= end_utc:
                filtered.append(record)
        return filtered

    def group_by_day(self, records: list[StoredRecord] | None = None) -> dict[str, list[StoredRecord]]:
        """Group records by UTC calendar day (YYYY-MM-DD)."""
        groups: dict[str, list[StoredRecord]] = defaultdict(list)
        for record in self.sort_chronologically(records):
            key = self.resolve_occurred_at(record).strftime("%Y-%m-%d")
            groups[key].append(record)
        return dict(groups)

    def group_by_month(self, records: list[StoredRecord] | None = None) -> dict[str, list[StoredRecord]]:
        """Group records by UTC calendar month (YYYY-MM)."""
        groups: dict[str, list[StoredRecord]] = defaultdict(list)
        for record in self.sort_chronologically(records):
            key = self.resolve_occurred_at(record).strftime("%Y-%m")
            groups[key].append(record)
        return dict(groups)

    def group_by_year(self, records: list[StoredRecord] | None = None) -> dict[str, list[StoredRecord]]:
        """Group records by UTC calendar year (YYYY)."""
        groups: dict[str, list[StoredRecord]] = defaultdict(list)
        for record in self.sort_chronologically(records):
            key = self.resolve_occurred_at(record).strftime("%Y")
            groups[key].append(record)
        return dict(groups)

    def _resolve_records(self, records: list[StoredRecord] | None) -> list[StoredRecord]:
        if records is None:
            return self._knowledge_query_service.list_all()
        return records

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
            metadata[key.strip()] = self._parse_scalar(raw_value.strip())
        return metadata

    def _parse_scalar(self, value: str) -> object:
        if not value:
            return ""
        if value.startswith('"') and value.endswith('"'):
            try:
                return json.loads(value)
            except json.JSONDecodeError:
                return value.strip('"')
        return value
