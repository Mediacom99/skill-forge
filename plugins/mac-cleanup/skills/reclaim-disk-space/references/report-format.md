<!-- verified against macOS 26.3 (build 25D125) · Apple Silicon (arm64) · 2026-07-17 — re-verify on a major macOS update -->

# Report format — the only output of Phase 1

Loaded when you produce the Phase 1 report. Keep it **scannable** — this is what the user decides
from. List **every** measured candidate above the ~100 MB floor; **do not truncate or summarize
rows to save space** — a long report is expected.

## 1. Disk state (all mounted, writable volumes — not just `/`)

On APFS, `/` is the **sealed system volume** and its used% is meaningless (it reads ~12 GB). Take
**used / %** from the **Data volume** (`/System/Volumes/Data`), and **free / available** from the
shared container. Say which volume each number came from. Include each volume's `.Trashes` size and
current snapshot bytes (from `tmutil listlocalsnapshots /`). Report **purgeable** only as a clearly
labeled **estimate** (e.g. container-free vs `df` delta), never a hard number.

Commands: `df -H /System/Volumes/Data /` · `tmutil listlocalsnapshots /`

## 2. Candidate rows, grouped by tier, sorted by GB reclaimable (largest first)

One row each:

```
[size] — [path] — [what it is] — [regenerable | irreplaceable] — [reversible (Trash) | PERMANENT] — [how to reclaim] — [risk: low/med/high]
```

## 3. Closing summary

- **Per-tier totals** and a **grand total** of *realistically* reclaimable space.
- A separate **"looks big but ISN'T truly reclaimable"** line — snapshots, purgeable estimate, iCloud stubs, VM/container images (report-only).
- A **"couldn't read — needs Full Disk Access"** list (rule 10 — never call these "empty").
- A **reconciliation line:** `total used − (reclaimable + kept-irreplaceable + system/other users + snapshots/purgeable)` so any large unexplained remainder is visible.

---

## Worked example (illustrative — real numbers will differ)

> **Disk state** (APFS container `disk3`, Apple Silicon)
> - **Data volume** `/System/Volumes/Data`: **236 GB used** of 494 GB · **230 GB available** (51% used).
> - Sealed system `/` reads 12 GB — ignored (not user-reclaimable).
> - Local snapshots: none (`tmutil listlocalsnapshots /` empty). `~/.Trash`: 1.2 GB pending.
> - Purgeable: ~8 GB (rough estimate from container-free vs `df` — **not** a hard number).
>
> **Tier A — Regenerable, low-risk**
>
> | Size | Path | What | Class | Reverse | How | Risk |
> |------|------|------|-------|---------|-----|------|
> | 14.2 GB | `~/Library/Developer/Xcode/DerivedData` | Xcode build output | regenerable | Trash | Trash the dir | low |
> | 9.8 GB | Homebrew cache (`$(brew --cache)`) | old bottle downloads | regenerable | **PERMANENT** | `brew cleanup` (preview `-n`) | low |
> | 7.9 GB | iOS 26.5 simulator runtime | unused sim runtime | regenerable | **PERMANENT** | `xcrun simctl runtime delete <id>` | low |
> | 6.1 GB | Docker images/build cache | dangling images + build cache | regenerable | **PERMANENT** | `docker image prune` + `docker builder prune` (daemon up) | med |
> | 4.3 GB | `~/Library/pnpm/store/v10` | pnpm content-addressable store | regenerable | **PERMANENT** | `pnpm store prune` | low |
> | 3.5 GB | `~/dev/acme/node_modules` | deps (has `package.json`) | regenerable | Trash | Trash; `pnpm install` to restore | low |
>
> **Tier B — For your judgment (not pre-selected)**
>
> | Size | Path | What | Class | Reverse | How | Risk |
> |------|------|------|-------|---------|-----|------|
> | 22 GB | `~/.ollama/models` | local LLM weights | regenerable* | Trash | you choose — slow to re-pull | med |
> | 18 GB | `~/.orbstack/data` | **OrbStack VM disks** | **irreplaceable** | — | **report-only — I won't propose deleting** | — |
> | 5.4 GB | `~/Downloads/Xcode_16.xip` | installer | regenerable | Trash | you choose — re-downloadable | low |
>
> **Totals** — Tier A realistically reclaimable: **~45.8 GB**. Tier B (your call): ~27 GB regenerable, plus 18 GB VM image (report-only, not counted).
> **Looks big but ISN'T reclaimable:** purgeable ~8 GB (OS-managed), OrbStack 18 GB (live guest), iCloud stubs (du≈0).
> **Couldn't read — needs Full Disk Access:** `~/Library/Mail`, `~/Library/Messages` (flagged unknown, not empty).
> **Reconciliation:** 236 GB used ≈ 45.8 reclaimable + ~120 kept (media/projects/VMs) + ~62 system/other/snapshots/purgeable.

Then **stop** — let the user read the report before any Phase 2 removal.
