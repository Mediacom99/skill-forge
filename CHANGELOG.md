# Changelog

All notable changes to skill-forge are documented here. Format follows
[Keep a Changelog](https://keepachangelog.com/); this project uses per-plugin [SemVer](https://semver.org/).

## [Unreleased]

### Maintenance
- **Scheduled reference-freshness check (routine run, 2026-07-27):** re-fetched all 6 previously-tracked source
  URLs plus the newly-discovered Opus 5 prompting page in `_sources.md`.
  - **Claude Opus 5 has shipped and is now the current Opus flagship**, with its own dedicated prompting page
    (`prompting-claude-opus-5`, added as source **#7**). Rewrote `models/opus.md` off that page — the same
    treatment `models/sonnet.md` got when Sonnet 5 shipped — with the prior Opus 4.8 content kept as a
    "Migration deltas" section rather than dropped. Biggest behavioral changes distilled: **thinking is on by
    default and disabling it is only accepted at effort `high` or below** (400 error at `xhigh`/`max`);
    **effort no longer controls visible response length** (prompt for conciseness explicitly instead); Opus 5
    **verifies and self-corrects its own work without being told**, so explicit verification/double-check
    scaffolding carried over from Opus 4.8 prompts now causes over-verification and should be removed rather
    than rewritten; it narrates more before tool calls and delegates to subagents more readily; running with
    thinking disabled can leak a tool call as plain text or leak internal XML tags into visible output. Also
    carried the still-applicable 4.8-era Design/frontend-defaults and Computer-use sections forward with a note
    that Opus 5's own page doesn't yet restate them. Updated `techniques-advanced.md`'s adaptive-thinking-default
    volatile note to include Opus 5 alongside Sonnet 5.
  - **`prompting-tools` (source #5) has been retired**: it now 307-redirects to `claude-prompting-best-practices`
    (#2), and the destination no longer carries the Console prompt-generator/-improver/template-variable content
    it used to cover. This matches Anthropic's own notice that the experimental Console prompt-tools APIs and
    the Workbench are sunsetting **2026-08-17**. No reference file cited #5 in prose — only `_sources.md`'s
    backing-source table did, for `techniques.md`'s "Template variables" technique — and that technique remains
    valid on general prompting grounds (`{{var}}`-style placeholders are still demonstrated directly on #2's
    live page), so nothing was removed; only the citation was repointed to #2 and #5's row was marked dead so
    `check-sources` won't re-flag it as fresh drift.
  - Minor accuracy fix in `techniques.md`: "especially on Opus 4.x" (technique 7, positive framing) was
    version-pinned to a superseded model; reworded to "current Opus/Sonnet models." Also double-checked that
    Fable 5's Opus-fallback target is still **Opus 4.8**, not Opus 5 — reconfirmed unchanged. Reconfirmed
    `prompting-claude-haiku-4-5` still 404s (no dedicated Haiku page).
  - **Left out again, still flagging for a human** (carried over from the 2026-07-20 cycle, unchanged): the
    best-practices page's "Reduce file creation in agentic coding" subsection, and the "context awareness"
    capability for Sonnet 5 / Sonnet 4.6 / Sonnet 4.5 / Haiku 4.5 (tracking remaining context window). Both
    still look like genuine, narrower additions rather than corrections — a deliberate maintainer call, not
    something to guess at inside an automated cycle.
  - Bumped `last-verified` to 2026-07-27 in `_sources.md`, `models/opus.md`, `models/haiku.md` (comment-only
    fix — its "per-model pages" note was stale now that Opus 5 and Sonnet 5 both have dedicated pages),
    `techniques.md`, and `techniques-advanced.md`. `models/sonnet.md`, `models/fable.md`, and `examples.md`
    were checked against their sources and found current; their headers are unchanged.

- **Scheduled reference-freshness check (routine run, 2026-07-20):** re-fetched all 6 tracked source URLs in
  `_sources.md` and reconfirmed `prompting-claude-haiku-4-5` still 404s (no dedicated Haiku prompting page).
  No URLs moved; no factual drift found in any per-model page beyond what the 2026-07-13 cycle already fixed
  (Opus 4.8's "4 distinct visual directions" wording and its mid-conversation-system-messages migration note
  — both still accurate against the live page).
  - **Added one genuinely new technique to `techniques-advanced.md`:** an **"Optimize parallel tool calling"**
    bullet under Tool use & agentic systems, distilled from `claude-prompting-best-practices`'s
    "Optimize parallel tool calling" subsection — current models already parallelize independent tool calls at
    a high success rate, and a short instruction pushes this close to 100% (with the inverse instruction for
    when parallel execution would destabilize a shared resource). This subsection had been flagged as
    unreviewed in the 2026-07-13 PR; resolved it now since it's a concrete, high-leverage, already-official
    technique directly backing this file. Bumped `techniques-advanced.md`'s `last-verified` to 2026-07-20.
  - **Left out, flagging for a human:** the same source page's "Reduce file creation in agentic coding"
    subsection (narrower scratch-file scaffolding tip) and the "context awareness" capability mentioned for
    Sonnet 5 / Sonnet 4.6 / Sonnet 4.5 / Haiku 4.5 (tracking remaining context window) — both plausibly
    genuinely new, but narrower/more judgment-call than the parallel-tool-calling addition, so kept out to
    keep the core lean. Worth a deliberate look if a maintainer wants either folded in.
  - Bumped `last-verified` to 2026-07-20 in `_sources.md`. `techniques.md`, `models/opus.md`, `models/sonnet.md`,
    `models/haiku.md`, `models/fable.md`, and `examples.md` were checked against their sources and found
    current; their headers are unchanged.

- **Scheduled reference-freshness check (routine run, 2026-07-13):** re-fetched all 6 tracked source URLs in
  `_sources.md` (`overview`, `claude-prompting-best-practices`, `prompting-claude-opus-4-8`,
  `prompting-claude-fable-5`, `prompting-tools`, `prompting-claude-sonnet-5`) and reconciled
  `claude-prompt-crafting`'s reference library — triggered by issue #6 flagging the best-practices and Opus 4.8
  pages as changed.
  - **`models/opus.md`:** the live Opus 4.8 page asks for **4** (not "3–4") distinct visual directions before
    building — corrected the design/frontend-defaults bullet to match. Also added **mid-conversation system
    messages** to the Opus 4.7→4.8 migration-delta list; the live page's migration note now names it alongside
    sampling params, the `effort` default, and the 1M-context default.
  - All other tracked facts were re-verified with **no drift**: prefill removal (4.6+ and the 5-series), the
    core techniques in `techniques.md`/`techniques-advanced.md` (clarity, XML tags, examples, thinking/effort
    guidance, self-check), the Opus 4.8 effort ladder and design/computer-use specifics, the Sonnet 5 effort
    ladder/adaptive-thinking-on-by-default/rejected sampling params/new tokenizer, the Fable 5 / Mythos 5
    refusal categories (`reasoning_extraction`, offensive-cyber, bio/life-sciences) and Opus 4.8 fallback, and
    the prompt-generator/template-variable docs (`prompting-tools`). No URLs moved or 404'd.
  - Bumped `last-verified` to 2026-07-13 in `_sources.md` and `models/opus.md`. `techniques.md`,
    `techniques-advanced.md`, `models/sonnet.md`, `models/haiku.md`, `models/fable.md`, and `examples.md` were
    checked against their sources and found current; their `last-verified` headers are unchanged.

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
