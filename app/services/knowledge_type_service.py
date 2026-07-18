from __future__ import annotations

import warnings

from app.models.knowledge_types import ALL_SUPPORTED_TYPES, LEGACY_TYPE_ALIASES


class KnowledgeTypeService:
    _SUPPORTED_TYPES: tuple[str, ...] = ALL_SUPPORTED_TYPES

    def list_supported_types(self) -> tuple[str, ...]:
        return self._SUPPORTED_TYPES

    def default_type(self) -> str:
        return "journal"

    def normalize_type(self, value: str) -> str:
        return value.strip().lower()

    def canonicalize_type(self, value: str) -> str:
        normalized = self.normalize_type(value)
        return LEGACY_TYPE_ALIASES.get(normalized, normalized)

    def is_supported_type(self, value: str) -> bool:
        normalized = self.canonicalize_type(value)
        return normalized in self._SUPPORTED_TYPES

    def validate_type(self, value: str) -> str:
        normalized = self.canonicalize_type(value)
        if normalized not in self._SUPPORTED_TYPES:
            supported = ", ".join(self._SUPPORTED_TYPES)
            warnings.warn(
                (
                    f"Unsupported knowledge type '{value}'. "
                    "Record remains readable for backward compatibility. "
                    f"Supported types: {supported}"
                ),
                UserWarning,
                stacklevel=2,
            )
        return normalized
