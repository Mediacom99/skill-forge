# Changelog

All notable changes to skill-forge are documented here. Format follows
[Keep a Changelog](https://keepachangelog.com/); this project uses per-plugin [SemVer](https://semver.org/).

## [Unreleased]

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
