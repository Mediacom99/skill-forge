---
name: gpt-prompt-crafting
description: >
  Turn a rough, messy, or half-formed idea into a production-grade prompt FOR OPENAI / GPT
  models (GPT-5.x, the reasoning family, GPT-4.1), through a short, sharp alignment dialogue
  that nails down intent before writing a single line of the prompt. Use this whenever the user
  wants to write, design, build, improve, refine, fix, or debug a prompt, system/developer
  message, or agent instructions aimed at GPT / OpenAI / ChatGPT / o-series / "the OpenAI API" —
  or says things like "help me write a prompt for GPT", "make this OpenAI prompt better",
  "developer message", "prompt for o3 / GPT-5", or invokes /gpt-prompt-crafting. Use it even when
  the user only describes a task they want GPT to do repeatedly and never says the word "prompt".
  For prompts targeting Claude/Anthropic models, use the claude-prompt-crafting skill instead.
argument-hint: "[your rough idea] [--quick | --deep] [--refine]"
version: 0.1.0
metadata:
  tags: prompt-engineering, prompts, gpt, openai, chatgpt, reasoning-models, developer-message
---

# GPT Prompt Crafting

Craft an excellent prompt **for OpenAI / GPT models** from whatever the user gives you — even a
vague, repetitive, or contradictory description. Output quality is overwhelmingly determined by how
well intent was understood before writing. So the work splits in two: **first align, then craft.**
Do not skip the aligning.

Your job: run a tight discovery dialogue that converges on a complete spec, then craft a prompt
grounded in OpenAI's official prompt-engineering guidance (bundled in `references/`, loaded only at
the craft step). GPT has a critical extra fork the Claude side doesn't: **reasoning model vs
non-reasoning workhorse**, which changes how you write the prompt. Pin that down.

## Operating principles

- **Align before crafting.** Never write the prompt until intent is pinned down and confirmed.
- **Ask only what you cannot infer.** Extract everything the user's idea already answers; ask about the
  gaps only, highest-leverage first.
- **Be decisive.** Recommend an option, don't present an open menu.
- **One checkpoint.** Restate the spec once, get a yes, then craft.
- **Ground the craft in real guidance**, not memory. Load `references/` at craft time.

## Step 0 — Detect mode and depth

- **Mode:** *craft-new* (default) or *refine-existing* (user pasted a prompt, passed `--refine`, or asked
  to improve/fix one — diagnose against the dimensions, then rebuild weak parts).
- **Depth:** `--quick` (one round max, sensible assumptions) · *standard* (1–2 rounds) · `--deep`
  (exhaustive alignment, advanced references, optional real test-run before delivery).

## Step 1 — Intake (do this silently)

Parse the idea and map it to the **nine dimensions of a complete prompt spec**, marking each
*known / partial / unknown*:

1. **Goal** — the real job to be done.
2. **Output** — format, length, structure.
3. **Audience** — who consumes the output (a person? a program?).
4. **Success criteria** — what great looks like, concretely.
5. **Failure modes** — what must never happen.
6. **Context GPT needs** — facts, documents, definitions.
7. **Constraints** — tone, must/must-not, limits.
8. **Target model + usage** — **reasoning vs non-reasoning model**; developer/system vs user message;
   Responses API vs Chat Completions; one-shot vs agentic; `reasoning_effort` / `verbosity`; reuse/variables.
9. **Examples available** — samples for few-shot.

Dimension #8 carries the GPT-specific reasoning fork — treat it as load-bearing.

## Step 2 — Alignment dialogue

Ask about *unknown/partial* dimensions only, most important first.

- Use **AskUserQuestion** for bounded choices (target model, output format, tone) — lead with a
  recommended option. Use freeform questions for the user's own words (domain facts, the real goal).
