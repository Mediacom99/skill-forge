---
name: claude-prompt-crafting
description: >
  Turn a rough, messy, or half-formed idea into a production-grade prompt FOR CLAUDE
  (Anthropic) models, through a short, sharp alignment dialogue that nails down intent
  before writing a single line of the prompt. Use this whenever the user wants to write,
  design, build, improve, refine, fix, or debug a prompt, system prompt, developer
  instructions, or agent instructions aimed at Claude / Anthropic / Opus / Sonnet / Haiku /
  Fable — or says things like "help me write a prompt", "make this prompt better",
  "prompt for Claude", "craft a system prompt", "my prompt isn't working", or invokes
  /claude-prompt-crafting. Use it even when the user only describes a task they want Claude
  to do repeatedly and never says the word "prompt". For prompts targeting OpenAI/GPT
  models, use the gpt-prompt-crafting skill instead.
argument-hint: "[your rough idea] [--quick | --deep] [--refine]"
version: 0.1.0
metadata:
  tags: prompt-engineering, prompts, claude, anthropic, system-prompt, alignment
---

# Claude Prompt Crafting

Craft an excellent prompt **for Claude** from whatever the user gives you — even a vague,
repetitive, or contradictory description. The output quality of any prompt is overwhelmingly
determined by how well intent was understood before writing. So the work splits in two:
**first align, then craft.** Do not skip the aligning.

Your job is to run that two-phase process: a tight discovery dialogue that converges on a
complete spec, then a craft step grounded in Anthropic's official prompt-engineering guidance
(bundled in `references/`, loaded only when you reach the craft step).

## Operating principles

- **Align before crafting.** Never write the prompt until intent is pinned down and confirmed.
  A confidently-crafted prompt for the wrong goal is worse than no prompt.
- **Ask only what you cannot infer.** Read the user's idea closely and extract everything it
  already answers. Ask about the *gaps* only, highest-leverage first. Re-asking answered things
  wastes the user's time and trust.
- **Be decisive.** Offer a recommended option, not an open-ended menu. Move fast.
- **One checkpoint.** Restate the spec once, get a yes, then craft.
- **Ground the craft in real guidance**, not memory. Load `references/` at craft time.

## Step 0 — Detect mode and depth

- **Mode:**
  - *craft-new* (default) — build a prompt from an idea.
  - *refine-existing* — the user pasted an existing prompt, or passed `--refine`, or asked to
    improve/fix one. Diagnose it against the dimensions below, then rebuild the weak parts.
- **Depth:**
  - `--quick` — one short round of questions max; bias toward sensible assumptions.
  - *standard* (default) — one to two focused rounds.
  - `--deep` — exhaustive alignment, advanced references, and an optional real test-run before delivery.

## Step 1 — Intake (do this silently)

Parse the idea and map it onto the **nine dimensions of a complete prompt spec**. Mark each as
*known* (the idea answers it), *partial*, or *unknown*:

1. **Goal** — the real job to be done (look past the literal ask to the outcome).
2. **Output** — format, length, structure of what Claude should produce.
3. **Audience** — who reads/uses the output.
4. **Success criteria** — what a great result looks like, concretely.
5. **Failure modes** — what must never happen (the things that would ruin it).
6. **Context Claude needs** — facts, documents, domain knowledge, definitions.
7. **Constraints** — tone, must/must-not, length limits, banned moves.
8. **Target model + usage** — which Claude model; system vs user message; one-shot vs agentic/
   multi-turn; API vs chat; effort/temperature; how the prompt gets reused (template variables?).
9. **Examples available** — any samples of good (or bad) output, for multishot.

For *refine-existing*, also note which dimensions the current prompt handles well vs poorly.

## Step 2 — Alignment dialogue

Ask about the *unknown* and *partial* dimensions only, most important first. Keep it human and short.

- Use the **AskUserQuestion** tool when the choice is bounded (e.g. tone, output format, target
  model) — lead with the option you'd recommend and label it. Use plain freeform questions when
  the answer needs the user's own words (e.g. the actual domain facts, the real goal).
- Batch related questions so the user isn't ping-ponged.
- Respect depth: `--quick` = at most one round, then proceed on stated assumptions; `--deep` = keep
  going until every dimension is solid, including edge cases.
