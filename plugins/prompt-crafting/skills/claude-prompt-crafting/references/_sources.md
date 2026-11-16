# Sources — claude-prompt-crafting references

**last-verified: 2026-11-16** · vendor: Anthropic · official docs only.

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
| 8 | https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5-1 | **Fable 5.1 / Mythos 5.1** (**legacy as of this cycle — superseded by Fable 5.2, #13**; added 2026-09-07): effort re-sweep, progress updates, tool-call batching, append-only history, writing density, chat formatting, quoting sources, finishing the task, compaction summaries, scope/test sprawl, low-effort search, safeguard false positives, targeted edits, long outputs, async subagents, vision crop/zoom |
| 9 | https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5-5 | **Opus 5.5** (current Opus flagship; added 2026-09-28): effort default drops to `medium`, thinking cannot be disabled at all, migrating a thinking-disabled Opus 5 integration, two new safeguard-refusal categories (biology, reasoning-extraction), unattended-run text-only turn-ends, progress-update mechanics, multi-app exploration, multiagent time budgets, chat thinking instructions, pasted-text marking, vision tooling, frontend defaults |
| 10 | https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-sonnet-5-5 | **Sonnet 5.5** (current Sonnet flagship; added 2026-10-12): recalibrated effort (workload-dependent starting point), the new `between_tools` lowest-thinking setting, initiative/scope steering, JSON output on reasoning tasks, progress updates, tool use in chat, mid-turn-user-message injection misread, coding verification, tolerant tool-call handling, vision tooling, 5-category safeguard refusals (`cyber`/`bio`/`frontier_llm`/`reasoning_extraction`/`general_harms`) with partial fallback |
| 11 | https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-haiku-5-5 | **Haiku 5.5** (current Haiku flagship; added 2026-10-12) — **first-ever dedicated Haiku prompting page**: first Haiku model with `effort` levels (replaces `budget_tokens`), search grounding with today's date, JSON output with custom tools, early-stopping prevention, coding verification, mid-turn-user-message injection misread, chatbot system-prompt adherence, 4-category safeguard refusals (`cyber`/`frontier_llm`/`bio`/`general_harms`, no `reasoning_extraction`), no server-side fallback |
| 12 | https://platform.claude.com/docs/en/models/fable-5-1/whats-new-fable-5-1 | **Untracked, cited only to resolve a specific fact** (not added to `.source-hashes.json` — out of scope, owned by the check-sources Action): its "Refusals, fallback, and billing" section states "The permitted fallback targets for Claude Fable 5.1 are Claude Opus 4.8 and Claude Opus 5" — resolves the fallback-target ambiguity flagged in `models/fable.md` for four prior cycles (the dedicated 5.1 prompting page, #8, links here instead of naming a model itself) |
| 13 | https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5-2 | **New this cycle — Fable 5.2 / Mythos 5.2 (now the current Fable flagship, superseding 5.1).** Discovered via the Fable 5.1 model-overview page ("Claude Fable 5.1 is a legacy model, and Claude Fable 5.2 is the current Fable model") and the best-practices page's (#2) now-updated model-guidance table. Covers: effort calibration, finishing the whole task, approvals, code ownership, user-facing progress updates, subagent delegation expectations, caution that builds up across sessions, reviewing prompts/harnesses written for earlier models, writing reports for low-context readers, and a widened (5-category) safeguard-refusal taxonomy. **Not yet added to `.source-hashes.json`** — out of scope this cycle, owned by the check-sources Action; flagged below alongside the still-missing Opus 5.5 / Sonnet 5.5 / Haiku 5.5 entries |
| 14 | https://platform.claude.com/docs/en/models/fable-5-2/whats-new-fable-5-2 | **New this cycle, untracked** (cited only for facts the dedicated prompting page, #13, doesn't itself state): its "Refusals, fallback, and billing" section names the permitted fallback targets for Claude Fable 5.2 as Claude Opus 4.8 and Claude Opus 5 (same as 5.1); also the source for the four breaking API changes (prefix-check 400s, thinking-block model-pairing, `computer_20251124` retirement, advisor-tool pairing) and pricing (Fable 5.2 input/output run ~20% cheaper than Fable 5.1) |

## Reference files → sources
Which source backs which reference file (reconcile the file when its backing source drifts). Each per-model
file also carries its own `last-verified` header.

| Reference file | Backed by |
|----------------|-----------|
| `techniques.md` · `techniques-advanced.md` | #1, #2 (template variables now covered by #2; former #5 retired) |
| `models/opus.md` (Opus 5.5 + Opus 5 deltas + legacy Opus 4.8 notes) | **#9** primary (current flagship) + **#3** (Opus 5, previous generation) + **#7** (legacy Opus 4.8) |
| `models/fable.md` (Fable 5.2 / Mythos 5.2 + legacy Fable 5.1 / Fable 5 deltas) | **#13** primary (current frontier) + **#8** (Fable 5.1, now legacy) + **#4** (Fable 5 base) + **#12**, **#14** (untracked, cited only for fallback-target facts) |
| `models/sonnet.md` (Sonnet 5.5 + Sonnet 5 deltas) | **#10** primary (current flagship) + **#6** (Sonnet 5, previous generation) |
| `models/haiku.md` (Haiku 5.5 + legacy Haiku 4.5 notes) | **#11** primary (current flagship, first dedicated Haiku page) + **#2** for the legacy Haiku 4.5 section (no dedicated 4.5 page ever shipped) |

> Thirteen prompting URLs are now identified (eleven previously tracked plus **Fable 5.2**, #13, discovered
> this cycle from the Fable 5.1 model-overview page's "Fable 5.1 is a legacy model, Fable 5.2 is the current
> Fable model" notice and the best-practices page's now-updated model-guidance table). This refresh **cannot
> seed `.source-hashes.json` itself** — editing that file is out of scope for this cycle (the check-sources
> Action owns it exclusively); the Action (or a maintainer) needs to add `prompting-claude-fable-5-2`,
> `prompting-claude-opus-5-5`, `prompting-claude-sonnet-5-5`, and `prompting-claude-haiku-5-5` — each seeded
> `null` — before drift detection covers them. **All four are still absent from `.source-hashes.json` as of
> this cycle** (only the original seven URLs are tracked) — the Opus/Sonnet/Haiku 5.5 gap was flagged again in
> the 0.7.5/0.7.6 PRs and remains unresolved; Fable 5.2 is a new instance of the same gap, and a structural one:
> **hash-diffing can only ever flag drift on a URL already in the file — it cannot discover a brand-new page.**
> The Fable 5.2 release was found by this cycle's manual source-by-source fetch, not by the Action, precisely
> because no hash entry existed to drift. A maintainer should add all four URLs in one pass.

## Volatile items to recheck each cycle
- **Prefill removal** — applies to Claude 4.6 and newer, incl. the whole 5-series (Fable 5.2 / Mythos 5.2 /
  Fable 5.1 / Mythos 5.1 / Fable 5 / Mythos 5 / Opus 5.5 / Opus 5 / Sonnet 5.5 / Sonnet 5 / Haiku 5.5) **and
  Claude Mythos Preview**; it's the *last* assistant turn only. *(Settled 2026-09-07: "Claude Mythos Preview"
  is a distinct model named on #2 — it links to anthropic.com/glasswing — not alternate naming for Mythos 5.
  It has no dedicated prompting page; don't re-flag it.)*
- **Effort levels & adaptive thinking** — parameter names, levels (low…max), defaults move per model
  (**Fable 5.2** (new this cycle — current frontier): default `high`, re-sweep rather than porting a 5.1
  value, most of the capability gain is already present at `high`, `low` scores close to what 5.1 needed
  higher effort for; **Fable 5.1** (now legacy): default `high`, gains largest at the top, `medium` ≈ Fable 5
  at lower cost, `low` competitive with smaller models; **Opus 5.5** (current Opus flagship): default
  **`medium`** (down from Opus 5's `high`), thinking **cannot be disabled at all**; **Opus 5** (previous
  generation): default `high`, `low`/`medium` efficient/liberal, `xhigh` for demanding coding/agentic,
  thinking on by default but disable-able at effort ≤ `high`; **Sonnet 5.5** (current flagship): levels
  **recalibrated** vs. Sonnet 5 (re-sweep, don't port), `high` is the API default but pick a
  workload-dependent starting point (`medium` for well-specified agentic coding, `medium`/`low` for chat);
  lowest thinking setting is **`between_tools`** (not `disabled` — Sonnet 5.5 has no `disabled` mode),
  accepted at effort ≤ `high` only; **Sonnet 5** (previous generation): `high` default, thinking on by
  default, disable-able (`disabled`) at any effort; **Haiku 5.5** (current flagship, **first Haiku model
  with effort levels at all**): default **`medium`**, thinking on by default, disable-able (`disabled`) at
  effort ≤ `high` only (400 at `xhigh`/`max`) — replaces Haiku 4.5's `budget_tokens`. Legacy Opus 4.8 /
  Sonnet 4.6 default thinking **off**. The Fable family (5.2 / 5.1 / 5) and **Opus 5.5** are
  adaptive-thinking-only with no disable option at all. **Effort names do not map to the same amount of
  thinking across models or even across generations of the same family** — re-sweep per model, every cycle a
  new generation ships (Opus 5→5.5, Sonnet 5→5.5, Haiku 4.5→5.5, and now Fable 5.1→5.2 all moved the
  cost/quality curve).
- **`between_tools` thinking mode (Sonnet 5.5 only, new this cycle)** — a third thinking state alongside
  adaptive-on and (on models that support it) disabled: lowest-latency, accepted only at effort ≤ `high`
  (400 at `xhigh`/`max`), rejects `display`/`budget_tokens`/`block_binding` fields (400), and blocks
  per-message effort changes (400 — use adaptive thinking if you need mid-conversation effort changes). In a
  tool-less request it means **no thinking at all**, unlike adaptive thinking at low effort which still thinks
  when complexity warrants it — recheck whether any other model picks up this mode in a future cycle.
- **Per-model pages** — model names (Opus / Sonnet / Haiku / Fable / Mythos + versions) and their tips
  change; current set: **Fable 5.2 / Mythos 5.2** (new this cycle — current frontier, own page — #13),
  Fable 5.1 / Mythos 5.1 (**now legacy**, own page — #8), Fable 5 / Mythos 5, **Opus 5.5** (current Opus
  flagship, own page — #9), Opus 5 (previous generation, own page — #3), **Sonnet 5.5** (current Sonnet
  flagship, own page — #10), Sonnet 5 (previous generation, own page — #6), **Haiku 5.5** (current Haiku
  flagship, own page — #11 — **the first dedicated Haiku prompting page ever shipped**), Haiku 4.5 (legacy,
  no dedicated page of its own — still backed by #2 + the model overview). **Opus 4.8 / 4.7 / 4.6 are
  legacy** (the 4.8 page is still live, tracked as #7). Every current-generation flagship across all four
  families (Fable 5.2, Opus 5.5, Sonnet 5.5, Haiku 5.5) now has a dedicated page, named together on the
  best-practices page's (#2) model-guidance table. Re-checked this cycle: Opus 5.5, Sonnet 5.5, and Haiku
  5.5 are all still current — no "5.6" generation has shipped for any of those three families; Fable is the
  only family that moved.
- **Safeguard refusal category taxonomy is widening and diverging by model** — Opus 5.5 names 3 categories
  (biology, cybersecurity, `reasoning_extraction`); **Sonnet 5.5 names 5** (`cyber`, `bio`, `frontier_llm`,
  `reasoning_extraction`, `general_harms`); **Haiku 5.5 names 4** (`cyber`, `frontier_llm`, `bio`,
  `general_harms` — **no** `reasoning_extraction`); **Fable 5.2 names 5 plus a `null` fallback** (`cyber`,
  `bio`, `frontier_llm`, `reasoning_extraction`, `general_harms`, `null`) — widened this cycle from Fable
  5.1's 3 (`cyber`, `bio`, `reasoning_extraction`, no `frontier_llm`/`general_harms`), now matching Sonnet
  5.5's taxonomy plus the explicit `null` catch-all. `frontier_llm` (declining requests that could assist a
  competing model's development) now appears on Sonnet 5.5, Haiku 5.5, and Fable 5.2 — still absent from
  Opus 5.5's own page as fetched this cycle; recheck next cycle whether Opus 5.5 gains it too. **Resolved
  2026-11-02:** the dedicated **Opus 5** page (previous generation, #3) carries its own "Reasoning in the
  response" section naming `reasoning_extraction` — so that category was not new to Opus 5.5, only
  **biology** was. Re-fetch the best-practices page's own cross-model note (its "rely on thinking instead"
  list names Opus 5, Opus 5.5, Fable 5.2, Fable 5.1, Fable 5, and Sonnet 5.5 for this as of this cycle — still
  not Haiku 5.5) if the model list there changes again. **Server-side fallback scope also diverges by
  model**: Opus 5.5 retries every category except `reasoning_extraction`; **Sonnet 5.5 retries only `cyber`
  and `frontier_llm`** (not `bio`, `reasoning_extraction`, or `general_harms`); **Haiku 5.5 has no
  server-side fallback at all**; **Fable 5.2 and Fable 5.1 both fall back to Claude Opus 4.8 or Claude
  Opus 5**, with categories that have no recommended fallback (e.g. `reasoning_extraction`) returning the
  refusal unretried. Don't assume parity across families — recheck each model's own page every cycle.
- **Mid-turn user messages can be misread as prompt injection (Sonnet 5.5, Haiku 5.5 — new this cycle)** — both
  pages describe the same failure: a genuine user message arriving right after a `tool_result` (inside the
  block, or as a mid-conversation system message placed directly after one) can be treated as untrusted
  injected text. Fix is the same on both: never put user text inside a `tool_result` block; append it as a
  text block after the last `tool_result` in the user turn; keep harness notices in a separate
  mid-conversation system message. Recheck whether Opus 5.5 / Fable 5.1 share this behavior — their pages as
  fetched this cycle don't mention it either way.
- **Refusal categories & fallback (Fable family)** — **Fable 5.2** (new this cycle) widened to 5 named
  categories plus `null` (`cyber`, `bio`, `frontier_llm`, `reasoning_extraction`, `general_harms`, `null`) —
  see the taxonomy item above. Its untracked "What's new in Claude Fable 5.2" page (#14) states **"The
  permitted fallback targets for Claude Fable 5.2 are Claude Opus 4.8 and Claude Opus 5"** — unchanged from
  5.1's targets despite the wider taxonomy. **Fable 5.1** (now legacy) keeps its narrower 3-category taxonomy
  (`cyber`, `bio`, `reasoning_extraction`) and the same two fallback targets, resolved last cycle
  (2026-11-09) via its own untracked "What's new" page (#12) after sitting unconfirmed for four prior
  cycles. `models/fable.md` and `examples.md` updated to match both generations. On **Fable 5.2** (new) and
  **Fable 5.1**, false positives are down from Fable 5's launch and source-code vulnerability finding is
  permitted; the three triggers (compile-check phrasing, lesser-known languages, base64 in tool output)
  persisted unchanged this cycle (2026-11-16) and apply to both generations.
- **Preserved thinking / append-only history** — editing earlier turns invalidates later thinking blocks: a
  400 for accounts created on or after **2026-08-31** (unchanged this cycle), still not universal as of
  2026-11-16. The best-practices page's (#2) migration note now enumerates **seven** models — "Claude Fable
  5.2, Claude Mythos 5.2, Claude Fable 5.1, Claude Mythos 5.1, Claude Opus 5.5, Claude Sonnet 5.5, and Claude
  Haiku 5.5" — up from the four named last cycle (Fable 5.1, Opus 5.5, Sonnet 5.5, Haiku 5.5): Fable 5.2 and
  Mythos 5.2 are the additions, confirmed independently on Fable 5.2's own "What's new" page (#14, its
  "Editing earlier turns invalidates thinking blocks" breaking-change section). Still confirmed *not* Fable
  5/Mythos 5, Opus 5, or Sonnet 5. The opt-in `thinking.block_binding.prefix_mismatch_behavior: "drop_block"`
  (beta, `thinking-binding-controls-2026-08-01`) escape hatch is unchanged and documented in `models/fable.md`
  and `models/opus.md`. Recheck the enforcement date and whether it has gone universal, and whether it
  extends to Sonnet 5.5 / Haiku 5.5's own pages explicitly (neither states it in those terms as fetched this
  cycle — only the central migration note and the Fable pages do). One previously untracked nuance, still not
  folded into our docs as it's Mythos-specific and below this library's bar for per-model nuance: the
  enforcement table gives **Claude Mythos 5.1** a 400 regardless of account-creation date (unlike the other
  5.1-era models) — recheck whether Mythos 5.2 inherits the same carve-out.
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
  toolset and `browser_toolset_20260801` alongside the older `computer_20251124`; resolutions still cap at
  2576px / 3.75MP. Neither the Sonnet 5.5 nor the Haiku 5.5 page repeats toolset version strings (their
  vision sections cover crop/zoom tooling only) — not necessarily a drop, just not reiterated; recheck if a
  computer-use-specific page appears for either. **New this cycle:** Fable 5.2 retires the older
  `computer_20251124` tool outright (400 on every platform except Amazon Bedrock) — only the
  `computer_toolset_20260801` toolset is accepted elsewhere, per its untracked "What's new" page (#14).
- **Structured Outputs / API surface** — verify the current way to force formats. New this cycle: Sonnet 5.5's
  page documents a `stop_reason: "max_tokens"` failure mode specific to combining structured outputs with
  reasoning-heavy JSON tasks at low/medium effort — treat that stop reason as a failed attempt and retry,
  per `models/sonnet.md`.

> NOTE: Anthropic docs are also served from `docs.anthropic.com` / `docs.claude.com`; the
> `platform.claude.com` paths above are the canonical ones as of the verified date.
