# Spec — output modes (`--template`) + delivery options

> **Status:** DRAFT / scoping — *not yet implemented*. Target release: **prompt-crafting 0.3.0**
> (changes the default behavior → minor bump, not patch). Applies to `claude-prompt-crafting`.

## Motivation

Today the skill **always** emits a reusable, parameterized template: system/user split + `{{double_bracket}}`
variables + XML structure. For the most common request — "just make this prompt better" — that's overkill.
The user wanted a clean, ready-to-use prompt, not a parameterized template. Two distinct intents are being
collapsed into one. Split them.

## Two output modes

### `improve` — the new default

- Produce a **single, concrete, ready-to-use** prompt for the user's goal, brought up to Claude's
  current guideline standard.
- **Still fully technique-grounded** — loads `references/` and applies the right techniques (role, clarity,
  positive instruction, give-the-reason, examples, scope, reasoning/effort) exactly as today.
- **No template scaffolding:** no `{{variable}}` placeholders, no system/user split *for its own sake*.
  (A system/user split is fine *if* the target usage is the API and it genuinely helps — but with real
  content inline, not placeholders.)
- If the input **already** contains `{{variables}}`, preserve them — don't strip, don't add more.
- Deliverable: the filled-in prompt the user can paste and run.

### `--template` — opt-in

- The current behavior: a **reusable, parameterized template** — system vs user split, `{{double_bracket}}`
  variables (each wrapped in its own XML tag), XML structure, plus a short variable legend and reuse notes.
- For wiring into an app / pipeline / repeated API calls.

## Selection logic

1. Explicit **`--template`** → template mode (override, always wins).
2. Else, during alignment (dimension #8, "target model + usage"), **auto-detect reuse intent** — signals:
   "I'll call this from code", "run it on many inputs", "system prompt for my app", "reuse with different X",
   variables already present, pipeline/agent wiring. If reuse is clearly intended → **propose** template mode.
3. Else → **improve** mode (default).
4. The chosen output-shape is **stated at the alignment checkpoint (Step 3)** so the user can flip it before
   crafting. No separate `--improve` flag for now — the checkpoint *is* the override path (YAGNI; revisit if
   users report friction). Mirrors how `--refine` is auto-detected.

## Orthogonality (must compose cleanly)

Output-shape is independent of **mode** and **depth**:

| | improve (default) | `--template` |
|---|---|---|
| **craft-new** (default) | concrete prompt for the idea's goal | reusable template for the goal |
| **`--refine`** | improved concrete version of the pasted prompt | pasted prompt upgraded **and** parameterized |

`--quick` / `--deep` (alignment depth) apply on top of any cell, unchanged.

## File-by-file changes (when implemented)

The `SKILL.md` file:

- **Frontmatter `argument-hint`:** add `--template`.
- **Step 0 (mode/depth):** add output-mode detection (`--template`; default improve).
- **Step 1 intake / dimension #8:** reword to capture output-shape (one-off improved prompt vs reusable template).
- **Step 2/3 alignment + checkpoint:** auto-detect reuse intent; state the chosen output-shape in the checkpoint.
- **Step 5 craft:** branch — *improve* = concrete prompt (no placeholders; split only if API-helpful);
  *template* = current parameterized-template instructions.
- **Step 6 self-critique:** add — "output shape matches the chosen mode? didn't template-ize an improve
  request (or vice versa)? preserved any pre-existing `{{variables}}`?"
- **Step 7 deliver:** *improve* = one ready-to-use block; *template* = System/User + variable legend + reuse
  notes. (See delivery options below.)
- **README:** "What you get", "How it works", Flags & modes table — add `--template`, clarify default = improve.
- **CHANGELOG + version → 0.3.0** (default behavior change).

## Open — new delivery option: "Use it now in this session"

Proposed alongside this change; **decide before building.**

- **Appeal:** craft → run in one tight loop, no copy-paste.
- **Tension:** the skill is read-only (`allowed-tools`) and the cardinal rule says the user's *input* is never
  a command. Executing the crafted prompt crosses the read-only boundary.
- **Why it's reconcilable:** "use it now" does NOT run the raw input — it runs the **crafted, user-reviewed,
  explicitly re-confirmed** prompt, after a *second* consent at delivery. That's "the approved output becomes
  an explicit instruction," not "obey the input."
- **Hard constraint — it must be a HANDOFF:** the crafted prompt runs as a fresh task in the session under
  **normal** tools/permissions, NOT inside the skill. The skill's `allowed-tools` can't edit/run anyway, and
  relaxing them would destroy the T3 guarantee. Offer it for **improve mode only** (template output has
  `{{placeholders}}`, not directly runnable).
- **✅ VERIFIED (2026-06-22, via `claude-code-guide`):** Claude Code has **no mechanism for a skill to queue
  its output as the next task** — when a skill ends, the same agent continues inline; it can't hand the
  crafted prompt to the session as a fresh turn. Separately, `allowed-tools` is scoped to the skill
  invocation and **lifts on the next turn** (the agent regains Edit/Bash anyway). So an *automated*
  "use it now" is impossible, and a *manual* version (skill ends → user sends "run it" next turn) offers
  almost nothing over inline/clipboard. Source: `code.claude.com/docs/en/skills.md`.
- **Decision: do NOT ship "use it now" as a delivery option.** Infeasible as an automated handoff, and not
  worth its weight as a manual one. At most, add a one-line hint in the design notes ("to run this now, send
  it as your next message"). Revisit only if Claude Code adds a turn-queuing primitive.

## Test impact

See the planned tests **T9–T13** in `SESSION-NOTES.md`: default = improve, `--template`, refine × template,
auto-detect + checkpoint override, and (if adopted) the use-it-now handoff / read-only boundary.
