<!--
last-verified: 2026-07-27
source: _sources.md #7 — prompting-claude-opus-5 (dedicated Opus 5 page, current flagship); #3 — dedicated
Opus 4.8 page (prior flagship, kept for the migration-deltas section below)
scope: Per-model tuning for Claude Opus 5 (current Opus flagship). Loaded at craft time only when the
target model is Opus. Applies on top of techniques.md; note 4.8/4.7/4.6 deltas inline.
-->

# Tuning for Claude Opus 5

Opus 5 is the flagship for complex agentic coding, long-horizon agentic work, and enterprise/knowledge work.
It performs well out of the box on existing Opus 4.8 prompts, but several **defaults changed**: read the
migration deltas below before porting a 4.8 prompt as-is. It completes full tasks rather than leaving stubs,
and performs best when given the complete task spec upfront and left to run.

## Effort is the primary lever
- Ladder (intelligence ↔ latency/cost): `max` · `xhigh` · `high` · `medium` · `low` — Opus 5 supports all five.
  - **`high`** — the **default**. Balances token usage and intelligence for most use cases.
  - **`xhigh`** — for demanding coding and agentic work.
  - **`max`** — when a task justifies genuinely unconstrained token spend.
  - **`medium` / `low`** — use liberally as the primary lever for token cost and response time; Opus 5 holds
    quality well at lower effort (unlike prior Opus generations, where `low` carried real under-thinking risk).
- **Don't carry over an old effort default.** If migrating a prompt tuned for Opus 4.8's `xhigh`-for-coding
  guidance, re-run an effort sweep against your own evals — Opus 5's lower levels are strong enough that the
  right default may now be `medium` or `low`.
- At **`xhigh`/`max`, set a large max-output budget** (start ~**64k tokens**) so it has room to think and act
  across subagents and tool calls.

## Thinking — default flipped vs. 4.8, and disabling it is now capped
- **Thinking is ON by default on Opus 5.** A request with no `thinking` field now runs with adaptive thinking —
  on Opus 4.8 the same request ran with thinking off. Because `max_tokens` is a hard cap on *thinking + response
  text combined*, **revisit `max_tokens` budgets** ported from Opus 4.8 workloads that previously ran without
  thinking.
- **Disabling thinking (`thinking: {type: "disabled"}`) is only accepted at effort `high` or below.** Combining
  it with `xhigh` or `max` effort returns a **400 error** — Opus 4.8 accepted that combination, so audit any
  request that disables thinking before migrating.
- For most tasks, **thinking enabled at `low` effort outperforms thinking disabled** at similar cost — prefer
  that over disabling thinking to save tokens.
- Adaptive-thinking triggering is steerable: if a large/complex system prompt makes it think more than wanted,
  add a line to only think when it will meaningfully improve the answer.

## Response length is not controlled by effort
- Opus 5's default user-facing responses run **longer** than prior Opus models', and unlike effort's usual
  effect elsewhere, raising or lowering effort does **not reliably change visible response length** — effort
  controls thinking volume, not what's shown. To control length, **prompt for it explicitly**: "Keep responses
  focused, brief, and concise; keep disclaimers short; give a high-level summary unless an in-depth explanation
  is specifically requested."
- **Written deliverables (files, reports, Markdown docs) are also longer by default**, separate from
  conversational verbosity — calibrate this separately: "Match the length of written documents to what the
  task needs; don't pad with filler sections, redundant summaries, or boilerplate."

## Narrates readily — tune the cadence
- Opus 5 tends to announce what it's about to do before tool calls, and per-message output in agentic sessions
  runs longer than prior models'. If you want less narration, describe the cadence directly (e.g. one sentence
  before the first tool call, brief updates only on findings/direction changes, lead the final summary with the
  outcome). Positive examples of the style you want steer better than "don't announce things."

## Verifies and self-corrects without being told — remove old scaffolding
- **This is the biggest behavioral flip from Opus 4.8.** Opus 4.8-era prompts often *added* explicit
  verification instructions ("include a final check," "use a subagent to verify") to get coverage. On Opus 5,
  those same instructions cause **over-verification** — wasted tokens with no quality gain, because Opus 5
  already verifies and self-corrects its own work by default. **Remove them when migrating** rather than
  rewriting them.
- Same for self-correction nudges ("double-check your answer," "re-verify before responding") — redundant with
  built-in behavior, and it also **narrates corrections** more than prior models. If that's undesirable in a
  user-facing product, scope it down: only surface a correction when the error would actually change the
  user's code, conclusions, or decisions.

