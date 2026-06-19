# KGDB Tasks Board

## Current State Summary

- Objective: make `kgdb` a real graph persistence/query substrate
- Current blocker: substrate role is conceptually clear but operationally underspecified

## Delivery Phases

### Phase 1 - Define the substrate contract
- `desk/tasks/001-define-graph-io-contract.md`
- `desk/tasks/002-define-persistence-model.md`

### Phase 2 - Prove ingest and query
- `desk/tasks/003-implement-minimal-ingest.md`
- `desk/tasks/004-implement-minimal-query.md`

### Phase 3 - Prove downstream use
- `desk/tasks/005-create-substrate-fixture.md`
- `desk/tasks/006-prove-downstream-consumer-contract.md`

### Phase 4 - Stress-Test Corrections *(closed)*
- `desk/tasks/007-fix-load_graph-graphsnapshot-format.md` ✓
- `desk/tasks/008-add-user-friendly-error-messages.md` ✓
- `desk/tasks/009-add-ingest-input-validation.md` ✓
- `desk/tasks/010-fix-utf8-output-and-exit-code-consistency.md` ✓
- `desk/tasks/011-improve-cli-discoverability.md` ✓

## Active

| ID | Domain | Task | Priority | Depends On |
|----|--------|------|----------|------------|
| 001 | contract | Define graph IO contract | p0 | none |
| 002 | persistence | Define persistence model | p0 | 001 |
| 003 | ingest | Implement minimal ingest | p1 | 001, 002 |
| 004 | query | Implement minimal query | p1 | 001, 002 |
| 005 | fixtures | Create substrate fixture | p1 | 001, 002 |
| 006 | integration | Prove downstream consumer contract | p1 | 003, 004, 005 |

## Blocked

| ID | Domain | Task | Priority | Depends On |
|----|--------|------|----------|------------|
| - | - | none | - | - |

## Working Rules

1. Start from `desk/SPEC.md`.
2. Define contracts before implementation.
3. Prove each phase with fixtures before advancing.
