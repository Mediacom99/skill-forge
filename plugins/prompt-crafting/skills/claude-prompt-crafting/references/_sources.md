# Sources — claude-prompt-crafting references

**last-verified: 2026-06-21** · vendor: Anthropic · official docs only.

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

## Volatile items to recheck each cycle
- **Prefill removal** — applies to Claude 4.6+; confirm still current and which models.
- **Effort levels & adaptive thinking** — parameter names, levels (low…max), defaults move per model.
- **Per-model pages** — model names (Opus/Sonnet/Haiku/Fable + versions) and their specific tips change;
  the doc set was consolidated once already (old per-technique pages now redirect).
- **Structured Outputs / API surface** — verify the current way to force formats.

> NOTE: Anthropic docs are also served from `docs.anthropic.com` / `docs.claude.com`; the
> `platform.claude.com` paths above are the canonical ones as of the verified date.
