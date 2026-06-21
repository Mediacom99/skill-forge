# Sources — gpt-prompt-crafting references

**last-verified: 2026-06-21** · vendor: OpenAI · official developer docs only.

The `refresh-references` skill and `check-sources.yml` workflow read the URL list below. When updating,
re-fetch each URL, reconcile `techniques.md` / `techniques-advanced.md`, then bump the `last-verified`
dates here and in those files.

> Host note: `platform.openai.com` and `cookbook.openai.com` now redirect to `developers.openai.com`.
> If the canonical host shifts again, update these URLs.

| # | URL | Covers |
|---|-----|--------|
| 1 | https://developers.openai.com/cookbook/examples/gpt4-1_prompting_guide | GPT-4.1: literalness, markdown structure, delimiters, long-context placement, agentic reminder trio, tools-via-API |
| 2 | https://developers.openai.com/api/docs/guides/reasoning-best-practices | Reasoning vs non-reasoning choice; avoid CoT prompting; keep prompts simple; `reasoning_effort` |
| 3 | https://developers.openai.com/api/docs/guides/prompt-engineering | Role hierarchy (developer/user/assistant); Responses vs Chat Completions; prompt-object deprecation |
| 4 | https://developers.openai.com/cookbook/examples/gpt-5/gpt-5_prompting_guide | GPT-5: agentic eagerness, tool preambles, verbosity, contradiction sensitivity, markdown control |
| 5 | https://developers.openai.com/cookbook/examples/gpt-5/gpt-5-1_prompting_guide | GPT-5.1: `none` reasoning mode, persistence prompting, named tools (apply_patch, shell) |
| 6 | https://developers.openai.com/api/docs/guides/latest-model | Current flagship settings: `reasoning_effort` (none…xhigh), `verbosity`, unified reasoning family |
| 7 | https://developers.openai.com/api/docs/guides/structured-outputs | Structured Outputs vs JSON mode; strict:true; schema rules; model support |
| 8 | https://developers.openai.com/api/docs/models | Current model catalog / IDs — MOST VOLATILE page |
| 9 | https://developers.openai.com/cookbook/examples/partners/model_selection_guide/model_selection_guide | Model-selection framework + tiered routing pattern |

## Volatile items to recheck each cycle
1. **Model IDs** (`gpt-5.5`, `gpt-5.4`, mini/nano) — OpenAI ships ~quarterly.
2. **`reasoning_effort` enum + default** — expanded to none→xhigh; defaults move per model.
3. **`none` / `minimal` semantics** — version-specific (minimal=GPT-5, none=GPT-5.1+).
4. **o-series existence** — folding into the unified GPT-5 family; legacy docs still name o3/o4-mini.
5. **`v1/prompts` shutdown** — reusable prompt objects end 2026-11-30.
6. **Host migration** — platform/cookbook → developers.openai.com.
7. **Named tools** (`apply_patch`, `shell`) and the Structured-Outputs model floor.
