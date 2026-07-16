from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(slots=True)
class StoredRecord:
    path: Path
    content: str


class StorageService:
    def __init__(self, records_dir: Path | None = None) -> None:
        self._records_dir = records_dir or Path(__file__).resolve().parents[2] / "data" / "records"

    def save_markdown(self, record_id: str, document: str) -> Path:
        self._records_dir.mkdir(parents=True, exist_ok=True)
        path = self._records_dir / f"{record_id}.md"
        path.write_text(document, encoding="utf-8", newline="\n")
        return path

    def list_recent_records(self, limit: int = 20) -> list[StoredRecord]:
        if not self._records_dir.exists():
            return []
        markdown_files = [path for path in self._records_dir.glob("*.md") if path.is_file()]
        markdown_files.sort(key=lambda path: path.stat().st_mtime, reverse=True)
        recent_files = markdown_files[:limit]
        return [StoredRecord(path=path, content=path.read_text(encoding="utf-8")) for path in recent_files]

    def read_markdown(self, path: Path) -> str:
        return path.read_text(encoding="utf-8")

    def record_exists(self, record_id: str) -> bool:
        return (self._records_dir / f"{record_id}.md").exists()