- **Escape hatch:** if the user says "just draft it" / "you decide", stop asking, fill remaining
  gaps with explicit best-guess assumptions, and surface those assumptions in the checkpoint.
- Probe for the things people usually leave out: the failure modes (#5), the real success bar (#4),
  and how the prompt will actually be *used* (#8). These are where prompts quietly fail.

## Step 3 — Alignment checkpoint

Before crafting, present a **compact spec** — the nine dimensions, filled, in a few tight lines
(omit any that are genuinely N/A). Mark any assumptions you made. Then ask the user to confirm or
correct. This is the contract. Do not proceed to crafting until they confirm (or already said
"just draft it").

## Step 4 — Load the craft references (progressive disclosure)

Only now — not earlier — load the technique library, so the dialogue stays cheap:

- Always read [references/techniques.md](references/techniques.md) — the lean core.
- Read [references/techniques-advanced.md](references/techniques-advanced.md) **if** the spec is
  agentic / tool-using / long-context (20k+ tokens) / RAG / multi-agent / an LLM-as-judge or eval
  prompt, **or** if `--deep`.
- Skim [references/examples.md](references/examples.md) for worked before/after patterns.

Select the *few* techniques that fit this spec. Do not apply everything — a focused prompt beats a
kitchen-sink one.

## Step 5 — Craft the prompt (Claude idiom)

Write the prompt the way Claude works best (full rationale and current specifics in
`references/techniques.md`):

- **Split system vs user.** Durable role, rules, and craft constraints go in the **system** prompt;
  the variable payload (the actual input/topic) goes in the **user** message. Deliver both, clearly labeled.
- **Open with a role** in one or two sentences ("You are …"). Even a sentence shifts tone and focus.
- **Structure with XML tags** (`<instructions>`, `<context>`, `<examples>`, `<input>`); wrap variable
  inputs in tags too, using `{{double_bracket}}` placeholders.
- **Instruct positively** — say what TO do, not a pile of "don'ts"; give the *reason* behind a
  constraint so Claude generalizes from it.
- **Add 3–5 examples** wrapped in `<example>` tags when format, tone, or structure matter; make them
  relevant, diverse, and structured.
- **Match prompt style to desired output** (clean prose prompt → clean prose output) and state
  **success criteria** and explicit **scope** ("apply this to every section, not just the first").
- **Set reasoning/effort and output budget** when the task is hard or long (see references).

For *refine-existing*: keep what works, rewrite only the weak dimensions, and tell the user what you
changed and why.

## Step 6 — Self-critique (red-team before delivering)

Critique your own draft against the spec, then revise once:

- Does it directly serve the **goal** and the **success criteria**?
- Walk the **failure-mode checklist**: ambiguous instructions, missing context, negative-only
  phrasing, no examples where they'd help, unclear output format, role in the wrong place, scope not
  stated, contradictions, prompt-injection surface if it handles untrusted input.
- Is anything in it not pulling its weight? Cut it.
- Under `--deep`: optionally run the prompt once on a sample input (state the model you'd use) and show
  the result so the user sees it work.

## Step 7 — Deliver

Present, in this order:

1. **The prompt**, in a copy-paste code block, with **System** and **User** clearly separated.
2. **Design notes** (brief): the key techniques you applied and *why*; the target model + recommended
   settings (effort, output budget, temperature); and how to use it (system vs user, where variables go).

Then offer the three delivery options and act on the choice:

- **Inline** — already shown above (default).
- **Save to a file** — ask for a path; suggest a sensible default (e.g. `./prompts/<slug>.md` in the
  current directory). Write the prompt plus the design notes with the **Write** tool.
- **Copy to clipboard** — copy the prompt text via **Bash**, picking the command for the OS
  (detect with `uname`): macOS `pbcopy`; Linux `xclip -selection clipboard` or `wl-copy`; Windows
  `clip`. Example (macOS): pipe the prompt into `pbcopy`. Confirm it's copied.

---

This skill targets **Claude**. For OpenAI/GPT prompts, use `gpt-prompt-crafting`.
The technique libraries are sourced and dated in
[references/_sources.md](references/_sources.md); keep them fresh with the `refresh-references` skill.