## Task scope — state it explicitly for narrow asks
- Opus 5 can expand a task's scope on its own initiative (adding unrequested steps, applying its own judgment
  about what "the task" should include). For narrow asks, state the intended scope directly: deliver what was
  asked, make routine judgment calls itself, and check in only when different readings would lead to
  materially different work.
- Like current Sonnet/Fable, it interprets prompts **literally**, especially at lower effort; it will not
  silently generalize one instruction to other items. State scope explicitly when an instruction should apply
  broadly ("Apply this to every section, not just the first.").

## Running with thinking disabled — output artifacts
- If you must keep thinking off (e.g. capped at effort `high`), watch for two artifacts: **(1)** a tool call
  occasionally written into the visible text instead of a structured call — the turn completes, the call never
  runs, and the leaked text persists in later-turn context; **(2)** internal `<thinking>` or other XML tags
  leaking into visible output. The primary mitigation is to **keep thinking on at a lower effort** instead of
  disabling it. If disabling is required, give explicit permission to speak briefly before a tool call and a
  general "no internal/system XML tags" rule — don't name thinking tags specifically, which increases leakage.

## Subagent spawning — delegates more readily than prior Opus
- Opus 5 delegates to subagents more readily than Opus 4.8 and coordinates multi-agent teams well (effective
  writer-verifier patterns, few overwrite conflicts). Delegation pays off on genuinely independent, sizeable
  work; it multiplies cost on small tasks. For cost-sensitive workloads, cap delegation explicitly: delegate
  only for large, genuinely parallelizable work, don't delegate what a handful of direct tool calls would
  finish, and don't spawn a subagent just to verify/double-check its own work.

## Code-review harnesses
- High precision **and** recall on bug-finding, holding accuracy at lower effort (a fast pass at low/medium,
  a thorough pass later is viable). Still follows "only report high-severity / be conservative" literally and
  may under-report as a result — for coverage, ask it to report every finding with confidence + severity and
  filter downstream, same as prior Opus/Sonnet generations.

## Design and frontend defaults
*(Carried over from the Opus 4.8 page — Opus 5's own dedicated page doesn't yet restate design guidance, and
nothing found this cycle contradicts it; reverify against a live page if Anthropic publishes Opus 5-specific
design guidance.)*
- Has a **persistent default house style** on open-ended briefs: warm cream/off-white backgrounds
  (~`#F4F1EA`), serif display type (Georgia, Fraunces, Playfair), italic word-accents, terracotta/amber
  accent. Reads well for editorial/hospitality/portfolio work; feels off for dashboards, dev tools, fintech,
  healthcare, or enterprise apps.
- Generic pushback ("don't use cream," "make it clean and minimal") just shifts the model to a *different*
  fixed palette, not variety. Two things reliably work instead: **(1)** give a concrete, fully-specified
  alternative spec (colors, type, layout) — it follows explicit specs precisely; or **(2)** have it **propose
  4 distinct visual directions first**, then implement the one picked — this is also the substitute for
  `temperature`-based variety.
- Needs **less frontend-aesthetics scaffolding** than earlier models to avoid the generic "AI slop" look;
  a short `<frontend_aesthetics>` steer (avoid Inter/Roboto/Arial, purple-gradient clichés, cookie-cutter
  layouts) is enough — no need for a lengthy prompt snippet.

## Computer use
*(Also carried over from the Opus 4.8 page for the same reason as Design above.)*
- Supports resolutions **up to 2576px / 3.75MP**. **1080p** is the good performance/cost balance for testing;
  **720p / 1366×768** for cost-sensitive workloads.

## Migration deltas from Opus 4.8 (and earlier)
- **Thinking on by default; disabling capped at `high` effort** — see Thinking above, the largest behavioral
  change in this migration.
- **Effort default unchanged** — still `high` if you already set it explicitly.
- **1M-token context window is now the default**, with no beta header required (drop any compatibility header
  your client was passing for older models).
- **Prompt-caching minimum dropped to 512 tokens** (lower than 4.8) — prompts too short to cache before may
  cache now with no code changes.
- **Refusal `stop_details` is now publicly documented** — declines identify a refusal category, not just the
  `refusal` stop reason.
- **Sampling params unchanged**: `temperature`/`top_p`/`top_k` at non-default values still return 400, same as
  on 4.8.
- **Opus 4.7 / 4.6:** mid-conversation `role: "system"` messages (accepted since 4.8, rejected with a 400 on
  4.7), sampling params, the effort default, and refusal details changed across that earlier migration —
  verify against the current migration guide if targeting an older Opus directly.
