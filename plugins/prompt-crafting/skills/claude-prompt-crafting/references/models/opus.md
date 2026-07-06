<!--
last-verified: 2026-07-06
source: _sources.md #3 — prompting-claude-opus-4-8 (dedicated Opus 4.8 page)
scope: Per-model tuning for Claude Opus 4.8 (current Opus flagship). Loaded at craft time only when the
target model is Opus. Applies on top of techniques.md; note 4.7/4.6 deltas inline.
-->

# Tuning for Claude Opus 4.8

Opus 4.8 is the flagship for long-horizon agentic work, knowledge work, vision, and memory. It follows
instructions **literally** and calibrates its own length and depth to the task — so the biggest levers are
`effort`, explicit scope, and telling it the length/tone you want.

## Effort is the primary lever
- Ladder (intelligence ↔ latency/cost): `max` · `xhigh` · `high` · `medium` · `low`.
  - **`xhigh`** — best default for **coding and agentic** work.
  - **`high`** — minimum for most **intelligence-sensitive** tasks; balances tokens vs. intelligence.
  - **`medium`** — cost-sensitive work that can trade off some intelligence.
  - **`low`** — short, scoped, latency-sensitive work only. Opus 4.8 scopes **strictly** at the low end;
    on moderately complex tasks at `low` there's real under-thinking risk.
  - **`max`** — for the most intelligence-demanding tasks; diminishing returns and some overthinking risk.
- If reasoning looks shallow on a hard problem, **raise `effort`** rather than prompting around it. Effort
  matters more on this model than any prior Opus — recommend tuning it actively.
- At **`xhigh`/`max`, set a large max-output budget** (start ~**64k tokens**) so it has room to think and act.

## Thinking
- Thinking is **off** unless you set **`thinking: {type: "adaptive"}`**. Adaptive triggering is steerable; if
  a large/complex system prompt makes it think more than you want, add a line telling it to think only when
  it will meaningfully improve the answer and otherwise respond directly.

## Literal instruction-following → state scope
- Opus 4.8 interprets prompts literally, especially at lower effort; it will **not** silently generalize one
  instruction to other items or infer requests you didn't make. When an instruction should apply broadly,
  **say so**: "Apply this to every section, not just the first." Great for structured extraction and pipelines
  where predictable behavior matters.

## Length, verbosity, tone
- It **calibrates length to task complexity** (short on lookups, long on open-ended analysis). If you need a
  specific verbosity, ask for it explicitly (e.g. "concise, focused responses; skip non-essential context").
- **Positive framing beats "don't."** Positive examples of the concision/style you want steer better than
  negative instructions.
- Prose baseline is **direct and opinionated**, minimal validation-forward phrasing, sparing emoji.
  **Re-evaluate old voice/style prompts** against this baseline; add warmth/tone explicitly if the product
  needs it.
- **Front-load the full task in the first turn.** Well-specified, upfront intent + constraints maximize
  autonomy and token efficiency; ambiguous, progressively-revealed asks cost more and can hurt performance.

## Agentic targets (only if the prompt is tool-using / multi-agent)
- Favors **reasoning over tool calls** by default — raise `effort` (`high`/`xhigh`) for more tool use, or
  describe explicitly when/why to use a given tool.
- Spawns **fewer subagents** by default; if you want fan-out, give explicit guidance on when delegation is
  desirable.
- Gives good **interim progress updates** on its own — remove any "summarize progress every N tool calls"
  scaffolding; describe the update style you want instead.
- **Code-review harnesses:** it follows "only report high-severity / be conservative" faithfully and may
  report fewer low-severity bugs. For coverage, instruct it to report every finding with a confidence +
  severity and let a downstream step filter.

## Design and frontend defaults
- Has a **persistent default house style** on open-ended briefs: warm cream/off-white backgrounds
  (~`#F4F1EA`), serif display type (Georgia, Fraunces, Playfair), italic word-accents, terracotta/amber
  accent. Reads well for editorial/hospitality/portfolio work; feels off for dashboards, dev tools, fintech,
  healthcare, or enterprise apps.
- Generic pushback ("don't use cream," "make it clean and minimal") just shifts the model to a *different*
  fixed palette, not variety. Two things reliably work instead: **(1)** give a concrete, fully-specified
  alternative spec (colors, type, layout) — it follows explicit specs precisely; or **(2)** have it **propose
  3–4 distinct visual directions first**, then implement the one picked — this is also the substitute for
  `temperature`-based variety.
- Needs **less frontend-aesthetics scaffolding** than earlier models to avoid the generic "AI slop" look;
  a short `<frontend_aesthetics>` steer (avoid Inter/Roboto/Arial, purple-gradient clichés, cookie-cutter
  layouts) is enough — no need for a lengthy prompt snippet.

## Computer use
- Supports resolutions **up to 2576px / 3.75MP**. **1080p** is the good performance/cost balance for testing;
  **720p / 1366×768** for cost-sensitive workloads.

## Version deltas
- **Opus 4.7 / 4.6:** 4.8 performs well out of the box on existing 4.7 prompts; sampling params, the `effort`
  default, 1M-context default, and refusal details changed across the migration — verify against the current
  migration guide if targeting an older Opus.
