<!--
last-verified: 2026-07-03
source: _sources.md #6 — prompting-claude-sonnet-5 (dedicated Sonnet 5 prompting page)
scope: Per-model tuning for Claude Sonnet 5 (current Sonnet flagship). Loaded at craft time only when the
target model is Sonnet. Applies on top of techniques.md; note the 4.6 migration deltas inline.
-->

# Tuning for Claude Sonnet 5

Sonnet 5 is the **balanced, agentic workhorse** — particular strengths in coding and agentic tasks, and the
sensible default for most production/programmatic work. It performs well out of the box on existing Sonnet 4.6
prompts, but several **defaults changed**: read the migration deltas below before porting a 4.6 prompt as-is.

## Effort is the primary lever
- Ladder (intelligence ↔ latency/cost): `max` · `xhigh` · `high` · `medium` · `low`.
  - **`high`** — the **default** (same default as Sonnet 4.6). Balances token usage and intelligence for most use cases.
  - **`xhigh`** — recommended for the **hardest coding and agentic** use cases.
  - **`medium`** — cost-sensitive work that can trade off some intelligence.
  - **`low`** — short, scoped, latency-sensitive work only. Sonnet 5 scopes **strictly** at the low end; real
    under-thinking risk on moderately complex tasks at `low`.
  - **`max`** — absolute maximum capability, no constraint on token spend.
- **Cross-model mapping when migrating from 4.6:** Sonnet 5 at `medium` ≈ Sonnet 4.6 at `high`; Sonnet 5 at
  `high` ≈ Sonnet 4.6 at `max`. Match by observed thinking length, not by effort name alone.
- If reasoning looks shallow on a hard problem, **raise `effort`** rather than prompting around it.

## Thinking — default flipped vs. 4.6
- **Adaptive thinking is ON by default on Sonnet 5.** A request with no `thinking` field now runs with
  adaptive thinking — on Sonnet 4.6 the same request ran with thinking off. To turn it off entirely, pass
  `thinking: {type: "disabled"}`.
- Because `max_tokens` is a hard cap on *thinking + response text combined*, **revisit `max_tokens` budgets**
  ported from Sonnet 4.6 workloads that previously ran with thinking off.
- **Manual extended thinking (`budget_tokens`) is removed** — passing it returns a 400 error (it was already
  deprecated on 4.6). Use adaptive thinking + `effort` instead.
- Adaptive-thinking triggering is steerable: if a large/complex system prompt makes it think more than wanted,
  add a line to only think when it will meaningfully improve the answer.

## New tokenizer — re-check `max_tokens`
- Sonnet 5 uses a **new tokenizer that produces ~30% more tokens for the same text** than Sonnet 4.6's. A
  `max_tokens` budget tuned for 4.6 can now truncate equivalent output (worse at `xhigh`/`max`, where adaptive
  thinking can consume a large share of the budget — watch for `stop_reason: "max_tokens"` with a mostly-thinking,
  truncated response). Raise `max_tokens` or drop effort if you see this.

## Sampling parameters are rejected
- **`temperature`, `top_p`, `top_k` set to a non-default value now return a 400 error** — new for Sonnet-class
  models. Drop any reliance on `temperature` for output variety; use system-prompt instructions instead (e.g.
  "propose N distinct directions, then commit to one" — see Design below).

## Literal instruction-following → state scope
- Like current Opus/Fable, Sonnet 5 interprets prompts literally, especially at lower effort; it won't silently
  generalize one instruction to other items. State scope explicitly when an instruction should apply broadly
  ("Apply this to every section, not just the first.").

## Tool use & agentic behavior
- **More agentic than Sonnet 4.6 by default** — reaches for tools and runs self-verification loops more readily.
- **With thinking disabled, it's less likely to reach for tools** — if you rely on tool calls with thinking off,
  add an explicit nudge in the system prompt.
- `high`/`xhigh` effort shows substantially more tool use in agentic search and coding.
- Gives good interim progress updates on its own — remove forced "summarize every N calls" scaffolding.
- **Code-review harnesses:** follows "only report high-severity / be conservative" faithfully and may under-report
  low-severity bugs as a result (precision up, measured recall down). For coverage, ask it to report every
  finding with confidence + severity and filter downstream.

## Design & frontend defaults
- Can settle into a consistent default visual style on open-ended briefs. Since `temperature` can no longer be
  used for variety, prefer: (1) a concrete, fully-specified alternative spec, or (2) "propose 4 distinct visual
  directions first, then implement the one picked" — the reliable ways to break the default now.

## Computer use
- Supports the `computer_20251124` tool version, up to 2576px / 3.75MP. 1080p is the good performance/cost
  balance for testing; 720p / 1366×768 for cost-sensitive workloads.

## When to pick Sonnet
- Default for balanced production prompts, API pipelines, and coding/agentic tasks. Step **up to Opus** for the
  hardest long-horizon/agentic/reasoning work; step **down to Haiku** for high-volume, latency-sensitive,
  well-scoped tasks.
