from __future__ import annotations

"""Knowledge relation type catalog.

Defines platform-standard relation types while keeping an extension-friendly
model for future domains and products.
"""

STANDARD_RELATION_TYPES: tuple[str, ...] = (
    "related_to",
    "belongs_to",
    "contains",
    "mentions",
    "created_by",
    "derived_from",
    "follows",
    "precedes",
    "occurred_at",
    "uses",
    "verified_by",
)

# Reserved examples for future product-level extension documentation.
RESERVED_EXTENSION_EXAMPLES: tuple[str, ...] = (
    "features",
    "located_in",
)

ALL_KNOWN_RELATION_TYPES: tuple[str, ...] = (
    *STANDARD_RELATION_TYPES,
    *RESERVED_EXTENSION_EXAMPLES,
)
