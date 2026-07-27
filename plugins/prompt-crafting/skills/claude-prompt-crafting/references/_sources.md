# Sources — claude-prompt-crafting references

**last-verified: 2026-07-27** · vendor: Anthropic · official docs only.

The `refresh-references` skill and the `check-sources.yml` workflow read the URL list below.
When updating, re-fetch each URL, reconcile `techniques.md` / `techniques-advanced.md`, then bump
the `last-verified` dates here and in those files.

| # | URL | Covers |
|---|-----|--------|
| 1 | https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/overview | Prompt-engineering router; presupposes success criteria + a way to test |
| 2 | https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices | The living reference: clarity, examples, XML, roles, thinking, chaining, output/format, tool use, agentic, capability tips |
| 3 | https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-4-8 | Opus 4.8-specific (prior flagship, kept for migration deltas): literal instruction-following, effort, output budget, scope, tone |
| 4 | https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5 | Fable-specific: brief instructions, give-the-reason, memory file, no inline reasoning |
| 5 | https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-tools | **Retired 2026-07-27 cycle** — now 307-redirects to #2, and the destination no longer carries the Console prompt-generator/-improver/template-variable content this URL used to cover. Matches Anthropic's public notice that the experimental Console prompt-tools APIs and Workbench are sunsetting **2026-08-17**. Kept in the table as a dead/merged entry so `check-sources` doesn't re-flag it as new drift; no reference content depended on it beyond the generic `{{var}}` convention, which #2 still demonstrates directly (see its long-context document-variable examples). |
| 6 | https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-sonnet-5 | Sonnet-specific: effort default/ladder, adaptive thinking on-by-default, new tokenizer, no sampling params |
| 7 | https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5 | **New this cycle** — Opus 5 is now the current Opus flagship (superseding 4.8), with its own dedicated page: effort ladder/default, thinking-on-by-default capped-at-`high` disable rule, response-length/narration/self-verification/subagent-delegation deltas from Opus 4.8 |

## Reference files → sources
Which source backs which reference file (reconcile the file when its backing source drifts). Each per-model
file also carries its own `last-verified` header.

| Reference file | Backed by |
|----------------|-----------|
| `techniques.md` · `techniques-advanced.md` | #1, #2 |
| `models/opus.md` | **#7** — dedicated Opus 5 prompting page (current flagship); **#3** for the Opus 4.8 migration-deltas section |
| `models/fable.md` (Fable 5 + Mythos 5) | **#4** — dedicated Fable 5 / Mythos 5 prompting page |
| `models/sonnet.md` | **#6** — dedicated Sonnet 5 prompting page |
| `models/haiku.md` | **#2** + the Haiku 4.5 model overview — **no dedicated prompting page** exists as of last-verified (reconfirmed 404 on `prompting-claude-haiku-4-5` this cycle) |

> Seven prompting URLs are tracked here; six have committed content hashes in `.source-hashes.json` (the
> check-sources workflow owns adding #7's hash on its next run — do not hand-edit that file). #5 is a dead/merged
> entry (see its row above) and was never content-diffed beyond confirming the redirect, so it carries no hash.
> The Haiku overview page is not tracked — it churns on pricing/availability; `models/haiku.md`'s prompting
> substance comes from the cross-model best-practices page (#2). Add a new tracked URL only if Anthropic ships a
> dedicated Haiku prompting page.

## Volatile items to recheck each cycle
- **Prefill removal** — applies to Claude 4.6 and newer, incl. the 5-series (Fable 5 / Mythos 5 / Sonnet 5 /
  Opus 5); confirm.
- **Effort levels & adaptive thinking** — parameter names, levels (low…max), defaults move per model.
  Opus 5 (current flagship): default `high`, supports all five levels, thinking on by default, and
  **disabling thinking is only accepted at effort `high` or below** — `xhigh`/`max` + `thinking: {type:
  "disabled"}` returns a 400. Opus 4.8 (prior flagship, kept for migration deltas): `xhigh` for coding/agentic,
  `high` min for intelligence-sensitive, thinking off by default. Sonnet 5: `high` default, adaptive thinking
  **on by default** (a change from Sonnet 4.6, where it was off by default).
- **Per-model pages** — model names (Opus / Sonnet / Haiku / Fable / Mythos + versions) and their tips
  change; current set: Fable 5, Mythos 5, **Opus 5** (new flagship, own dedicated page as of this cycle),
  Opus 4.8 / 4.7 / 4.6, Sonnet 5, Sonnet 4.6, Haiku 4.5. The doc set was consolidated once already (old
  per-technique pages now redirect, and `prompting-tools` joined that list this cycle) and has since grown
  dedicated Sonnet and Opus 5 pages — recheck whether Haiku gets one too.
- **Refusal categories & fallback (Fable 5 / Mythos 5)** — `reasoning_extraction` (don't ask the model to
  reproduce its reasoning as text), offensive-cyber, bio/life-sciences; declined requests fall back to
  Opus 4.8 (confirmed still Opus 4.8, not Opus 5, on Fable 5's own page). New since the 0.1.0 distillation.
  Reconfirmed unchanged this cycle.
- **Sonnet 5 API constraints** — `temperature`/`top_p`/`top_k` at non-default values now return 400; manual
  extended-thinking `budget_tokens` is removed (400 error); a new tokenizer produces ~30% more tokens for the
  same text (re-check `max_tokens` budgets ported from Sonnet 4.6).
- **Opus 5 API constraints (new this cycle)** — thinking on by default (revisit `max_tokens` for workloads
  that ran without thinking on Opus 4.8); disabling thinking capped at effort `high`; 1M-token context window
  is now the default with no beta header; prompt-caching minimum prompt length dropped to 512 tokens;
  `temperature`/`top_p`/`top_k` still 400 at non-default values (unchanged from 4.8); `stop_details` on
  refusals now publicly documented.
- **Structured Outputs / API surface** — verify the current way to force formats; page still resolves (200),
  no drift found this cycle.
- **`prompting-tools` retirement** — the Console prompt-generator/-improver/template-variable page now
  redirects to #2, ahead of Anthropic's announced 2026-08-17 sunset of the experimental Console prompt-tools
  APIs and Workbench. Watch for the redirect itself disappearing (a hard 404) after that date.

> NOTE: Anthropic docs are also served from `docs.anthropic.com` / `docs.claude.com`; the
> `platform.claude.com` paths above are the canonical ones as of the verified date.
