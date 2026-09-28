# Sources — claude-prompt-crafting references

**last-verified: 2026-09-28** · vendor: Anthropic · official docs only.

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
| 6 | https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-sonnet-5 | Sonnet-specific: effort default/ladder, adaptive thinking on-by-default, new tokenizer, no sampling params |
| 7 | https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-4-8 | **Legacy** Opus 4.8 page (still live) — literal instruction-following, effort ladder, 64k budget, design house-style (`#F4F1EA`), computer-use toolsets |
| 8 | https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5-1 | **Fable 5.1 / Mythos 5.1** (current frontier; added 2026-09-07): effort re-sweep, progress updates, tool-call batching, append-only history, writing density, chat formatting, quoting sources, finishing the task, compaction summaries, scope/test sprawl, low-effort search, safeguard false positives, targeted edits, long outputs, async subagents, vision crop/zoom |
| 9 | https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5-5 | **Opus 5.5** (current Opus flagship; added 2026-09-28): effort default drops to `medium`, thinking cannot be disabled at all, migrating a thinking-disabled Opus 5 integration, two new safeguard-refusal categories (biology, reasoning-extraction), unattended-run text-only turn-ends, progress-update mechanics, multi-app exploration, multiagent time budgets, chat thinking instructions, pasted-text marking, vision tooling, frontend defaults |

## Reference files → sources
Which source backs which reference file (reconcile the file when its backing source drifts). Each per-model
file also carries its own `last-verified` header.

| Reference file | Backed by |
|----------------|-----------|
| `techniques.md` · `techniques-advanced.md` | #1, #2 (template variables now covered by #2; former #5 retired) |
| `models/opus.md` (Opus 5.5 + Opus 5 deltas + legacy Opus 4.8 notes) | **#9** primary (current flagship) + **#3** (Opus 5, previous generation) + **#7** (legacy Opus 4.8) |
| `models/fable.md` (Fable 5.1 / Mythos 5.1 + Fable 5 / Mythos 5 deltas) | **#8** primary (current frontier) + **#4** for the Fable 5 base and its deltas |
| `models/sonnet.md` | **#6** — dedicated Sonnet 5 prompting page |
| `models/haiku.md` | **#2** + the Haiku 4.5 model overview — **no dedicated prompting page** exists as of last-verified (reconfirmed 404 on `prompting-claude-haiku-4-5` on 2026-09-28) |

> Eight prompting URLs are now tracked for hashing (seven previously + the new **Opus 5.5** page, #9, added
> this cycle). This refresh **cannot seed `.source-hashes.json` itself** — editing that file is out of scope
> for this cycle (the check-sources Action owns it exclusively); the Action (or a maintainer) needs to add
> `https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5-5` to it,
> seeded `null`, before drift detection covers it. The Haiku overview page is not tracked — it churns on
> pricing/availability; `models/haiku.md`'s substance comes from the cross-model best-practices page (#2). Add
> a new tracked URL only if Anthropic ships a dedicated Haiku page.

## Volatile items to recheck each cycle
- **Prefill removal** — applies to Claude 4.6 and newer, incl. the whole 5-series (Fable 5.1 / Mythos 5.1 /
  Fable 5 / Mythos 5 / Opus 5.5 / Opus 5 / Sonnet 5) **and Claude Mythos Preview**; it's the *last* assistant
  turn only. *(Settled 2026-09-07: "Claude Mythos Preview" is a distinct model named on #2 — it links to
  anthropic.com/glasswing — not alternate naming for Mythos 5. It has no dedicated prompting page; don't
  re-flag it.)*
