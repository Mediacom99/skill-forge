# Sources — claude-prompt-crafting references

**last-verified: 2026-08-03** · vendor: Anthropic · official docs only.

The `refresh-references` skill and the `check-sources.yml` workflow read the URL list below.
When updating, re-fetch each URL, reconcile `techniques.md` / `techniques-advanced.md`, then bump
the `last-verified` dates here and in those files.

| # | URL | Covers |
|---|-----|--------|
| 1 | https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/overview | Prompt-engineering router; presupposes success criteria + a way to test |
| 2 | https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices | The living reference: clarity, examples, XML, roles, thinking, chaining, output/format, tool use, agentic, capability tips |
| 3 | https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-4-8 | Opus 4.8 migration deltas: literal instruction-following, effort, output budget, scope, tone |
| 4 | https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5 | Fable-specific: brief instructions, give-the-reason, memory file, no inline reasoning |
| 5 | ~~https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-tools~~ | **Retired 2026-08-03** — 307-redirects to #2 (confirmed via `curl -I`); no content lost, nothing on this list cited it in prose |
| 6 | https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-sonnet-5 | Sonnet-specific: effort default/ladder, adaptive thinking on-by-default, new tokenizer, no sampling params |
| 7 | https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5 | Opus-specific (current flagship): effort ladder/default, thinking-on-by-default (disable capped at `high` effort), response length independent of effort, self-verification/self-correction defaults, subagent delegation, thinking-disabled output artifacts |

## Reference files → sources
Which source backs which reference file (reconcile the file when its backing source drifts). Each per-model
file also carries its own `last-verified` header.

| Reference file | Backed by |
|----------------|-----------|
| `techniques.md` · `techniques-advanced.md` | #1, #2 |
| `models/opus.md` | **#7** — dedicated Opus 5 prompting page (current flagship); **#3** kept for Opus 4.8 migration deltas |
| `models/fable.md` (Fable 5 + Mythos 5) | **#4** — dedicated Fable 5 / Mythos 5 prompting page |
| `models/sonnet.md` | **#6** — dedicated Sonnet 5 prompting page |
| `models/haiku.md` | **#2** + the Haiku 4.5 model overview — **no dedicated prompting page** exists as of last-verified (reconfirmed 404 on `prompting-claude-haiku-4-5` this cycle) |

> Six prompting URLs are tracked in `.source-hashes.json` (#1–#4, #6, plus #5's now-dead URL until the
> check-sources workflow prunes it — do not hand-edit that file; it owns adding #7's hash on its next run).
> The Haiku overview page is not tracked — it churns on pricing/availability; `models/haiku.md`'s prompting
> substance comes from the cross-model best-practices page (#2). Add a new tracked URL only if Anthropic
> ships a dedicated Haiku prompting page.

## Volatile items to recheck each cycle
- **Prefill removal** — applies to Claude 4.6 and newer, incl. the 5-series (Fable 5 / Mythos 5 / Sonnet 5 /
  Opus 5); confirm.
- **Effort levels & adaptive thinking** — parameter names, levels (low…max), defaults move per model
  (Opus 5: `high` default, `xhigh` for demanding coding/agentic, `low`/`medium` newly efficient — re-run
  effort sweeps rather than assume prior-model tuning carries over; Sonnet 5: `high` default, adaptive
  thinking **on by default**). **Opus 5's thinking-disable constraint:** unlike Sonnet 5, thinking can only
  be turned off at effort `high` or below on Opus 5 — `thinking: {type: "disabled"}` combined with
  `xhigh`/`max` errors. Opus 4.8 (legacy): thinking off unless `thinking: {type: "adaptive"}` is set.
- **Per-model pages** — model names (Opus / Sonnet / Haiku / Fable / Mythos + versions) and their tips
  change; current set: Fable 5, Mythos 5, **Opus 5** (new dedicated page this cycle), Opus 4.8 / 4.7 / 4.6,
  Sonnet 5, Sonnet 4.6, Haiku 4.5. Haiku still has no dedicated prompting page — recheck each cycle.
- **Refusal categories & fallback (Fable 5 / Mythos 5)** — `reasoning_extraction` (don't ask the model to
  reproduce its reasoning as text), offensive-cyber, bio/life-sciences; declined requests fall back to
  Opus 4.8. Reconfirmed unchanged this cycle.
- **Sonnet 5 API constraints** — `temperature`/`top_p`/`top_k` at non-default values now return 400; manual
  extended-thinking `budget_tokens` is removed (400 error); a new tokenizer produces ~30% more tokens for the
  same text (re-check `max_tokens` budgets ported from Sonnet 4.6). Reconfirmed unchanged this cycle.
- **Opus 5 output artifacts with thinking disabled** — leaked tool-call text and internal XML tags can appear
  in visible output; Anthropic's own mitigation is to keep thinking on at a lower effort rather than disable it.
- **Structured Outputs / API surface** — verify the current way to force formats.

> NOTE: Anthropic docs are also served from `docs.anthropic.com` / `docs.claude.com`; the
> `platform.claude.com` paths above are the canonical ones as of the verified date.
