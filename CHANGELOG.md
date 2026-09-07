# Changelog

All notable changes to skill-forge are documented here. Format follows
[Keep a Changelog](https://keepachangelog.com/); this project uses per-plugin [SemVer](https://semver.org/).

## [Unreleased]

## prompt-crafting — scheduled reference-freshness check, 2026-09-07

### Added
- **Claude Fable 5.1 / Mythos 5.1 — new current-frontier release, added to `models/fable.md`.** Anthropic
  shipped a dedicated `prompting-claude-fable-5-1` page (now source #8 in `_sources.md`), superseding Fable 5 /
  Mythos 5 (page #4, kept as the still-valid baseline). Existing Fable 5 prompts carry over unchanged, but
  `models/fable.md` now documents the deltas worth checking: an effort re-sweep (gains largest at higher
  effort; `low` is now often cost-competitive with Opus/Sonnet at a higher effort while scoring better; `xhigh`
  /`max` on a long deliverable can draft the output twice — once in thinking, once in the reply); fewer
  user-facing progress updates by default in long tool-calling turns (and a note that progress-update
  `thinking` blocks are empty unless you opt into the `thinking.display` beta); tool-call batching regressing
  to one-per-turn in coding/computer-use loops; a new **conversation-history append-only constraint** on newer
  accounts (a replayed thinking block whose prefix changed now 400s or drops, so mid-conversation edits to
  `system`/`tools` or in-place summarization need to move to turn-scoped/mid-conversation system messages or
  server-side compaction); denser default prose ("mannered prose"); less default chat formatting; a reversal
  from Fable 5 on file edits (5.1 leans toward whole-file rewrites — prompt for surgical edits); scope creep on
  open-ended feature work (unrequested fixes/extensions, over-committed test files); weaker search triggering
  at `low` effort; and fewer safeguard false positives (three residual triggers: compile-check phrasing,
  lesser-known languages, base64 in tool output).

### Changed
- Bumped `last-verified` to 2026-09-07 in `_sources.md`, `models/fable.md`, and `techniques-advanced.md`
  (the latter's cross-model adaptive-thinking note now names Fable 5.1 / Mythos 5.1 alongside Fable 5 /
  Mythos 5 as always-on, adaptive-thinking-only models).
- `_sources.md`'s refusal-categories volatile item now flags that the Fable 5.1 page reconfirms the same
  three refusal categories but does **not** restate the Opus-4.8 fallback target on-page (that detail lives on
  the untracked `whats-new-fable-5-1` page) — treat the fallback target as likely-unchanged but unconfirmed for
  5.1 specifically rather than asserting it.

### Notes
- **Re-fetched and reconciled all 7 previously-tracked source URLs plus the new Fable 5.1 page (8 total)**
  against every reference file. Everything besides the Fable 5.1 addition reconfirmed unchanged: the Sonnet 5
  computer-use toolset and Opus 5 subagent-cap env vars added last cycle (2026-08-24, PR #10) are still
  accurate; effort ladders/defaults, adaptive-thinking on/off-by-default, `max_tokens`/tokenizer/sampling-
  parameter behavior on Sonnet 5, prefill removal on 4.6+, parallel-tool-calls guidance, and Structured Outputs
  as the prefill replacement all still match. No content was removed and no other URLs moved or 404'd.
- **`.source-hashes.json` was intentionally left untouched** (this routine's instructions bar it from editing
  that file — the check-sources Action owns it). The new Fable 5.1 URL still needs to be seeded there with a
  `null` hash by a maintainer or the next Action run; see the note in `_sources.md`.
- **Flagging for a human:** `SKILL.md` (outside this routine's `references/**` + `CHANGELOG.md` scope) still
  describes `--model fable` as selecting "Fable 5 / Mythos 5" in its model-selector table and footer — worth a
  follow-up edit to mention Fable 5.1 / Mythos 5.1 now that `models/fable.md` covers both.
- **Deliberately left alone** (per existing `ROADMAP.md` backlog entries, not missed): cross-model **context
  awareness** and **reduce-file-creation-in-agentic-coding**, still queued for a deliberate distillation pass.

## prompt-crafting — scheduled reference-freshness check, 2026-08-24

### Changed
- **`models/sonnet.md` — computer-use tool surface updated.** Claude Sonnet 5 now additionally supports the
  `computer_toolset_20260801` toolset and, for in-webpage tasks, the browser use tool
  (`browser_toolset_20260801`), alongside the previously-documented `computer_20251124` tool version. Sourced
  from the live `prompting-claude-sonnet-5` page (source #6); the Opus 4.8 page (#7) shows the same toolset
  update, but `models/opus.md` doesn't cover Opus 4.8 computer use in detail (it only points to the legacy
  page), so no edit was needed there.
- **`models/opus.md` — added deterministic subagent-spawn caps for Claude Code / Agent SDK.** The dedicated
  Opus 5 page (#3) now documents `CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH` / `CLAUDE_CODE_MAX_CONCURRENT_SUBAGENTS`
  env vars and the SDK's `max_budget_usd` option as concrete caps on Opus 5's readier subagent delegation
  (requires Claude Code 2.1.217+), plus the note that Claude Code only adds its own damping instruction under
  the `claude_code` system-prompt preset. Added as a second bullet under "Subagents" — directly extends the
  existing "cap it" guidance with an actionable, sourced mechanism.
- Bumped `last-verified` to 2026-08-24 in `_sources.md` and in the two touched files above.

### Notes
- **Re-fetched and reconciled all 6 tracked source URLs** (overview, best-practices, and the four per-model
  pages) against `techniques.md`, `techniques-advanced.md`, and all four `models/*.md` files. Everything else
  checked out unchanged and faithful: effort ladders/defaults, adaptive-thinking on/off-by-default and the
  Opus-5-disable-only-at-≤-`high` constraint, `max_tokens`/tokenizer/sampling-parameter behavior on Sonnet 5,
  the Fable 5 refusal categories (`reasoning_extraction`, offensive-cyber, bio/life-sciences) and Opus 4.8
  fallback, prefill removal on 4.6+ (including the 5-series), parallel-tool-calls guidance, and Structured
  Outputs as the prefill replacement. No content was removed and no URLs moved or 404'd.
- **Issue #9** (`Source docs changed`) has flagged all 6 URLs as changed on every check-sources cycle since
  2026-08-10 (including today, 2026-08-24) with no corresponding real content drift found this pass beyond the
  two items above — worth a human look at whether `check_sources.py`'s normalization still has a
  non-deterministic input (timestamp, nonce, ordering) causing a hash flip every run. Left the issue open per
  procedure (a PR closes it once merged); flagged here rather than guessing at the hashing bug.
- **Deliberately left alone** (per existing `ROADMAP.md` backlog entries, not missed): cross-model **context
  awareness** (Sonnet 5/4.6/4.5, Haiku 4.5) and **reduce-file-creation-in-agentic-coding** — both still present
  on the best-practices page (#2), both still queued in `ROADMAP.md` for a deliberate distillation pass rather
  than an automated one.

## prompt-crafting 0.6.1 — 2026-07-28

### Changed
- **Retired dead source #5 (`prompting-tools`).** The Console prompt-tools page now 307-redirects to
  `claude-prompting-best-practices` (#2), and the Console prompt generator/improver + Workbench are sunsetting
  2026-08-17. Removed it from `.source-hashes.json` tracking (its normalized content already mirrored #2),
  marked its `_sources.md` row retired, and repointed the template-variable citation to #2 (the
  `{{double_bracket}}` convention is still demonstrated there). No technique was dropped.
- **Added the "parallel tool calls" technique** to `techniques-advanced.md` — independent tool calls run in
  parallel by default; a one-line system-prompt nudge pushes it to ~100% (distilled from #2).

### Notes
- Salvaged from the auto-reconcile routine's **PR #7** (its 2026-07-27 cycle), which caught these two items the
  0.6.0 manual pass missed. PR #7 closed as superseded by 0.6.0 + this patch; drift issue #6 closed. Two
  further additive topics it surfaced — cross-model **context awareness** and **reduce-file-creation** — moved
  to `ROADMAP.md` for a deliberate distill rather than an automated guess.

## prompt-crafting 0.6.0 — 2026-07-28

### Added
- **Claude Opus 5 (`claude-opus-5`) — the new Opus flagship — added to the per-model tuning matrix.** Rewrote
  `references/models/opus.md` from the dedicated *Prompting Claude Opus 5* page (now source #3). Opus 5 is
  built for complex agentic coding + enterprise work and is the recommended default ("start with Opus 5"; step
  up to Fable 5 only for frontier capability). `--model opus` now loads Opus 5 tuning; the SKILL model
  selector, README model lists, and the skill footer all name Opus 5.

### Changed
- **Opus effort + thinking defaults moved with Opus 5** (distinct from now-legacy Opus 4.8):
  - **Effort defaults to `high`** (Opus 4.8 recommended `xhigh` for coding/agentic); `low`/`medium` are now
    efficient enough to use liberally as the primary cost/latency control, with `xhigh` for demanding
    coding/agentic. Migrating prompts should re-run an effort sweep — the cost/quality curve moved.
  - **Adaptive thinking is now ON by default** (a flip from Opus 4.8's off-by-default) and can be **disabled
    only at effort ≤ `high`**. Updated `techniques-advanced.md`'s cross-model thinking note (Opus 5 + Sonnet 5
    on by default; legacy Opus 4.8 / Sonnet 4.6 off; Fable 5 / Mythos 5 always on).
  - New Opus 5 tuning captured: longer default verbosity + written-deliverable length (prompt for concision),
    readier agentic narration (tune cadence), **self-verification without prompting** (remove legacy "verify"
    instructions — they now cause over-verification), scope-widening (constrain for narrow tasks), readier
    subagent delegation (cap it), correction-narration control, and the thinking-disabled artifacts
    (tool-call-as-text, internal XML-tag leakage → prefer thinking-on at low effort). 1M context (default and
    max), 128k output, no manual `budget_tokens`.
- The Opus-4.8-only sections (cream/`#F4F1EA` design house-style, computer-use resolutions) are **not** on the
  Opus 5 page, so they were dropped from `models/opus.md` — kept only as a pointer to the legacy Opus 4.8 page
  (#7) rather than fabricated for Opus 5.

### Maintenance
- **Sourced against live docs (2026-07-28).** Repointed source #3 → `prompting-claude-opus-5` and moved the
  legacy Opus 4.8 page to #7 in `_sources.md`; seeded the Opus 5 URL `null` in `.source-hashes.json` (the
  check-sources Action captures its baseline hash on the next run — existing hashes untouched). Bumped
  `last-verified` to 2026-07-28 on every touched file. Opus 4.8 / 4.7 / 4.6 are now labeled **legacy**.
  Re-verified the **Fable 5 fallback target is still Claude Opus 4.8** on the live Fable page (unchanged — left
  `models/fable.md` and `examples.md` as-is). Current model set: Fable 5, Mythos 5, Opus 5, Sonnet 5, Haiku
  4.5 (still no dedicated Haiku prompting page). Bumped `prompt-crafting` to 0.6.0.
- **Scheduled reference-freshness check (routine run, 2026-07-06):** re-fetched all 6 tracked source URLs
  in `_sources.md` and reconciled `claude-prompt-crafting`'s reference library.
  - **`models/opus.md` was missing two sections that exist on the live Opus 4.8 prompting page** and were
    already distilled for Sonnet 5 in `models/sonnet.md`: **Design and frontend defaults** (Opus 4.8's
    persistent default house style — warm cream/off-white ~`#F4F1EA` backgrounds, serif display type,
    terracotta/amber accent — and the two reliable ways to break it) and **Computer use** (resolution support
    up to 2576px / 3.75MP; 1080p as the performance/cost balance, 720p/1366×768 for cost-sensitive work).
    Added both, matching the depth already given to Sonnet.
  - **`models/fable.md`:** added two scaffolding tips from the live Fable 5 page's "Recommended scaffolding
    changes" section that weren't yet distilled — aiming at the top of one's difficulty range (testing Fable 5
    only on simpler workloads undersells it), and preferring fresh-context verifier subagents over self-critique
    for long-running tasks.
  - All other tracked facts were re-verified with **no drift**: prefill removal (4.6+ and the 5-series),
    the Opus 4.8 and Sonnet 5 effort ladders and defaults, Sonnet 5's adaptive-thinking-on-by-default /
    removed `budget_tokens` / rejected sampling params / new tokenizer, the Fable 5 / Mythos 5 refusal
    categories (`reasoning_extraction`, offensive-cyber, bio/life-sciences) and Opus 4.8 fallback, and the
    prompt-generator/template-variable docs (`prompting-tools`). Reconfirmed `prompting-claude-haiku-4-5`
    still 404s — no dedicated Haiku prompting page yet.
  - Bumped `last-verified` to 2026-07-06 in `_sources.md`, `models/opus.md`, and `models/fable.md`.
    `techniques.md`, `techniques-advanced.md`, `models/sonnet.md`, `models/haiku.md`, and `examples.md` were
    checked against their sources and found current; their `last-verified` headers are unchanged.

## mac-cleanup 0.1.0 — 2026-07-17

### Added
- **New plugin `mac-cleanup` with the `reclaim-disk-space` skill** — safely reclaim SSD/disk space
  on an **Apple Silicon (M-series) Mac**. It runs a strict two-phase flow whose #1 requirement is
  **zero irreversible data loss**: **Phase 1** scans **read-only** (never mutating) and produces a
  ranked report of reclaimable space; **Phase 2** removes **only what the user approves, batch by
  batch**, Trash-first, blocking after every batch. Registered in `marketplace.json`; installs via
  `/plugin install mac-cleanup@skill-forge`.
- **Packaged from a fact-checked, red-teamed source prompt** (developed with the `prompt-crafting`
  skill), with its full safety architecture preserved: the 10 absolute safety rules (Trash-first + confirm
  moved; VM/container images report-only; account for APFS snapshots / purgeable / iCloud stubs;
  never `sudo`; app-quit-vs-daemon-running; FDA-denied ≠ empty), Phase-1 command safety, and the
  per-batch authorization protocol (empty-Trash is a dedicated final PERMANENT batch) all live in
  `SKILL.md` and load every invocation.
- **Progressive-disclosure references** loaded at the step that needs them: `references/scan-catalog.md`
  (Tier A/B/C candidates + exact sizing commands + verify-before-listing predicates),
  `references/report-format.md` (report spec + a worked example), and `references/reclaim-commands.md`
  (argv-safe Trash / `tmutil` / `brew` / `docker` / `simctl` / `pnpm` / `go` recipes).
- **Verified against live macOS 26.3 (Apple Silicon) on 2026-07-17** (each reference carries a
  verification header). Findings folded in: resolve the pnpm store via `pnpm config get store-dir`
  (plain `pnpm store path` can trigger a Corepack download) and the Go module cache via
  `go env GOMODCACHE`; `xcrun simctl` can provision CoreSimulator components on first run even with
  Xcode installed, so `xcode-select -p` guarding is necessary but not sufficient; read used/free from
  the `/System/Volumes/Data` volume, not the sealed `/`. Uses broad `Bash` (a cleanup skill needs it
  in both phases) — CI's read-only `allowed-tools` guard only applies to `*-prompt-crafting` skills.

## prompt-crafting 0.5.2 — 2026-07-03

### Changed
- **Clarified that `--model` sets the *target* model — the model the crafted prompt will *run on* — not the
  runtime session.** Sharpened the flag description (Step 0 + README) and made the alignment checkpoint state
  both when they differ (e.g. "crafting on Opus 4.8 · tuned for **Fable 5**"). No behavior change — the flag
  always meant the destination model (you craft *on* Opus but *for* Fable); the wording just invited confusion.

## prompt-crafting 0.5.1 — 2026-07-03

### Added
- **Automated reference reconcile.** A scheduled [claude.ai routine](docs/auto-reconcile-routine.md) re-verifies
  the sources weekly and, when they've drifted, reconciles the references and opens a **pull request** for review
  (subscription-billed, no API key; the PR is the review gate). Adds `.github/workflows/notify-pr.yml` (emails the
  maintainer on `auto/refresh*` PRs, inert until SMTP secrets are set) and `docs/auto-reconcile-routine.md` (routine
  prompt + setup). Its first run (PR #4) autonomously shipped the Sonnet 5 refresh below.

### Maintenance
- **Refreshed `claude-prompt-crafting` references against the live docs (2026-07-03): Anthropic shipped a
  dedicated Claude Sonnet 5 prompting page** (`prompting-claude-sonnet-5`) since the last cycle, replacing the
  "no dedicated Sonnet page" note from 0.5.0. Rewrote `models/sonnet.md` off that page: effort defaults to
  `high` (same as 4.6) with `xhigh` for the hardest coding/agentic work and a cross-model effort mapping
  (Sonnet 5 `medium` ≈ 4.6 `high`; Sonnet 5 `high` ≈ 4.6 `max`); **adaptive thinking is now on by default**
  (a flip from 4.6, where it was off unless requested — disable via `thinking: {type: "disabled"}`); manual
  extended thinking (`budget_tokens`) is fully removed (400 error); `temperature`/`top_p`/`top_k` at
  non-default values now 400 (new for Sonnet-class models — breaks any prompt relying on `temperature` for
  output variety, replaced with "propose N directions first"); a new tokenizer produces \~30% more tokens for
  the same text, so `max_tokens` budgets ported from 4.6 may need raising; added `computer_20251124` tool-version
  note. Added source #6 (`prompting-claude-sonnet-5`) to `_sources.md` and repointed `models/sonnet.md`'s
  backing source at it. All other tracked sources (#1–#5) were re-fetched and reconciled with no drift: prefill
  removal, the Opus 4.8 effort ladder, the Fable 5 / Mythos 5 refusal categories (`reasoning_extraction`,
  offensive-cyber, bio/life-sciences) and Opus 4.8 fallback, and the prompt-generator/template-variable docs are
  all unchanged. Also fixed a now-stale blanket claim in `techniques-advanced.md` ("[adaptive thinking is] off
  by default") — no longer true across the board now that Sonnet 5 defaults it on and Fable 5 / Mythos 5 run
  it always-on; the line now flags this as model-specific and points at each model's file. Bumped
  `last-verified` to 2026-07-03 in `_sources.md`, `models/sonnet.md`, and `techniques-advanced.md`.
- Follow-up to the Sonnet 5 refresh: aligned the `SKILL.md` model-selector row + README bullet from "Sonnet 4.6"
  to **Sonnet 5** (skill files, outside the routine's references-only scope), and seeded the new
  `prompting-claude-sonnet-5` URL to `null` in `.source-hashes.json` so `check-sources` captures its baseline
  hash on the next run. This whole reference refresh was produced autonomously by the claude.ai reconcile
  routine (PR #4) and merged after human review.
- Re-verified `claude-prompt-crafting` references against the live docs (drift issue #3, 2026-07-01): another
  cosmetic site re-render — all volatile facts unchanged; bumped `last-verified` to 2026-07-01.
- **`check-sources` now hashes *normalized* page text** (scripts/styles/tags stripped, whitespace collapsed)
  instead of raw bytes, so cosmetic docs-site re-renders stop tripping false drift. Existing snapshots reset to
  `null` so the next run re-baselines with the new hashing.

## prompt-crafting 0.5.0 — 2026-07-03

### Added
- **Per-model prompt tuning — one reference file per Claude family, loaded on demand.** The craft step now
  loads guidance for the **target model only** (`references/models/{opus,sonnet,haiku,fable}.md`) and applies
  it, so a prompt for Haiku, Sonnet, Opus 4.8, or Fable 5 / Mythos 5 is tuned to that model instead of getting
  one-size-fits-all advice. Previously all per-model tips were ~3 bullets in the advanced appendix, which a
  *standard* craft never loaded at all.
- **`--model <opus|sonnet|haiku|fable>` flag + auto-detect.** Target model is now a **required** field at the
  alignment checkpoint, resolved in order: `--model` flag → stated/implied in the dialogue → **auto-detected
  from the model the skill is running as** (surfaced as a flippable assumption) → ask. A compact model-selector
  table in Step 0 lets the dialogue recommend a model without loading references.
- **Dedicated Claude Fable 5 / Mythos 5 guidance** (`models/fable.md`), verified against Anthropic's
  now-released Fable 5 prompting page: `high`-default effort, brief outcome-led instructions over enumeration,
  give-the-reason, stating boundaries, grounding progress claims, the memory-file / parallel-subagent /
  `send_to_user` agentic scaffolding, and the **`reasoning_extraction` refusal** (never ask Fable 5 to
  echo/transcribe/explain its reasoning as output → Opus 4.8 fallback). Far richer than the prior 2-bullet distill.

### Changed
- Moved per-model tips out of `techniques-advanced.md` into `references/models/`; `techniques.md` and the
  advanced appendix now point there. Self-critique gains a **model-fit** check.
- `_sources.md` now maps each reference file to its backing source and records that Sonnet 4.6 / Haiku 4.5
  have **no dedicated prompting page** (confirmed 404) — those two files derive from the cross-model
  best-practices page (#2) + model overviews. No new hash-tracked URLs.

### Verified
- Opus 4.8 and Fable 5 / Mythos 5 guidance re-grounded against their live dedicated pages (2026-07-03).

## prompt-crafting 0.4.2 — 2026-07-01

### Changed
- **Clipboard delivery no longer writes a file at all.** It pipes the prompt to the clipboard command via a
  here-doc (`pbcopy << 'EOF' … EOF`) on stdin — still a single scoped clipboard command, but nothing touches
  disk, so there's no scratch file to leave behind or clean up. Supersedes 0.4.1's write-to-cwd + empty-after
  approach (which left a harmless 0-byte file). A documented file fallback remains for shells without here-doc
  support. Stays fully read-only — no `rm`, no `allowed-tools` change.

## prompt-crafting 0.4.1 — 2026-06-29

### Changed
- **Clipboard delivery writes its scratch file to the current working directory** (`./.skill-forge-clipboard.txt`,
  a fixed hidden name) instead of the system temp dir — keeps the Write inside the project so it doesn't trip a
  path-approval prompt.
- **Auto-cleanup after copy:** once the prompt is on the clipboard, the scratch file is overwritten to empty so
  the prompt text doesn't linger. (The skill can't `rm` without breaking the read-only guarantee, so emptying is
  the cleanup; a harmless 0-byte hidden file remains — gitignored here, reused next time.)

## prompt-crafting 0.4.0 — 2026-06-26

### Removed
- **Dropped the `gpt-prompt-crafting` skill — skill-forge is now Claude-only.** A GPT prompt skill is
  off-audience for a Claude Code marketplace, couldn't be dogfooded by the maintainer, doubled reference
  maintenance, and its description was being dropped from the skill listing (so it under-triggered). It
  remains recoverable from git history if there's demand.

### Changed
- README, `marketplace.json`, and `plugin.json` refocused on Claude; added a hero screenshot and an
  API/programmatic-use angle.

### Maintenance
- Re-verified `claude-prompt-crafting` references against the live Anthropic docs (drift issue #2,
  2026-06-26): a cosmetic site-wide re-render — all volatile facts unchanged; bumped `last-verified` to 2026-06-26.

## prompt-crafting 0.3.1 — 2026-06-26

### Fixed
- **`--template` auto-detect calibration (F2).** No longer infers a reusable template from the task
  *domain* alone (e.g. "contract review / release notes are usually recurring"). Template is auto-detected
  only from an explicit, durable reuse signal — an existing `{{variable}}` in the input, or the user saying
  it will run repeatedly / on many inputs / from code or an API / in a pipeline. *Improve* is framed as the
  default; `--template` still forces a template. Surfaced by the test suite (T7 over-triggered; T11/T12 correct).
- **GPT skill internal contradiction (F1).** The shared "Roles" rule no longer mandates a developer/user
  split as universal — splitting is governed by the output shape, so it no longer contradicts improve mode.
- **Preserve existing placeholders in any syntax (F6).** Improve/refine keeps `{{var}}`, `{var}`, `${var}`,
  and `<var>` placeholders as-is, not only `{{double_bracket}}`.
- **Tighter skill descriptions.** Trimmed both `description:` frontmatter blocks so they fit the default
  skill-listing budget (the GPT skill's description was being dropped, hurting auto-triggering) and added
  API / programmatic-use framing.
- **README:** the "What you get" table and "See it work" example now describe the default as an *improved,
  ready-to-use prompt* rather than a template.

## prompt-crafting 0.3.0 — 2026-06-22

### Added
- **`--template` flag + an "improve" default (output-shape split).** By default both skills now return a
  single, concrete, **ready-to-use** prompt brought up to current guideline standard — no forced
  system/user split or `{{variables}}`. Pass `--template` (or let the skill auto-detect clear reuse intent)
  to get the previous behavior: a **reusable, parameterized template**. Output shape is orthogonal to
  `--refine` and `--quick`/`--deep`, is stated at the alignment checkpoint, and is checked in self-critique.

### Fixed
- Corrected stale "real test-run" wording in `--deep` (Step 0 and README) to the **dry paper simulation**
  that 0.2.0 actually introduced — the skill never executes the described task.

## prompt-crafting 0.2.2 — 2026-06-22

### Changed
- **`claude-prompt-crafting` references refreshed against Anthropic's current docs** (drift issue #1).
  Repositioned Claude Fable 5 from "creative writing" to its current long-horizon / agentic framing and
  added Claude Mythos 5; documented the `reasoning_extraction` refusal category and Opus 4.8 fallback for
  Fable 5 / Mythos 5; sharpened Opus 4.8 effort guidance (`xhigh` for coding/agentic, `high` minimum for
  intelligence-sensitive tasks); clarified that prefill removal covers the 5-series. Bumped `last-verified`
  to 2026-06-22. (Source hashes were already refreshed by the `check-sources` workflow.) The plugin version
  bump applies to both skills; `gpt-prompt-crafting` content is unchanged.

## prompt-crafting 0.2.1 — 2026-06-21

### Changed
- **Cardinal rule clarified: the user's input is always a prompt to *improve*, never a command to obey.**
  Replaced the 0.2.0 "scope gate" (which could refuse non-craft requests or hand the task back) — that was a
  misread. Whatever the user writes ("clean up my repo", "find the bugs and fix them", "check everything we
  did"), the skill now always crafts a better prompt *for that same goal* and never performs the task,
  changes the goal, or refuses. Humans are bad at writing prompts; the skill always improves what they wrote.

## prompt-crafting 0.2.0 — 2026-06-21

### Changed
- **Read-only until delivery, enforced at the tool level.** Both prompt skills now declare
  `allowed-tools: Read, Grep, Glob, AskUserQuestion, Write` plus a fixed set of clipboard commands —
  no edit, no arbitrary shell — so even in auto / auto-accept mode they cannot modify your code or run
  commands. The only file write is saving the finished prompt when you ask for it.
- **Hard boundaries.** A **start boundary** (scope gate): on invocation the skill states the single prompt
  it's crafting, refuses to morph into a general assistant for non-craft requests, and crafts exactly one
  prompt per run (no self-initiated extras). A **mandatory interactive end boundary**: it always asks how
  to deliver via AskUserQuestion and never assumes a save path — overriding any host-project
  "be decisive / version it / don't ask" convention.
- **Cross-platform clipboard, safely.** Clipboard delivery is kept and works on macOS (`pbcopy`),
  Windows/WSL (`clip.exe`/`clip`), and Linux (`wl-copy` → `xclip`/`xsel`), via a temp-file + input
  redirect (no fragile pipes), scoped through `allowed-tools` so no arbitrary shell is exposed.
- **`--deep` test-run is now a dry paper simulation**, never real execution of the described task.

## prompt-crafting 0.1.0 — 2026-06-21

### Added
- **`claude-prompt-crafting`** skill — align-then-craft engine targeting Claude/Anthropic models, with a
  lean + advanced reference library distilled from Anthropic's official prompt-engineering docs
  (verified 2026-06-21).
- **`gpt-prompt-crafting`** skill — same engine targeting OpenAI/GPT models, with an explicit
  reasoning-vs-non-reasoning branch, distilled from OpenAI's official developer docs (verified 2026-06-21).
- Both skills support craft-new and refine-existing modes, `--quick`/`--deep` depth, an alignment
  checkpoint, a self-critique pass, and three-way delivery (inline / save / clipboard).

## maintenance 0.1.0 — 2026-06-21

### Added
- **`refresh-references`** skill — re-fetches the official sources behind any `_sources.md`-backed
  reference library, diffs them, and proposes updates.

## skill-forge (marketplace) — 2026-06-21

### Added
- Marketplace scaffold (`.claude-plugin/marketplace.json`) hosting the `prompt-crafting` and
  `maintenance` plugins.
- `validate.yml` (install-safety gate) and `check-sources.yml` (weekly doc-drift detector) workflows,
  with local-runnable scripts in `.github/scripts/`.
