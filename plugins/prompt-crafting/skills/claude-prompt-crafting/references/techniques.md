<!--
last-verified: 2026-06-21
sources: see _sources.md (official Anthropic prompt-engineering docs)
scope: LEAN CORE — the high-leverage techniques that apply to most Claude prompts.
For agentic/tool-use/long-context/RAG/eval/model-specific guidance, see techniques-advanced.md.
-->

# Claude prompt techniques — lean core

The ~15 highest-leverage techniques for crafting prompts that target Claude. Apply the few that
fit the spec; do not apply all of them. Each entry: **what · when · how**.

> **VOLATILE (recheck on update):** prefill removal applies to Claude 4.6+; reasoning/`effort`
> parameters and model-specific tips change per model. See the flagged items below and `_sources.md`.

## Structure & roles

1. **Role in the system prompt.** *What:* one or two sentences defining who Claude is.
   *When:* almost always. *How:* put it first, in the `system` field, not the user turn — "You are a
   senior X who…". Even a single sentence measurably shifts tone and focus.

2. **System vs user split.** *What:* durable instructions in `system`; variable payload in `user`.
   *When:* any reusable prompt. *How:* role, rules, format, examples → system. The actual topic/input
   for this run → user. This makes the prompt a reusable template.

3. **XML tags for structure.** *What:* wrap each part in named tags (`<instructions>`, `<context>`,
   `<examples>`, `<input>`). *When:* any prompt mixing instructions + data + examples. *How:* consistent,
   descriptive tag names; nest for hierarchy; wrap variable inputs in tags too.

4. **Template variables.** *What:* `{{double_bracket}}` placeholders. *When:* the prompt is reused with
   different inputs. *How:* wrap each variable in its own XML tag so the boundary is unambiguous.

## Clarity & steering

5. **Be clear, direct, specific.** *What:* explicit instructions about output and constraints.
   *When:* always. *How:* "Show the prompt to a colleague with no context — if they'd be confused,
   so is Claude." Number sequential steps when order/completeness matters. If you want above-and-beyond
   effort, ask for it explicitly.

6. **Give the reason (motivation).** *What:* explain *why* a constraint exists. *When:* any non-obvious
   rule. *How:* "…will be read aloud by text-to-speech, so never use ellipses." Claude generalizes from
   the reason far better than from the bare rule.

7. **Instruct positively.** *What:* say what TO do, not a list of "don'ts". *When:* always. *How:*
   "Do not use markdown" → "Write in smoothly flowing prose paragraphs." Positive examples beat negative
   instructions, especially on Opus 4.x.

8. **State scope explicitly.** *What:* name how broadly an instruction applies. *When:* multi-part or
   long outputs. *How:* "Apply this to every section, not just the first." Newer models follow
   instructions literally and won't silently generalize one item to all.

## Examples & format

9. **Multishot (3–5 examples).** *What:* worked examples of the desired output. *When:* format, tone, or
   structure matter — one of the most reliable steering levers. *How:* wrap each in `<example>`, collect
   in `<examples>`; make them **relevant, diverse, structured**. Diversity stops Claude from latching onto
   an unintended pattern.

10. **Match prompt style to output.** *What:* the prompt's own formatting bleeds into the output.
    *When:* you care about output formatting. *How:* want clean prose? Write the prompt in clean prose
    (less markdown in → less markdown out). For strict prose, add a short "flowing prose, complete
    paragraphs, no bullet lists" block.

11. **Control format with indicators.** *What:* tell Claude the exact shape. *When:* structured output
    needed. *How:* describe the format, or use an XML wrapper for the answer (`<answer>…</answer>`); for
    guaranteed schemas use **Structured Outputs** (API) rather than asking.

## Reasoning & quality

12. **Ask for reasoning, generally.** *What:* let Claude think before answering. *When:* non-trivial
    reasoning. *How:* "Think thoroughly" usually beats a hand-written step list. With extended thinking
    off, separate reasoning from output via `<thinking>`/`<answer>` tags. *(VOLATILE: on some models the
    literal word "think" is sensitive — prefer "consider/evaluate/reason through" when thinking is off.)*

13. **Set success criteria + self-check.** *What:* tell Claude what "good" is and have it verify.
    *When:* accuracy/quality-critical. *How:* state the bar; add "Before finishing, verify your answer
    against [criteria]."

14. **Break the default ("propose options first").** *What:* counter Claude's pull toward generic, "on
    distribution" output. *When:* creative or design tasks. *How:* "Before producing, propose 3–4 distinct
    directions, then commit to one." This creates variety more reliably than temperature, and names the
    anti-convergence goal explicitly ("surprise and delight; don't converge on the obvious").

## VOLATILE / model mechanics

15. **No prefill on 4.6+.** *What:* prefilling the assistant turn is unsupported on Claude 4.6+ (returns
    400). *Instead:* force format via Structured Outputs or a direct instruction ("Respond directly, no
    preamble; do not start with 'Here is…'"); put continuations in the user turn.

16. **Effort & output budget (current models).** *What:* harder tasks want more reasoning effort and a
    bigger output budget. *When:* complex or long generations. *How:* raise `effort` (e.g. high/xhigh)
    rather than prompting around shallow reasoning; set a large max-output budget for long outputs.
    *(VOLATILE: exact effort levels and defaults are model-specific — see techniques-advanced.md + _sources.md.)*

---
For tool use, agents, long context, RAG, evals, prompt chaining, and per-model tips
(Opus / Sonnet / Haiku / Fable), see [techniques-advanced.md](techniques-advanced.md).
