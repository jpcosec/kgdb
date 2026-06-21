---
id: pill-board-md-frontmatter-is-the-routing-truth
tags:
- workspace:desk
- artifact:pill
---

# Board.md frontmatter is the routing truth

## What

_Define the context or guardrail this pill carries._

The tasks: list in desk/tasks/Board.md frontmatter is the source of truth for active task routing. Pills: and rituals: are the same kind of truth for those artifacts.

## Why

_Explain why this context matters for safe execution._

If routing lives only in narrative Markdown, the desk becomes inconsistent; routing must be machine-readable so tooling can act on it without parsing free text.

## When

_Describe when an agent should apply this pill._

Adding or removing tasks, pills, or rituals; updating the active routing set.

## Where

_Name the files, surfaces, or scope this pill applies to._

desk/tasks/Board.md frontmatter; any tool or ritual that walks the active set.

## How

_Describe the correct way to apply this guidance._

Keep the frontmatter tasks/pills/rituals lists synchronized with the actual files. Treat the frontmatter as authoritative; treat the narrative as documentation.

## How Not

_Describe the shortcut or failure mode to avoid._

Do not reference tasks in narrative only; do not leave stale entries in the frontmatter; do not let a task exist on disk without being in the frontmatter (or vice versa).
