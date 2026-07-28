<!--
last-verified: 2026-07-28
source: _sources.md #2 — claude-prompting-best-practices (cross-model) + the Haiku 4.5 model overview.
No dedicated Haiku prompting page exists as of last-verified (the per-model prompting pages cover Opus 5,
Sonnet 5, and Fable 5 / Mythos 5 only). Loaded at craft time only when the target model is Haiku.
-->

# Tuning for Claude Haiku 4.5

Haiku 4.5 is the **fast, low-cost** model — built for high-volume, latency-sensitive, well-scoped work:
classification, extraction, routing, tagging, short generation, and cheap steps inside a larger pipeline.
There is no Haiku-specific prompting page; the difference is in **how tightly you prompt it**.

## How to tune
- **Be tighter and more explicit than you'd be for Opus.** Spell out the exact task, the exact output shape,
  and the constraints; leave less to inference.
- **Lean hard on examples and format control.** Multishot is one of the most reliable levers here: 3–5
  diverse `<example>`s plus an explicit output format (or **Structured Outputs**) lock behavior far better
  than prose description alone.
- **Keep the prompt focused.** Fewer, high-value instructions beat a long list; don't bury the task in
  context it doesn't need.
- **Don't lean on deep multi-step reasoning.** For hard reasoning, either decompose the task into small,
  well-defined steps or route that step to Sonnet/Opus. Use Haiku for the many cheap, well-scoped calls.
- **No prefill** (4.6/4.5-era and newer): force format via Structured Outputs or a direct instruction.

## When to pick Haiku
- High-throughput or latency-critical steps where the task is well-defined and the format is fixed. Step
  **up to Sonnet** when a step needs more general capability or non-trivial reasoning.
