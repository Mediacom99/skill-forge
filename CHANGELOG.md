# Changelog

All notable changes to skill-forge are documented here. Format follows
[Keep a Changelog](https://keepachangelog.com/); this project uses per-plugin [SemVer](https://semver.org/).

## [Unreleased]

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
