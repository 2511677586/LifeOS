# Architecture

## Milestone 1 — Memory Foundation Architecture

LifeOS currently uses a three-layer separation:

### Presentation Layer
- Tkinter UI
- Multiline text capture view
- Save button
- Recent records browser

### Service Layer
- Capture Service
- Validation and save orchestration

### Storage Layer
- Markdown files on disk

Current responsibilities are kept separate so the UI does not write files directly and the storage layer remains replaceable.

## Milestone 2 — Knowledge Foundation Architecture

Milestone 2 expands LifeOS from simple memory capture into the foundation of a structured personal knowledge system.

### Presentation Layer
- Capture View
- Recent Records Browser
- Future Knowledge Browser
- Future Search Interface
- Future Knowledge Detail View

### Service Layer
- Capture Service
- Knowledge Service
- Knowledge Query Service
- Metadata Service
- KnowledgeTypeService
- KnowledgeRelationService
- TimelineService
- Future Index Service
- Future Search Service
- Future Linking Service

### Storage Layer
- Markdown documents
- Structured Markdown front matter
- Future JSON index
- Future SQLite index

### Knowledge Layer Transition

The Knowledge Foundation introduces `KnowledgeService` as the unified entry
point for knowledge operations.

Current runtime path (Milestone 1 baseline):

```text
UI -> Capture Service -> Storage Service -> Markdown
```

Target Knowledge Layer path (Milestone 2 architecture):

```text
UI -> Knowledge Service -> Knowledge Query Service -> Knowledge Repository -> Storage Service -> Markdown
```

`KnowledgeService` centralizes knowledge-level orchestration while preserving
the existing Markdown file format and storage behavior.

### Query Layer

`KnowledgeQueryService` is the read-oriented query boundary for Knowledge
Objects.

- Uses `KnowledgeRepository` only
- Retrieves records by id and list operations
- Applies metadata-based filtering (type, tag, date range)
- Preserves compatibility with legacy Markdown without front matter

### Repository Layer

`KnowledgeRepository` is the persistence boundary for Knowledge Objects.

- Receives persistence requests from `KnowledgeService`
- Delegates file operations to `StorageService`
- Preserves compatibility with existing Markdown files
- Keeps persistence logic out of the service orchestration layer

### Metadata Layer

`MetadataService` defines and manages the standard metadata envelope used by
Knowledge Objects:

- id
- title
- type
- created
- updated
- tags
- source
- version

Metadata is generated and validated in the service layer, then serialized into
Markdown front matter to keep records human-readable and machine-readable.
For backward compatibility, front matter continues to include legacy
`created_at` and `updated_at` aliases.

### Knowledge Type System

`KnowledgeTypeService` validates and canonicalizes metadata type values based on
the shared catalog in `models/knowledge_types.py`.

Standard types:

- journal
- idea
- meeting
- project
- document
- photo
- video
- conversation
- book
- article
- person
- place
- event

Reserved extension examples:

- MineSystem: shipment, inspection, laboratoryreport, vehicle, container
- ICE Studio: character, world, story, scene, dialogue

Compatibility rule:

- Unknown or legacy types remain readable.
- Validation emits a clear warning instead of breaking existing records.
- Legacy aliases are canonicalized where applicable (for example, `memory` -> `journal`).

### Relation Layer

`KnowledgeRelationService` provides platform-oriented relation modeling between
stable Knowledge IDs.

Core relation model:

- source_id
- relation_type
- target_id
- metadata (optional, extensible)

Standard relation types:

- related_to
- belongs_to
- contains
- mentions
- created_by
- derived_from
- follows
- precedes
- occurred_at
- uses
- verified_by

Compatibility and integrity rules:

- Empty source_id and target_id are rejected.
- Referenced objects are not required to exist at creation time.
- Referential integrity is deferred to future repository integration.
- Unknown relation types remain readable and produce a clear validation warning.

Persistence boundary:

- Relation business logic stays in `KnowledgeRelationService`.
- UI and `StorageService` do not own relation business logic.
- TODO: Persist relations through a dedicated relation repository once Markdown
    relation storage format is finalized.

Platform-oriented examples (architecture reuse):

- LifeOS: Journal mentions Person; Event occurred_at Place; Note belongs_to Project
- MineSystem: Shipment uses Vehicle; Shipment contains Container; Shipment verified_by Inspection
- ICE Studio: Scene features Character; Scene located_in World; Scene follows Scene

### Time Model

`KnowledgeTime` defines temporal semantics for Knowledge Objects:

- created_at: object creation time in LifeOS
- updated_at: last modification time in LifeOS
- occurred_at: represented real-world event time
- optional future-compatible fields: ended_at, timezone, precision, source

These timestamps are not interchangeable and must be interpreted by their
separate semantics.

Backward compatibility behavior:

- Existing Markdown may omit occurred_at.
- Timeline resolution fallback order is:
    occurred_at -> created -> created_at -> file timestamp
- Unknown time metadata is preserved as-is.
- Historical Markdown files are not rewritten automatically.

### Timeline Service

`TimelineService` provides temporal normalization and grouping logic while
staying within service boundaries:

- Uses `KnowledgeQueryService` for record retrieval
- Does not access `StorageService` directly
- Uses ISO 8601-compatible, timezone-aware datetime handling
- Rejects invalid or naive datetime values with clear validation behavior

Future foundation support (architecture reuse):

- LifeOS: journals, photos, conversations, travel events, personal milestones
- MineSystem: departure time, arrival time, loading completion time, return-to-port time
- ICE Studio: fictional chronology, scene order, world history, character events

Long-term direction:

- Future Life Timeline views can reuse this service layer.
- Future Life Map features can consume normalized occurred_at semantics without
    changing the core model.

### Architecture Diagram

```mermaid
graph TD
    UI[Presentation Layer] --> CV[Capture View]
    UI --> RB[Recent Records Browser]
    UI --> KB[Future Knowledge Browser]
    UI --> SI[Future Search Interface]
    UI --> DV[Future Knowledge Detail View]

    CV --> CS[Capture Service]
    RB --> CS
    KB --> KS[Knowledge Service]
    SI --> SS[Future Search Service]
    DV --> LS[Future Linking Service]

    CS --> MS[Metadata Service]
    MS --> KTS[KnowledgeTypeService]
    KS --> KRS[KnowledgeRelationService]
    KS --> KQS[Knowledge Query Service]
    KS --> TLS[TimelineService]
    TLS --> KQS
    KQS --> KR[Knowledge Repository]
    KS --> MS
    KS --> KTS
    MS --> SD[Structured Markdown Front Matter]
    CS --> MD[Markdown Documents]
    KR --> ST[Storage Service]
    ST --> MD
    SS --> IX[Future Index Service]
    LS --> IX

    MD --> FS[(Filesystem)]
    IX --> JI[Future JSON Index]
    IX --> SQ[Future SQLite Index]
```

### Architectural Rules
- Markdown remains the canonical source of truth.
- Metadata must be readable by both humans and software.
- SQLite must not become the canonical content store.
- Search indexes must be rebuildable from Markdown files.
- UI code must not directly read or write Markdown files.
- Knowledge IDs must remain stable.
- Knowledge type values must be validated through the service layer.
- Future AI functionality must consume the service layer rather than directly accessing the UI or storage layer.
- Existing Memory Foundation behavior must remain intact while the knowledge layer is added.
