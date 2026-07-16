from __future__ import annotations


class KnowledgeTypeService:
    _SUPPORTED_TYPES: tuple[str, ...] = (
        "memory",
        "idea",
        "project",
        "person",
        "event",
        "decision",
        "reference",
        "note",
    )

    def list_supported_types(self) -> tuple[str, ...]:
        return self._SUPPORTED_TYPES

    def default_type(self) -> str:
        return "memory"

    def normalize_type(self, value: str) -> str:
        return value.strip().lower()

    def is_supported_type(self, value: str) -> bool:
        normalized = self.normalize_type(value)
        return normalized in self._SUPPORTED_TYPES

    def validate_type(self, value: str) -> str:
        normalized = self.normalize_type(value)
        if normalized not in self._SUPPORTED_TYPES:
            supported = ", ".join(self._SUPPORTED_TYPES)
            raise ValueError(f"Unsupported knowledge type: {value}. Supported types: {supported}")
        return normalized
