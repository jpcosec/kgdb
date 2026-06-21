---
id: pill-validation-findings-are-structured-not-crashes
tags:
- workspace:desk
- artifact:pill
---

# Validation findings are structured, not crashes

## What

_Define the context or guardrail this pill carries._

kgdb snapshot validate produces a structured ValidationResult with findings[], not a Python traceback, not an opaque exit code.

## Why

_Explain why this context matters for safe execution._

Downstream CI and humans need to react to specific violations; raw crashes hide the actual problem and break automation.

## When

_Describe when an agent should apply this pill._

Designing validation logic, especially for snapshots and provenance blocks.

## Where

_Name the files, surfaces, or scope this pill applies to._

Applies to SV-1, FR-5, FR-6, FR-7, FR-9, and the validate_snapshot() Python API.

## How

_Describe the correct way to apply this guidance._

Define ValidationResult with structured findings (id, severity, message, location). Emit findings, exit non-zero on any error finding, exit zero only on full success.

## How Not

_Describe the shortcut or failure mode to avoid._

Do not print a Python traceback as the diagnostic; do not exit non-zero without a structured diagnostic list; do not silently pass invalid snapshots.