- **Effort levels & adaptive thinking** — parameter names, levels (low…max), defaults move per model
  (**Fable 5.1**: default `high`, gains largest at the top, `medium` ≈ Fable 5 at lower cost, `low`
  competitive with smaller models; **Opus 5.5** (new 2026-09-28 — current flagship): default **`medium`**
  (down from Opus 5's `high`), thinking **cannot be disabled at all**; **Opus 5** (previous generation):
  default `high`, `low`/`medium` efficient/liberal, `xhigh` for demanding coding/agentic, thinking on by
  default but disable-able at effort ≤ `high`; **Sonnet 5**: `high` default, thinking on by default,
  disable-able at any effort. Legacy Opus 4.8 / Sonnet 4.6 default thinking **off**. The Fable family
  (5.1 / 5) and **Opus 5.5** are adaptive-thinking-only with no disable option at all.) **Effort names do not
  map to the same amount of thinking across models** — re-sweep per model, and re-sweep again when moving
  from Opus 5 to Opus 5.5 (5.5 thinks more per turn at a given effort *value*, especially at `xhigh`/`max`).
- **Per-model pages** — model names (Opus / Sonnet / Haiku / Fable / Mythos + versions) and their tips
  change; current set: **Fable 5.1 / Mythos 5.1** (frontier, own page — #8), Fable 5 / Mythos 5,
  **Opus 5.5** (current Opus flagship, own page — #9, added 2026-09-28), Opus 5 (previous generation, own
  page — #3), Sonnet 5, Haiku 4.5. **Opus 4.8 / 4.7 / 4.6 are legacy** (the 4.8 page is still live, tracked
  as #7). Dedicated prompting pages exist for Fable 5.1, Fable 5, Opus 5.5, Opus 5, Sonnet 5, and legacy
  Opus 4.8; **no Haiku page** yet — reconfirmed 404 on `prompting-claude-haiku-4-5` again this cycle
  (2026-09-28).
- **Opus 5.5 safeguard refusals** — new vs. Opus 5: biology (same classifier as Fable 5.1's) and
  `reasoning_extraction` (declines a request that pushes the model to reproduce its reasoning as response
  text; server-side fallback returns this category to the caller rather than retrying it). Cybersecurity
  (vuln-finding allowed, high-risk dual-use not) is unchanged from Opus 5. Recheck whether Opus 5's own page
  gains these categories too, or stays Opus-5.5-only.
- **Refusal categories & fallback (Fable family)** — `reasoning_extraction` (don't ask the model to
  reproduce its reasoning as text), offensive-cyber, bio/life-sciences. **The Opus 4.8 fallback target is
  stated on #4 (Fable 5) only**; #8 defers to the untracked `whats-new-fable-5-1` page and names no model, so
  `models/fable.md` flags it rather than asserting it for 5.1 — reconfirmed still unresolved on 2026-09-28
  (and reconsider tracking that page). On **Fable 5.1** false positives are down and source-code
  vulnerability finding is permitted; the three triggers (compile-check phrasing, lesser-known languages,
  base64 in tool output) persisted unchanged this cycle (2026-09-28).
- **Preserved thinking / append-only history (Fable 5.1)** — editing earlier turns invalidates later
  thinking blocks: a 400 for accounts created on or after **2026-08-31** (unchanged this cycle), and
  expected to be enforced for everyone on later models — still not universal as of 2026-09-28. The opt-in
  `thinking.block_binding.prefix_mismatch_behavior: "drop_block"` (beta,
  `thinking-binding-controls-2026-08-01`) escape hatch is unchanged and still documented in
  `models/fable.md`. **Opus 5.5's own preserved-thinking behavior is the same shape** (a request that
  replays a thinking block after its prefix changed either 400s or drops the block under the same
  `drop_block` opt-in) — confirmed on the Opus 5.5 page this cycle; `models/opus.md` now notes it too.
  Recheck the enforcement date and whether it has gone universal.
- **Turn-scoped and mid-conversation system messages** — the `clear_at: "next_user_message"` and
  `thinking.display: "updates"` mechanics that #8's batching/progress-update advice and **#9's Opus 5.5
  progress-update and unattended-run advice** depend on are in **beta** (headers
  `mid-conversation-system-clear-at-2026-08-21`, `thinking-display-updates-2026-08-18`). Reconfirmed still
  beta with the same header dates as of 2026-09-28, and now confirmed used identically on Opus 5.5. Recheck
  for GA / header changes.
- **Sonnet 5 API constraints** — `temperature`/`top_p`/`top_k` at non-default values return 400; manual
  extended-thinking `budget_tokens` is removed (400); the tokenizer produces ~30% more tokens for the same
  text (re-check `max_tokens` budgets ported from Sonnet 4.6).
- **Computer / browser tool versions** — Sonnet 5 and Opus 4.8 now list the `computer_toolset_20260801`
  toolset and `browser_toolset_20260801` alongside the older `computer_20251124`; resolutions still cap at
  2576px / 3.75MP. Recheck the toolset date strings.
- **Structured Outputs / API surface** — verify the current way to force formats.

> NOTE: Anthropic docs are also served from `docs.anthropic.com` / `docs.claude.com`; the
> `platform.claude.com` paths above are the canonical ones as of the verified date.
