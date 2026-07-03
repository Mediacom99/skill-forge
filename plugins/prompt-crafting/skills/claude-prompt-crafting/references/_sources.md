# Sources — claude-prompt-crafting references

**last-verified: 2026-07-03** · vendor: Anthropic · official docs only.

The `refresh-references` skill and the `check-sources.yml` workflow read the URL list below.
When updating, re-fetch each URL, reconcile `techniques.md` / `techniques-advanced.md`, then bump
the `last-verified` dates here and in those files.

| # | URL | Covers |
|---|-----|--------|
| 1 | https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/overview | Prompt-engineering router; presupposes success criteria + a way to test |
| 2 | https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices | The living reference: clarity, examples, XML, roles, thinking, chaining, output/format, tool use, agentic, capability tips |
| 3 | https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-4-8 | Opus-specific: literal instruction-following, effort, output budget, scope, tone |
| 4 | https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5 | Fable-specific: brief instructions, give-the-reason, memory file, no inline reasoning |
| 5 | https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-tools | Console prompt generator / improver, template variables |

## Reference files → sources
Which source backs which reference file (reconcile the file when its backing source drifts). Each per-model
file also carries its own `last-verified` header.

| Reference file | Backed by |
|----------------|-----------|
| `techniques.md` · `techniques-advanced.md` | #1, #2 (+ #5 for template variables) |
| `models/opus.md` | **#3** — dedicated Opus 4.8 prompting page |
| `models/fable.md` (Fable 5 + Mythos 5) | **#4** — dedicated Fable 5 / Mythos 5 prompting page |
| `models/sonnet.md` | **#2** + the Sonnet 4.6 model overview — **no dedicated prompting page** exists as of last-verified (confirmed 404 on `prompting-claude-sonnet-4-6`) |
| `models/haiku.md` | **#2** + the Haiku 4.5 model overview — **no dedicated prompting page** exists as of last-verified (confirmed 404 on `prompting-claude-haiku-4-5`) |

> Only the five prompting URLs above are hash-tracked in `.source-hashes.json`. Model *overview* pages
> (Sonnet/Haiku) are not tracked — they churn on pricing/availability; the prompting substance for those two
> files comes from the cross-model best-practices page (#2). Add a new tracked URL only if Anthropic ships a
> dedicated Sonnet/Haiku prompting page.

## Volatile items to recheck each cycle
- **Prefill removal** — applies to Claude 4.6 and newer, incl. the 5-series (Fable 5 / Mythos 5); confirm.
- **Effort levels & adaptive thinking** — parameter names, levels (low…max), defaults move per model
  (Opus 4.8: `xhigh` for coding/agentic, `high` min for intelligence-sensitive).
- **Per-model pages** — model names (Opus / Sonnet / Haiku / Fable / Mythos + versions) and their tips
  change; current set: Fable 5, Mythos 5, Opus 4.8 / 4.7 / 4.6, Sonnet 4.6, Haiku 4.5. The doc set was
  consolidated once already (old per-technique pages now redirect).
- **Refusal categories & fallback (Fable 5 / Mythos 5)** — `reasoning_extraction` (don't ask the model to
  reproduce its reasoning as text), offensive-cyber, bio/life-sciences; declined requests fall back to
  Opus 4.8. New since the 0.1.0 distillation.
- **Structured Outputs / API surface** — verify the current way to force formats.

> NOTE: Anthropic docs are also served from `docs.anthropic.com` / `docs.claude.com`; the
> `platform.claude.com` paths above are the canonical ones as of the verified date.
