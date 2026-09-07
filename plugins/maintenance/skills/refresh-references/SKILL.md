---
name: refresh-references
description: >
  Refresh a sourced reference library against its official source docs. Use this when the user wants to
  update, refresh, re-verify, or check a skill's references for staleness — e.g. "refresh the prompt
  references", "the Anthropic docs changed, re-verify the claude techniques", "check if my skill's sources
  are out of date", or invokes /refresh-references. This is a MAINTAINER tool for
  skills that follow the _sources.md convention (a reference/ folder with a _sources.md manifest of URLs
  and a last-verified date). It re-fetches each source, diffs it against the distilled reference, proposes
  targeted edits, and updates the verification dates and CHANGELOG.
argument-hint: "[path to a skill or its references/ folder]"
version: 0.2.0
metadata:
  tags: maintenance, references, freshness, docs, prompt-engineering
---

# Refresh References

Keep a skill's distilled reference library faithful to its official sources. Reference libraries go stale
when vendors update docs or ship new models; this skill turns "the docs changed" into a quick, safe chore.

It works on any skill that follows the **`_sources.md` convention**: a `references/` (or `reference/`)
folder containing distilled docs plus a `_sources.md` manifest that lists the canonical source URLs, a
`last-verified` date, and a "volatile items" list.

> **This file is the single source of truth for the reconcile procedure.** The scheduled cloud routine
> ([`docs/auto-reconcile-routine.md`](../../../../docs/auto-reconcile-routine.md)) runs this same procedure
> unattended and adds only its delivery rules on top. Fix the procedure here, not in two places.

## Two ways this runs

- **Interactive** (a maintainer invoked it) — you have a human. Check in at Step 4 before large or
  judgment-heavy edits, and ask rather than guess.
- **Unattended** (the scheduled routine) — no one is watching, and the caller's own instructions supply the
  delivery rules. Don't pause for approval on in-scope, reversible work; the PR is the review gate. In
  exchange, be *more* conservative: anything ambiguous goes to the caller's escalation path (Step 4) instead
  of into a guess.

Everything else below applies identically to both.

## Step 1 — Locate the target

- If the user named a skill or path, use it. Otherwise, find candidates by searching for
  `references/_sources.md` files (e.g. with `Bash`: `find . -name _sources.md`) and ask which to refresh.
  Unattended, refresh **every** library you find rather than asking.
- Work from an **up-to-date `main`** (`git fetch origin && git status`). A reconcile branched from a stale
  base redoes work that already shipped — this has produced duplicate, closed-as-superseded PRs twice.
- Read the target's `_sources.md` to get the **source URL list**, the current `last-verified` date, and the
  **volatile items** list.
- Read the reference files it governs (`techniques.md`, `techniques-advanced.md`, `models/*.md`,
  `examples.md`) so you know what was previously distilled.
- Check whether the `check-sources` workflow has an open **drift issue** ("Source docs changed") — it names
  which URLs moved, which is the fastest way to find what to look at.

## Step 2 — Re-fetch the sources

For each URL in `_sources.md`, fetch the current content with **WebFetch**. If a URL now redirects or 404s,
confirm it with a direct `curl -I` before acting — a fetch tool can silently follow a redirect and make a
dead page look alive. A moved or removed source is itself an update to record.

**If a source can't be fetched, note it and move on — never delete or rewrite content over a failed fetch.**
An unreachable page is not evidence that its content is wrong.

## Step 3 — Diff against the distilled references

Compare each freshly fetched source against what the reference files currently claim. Focus on the
**volatile items** the manifest flags — for prompt-crafting: model IDs and versions, effort/reasoning
parameter names and their enums and per-model defaults, feature availability (prefill removal, adaptive
thinking), refusal categories and fallback targets, API constraints, and Structured Outputs / API surface.
Identify:

- Facts that changed (update them).
- New high-leverage techniques worth adding (add sparingly — keep the core lean).
- Things no longer true (remove or correct).
- Broken or moved URLs (fix in `_sources.md`).

Watch for the **cosmetic diff**: docs sites re-render, and a page can change bytes with every tracked fact
still identical. That is a no-op, not a reconcile.

## Step 4 — Decide: reconcile, or escalate

Sort what you found into three outcomes.

**A — Nothing to do.** References already current, or the pages only re-rendered cosmetically. Say so and
stop. Don't manufacture an edit to justify the run.

**B — Reconcile you can do faithfully.** Facts to correct, a genuinely new high-leverage technique to
distill, a moved URL to fix. The normal path — proceed to Step 5.

**C — Needs the maintainer.** Escalate rather than guess when:

- a change's faithful distillation is genuinely ambiguous, or a judgment call;
- a source 404'd or redirected, or a **new model / new dedicated page** appeared — deciding what to *track*
  is a maintainer call;
- the fix requires touching something outside this skill's scope (see Hard boundaries), e.g. adding or
  retiring a URL in `.source-hashes.json`, or editing a `SKILL.md`;
- you can't make the edit with confidence.

State exactly what needs doing and why you couldn't, quote the relevant source text, and name the affected
reference files. Interactively that's a message to the maintainer; unattended, the caller's instructions say
where it goes. **Escalating is a success, not a failure** — a flagged judgment call is worth more than a
confident wrong edit. B and C are not exclusive: do the part you can, escalate the part you can't, and
cross-reference them.

## Step 5 — Apply

Interactively, present a concise **diff summary** first — what changed, what you'd edit, anything ambiguous
— before making large changes; apply clear factual corrections directly with **Edit**.

Make the **minimal faithful edit**. Preserve each file's structure and its lean/advanced split; don't bloat
the core. Every factual claim must trace to a URL in `_sources.md`.

## Step 6 — Stamp and log

- Bump `last-verified` in `_sources.md` and in the header of **every file you touched**.
- Update moved URLs and refresh the **volatile items** notes in `_sources.md` — including removing an item
  that's now settled, so the next cycle doesn't re-flag it.
- Append a dated entry to `CHANGELOG.md` describing what changed (e.g. "claude: Opus 5 added as flagship;
  effort defaults moved").
- If a `check-sources` **drift issue** prompted this run, close it — or have the PR close it (`Closes #<n>`).
- Bump the plugin's version in **both** `plugin.json` and the skill's `version:` frontmatter — `validate.py`
  fails the build if they disagree.

Before you finish, re-read your own edits: confirm every changed fact traces to a source you actually
fetched this run, and that the `last-verified` dates match.

## Hard boundaries

- **Never edit `references/.source-hashes.json`.** The `check-sources` GitHub Action owns that file and
  populates it on its next scheduled run. Adding or retiring a *tracked URL* is a maintainer action — a
  Step 4C escalation, not an edit. (Seeding a brand-new URL as `null` is the one exception, and only when a
  maintainer asks for it; never touch an existing hash **value**.)
- **Never delete content because a fetch failed.**
- **Never push to `main`.** Changes go on a branch; the caller decides how they ship.

## Notes

- The goal is a reference that is faithful, *current*, and still **lean** — not a bigger one.
- Surface uncertainty rather than silently rewriting. When in doubt, escalate (Step 4C).
