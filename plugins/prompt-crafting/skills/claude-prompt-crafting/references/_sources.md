# Sources — claude-prompt-crafting references

**last-verified: 2026-10-12** · vendor: Anthropic · official docs only.

The `refresh-references` skill and the `check-sources.yml` workflow read the URL list below.
When updating, re-fetch each URL, reconcile `techniques.md` / `techniques-advanced.md`, then bump
the `last-verified` dates here and in those files.

| # | URL | Covers |
|---|-----|--------|
| 1 | https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/overview | Prompt-engineering router; presupposes success criteria + a way to test |
| 2 | https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices | The living reference: opens with a **model-specific guidance table** (which page to read per model), then clarity, examples, XML, roles, thinking, chaining, output/format, tool use, agentic, capability tips, migration |
| 3 | https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5 | **Opus 5** (previous Opus generation — current flagship is Opus 5.5, #9): effort default `high`, thinking on-by-default (disable only ≤ `high`), verbosity/narration, scope + over-verification, subagents |
| 4 | https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5 | **Fable 5 / Mythos 5** (still live, now the previous Fable generation): brief instructions, give-the-reason, memory file, no inline reasoning |
| 5 | _(retired 2026-07-28)_ `prompting-tools` | **RETIRED** — now 307-redirects to #2 (best-practices); the Console prompt-generator/-improver + Workbench sunset 2026-08-17. Removed from tracking (its normalized content already mirrored #2). The `{{double_bracket}}` template convention it covered is still demonstrated on #2. |
| 6 | https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-sonnet-5 | **Sonnet 5** (previous Sonnet generation — current flagship is Sonnet 5.5, #10): effort default `high`, adaptive thinking on-by-default (disable at any effort), new tokenizer, no sampling params |
| 7 | https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-4-8 | **Legacy** Opus 4.8 page (still live) — literal instruction-following, effort ladder, 64k budget, design house-style (`#F4F1EA`), computer-use toolsets |
| 8 | https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5-1 | **Fable 5.1 / Mythos 5.1** (current frontier; added 2026-09-07): effort re-sweep, progress updates, tool-call batching, append-only history, writing density, chat formatting, quoting sources, finishing the task, compaction summaries, scope/test sprawl, low-effort search, safeguard false positives, targeted edits, long outputs, async subagents, vision crop/zoom |
| 9 | https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5-5 | **Opus 5.5** (current Opus flagship; added 2026-09-28): effort default drops to `medium`, thinking cannot be disabled at all, migrating a thinking-disabled Opus 5 integration, two new safeguard-refusal categories (biology, reasoning-extraction), unattended-run text-only turn-ends, progress-update mechanics, multi-app exploration, multiagent time budgets, chat thinking instructions, pasted-text marking, vision tooling, frontend defaults |
| 10 | https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-sonnet-5-5 | **Sonnet 5.5** (current Sonnet flagship; added 2026-10-12): recalibrated effort (workload-dependent starting point), the new `between_tools` lowest-thinking setting, initiative/scope steering, JSON output on reasoning tasks, progress updates, tool use in chat, mid-turn-user-message injection misread, coding verification, tolerant tool-call handling, vision tooling, 5-category safeguard refusals (`cyber`/`bio`/`frontier_llm`/`reasoning_extraction`/`general_harms`) with partial fallback |
| 11 | https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-haiku-5-5 | **Haiku 5.5** (current Haiku flagship; added 2026-10-12) — **first-ever dedicated Haiku prompting page**: first Haiku model with `effort` levels (replaces `budget_tokens`), search grounding with today's date, JSON output with custom tools, early-stopping prevention, coding verification, mid-turn-user-message injection misread, chatbot system-prompt adherence, 4-category safeguard refusals (`cyber`/`frontier_llm`/`bio`/`general_harms`, no `reasoning_extraction`), no server-side fallback |

## Reference files → sources
Which source backs which reference file (reconcile the file when its backing source drifts). Each per-model
file also carries its own `last-verified` header.

| Reference file | Backed by |
|----------------|-----------|
| `techniques.md` · `techniques-advanced.md` | #1, #2 (template variables now covered by #2; former #5 retired) |
| `models/opus.md` (Opus 5.5 + Opus 5 deltas + legacy Opus 4.8 notes) | **#9** primary (current flagship) + **#3** (Opus 5, previous generation) + **#7** (legacy Opus 4.8) |
| `models/fable.md` (Fable 5.1 / Mythos 5.1 + Fable 5 / Mythos 5 deltas) | **#8** primary (current frontier) + **#4** for the Fable 5 base and its deltas |
| `models/sonnet.md` (Sonnet 5.5 + Sonnet 5 deltas) | **#10** primary (current flagship) + **#6** (Sonnet 5, previous generation) |
| `models/haiku.md` (Haiku 5.5 + legacy Haiku 4.5 notes) | **#11** primary (current flagship, first dedicated Haiku page) + **#2** for the legacy Haiku 4.5 section (no dedicated 4.5 page ever shipped) |

> Eleven prompting URLs are now tracked for hashing (eight from the prior cycle plus **Sonnet 5.5** and
> **Haiku 5.5**, #10–#11, discovered this cycle — both from the best-practices page's model-guidance table,
> which now lists all three current-generation flagships: Opus 5.5, Sonnet 5.5, Haiku 5.5). This refresh
> **cannot seed `.source-hashes.json` itself** — editing that file is out of scope for this cycle (the
> check-sources Action owns it exclusively); the Action (or a maintainer) needs to add `prompting-claude-opus-5-5`
> (still missing from last cycle — see below), `prompting-claude-sonnet-5-5`, and `prompting-claude-haiku-5-5`
> to it, each seeded `null`, before drift detection covers them. **`prompting-claude-opus-5-5` is still absent
> from `.source-hashes.json` as of this cycle** (`last_updated: 2026-10-05` on `main`, still only the original
> seven URLs) — flagged again in the 0.7.3 PR and still unresolved; a maintainer needs to add all three missing
> URLs in one pass. Haiku no longer lacks a dedicated page at all (resolved this cycle) — the old Haiku-overview
> fallback note only still applies to the legacy Haiku 4.5 section of `models/haiku.md`.

## Volatile items to recheck each cycle
- **Prefill removal** — applies to Claude 4.6 and newer, incl. the whole 5-series (Fable 5.1 / Mythos 5.1 /
  Fable 5 / Mythos 5 / Opus 5.5 / Opus 5 / Sonnet 5.5 / Sonnet 5 / Haiku 5.5) **and Claude Mythos Preview**;
  it's the *last* assistant turn only. *(Settled 2026-09-07: "Claude Mythos Preview" is a distinct model named
  on #2 — it links to anthropic.com/glasswing — not alternate naming for Mythos 5. It has no dedicated
  prompting page; don't re-flag it.)*
- **Effort levels & adaptive thinking** — parameter names, levels (low…max), defaults move per model
  (**Fable 5.1**: default `high`, gains largest at the top, `medium` ≈ Fable 5 at lower cost, `low`
  competitive with smaller models; **Opus 5.5** (current Opus flagship): default **`medium`** (down from
  Opus 5's `high`), thinking **cannot be disabled at all**; **Opus 5** (previous generation): default `high`,
  `low`/`medium` efficient/liberal, `xhigh` for demanding coding/agentic, thinking on by default but
  disable-able at effort ≤ `high`; **Sonnet 5.5** (new 2026-10-12 — current flagship): levels **recalibrated**
  vs. Sonnet 5 (re-sweep, don't port), `high` is the API default but pick a workload-dependent starting point
  (`medium` for well-specified agentic coding, `medium`/`low` for chat); lowest thinking setting is
  **`between_tools`** (not `disabled` — Sonnet 5.5 has no `disabled` mode), accepted at effort ≤ `high` only;
  **Sonnet 5** (previous generation): `high` default, thinking on by default, disable-able (`disabled`) at any
  effort; **Haiku 5.5** (new 2026-10-12 — current flagship, **first Haiku model with effort levels at all**):
  default **`medium`**, thinking on by default, disable-able (`disabled`) at effort ≤ `high` only (400 at
  `xhigh`/`max`) — replaces Haiku 4.5's `budget_tokens`. Legacy Opus 4.8 / Sonnet 4.6 default thinking **off**.
  The Fable family (5.1 / 5) and **Opus 5.5** are adaptive-thinking-only with no disable option at all.
  **Effort names do not map to the same amount of thinking across models or even across generations of the
  same family** — re-sweep per model, every cycle a new generation ships (Opus 5→5.5, Sonnet 5→5.5, and now
  Haiku 4.5→5.5 all moved the cost/quality curve).
- **`between_tools` thinking mode (Sonnet 5.5 only, new this cycle)** — a third thinking state alongside
  adaptive-on and (on models that support it) disabled: lowest-latency, accepted only at effort ≤ `high`
  (400 at `xhigh`/`max`), rejects `display`/`budget_tokens`/`block_binding` fields (400), and blocks
  per-message effort changes (400 — use adaptive thinking if you need mid-conversation effort changes). In a
  tool-less request it means **no thinking at all**, unlike adaptive thinking at low effort which still thinks
  when complexity warrants it — recheck whether any other model picks up this mode in a future cycle.
- **Per-model pages** — model names (Opus / Sonnet / Haiku / Fable / Mythos + versions) and their tips
  change; current set: **Fable 5.1 / Mythos 5.1** (frontier, own page — #8), Fable 5 / Mythos 5,
  **Opus 5.5** (current Opus flagship, own page — #9), Opus 5 (previous generation, own page — #3),
  **Sonnet 5.5** (current Sonnet flagship, own page — #10, added 2026-10-12), Sonnet 5 (previous generation,
  own page — #6), **Haiku 5.5** (current Haiku flagship, own page — #11, added 2026-10-12 — **the first
  dedicated Haiku prompting page ever shipped**), Haiku 4.5 (legacy, no dedicated page of its own — still
  backed by #2 + the model overview). **Opus 4.8 / 4.7 / 4.6 are legacy** (the 4.8 page is still live, tracked
  as #7). Every current-generation flagship (Opus 5.5, Sonnet 5.5, Haiku 5.5) now has a dedicated page, named
  together on the best-practices page's (#2) model-guidance table.
- **Safeguard refusal category taxonomy is widening and diverging by model** — Opus 5.5 names 3 categories
  (biology, cybersecurity, `reasoning_extraction`); **Sonnet 5.5 names 5** (`cyber`, `bio`, `frontier_llm`,
  `reasoning_extraction`, `general_harms`); **Haiku 5.5 names 4** (`cyber`, `frontier_llm`, `bio`,
  `general_harms` — **no** `reasoning_extraction`). `frontier_llm` (declining requests that could assist a
  competing model's development) is new to this cycle and appears only on the Sonnet 5.5 / Haiku 5.5 pages as
  fetched — recheck whether Opus 5.5 and the Fable family gain it too, or whether Opus 5's own page gains any
  of Opus 5.5's categories. **Server-side fallback scope also diverges by model**: Opus 5.5 retries every
  category except `reasoning_extraction`; **Sonnet 5.5 retries only `cyber` and `frontier_llm`** (not `bio`,
  `reasoning_extraction`, or `general_harms`); **Haiku 5.5 has no server-side fallback at all**. Don't assume
  parity across families — recheck each model's own page every cycle.
- **Mid-turn user messages can be misread as prompt injection (Sonnet 5.5, Haiku 5.5 — new this cycle)** — both
  pages describe the same failure: a genuine user message arriving right after a `tool_result` (inside the
  block, or as a mid-conversation system message placed directly after one) can be treated as untrusted
  injected text. Fix is the same on both: never put user text inside a `tool_result` block; append it as a
  text block after the last `tool_result` in the user turn; keep harness notices in a separate
  mid-conversation system message. Recheck whether Opus 5.5 / Fable 5.1 share this behavior — their pages as
  fetched this cycle don't mention it either way.
- **Refusal categories & fallback (Fable family)** — `reasoning_extraction` (don't ask the model to
  reproduce its reasoning as text), offensive-cyber, bio/life-sciences. **The Opus 4.8 fallback target is
  stated on #4 (Fable 5) only**; #8 defers to the untracked `whats-new-fable-5-1` page and names no model, so
  `models/fable.md` flags it rather than asserting it for 5.1 — reconfirmed still unresolved on 2026-10-12
  (and reconsider tracking that page; the Fable family's 3-category taxonomy also hasn't picked up
  `frontier_llm`/`general_harms` the way Sonnet 5.5/Haiku 5.5 have — recheck next cycle). On **Fable 5.1**
  false positives are down and source-code vulnerability finding is permitted; the three triggers
  (compile-check phrasing, lesser-known languages, base64 in tool output) persisted unchanged this cycle
  (2026-10-12).
- **Preserved thinking / append-only history** — editing earlier turns invalidates later thinking blocks: a
  400 for accounts created on or after **2026-08-31** (unchanged this cycle), still not universal as of
  2026-10-12. The best-practices page (#2) now names the affected set explicitly in its migration section:
  **Claude Fable 5.1, Claude Opus 5.5, Claude Sonnet 5.5, and Claude Haiku 5.5** — confirmed *not* Opus 5 or
  Sonnet 5 (the previous generations). The opt-in `thinking.block_binding.prefix_mismatch_behavior:
  "drop_block"` (beta, `thinking-binding-controls-2026-08-01`) escape hatch is unchanged and documented in
  `models/fable.md` and `models/opus.md`. Recheck the enforcement date and whether it has gone universal, and
  whether it extends to Sonnet 5.5 / Haiku 5.5's own pages explicitly (neither page states it in those terms
  as fetched this cycle — only the central migration note does).
- **Turn-scoped and mid-conversation system messages** — the `clear_at: "next_user_message"` and
  `thinking.display: "updates"` mechanics are in **beta** (headers `mid-conversation-system-clear-at-2026-08-21`,
  `thinking-display-updates-2026-08-18`), unchanged this cycle and now confirmed used identically on Opus 5.5
  and Sonnet 5.5. **New this cycle:** per-message effort changes need the `mid-conversation-output-config-2026-07-01`
  beta header (seen on the Haiku 5.5 page; Sonnet 5.5's page describes the same mechanism without citing the
  header string — confirm it matches next cycle). Recheck all three for GA / header changes.
- **Sonnet API constraints** — `temperature`/`top_p`/`top_k` at non-default values return 400 (unchanged,
  Sonnet 5 and carried to 5.5); manual extended-thinking `budget_tokens` is removed (400) on both generations.
  Sonnet 5's tokenizer produces ~30% more tokens for the same text vs. Sonnet 4.6 (re-check `max_tokens`
  budgets ported from 4.6); Sonnet 5.5's own page doesn't repeat a tokenizer-specific claim but does warn that
  effort levels are recalibrated — don't assume parity on either axis without re-sweeping.
- **Computer / browser tool versions** — Sonnet 5 and Opus 4.8 still list the `computer_toolset_20260801`
  toolset and `browser_toolset_20260801` alongside the older `computer_20251124` (reconfirmed on the Sonnet 5
  page this cycle, 2026-10-12); resolutions still cap at 2576px / 3.75MP. Neither the Sonnet 5.5 nor the
  Haiku 5.5 page repeats toolset version strings (their vision sections cover crop/zoom tooling only) — not
  necessarily a drop, just not reiterated; recheck if a computer-use-specific page appears for either.
- **Structured Outputs / API surface** — verify the current way to force formats. New this cycle: Sonnet 5.5's
  page documents a `stop_reason: "max_tokens"` failure mode specific to combining structured outputs with
  reasoning-heavy JSON tasks at low/medium effort — treat that stop reason as a failed attempt and retry,
  per `models/sonnet.md`.

> NOTE: Anthropic docs are also served from `docs.anthropic.com` / `docs.claude.com`; the
> `platform.claude.com` paths above are the canonical ones as of the verified date.