- **Always resolve the reasoning fork (dimension #8).** If the user doesn't know, recommend: reasoning
  model for ambiguous/multi-step/agentic/analysis tasks; non-reasoning workhorse for speed, cost, and
  well-defined execution. Most real systems mix both.
- Batch related questions. Respect depth. Escape hatch: on "just draft it", proceed on explicit assumptions.

## Step 3 — Alignment checkpoint

Present a **compact spec** (the nine dimensions, filled, a few tight lines; mark assumptions). Get the
user's confirmation or corrections before crafting.

## Step 4 — Load the craft references (progressive disclosure)

Only now, load the technique library:

- Always read [references/techniques.md](references/techniques.md) — the lean core, including the
  reasoning-vs-non-reasoning split.
- Read [references/techniques-advanced.md](references/techniques-advanced.md) **if** the spec is agentic /
  tool-using / long-context / RAG / structured-output-heavy / multi-agent / eval, **or** under `--deep`.
- Skim [references/examples.md](references/examples.md) for worked before/after patterns.

Pick the few techniques that fit; don't apply everything.

## Step 5 — Craft the prompt (GPT idiom)

Branch on the target model (full rationale in `references/techniques.md`):

**Shared (both kinds):**
- **Roles:** put top-priority instructions in the **developer** message (Responses API) or **system**
  message (Chat Completions) — they outrank the user. The **user** message holds the variable input.
  Deliver the messages clearly labeled.
- **Structure with Markdown** — headers and short sections. For embedded documents use XML-ish or
  key-value delimiters (`<doc id="1">…</doc>` or `ID:1 | TITLE:… | CONTENT:…`); avoid wrapping large
  doc sets in JSON.
- **Be explicit and internally consistent** — GPT follows instructions literally and precisely;
  contradictions are costly (the model burns effort reconciling them). Audit the prompt for conflicts.
- **Few-shot:** show desired behavior with examples, and make sure every behavior shown is also stated.
- For **JSON output**, use **Structured Outputs** (`strict: true`) rather than asking for JSON in prose.
- **Long context:** repeat key instructions at the **start and end**; if only once, put them above the context.

**If non-reasoning workhorse (GPT-4.1, or GPT-5.x at `none` effort):**
- **Induce planning explicitly** ("think step by step", or a Reasoning Steps section) — it won't reason
  internally on its own.
- For agents, add the **persistence / tool-calling / planning reminders** (keep going until solved;
  use tools instead of guessing; plan before and reflect after tool calls).
- A solid skeleton: `# Role and Objective` → `# Instructions` → `# Reasoning Steps` → `# Output Format`
  → `# Examples` → `# Context` → final reminder.

**If reasoning model (GPT-5.x thinking, o-series):**
- **Give the goal, not the chain of thought.** Do NOT add "think step by step" — it reasons internally and
  CoT prompting can hurt. Keep instructions brief, clear, direct.
- **Zero-shot first**; add few-shot only if needed.
- State constraints + success criteria; set `reasoning_effort` to match difficulty; add
  "Formatting re-enabled" if you need Markdown output.
- Add explicit **persistence** wording if the task must finish end-to-end in one turn.

For *refine-existing*: keep what works, rewrite weak dimensions, remove contradictions, and say what changed.

## Step 6 — Self-critique (red-team before delivering)

Critique the draft against the spec, then revise once:
- Serves the **goal** and **success criteria**?
- **Failure-mode checklist:** instruction contradictions (especially damaging for GPT), CoT prompting on a
  reasoning model (remove it), missing planning inducement on a workhorse, vague output format, untested
  schema, wrong role placement, prompt-injection surface on untrusted input.
- Cut anything not pulling its weight.
- Under `--deep`: optionally run the prompt once on a sample (state the model + settings) and show the result.

## Step 7 — Deliver

Present, in this order:
1. **The prompt**, in a copy-paste code block, with **Developer/System** and **User** messages clearly separated.
2. **Design notes** (brief): key techniques applied and *why*; target model + recommended settings
   (`reasoning_effort`, `verbosity`, API choice); how to use it.

Then offer the three delivery options and act on the choice:
- **Inline** — already shown (default).
- **Save to a file** — ask for a path; suggest a sensible default (e.g. `./prompts/<slug>.md`); write the
  prompt + design notes with the **Write** tool.
- **Copy to clipboard** — copy via **Bash**, OS-aware (detect with `uname`): macOS `pbcopy`; Linux
  `xclip -selection clipboard` or `wl-copy`; Windows `clip`. Confirm it's copied.

---

This skill targets **OpenAI / GPT**. For Claude prompts, use `claude-prompt-crafting`.
Sources are dated in [references/_sources.md](references/_sources.md); keep them fresh with `refresh-references`.
**Model IDs and reasoning settings change fast** — trust the references over memory and recheck `_sources.md`.
