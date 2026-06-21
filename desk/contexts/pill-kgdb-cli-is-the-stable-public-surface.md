---
id: pill-kgdb-cli-is-the-stable-public-surface
tags:
- workspace:desk
- artifact:pill
---

# kgdb CLI is the stable public surface

## What

_Define the context or guardrail this pill carries._

The kgdb command surface is the substrate's stable public API. Internal modules and storage backends can change; the CLI surface cannot change without versioning.

## Why

_Explain why this context matters for safe execution._

Downstream tools and humans script against the CLI. Surprise CLI breaks break them. A stable CLI is what lets the substrate be replaced or upgraded safely.

## When

_Describe when an agent should apply this pill._

Adding, renaming, or removing CLI commands or flags; changing command output formats.

## Where

_Name the files, surfaces, or scope this pill applies to._

Applies to kgdb/main.py, SV-1, TR-1, and every command listed in the CLI help.

## How

_Describe the correct way to apply this guidance._

Treat command names, flags, and output formats as a public API. Add commands freely; deprecate with --deprecated; never silently remove or rename.

## How Not

_Describe the shortcut or failure mode to avoid._

Do not change a flag's meaning silently; do not remove a command without a deprecation cycle; do not let internal refactors leak into the CLI surface.
