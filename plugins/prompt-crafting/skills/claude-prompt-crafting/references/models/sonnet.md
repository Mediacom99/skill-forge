<!--
last-verified: 2026-07-03
source: _sources.md #2 — claude-prompting-best-practices (cross-model) + the Sonnet 4.6 model overview.
No dedicated Sonnet prompting page exists as of last-verified (the per-model prompting pages cover Opus 4.8
and Fable 5 / Mythos 5 only). Loaded at craft time only when the target model is Sonnet.
-->

# Tuning for Claude Sonnet 4.6

Sonnet 4.6 is the **balanced general-purpose workhorse** — the sensible default for most production and
programmatic work where you want strong capability without Opus-level cost or latency. There is no
Sonnet-specific prompting page; it takes the **core techniques in `techniques.md`** cleanly. Tune from there.

## How to tune
- **Apply the lean core as-is.** Role in system, XML structure, positive instructions with the reason,
  3–5 diverse examples, explicit success criteria and scope, match prompt style to output.
- **`effort` to the task.** Raise it for multi-step reasoning, coding, and agentic work; keep it lower for
  scoped, latency-sensitive calls. (Exact levels are model-specific — see `techniques-advanced.md`.)
- **Adaptive thinking** where supported: let it decide when to think, calibrated by effort; keep it off for
  simple, high-throughput calls.
- **No prefill** (4.6 and newer): force format via Structured Outputs or a direct instruction, not by
  prefilling the assistant turn.
- **State scope explicitly** on multi-part outputs — like other current models it follows instructions
  literally and won't silently generalize one item to all.

## When to pick Sonnet
- Default for balanced production prompts, API pipelines, and everyday agentic tasks. Step **up to Opus** for
  the hardest long-horizon/agentic/reasoning work; step **down to Haiku** for high-volume, latency-sensitive,
  well-scoped tasks.
