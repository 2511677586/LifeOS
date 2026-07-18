from __future__ import annotations

"""Knowledge type catalog for LifeOS Knowledge Objects.

The catalog defines platform-standard types and reserved extension examples.
All values are stored as lowercase canonical keys for stable metadata and query
behavior.
"""

STANDARD_KNOWLEDGE_TYPES: tuple[str, ...] = (
    "journal",
    "idea",
    "meeting",
    "project",
    "document",
    "photo",
    "video",
    "conversation",
    "book",
    "article",
    "person",
    "place",
    "event",
)

MINESYSTEM_EXTENSION_TYPES: tuple[str, ...] = (
    "shipment",
    "inspection",
    "laboratoryreport",
    "vehicle",
    "container",
)

ICE_STUDIO_EXTENSION_TYPES: tuple[str, ...] = (
    "character",
    "world",
    "story",
    "scene",
    "dialogue",
)

# Legacy aliases keep existing Markdown records readable.
LEGACY_TYPE_ALIASES: dict[str, str] = {
    "memory": "journal",
    "reference": "document",
    "note": "document",
    "decision": "meeting",
}

ALL_SUPPORTED_TYPES: tuple[str, ...] = (
    *STANDARD_KNOWLEDGE_TYPES,
    *MINESYSTEM_EXTENSION_TYPES,
    *ICE_STUDIO_EXTENSION_TYPES,
)
