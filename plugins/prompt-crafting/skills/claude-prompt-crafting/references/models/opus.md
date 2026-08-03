<!--
last-verified: 2026-08-03
source: _sources.md #7 — prompting-claude-opus-5 (dedicated Opus 5 page, current flagship); #3 —
prompting-claude-opus-4-8, kept for the migration-deltas section (that page is still live).
scope: Per-model tuning for Claude Opus 5 (current Opus flagship). Loaded at craft time only when the
target model is Opus. Applies on top of techniques.md; note Opus 4.8 deltas inline for migrating prompts.
-->

# Tuning for Claude Opus 5

Opus 5 is the flagship for complex agentic coding, long-horizon agentic work, and enterprise/office tasks
(spreadsheets, decks, multi-agent coordination). It performs well out of the box on existing Opus 4.8
prompts — the behaviors below are what most often need tuning when migrating or writing fresh.

## Effort is the primary lever
- Ladder (intelligence ↔ latency/cost): `max` · `xhigh` · `high` · `medium` · `low`.
  - **`high`** — the **default**.
  - **`xhigh`** — for demanding coding and agentic work.
  - **`low`/`medium`** — newly **efficient** on Opus 5: strong quality at a fraction of the tokens/latency of
    higher settings vs. prior Opus models. Use liberally as the primary cost/latency lever wherever quality
    holds, rather than defaulting straight to `high`/`xhigh`.
  - **`max`** — absolute maximum capability, no constraint on token spend.
- If you carried effort defaults over from Opus 4.8 or another prior model, **re-run an effort sweep on your
  own evals** rather than assuming the old tuning transfers — the low/medium efficiency gain is new.
- If reasoning looks shallow on a hard problem, **raise `effort`** rather than prompting around it.

## Thinking — on by default, disable only at ≤ `high`
- **Thinking runs by default** when the `thinking` field is omitted (a change from Opus 4.8, where thinking
  was off unless explicitly enabled). To turn it off, pass `thinking: {type: "disabled"}` — but this is only
  accepted at effort **`high` or below**; combining `thinking: {type: "disabled"}` with `xhigh`/`max` errors.
- **With thinking disabled, two output artifacts can leak into visible text:** a tool call written as plain
  text instead of a structured call (the call never runs, and the leaked text persists in agentic-loop
  history), and internal/`<thinking>`-style XML tags appearing in the response. The primary mitigation for
  both is to **keep thinking on at a lower effort** instead of disabling it — for most tasks, thinking-enabled
  at `low` outperforms thinking-disabled at similar cost. If thinking must stay disabled, add explicit
  permission to speak briefly before a tool call, an escape hatch for when no tool fits, and a rule against
  internal tags — do not name the tags specifically, as that increases leakage.
- Adaptive triggering is steerable; if a large/complex system prompt makes it think more than you want, add a
  line telling it to think only when it will meaningfully improve the answer and otherwise respond directly.

## Response length is independent of effort
- Opus 5's **default user-facing responses run longer** than prior Opus models', and raising/lowering
  `effort` mostly changes *thinking* volume, not what's shown. **Prompt explicitly for conciseness** if you
  need it (e.g. "keep responses focused, brief, and concise; spend most of the response on the main answer").
- **Written deliverables** (reports, Markdown files) are also longer by default — if this matters, add
  explicit length calibration ("match length to what the task needs; don't pad with filler or boilerplate").

## Self-verification and self-correction — remove legacy instructions
- Opus 5 **verifies its own work without being told to**, and catches/fixes its own mistakes well unprompted.
  Explicit verification instructions carried over from prompts tuned for earlier models ("include a final
  verification step," "double-check your answer") now cause **over-verification** — wasted tokens/latency,
  no quality gain. **Remove**, don't rewrite, these instructions when migrating a prompt to Opus 5.
- It narrates corrections to its own earlier statements more than prior models; if that's undesirable
  user-facing, ask it to only flag corrections that would change the user's code/conclusions/decisions and
  otherwise just fix and continue silently.

## Task scope
- Opus 5 can expand scope on its own initiative, adding steps that weren't requested. For narrow tasks, state
  scope explicitly and tell it to flag — not silently apply — a different reading of the request.

## Literal instruction-following → state scope
- Interprets prompts literally, especially at lower effort; it will **not** silently generalize one
  instruction to other items or infer requests you didn't make. When an instruction should apply broadly,
  **say so**: "Apply this to every section, not just the first."

## Agentic targets (only if the prompt is tool-using / multi-agent)
- **Narrates readily before tool calls** and per-message output in agentic sessions runs longer than prior
  models'; if unwanted, describe the cadence you want explicitly (e.g. one sentence before the first tool
  call, brief updates only on findings/direction changes, lead with the outcome at the end).
- **Delegates to subagents more readily** than prior models — this pays off on genuinely independent,
  sizeable work but multiplies cost on small tasks. Give explicit guidance on when delegation is warranted or
  set a deterministic cap if your harness supports subagents.
- **Code-review harnesses:** high precision *and* recall even at lower effort settings; it may still follow
  "only report high-severity / be conservative" instructions faithfully and under-report as a result. For
  coverage, instruct it to report every finding with a confidence + severity and let a downstream step filter.

## Design, frontend defaults, and computer use
- Opus 5's dedicated page doesn't restate design/frontend-house-style or computer-use specifics — the
  guidance below is carried over from the still-live Opus 4.8 page and **not independently reconfirmed for
  Opus 5**; verify directly if it matters for your use case.
  - Opus 4.8 has a persistent default house style on open-ended briefs: warm cream/off-white backgrounds
    (~`#F4F1EA`), serif display type (Georgia, Fraunces, Playfair), italic word-accents, terracotta/amber
    accent. Break it with **(1)** a concrete, fully-specified alternative spec, or **(2)** having it **propose
    3–4 distinct visual directions first**, then implement the one picked.
  - Computer use supports resolutions **up to 2576px / 3.75MP**; **1080p** balances performance/cost for
    testing, **720p / 1366×768** for cost-sensitive workloads.

## Migration deltas from Opus 4.8
- **Thinking default flipped** (off → on) and disabling it is now capped at effort `high` or below (see
  Thinking above) — the single biggest prompt-breaking change when porting an Opus 4.8 prompt as-is.
- **Verification instructions that helped on 4.8 now hurt** — see Self-verification above.
- Opus 4.8 itself is unchanged and its dedicated page (`_sources.md` #3) is still live for prompts still
  targeting it; sampling params, the `effort` default, and 1M-context default also changed across the
  4.7→4.8 migration — verify against the current migration guide if targeting that older delta.
