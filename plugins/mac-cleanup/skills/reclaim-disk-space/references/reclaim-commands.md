<!-- verified against macOS 26.3 (build 25D125) · Apple Silicon (arm64) · 2026-07-17 — re-verify on a major macOS update -->

# Reclaim commands — exact, argv-safe recipes for Phase 2

Loaded before you execute a Phase 2 batch. Every recipe here is still bound by the **Absolute
safety rules** in `SKILL.md`: explicit per-batch approval (rule 1), Trash-first for files (rule 2),
quote/guard every path (rule 3), PERMANENT actions labeled and separately approved (rule 6), owning
app quit for file-level caches / daemon up for Docker (rule 9). **Show the exact command before
running it.**

---

## A. Trash-first file/folder removal (the default — reversible)

Never `rm`, never `mv` to `~/.Trash`. Use one of these, passing the path as an **argument** so
spaces / quotes / apostrophes can't break the command:

**Preferred — the `trash` CLI** (if `command -v trash` succeeds):
```bash
trash "/absolute/path/to/item"
```

**Fallback — Finder via `osascript`, path passed as argv** (never string-interpolated):
```bash
osascript - "/absolute/path/to/item" <<'OSA'
on run argv
  set p to POSIX file (item 1 of argv)
  tell application "Finder" to delete p
end run
OSA
```

**After every Trash op, confirm it moved** before reporting success:
```bash
test ! -e "/absolute/path/to/item" && echo "moved to Trash OK" || echo "STILL PRESENT — STOP"
```
If Trashing errors or is permission-denied, it needs **Automation / Apple-events** permission —
**STOP and report "needs Automation permission."** A failed Trash attempt is **never** license to
fall back to `rm`.

> Trashed items still occupy disk until the Trash is emptied — report them as "moved to Trash
> (pending)", separate from bytes actually freed. Emptying is the dedicated final batch (§H).

---

## B. Homebrew — PERMANENT
```bash
brew cleanup -n     # preview what would be removed (this is the Phase-1-safe form)
brew cleanup        # PERMANENT — after approval
du -sh "$(brew --cache)" 2>/dev/null   # size the downloads cache
```

## C. Docker — PERMANENT (daemon must be RUNNING; do not quit it)
```bash
docker ps -a                # show stopped containers FIRST — warn their data can be the only copy
docker system df            # size reclaimable
docker image prune          # dangling images only
docker builder prune        # build cache
```
**Never** `docker system prune -a` or `--volumes` unless the user explicitly asks (that deletes
tagged images / named volumes = potential live data).

## D. Xcode simulators — PERMANENT
```bash
xcrun simctl delete unavailable          # stale/unavailable devices
xcrun simctl runtime list                # find unused runtime IDs (may provision components once)
xcrun simctl runtime delete <RUNTIME_ID> # remove a specific unused runtime
```
Guard on `xcode-select -p` first. Quit the Simulator app before deleting devices (rule 9).

## E. pnpm store — PERMANENT
```bash
pnpm config get store-dir   # resolve store (avoids the Corepack-download side effect of `store path`)
pnpm store prune            # remove unreferenced packages
```

## F. Go module cache — PERMANENT (files are read-only; plain rm fails)
```bash
go env GOMODCACHE           # resolve the cache location
go clean -modcache          # the correct way to reclaim it
```

## G. Time Machine local snapshots — PERMANENT (no sudo)
```bash
tmutil listlocalsnapshots /                       # list; names look like com.apple.TimeMachine.<date>
tmutil deletelocalsnapshots <YYYY-MM-DD-HHMMSS>   # delete one by its date stamp
```
`tmutil thinlocalsnapshots` needs sudo → **out of scope.** After deletion, freed bytes may lag in
`df`; re-list snapshots to confirm.

---

## H. Empty the Trash — PERMANENT, and always the FINAL, SEPARATE batch

This is the action that actually frees Trashed space, and it finalizes everything trashed this
session — so it is **never** an early/"lowest-risk" batch. Do it last, on its own explicit yes.

```bash
du -sh ~/.Trash 2>/dev/null                 # size home Trash
du -sh /Volumes/*/.Trashes 2>/dev/null      # external-drive Trashes — flag items with no backup
```
List the largest items first, warn that emptying is unrecoverable, get a **separate explicit yes**,
then empty via Finder (argv-safe, no `rm`):
```bash
osascript -e 'tell application "Finder" to empty trash'
```
Then re-run `df -H /System/Volumes/Data` and report the space **truly** freed.

---

## Post-batch reporting
After each executed batch: report freed space from the **Data volume** (`df -H
/System/Volumes/Data`), note Trashed items are pending until §H. If `df` shows less freed than
expected, check `tmutil listlocalsnapshots /` — the bytes may be **snapshot-pinned**, not the
removal failing. Then **stop and wait** for the next instruction (rule 1).
