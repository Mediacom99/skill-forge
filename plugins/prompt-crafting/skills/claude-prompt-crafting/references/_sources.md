# Sources — claude-prompt-crafting references

**last-verified: 2026-08-24** · vendor: Anthropic · official docs only.

The `refresh-references` skill and the `check-sources.yml` workflow read the URL list below.
When updating, re-fetch each URL, reconcile `techniques.md` / `techniques-advanced.md`, then bump
the `last-verified` dates here and in those files.

| # | URL | Covers |
|---|-----|--------|
| 1 | https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/overview | Prompt-engineering router; presupposes success criteria + a way to test |
| 2 | https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices | The living reference: clarity, examples, XML, roles, thinking, chaining, output/format, tool use, agentic, capability tips |
| 3 | https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5 | **Opus 5** (current flagship): effort default `high`, thinking on-by-default (disable only ≤ `high`), verbosity/narration, scope + over-verification, subagents |
| 4 | https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5 | Fable-specific: brief instructions, give-the-reason, memory file, no inline reasoning |
| 5 | _(retired 2026-07-28)_ `prompting-tools` | **RETIRED** — now 307-redirects to #2 (best-practices); the Console prompt-generator/-improver + Workbench are sunsetting 2026-08-17. Removed from tracking (its normalized content already mirrored #2). The `{{double_bracket}}` template convention it covered is still demonstrated on #2. |
| 6 | https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-sonnet-5 | Sonnet-specific: effort default/ladder, adaptive thinking on-by-default, new tokenizer, no sampling params |
| 7 | https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-4-8 | **Legacy** Opus 4.8 page (still live) — literal instruction-following, effort ladder, 64k budget, design house-style (`#F4F1EA`), computer-use resolutions |

## Reference files → sources
Which source backs which reference file (reconcile the file when its backing source drifts). Each per-model
file also carries its own `last-verified` header.

| Reference file | Backed by |
|----------------|-----------|
| `techniques.md` · `techniques-advanced.md` | #1, #2 (template variables now covered by #2; former #5 retired) |
| `models/opus.md` | **#3** — dedicated **Opus 5** prompting page (current flagship; #7 is the legacy Opus 4.8 page) |
| `models/fable.md` (Fable 5 + Mythos 5) | **#4** — dedicated Fable 5 / Mythos 5 prompting page |
| `models/sonnet.md` | **#6** — dedicated Sonnet 5 prompting page (Anthropic shipped this since last cycle; Sonnet 4.6 had none) |
| `models/haiku.md` | **#2** + the Haiku 4.5 model overview — **no dedicated prompting page** exists as of last-verified (reconfirmed 404 on `prompting-claude-haiku-4-5` this cycle) |

> Six prompting URLs are tracked in `.source-hashes.json`: the **Opus 5** page (#3) was added seeded `null`
> (the check-sources Action captures its baseline on the next run), and the retired **prompting-tools** page
> (#5) was removed from tracking (it now mirrors #2). Add a *new* URL by seeding it `null`; never hand-edit
> existing hash *values* (the Action owns them). The Haiku overview page is not tracked — it churns on
> pricing/availability; `models/haiku.md`'s substance comes from the cross-model best-practices page (#2). Add
> a new tracked URL only if Anthropic ships a dedicated Haiku page.

## Volatile items to recheck each cycle
- **Prefill removal** — applies to Claude 4.6 and newer, incl. the 5-series (Fable 5 / Mythos 5 / Sonnet 5); confirm.
- **Effort levels & adaptive thinking** — parameter names, levels (low…max), defaults move per model
  (**Opus 5**: default `high`, `low`/`medium` efficient/liberal, `xhigh` for demanding coding/agentic; Sonnet
  5: `high` default. **Adaptive thinking is now on by default on both Opus 5 and Sonnet 5** — and on Opus 5 you
  can disable thinking only at effort ≤ `high`. Legacy Opus 4.8 / Sonnet 4.6 default thinking **off**).
- **Per-model pages** — model names (Opus / Sonnet / Haiku / Fable / Mythos + versions) and their tips
  change; current set: Fable 5, Mythos 5, **Opus 5** (new flagship, `claude-opus-5`, own dedicated page),
  Sonnet 5, Haiku 4.5. **Opus 4.8 / 4.7 / 4.6 are now legacy** (the 4.8 page is still live, tracked as #7).
  Dedicated prompting pages exist for Opus 5, Sonnet 5, Fable 5 / Mythos 5, and legacy Opus 4.8; **no Haiku
  page** yet — recheck.
- **Refusal categories & fallback (Fable 5 / Mythos 5)** — `reasoning_extraction` (don't ask the model to
  reproduce its reasoning as text), offensive-cyber, bio/life-sciences; declined requests fall back to
  Opus 4.8. New since the 0.1.0 distillation. Reconfirmed unchanged this cycle.
- **Sonnet 5 API constraints** — `temperature`/`top_p`/`top_k` at non-default values now return 400; manual
  extended-thinking `budget_tokens` is removed (400 error); a new tokenizer produces ~30% more tokens for the
  same text (re-check `max_tokens` budgets ported from Sonnet 4.6).
- **Structured Outputs / API surface** — verify the current way to force formats.
- **Computer-use tool versions** — Sonnet 5 and Opus 4.8 now additionally list the `computer_toolset_20260801`
  toolset and the `browser_toolset_20260801` browser-use tool (alongside the older `computer_20251124` tool
  version). Updated in `models/sonnet.md` this cycle (2026-08-24); recheck naming/versions each cycle — this
  surface has churned twice now.

> NOTE: Anthropic docs are also served from `docs.anthropic.com` / `docs.claude.com`; the
> `platform.claude.com` paths above are the canonical ones as of the verified date.
