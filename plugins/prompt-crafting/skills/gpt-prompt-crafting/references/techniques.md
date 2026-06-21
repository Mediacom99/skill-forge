<!--
last-verified: 2026-06-21
sources: see _sources.md (official OpenAI developer docs)
scope: LEAN CORE — high-leverage techniques for most GPT prompts, plus the reasoning-vs-non-reasoning
split. For agentic/tool-use/long-context/structured-output/eval depth, see techniques-advanced.md.
-->

# GPT prompt techniques — lean core

The highest-leverage techniques for prompts targeting OpenAI/GPT models. Apply the few that fit.
Each entry: **what · when · how**.

> **VOLATILE (recheck on update):** model IDs (`gpt-5.5`, `gpt-5.4`, mini/nano), the `reasoning_effort`
> enum and defaults, and `none`/`minimal` semantics change every few months. See flagged items + `_sources.md`.

## The big fork: reasoning vs non-reasoning

0. **Decide the model class first — it changes how you prompt.**
   - **Reasoning models** (GPT-5.x "thinking", o-series): reason internally. Give the *goal*, keep it brief.
     **Do NOT add "think step by step"** — CoT prompting is unnecessary and can hurt. Zero-shot first.
   - **Non-reasoning workhorse** (GPT-4.1; GPT-5.x at `none` effort): does NOT reason on its own —
     **induce planning explicitly** and lean on structure + examples.
   - Most real systems mix both (cheap model routes/filters → workhorse executes → reasoning model verifies).
   *(VOLATILE: reasoning is now unified into the GPT-5 family via tunable `reasoning_effort` rather than a
   separate o-series; verify the current lineup.)*

## Roles & structure

1. **Use the role hierarchy.** *What:* developer > user > assistant. *How:* top-priority instructions go in
   the **developer** message (Responses API) or **system** message (Chat Completions) — both are the same
   "highest-priority" slot; the **user** message carries the variable input. Mental model: developer = the
   function definition, user = the arguments.

2. **Structure with Markdown.** *What:* headers + short sections + lists + backticks for code. *When:* any
   non-trivial prompt. *How:* organize into Role/Objective, Instructions, Output Format, Examples, Context.

3. **Delimit embedded documents well.** *What:* clear separators for injected content. *When:* you paste
   docs/data. *How:* `<doc id="1" title="…">…</doc>` or `ID:1 | TITLE:… | CONTENT:…`. Avoid wrapping large
   document sets in JSON — it performs worse for long context.

## Steering

4. **Be explicit; GPT is literal.** *What:* state rules directly — recent GPT follows instructions closely and
   literally and infers little. *How:* if behavior drifts, one firm, unambiguous sentence usually fixes it.

5. **Eliminate contradictions.** *What:* internal consistency. *When:* always — *more* important on reasoning
   models, which waste reasoning tokens reconciling conflicts. *How:* audit the prompt; resolve any rule that
   fights another.

6. **Few-shot: show and tell.** *What:* concrete examples of desired behavior. *When:* format/behavior matters
   (workhorse especially). *How:* every behavior demonstrated in examples must also be stated in the rules.

## Reasoning inducement (non-reasoning models only)

7. **Prompt planning explicitly.** *What:* "think step by step" / a Reasoning Steps section. *When:* GPT-4.1 or
   GPT-5.x at `none`. *Why:* they won't reason internally; this lifts quality. **Skip this for reasoning models.**

8. **Agentic reminder trio (workhorse agents).** Add: **persistence** ("keep going until the query is fully
   resolved; only stop when solved"), **tool-calling** ("if unsure about content, use tools — don't guess"),
   and optional **planning** ("plan before each tool call and reflect after"). Big agentic lift.

## Output control

9. **Structured Outputs over JSON mode.** *What:* schema-guaranteed JSON. *When:* you need machine-readable
   output. *How:* set `strict: true` with a JSON schema (Chat Completions `response_format`, or Responses API
   `text.format`); root must be an object, all properties required, `additionalProperties: false`. Prefer this
   to asking for JSON in prose.

10. **Control verbosity / formatting.** *What:* length and markdown are tunable. *How:* GPT-5.x exposes a
    `verbosity` parameter (separate from reasoning length); Markdown can be off by default in the API — request
    it explicitly ("use Markdown only where semantically correct") and restate every few messages if it decays.

## Long context

11. **Repeat key instructions at start AND end.** *What:* instruction placement. *When:* large context.
    *How:* putting the instructions both before and after the context beats either alone; if only once, place
    them **above** the context.

## VOLATILE / API mechanics

12. **`reasoning_effort` budgets thinking.** *(VOLATILE)* current flagship enum ≈ `none | low | medium | high |
    xhigh` (default `medium`); `none` = no reasoning (classic non-reasoning behavior). Lower it (+ tool-call
    budgets + stop criteria) to reduce agentic eagerness; raise it for hard tasks. Verify enum/defaults per model.

13. **Prefer the Responses API for agentic/reasoning work.** *What:* it persists reasoning across tool calls via
    `previous_response_id`, saving tokens and improving latency/quality. *(VOLATILE: reusable prompt objects /
    `v1/prompts` are being deprecated — store prompts in app code.)*

---
For agents, tool use, long-context/RAG depth, structured-output edge cases, evals, and GPT-5.x/5.1 specifics,
see [techniques-advanced.md](techniques-advanced.md).
