from __future__ import annotations

import os
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path

from app.repositories.knowledge_repository import KnowledgeRepository
from app.services.knowledge_query_service import KnowledgeQueryService
from app.services.storage_service import StorageService
from app.services.timeline_service import TimelineService


class TimelineServiceTests(unittest.TestCase):
    def setUp(self) -> None:
        self._temp_dir = tempfile.TemporaryDirectory()
        records_dir = Path(self._temp_dir.name)

        storage_service = StorageService(records_dir=records_dir)
        repository = KnowledgeRepository(storage_service=storage_service)
        query_service = KnowledgeQueryService(repository)
        self.service = TimelineService(query_service)

        self._write_record(
            "knowledge-001",
            (
                "---\n"
                "id: \"knowledge-001\"\n"
                "created: \"2026-07-10T10:00:00+00:00\"\n"
                "updated: \"2026-07-10T11:00:00+00:00\"\n"
                "occurred_at: \"2026-07-01T09:30:00+00:00\"\n"
                "---\n\n"
                "With occurred_at"
            ),
            mtime_utc="2026-07-20T00:00:00+00:00",
        )
        self._write_record(
            "knowledge-002",
            (
                "---\n"
                "id: \"knowledge-002\"\n"
                "created: \"2026-07-03T08:00:00+00:00\"\n"
                "updated: \"2026-07-03T09:00:00+00:00\"\n"
                "---\n\n"
                "No occurred_at"
            ),
            mtime_utc="2026-07-20T00:00:00+00:00",
        )
        self._write_record(
            "knowledge-003",
            "Legacy without front matter",
            mtime_utc="2026-07-05T06:00:00+00:00",
        )
        self._write_record(
            "knowledge-004",
            (
                "---\n"
                "id: \"knowledge-004\"\n"
                "created: \"2026-08-02T00:00:00+00:00\"\n"
                "updated: \"2026-08-02T00:30:00+00:00\"\n"
                "---\n\n"
                "August record"
            ),
            mtime_utc="2026-08-02T00:00:00+00:00",
        )

    def tearDown(self) -> None:
        self._temp_dir.cleanup()

    def test_valid_iso_datetime_normalization(self) -> None:
        value = self.service.normalize_datetime("2026-07-18T08:00:00+08:00")
        self.assertEqual(value, datetime(2026, 7, 18, 0, 0, tzinfo=timezone.utc))

    def test_invalid_datetime_handling(self) -> None:
        with self.assertRaises(ValueError):
            self.service.normalize_datetime("invalid-date")

    def test_occurred_at_precedence(self) -> None:
        record = self._get_record("knowledge-001")
        occurred = self.service.resolve_occurred_at(record)
        self.assertEqual(occurred, datetime(2026, 7, 1, 9, 30, tzinfo=timezone.utc))

    def test_fallback_to_created_time(self) -> None:
        record = self._get_record("knowledge-002")
        occurred = self.service.resolve_occurred_at(record)
        self.assertEqual(occurred, datetime(2026, 7, 3, 8, 0, tzinfo=timezone.utc))

    def test_compatibility_with_missing_occurred_at(self) -> None:
        record = self._get_record("knowledge-003")
        occurred = self.service.resolve_occurred_at(record)
        self.assertEqual(occurred, datetime(2026, 7, 5, 6, 0, tzinfo=timezone.utc))

    def test_chronological_sorting(self) -> None:
        sorted_records = self.service.sort_chronologically()
        self.assertEqual([record.path.stem for record in sorted_records[:3]], ["knowledge-001", "knowledge-002", "knowledge-003"])

    def test_reverse_chronological_sorting(self) -> None:
        sorted_records = self.service.sort_chronologically(descending=True)
        self.assertEqual(sorted_records[0].path.stem, "knowledge-004")

    def test_filtering_by_time_range(self) -> None:
        start = datetime(2026, 7, 2, 0, 0, tzinfo=timezone.utc)
        end = datetime(2026, 7, 31, 0, 0, tzinfo=timezone.utc)
        records = self.service.filter_by_time_range(start, end)
        self.assertEqual({record.path.stem for record in records}, {"knowledge-002", "knowledge-003"})

    def test_grouping_by_day(self) -> None:
        grouped = self.service.group_by_day()
        self.assertIn("2026-07-03", grouped)
        self.assertEqual({record.path.stem for record in grouped["2026-07-03"]}, {"knowledge-002"})

    def test_grouping_by_month(self) -> None:
        grouped = self.service.group_by_month()
        self.assertIn("2026-07", grouped)
        july_records = {record.path.stem for record in grouped["2026-07"]}
        self.assertTrue({"knowledge-001", "knowledge-002", "knowledge-003"}.issubset(july_records))

    def test_grouping_by_year(self) -> None:
        grouped = self.service.group_by_year()
        self.assertIn("2026", grouped)
        self.assertEqual(len(grouped["2026"]), 4)

    def _write_record(self, record_id: str, content: str, *, mtime_utc: str) -> None:
        path = Path(self._temp_dir.name) / f"{record_id}.md"
        path.write_text(content, encoding="utf-8")
        timestamp = datetime.fromisoformat(mtime_utc).timestamp()
        os.utime(path, (timestamp, timestamp))

    def _get_record(self, record_id: str):
        for record in self.service.sort_chronologically():
            if record.path.stem == record_id:
                return record
        raise AssertionError(f"Record not found in fixture: {record_id}")


if __name__ == "__main__":
    unittest.main()
