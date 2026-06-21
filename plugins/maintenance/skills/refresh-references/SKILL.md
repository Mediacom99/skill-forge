---
name: refresh-references
description: >
  Refresh a sourced reference library against its official source docs. Use this when the user wants to
  update, refresh, re-verify, or check a skill's references for staleness — e.g. "refresh the prompt
  references", "the OpenAI docs changed, update the gpt skill", "re-verify the claude techniques", "check
  if my skill's sources are out of date", or invokes /refresh-references. This is a MAINTAINER tool for
  skills that follow the _sources.md convention (a reference/ folder with a _sources.md manifest of URLs
  and a last-verified date). It re-fetches each source, diffs it against the distilled reference, proposes
  targeted edits, and updates the verification dates and CHANGELOG.
argument-hint: "[path to a skill or its references/ folder]"
version: 0.1.0
metadata:
  tags: maintenance, references, freshness, docs, prompt-engineering
---

# Refresh References

Keep a skill's distilled reference library faithful to its official sources. Reference libraries go stale
when vendors update docs or ship new models; this skill turns "the docs changed" into a quick, safe chore.

It works on any skill that follows the **`_sources.md` convention**: a `references/` (or `reference/`)
folder containing distilled docs plus a `_sources.md` manifest that lists the canonical source URLs, a
`last-verified` date, and a "volatile items" list.

## Step 1 — Locate the target

- If the user named a skill or path, use it. Otherwise, find candidates by searching for
  `references/_sources.md` files (e.g. with `Bash`: `find . -name _sources.md`) and ask which to refresh.
- Read the target's `_sources.md` to get the **source URL list** and the current `last-verified` date.
- Read the reference files it governs (`techniques.md`, `techniques-advanced.md`, etc.) so you know what was
  previously distilled.

## Step 2 — Re-fetch the sources

For each URL in `_sources.md`, fetch the current content with **WebFetch**. If a URL now redirects or 404s,
note the new location (or that it's gone) — a moved/removed source is itself an update to record.

## Step 3 — Diff against the distilled references

Compare each freshly fetched source against what the reference files currently claim. Focus on the
**volatile items** the manifest flags (for prompt-crafting: model IDs, reasoning/effort parameters and
their enums/defaults, feature availability like prefill or `none` reasoning mode, API surface, host/URL
changes). Identify:
- Facts that changed (update them).
- New high-leverage techniques worth adding (add sparingly — keep the core lean).
- Things no longer true (remove or correct).
- Broken/moved URLs (fix in `_sources.md`).

## Step 4 — Propose, then apply

Present a concise **diff summary** to the user — what changed, what you'd edit, and anything ambiguous —
before making large changes. For clear factual corrections, apply them directly with **Edit**. Preserve the
file's structure and its lean/advanced split; don't bloat the core.

## Step 5 — Stamp and log

- Bump `last-verified` in `_sources.md` and in the header comment of each reference file you touched.
- Update any moved URLs and the volatile-items notes in `_sources.md`.
- Append a dated entry to the repo's `CHANGELOG.md` describing what changed (e.g. "gpt: updated flagship to
  gpt-5.6; reasoning_effort default changed").
- If the repo uses `check-sources.yml`, note that the committed `.source-hashes.json` will update on the next
  scheduled run (or refresh it if you have a local script for it).

## Notes
- This is a human-in-the-loop tool: surface uncertainty rather than silently rewriting. The goal is a faithful,
  *current*, still-lean reference — not a bigger one.
- Keep edits sourced: every factual claim in a reference file should trace to a URL in `_sources.md`.
