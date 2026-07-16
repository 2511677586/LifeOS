# Development Workflow

## 1. Purpose

LifeOS requires a unified workflow so product intent, architecture decisions, implementation quality, and delivery cadence stay aligned.

A single official workflow helps the team:
- Reduce ambiguity in responsibilities.
- Keep milestones and abilities delivered in a predictable order.
- Prevent architecture drift and scope creep.
- Ensure documentation and implementation remain consistent.

## 2. Team Roles

### Founder
- Defines product vision, milestones, priorities, and acceptance direction.
- Approves milestone scope and ability sequencing.
- Makes final product trade-off decisions.

### Chief Architect
- Designs and guards the system architecture and layering boundaries.
- Defines ability-level technical direction and constraints.
- Reviews architectural impact and long-term maintainability.

### Software Engineer (Copilot)
- Implements approved abilities according to architecture and documented constraints.
- Runs tests, fixes regressions, and verifies behavior before completion.
- Updates required documentation and executes Git commit/push workflow after completion.

Responsibility boundaries:
- Founder decides what and why.
- Chief Architect decides how at the system design level.
- Software Engineer (Copilot) executes implementation and verification within approved boundaries.

## 3. Development Lifecycle

Official lifecycle:

Idea
↓
Architecture
↓
Ability Planning
↓
Implementation
↓
Testing
↓
Documentation
↓
Git Commit
↓
Git Push

Stage purpose:
- Idea: Define user value and expected outcome.
- Architecture: Define system-level approach and constraints.
- Ability Planning: Break milestone work into sequenced, testable abilities.
- Implementation: Deliver the approved ability without scope expansion.
- Testing: Validate correctness, regression safety, and quality requirements.
- Documentation: Synchronize architecture and project records with delivered behavior.
- Git Commit: Create a clear, auditable checkpoint for the completed ability.
- Git Push: Publish validated work to shared remote history.

## 4. Git Workflow

Current Git strategy:
- Main branch: `main`
- Commit after each completed Ability.
- Push only after successful testing and documentation updates.
- No direct history rewriting on shared history.

Operational rules:
- Keep commits focused and ability-scoped.
- Avoid force push and rebasing shared published history.
- Preserve traceable milestone progression through commit history.

## 5. Commit Convention

Use conventional commit prefixes to clarify change intent:
- `feat:` new user-facing capability or behavior.
- `fix:` bug fix or regression correction.
- `docs:` documentation updates only.
- `test:` test additions or test maintenance.
- `refactor:` internal restructuring without behavior change.
- `chore:` tooling, maintenance, or non-functional updates.

Examples:
- `feat: add knowledge metadata foundation`
- `fix: prevent empty memory save from bypassing validation`
- `docs: add official development workflow`
- `test: cover metadata front matter serialization`
- `refactor: split metadata generation into dedicated service`
- `chore: update local development scripts`

## 6. Ability Development Rules

- One Ability = One Goal.
- One Ability = One Primary Commit.
- Complete the current Ability before moving to the next Ability.
- No Scope Creep.

Interpretation:
- A single ability should produce one clear functional outcome.
- Related support commits are acceptable during work, but delivery should land as one primary completion commit.
- Future ability work must not be mixed into the current ability implementation.

## 7. Documentation Rules

After completing an Ability, update the following documents:
- [Architecture.md](Architecture.md): Reflect current and planned architecture boundaries and component relationships.
- [Roadmap.md](Roadmap.md): Reflect milestone order, current ability, and next planned ability.
- [AbilityList.md](AbilityList.md): Reflect ability status, dependencies, and value statements.
- [DecisionLog.md](DecisionLog.md): Record architectural decisions actually made during implementation.
- [CHANGELOG.md](../CHANGELOG.md): Record delivered, user-visible or engineering-significant changes.

Documentation principles:
- Update docs in the same delivery cycle as implementation.
- Ensure docs describe actual behavior, not aspirational behavior.
- Avoid undocumented architectural decisions.

## 8. Quality Rules

Project quality principles:
- Bug count must be zero.
- Preserve architecture layers.
- Business logic belongs in services.
- Markdown remains the canonical knowledge source.
- Documentation must match implementation.

Enforcement guidance:
- Do not bypass service boundaries from UI.
- Do not weaken backward compatibility unless explicitly approved.
- Resolve regressions before ability completion.

## 9. Copilot Collaboration Rules

Copilot must:
- Follow the Architecture.
- Respect Ability boundaries.
- Do not introduce unrelated features.
- Preserve backward compatibility.
- Test before completion.
- Stop after the assigned Ability.

Execution guidance:
- Keep changes minimal, modular, and traceable.
- Prioritize implementation correctness over speculative enhancements.
- If blocked by missing environment prerequisites, report clearly and stop.

## 10. Future Expansion

The following topics are reserved for future formalization:
- Release Workflow
- Branch Strategy
- Code Review
- CI/CD

These topics are intentionally not defined in detail in this document yet.
