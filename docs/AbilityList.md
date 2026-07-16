# Ability List

## Ability-0006 — Knowledge Metadata Foundation
- Ability ID: Ability-0006
- Name: Knowledge Metadata Foundation
- Purpose: Add structured, machine-readable metadata to newly saved knowledge records while keeping Markdown human-readable.
- Expected user value: Records become easier to organize, search, and evolve without changing the capture workflow.
- Main architectural layer: Service Layer
- Dependencies: Milestone 1 capture flow, Markdown storage, stable record save workflow
- Status: Completed

## Ability-0007 — Knowledge Types
- Ability ID: Ability-0007
- Name: Knowledge Types
- Purpose: Add an extensible type field for classifying knowledge records.
- Expected user value: Users can distinguish memories, notes, ideas, and other knowledge categories.
- Main architectural layer: Service Layer
- Dependencies: Ability-0006 Knowledge Metadata Foundation
- Status: Completed

## Ability-0008 — Tag System
- Ability ID: Ability-0008
- Name: Tag System
- Purpose: Introduce tags as lightweight metadata for knowledge organization.
- Expected user value: Users can group related knowledge across topics and projects.
- Main architectural layer: Service Layer
- Dependencies: Ability-0006 Knowledge Metadata Foundation, Ability-0007 Knowledge Types
- Status: In Progress

## Ability-0009 — Knowledge Index
- Ability ID: Ability-0009
- Name: Knowledge Index
- Purpose: Build a derived index over Markdown knowledge records.
- Expected user value: Faster browsing and preparation for search and relationships.
- Main architectural layer: Storage Layer
- Dependencies: Ability-0006 Knowledge Metadata Foundation, Ability-0008 Tag System
- Status: Planned

## Ability-0010 — Knowledge Search
- Ability ID: Ability-0010
- Name: Knowledge Search
- Purpose: Search knowledge records by metadata and content.
- Expected user value: Users can find stored knowledge quickly.
- Main architectural layer: Service Layer
- Dependencies: Ability-0009 Knowledge Index
- Status: Planned

## Ability-0011 — Knowledge Detail View
- Ability ID: Ability-0011
- Name: Knowledge Detail View
- Purpose: Show a single knowledge record with its metadata and content.
- Expected user value: Users can inspect and understand an individual record in context.
- Main architectural layer: Presentation Layer
- Dependencies: Ability-0006 Knowledge Metadata Foundation, Ability-0009 Knowledge Index
- Status: Planned

## Ability-0012 — Knowledge Linking
- Ability ID: Ability-0012
- Name: Knowledge Linking
- Purpose: Add explicit relationships between knowledge records.
- Expected user value: Users can connect related ideas and build a knowledge graph.
- Main architectural layer: Service Layer
- Dependencies: Ability-0009 Knowledge Index, Ability-0011 Knowledge Detail View
- Status: Planned

## Ability-0013 — Knowledge Browser
- Ability ID: Ability-0013
- Name: Knowledge Browser
- Purpose: Provide a dedicated browsing experience for structured knowledge.
- Expected user value: Users can navigate their knowledge base beyond recent captures.
- Main architectural layer: Presentation Layer
- Dependencies: Ability-0009 Knowledge Index, Ability-0010 Knowledge Search, Ability-0011 Knowledge Detail View, Ability-0012 Knowledge Linking
- Status: Planned
