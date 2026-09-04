# Phase ritual

When all tasks in the current active layer are closed, run [closeout](closeout.md) for each, then update the board to surface the next dependency layer.

## Steps

1. Confirm all active tasks have been closed via the closeout ritual.
2. Update `desk/tasks/Board.md` — promote deferred tasks from drawer if they are now unblocked.
3. Update `desk/atoms/atom-kgdb.md` if the phase changed kgdb contracts, capabilities, or architecture.
4. Commit with message: `ritual: phase <name> - <summary>`.
5. Reflect on what should go into drawer (deferred) or inbox (suggestions for deskops/sldb).