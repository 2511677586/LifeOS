# Decision Log

## DL-001 — Markdown remains the canonical knowledge source
Decision: LifeOS knowledge records will continue to be stored as Markdown documents.
Rationale: Markdown remains human-readable, easy to inspect, and consistent with Milestone 1.

## DL-002 — YAML-style front matter for metadata
Decision: Metadata will initially be stored using YAML-style front matter at the top of each Markdown record.
Rationale: Front matter is readable by both humans and software and fits naturally into Markdown files.

## DL-003 — Stable unique knowledge IDs
Decision: Every knowledge record will receive a stable unique ID separate from the filename.
Rationale: Knowledge identity must survive renames and future storage changes.

## DL-004 — Derived indexes must be rebuildable
Decision: Search and browsing indexes are derived data and must be rebuildable from Markdown files.
Rationale: The Markdown files remain the source of truth and indexes should be disposable.

## DL-005 — SQLite is deferred
Decision: SQLite will not be introduced as the canonical store in Milestone 2 and remains a future option for indexing if justified.
Rationale: Milestone 2 should add metadata without introducing an unnecessary database dependency.

## DL-006 — Ability-0006 adds metadata without a database
Decision: Ability-0006 will introduce structured metadata generation and serialization without adding a full database layer.
Rationale: The smallest useful step is to make new records machine-readable while preserving the current save flow.

## DL-007 — Existing Markdown records remain readable
Decision: Existing Markdown files without front matter must continue to open in the recent records browser.
Rationale: The new metadata format must not break Milestone 1 records.

## DL-008 — No automatic migration in Ability-0006
Decision: Ability-0006 will not automatically rewrite or migrate existing records.
Rationale: Backward compatibility is required without changing user data unexpectedly.

## DL-009 — Knowledge types are centralized in a dedicated service
Decision: Ability-0007 introduces KnowledgeTypeService as the single service-layer source for supported knowledge types, normalization, validation, and default type selection.
Rationale: Centralizing type rules keeps metadata behavior consistent and avoids UI/storage coupling.
