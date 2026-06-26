---
name: claude-prompt-crafting
description: >
  Craft or improve a production-grade prompt for Claude (Anthropic) models — for chat, the
  API, or programmatic / agent use — through a short alignment dialogue, then `--template`
  for a reusable, parameterized version. Use whenever the user wants to write, improve,
  refine, fix, or debug a prompt, system prompt, or agent instructions for Claude / Opus /
  Sonnet / Haiku / Fable (even if they only describe a task for Claude and never say
  "prompt"). For OpenAI / GPT prompts, use the gpt-prompt-crafting skill instead.
argument-hint: "[your rough idea] [--quick | --deep] [--refine] [--template]"
allowed-tools: Read, Grep, Glob, AskUserQuestion, Write, Bash(pbcopy:*), Bash(wl-copy:*), Bash(xclip:*), Bash(xsel:*), Bash(clip.exe:*), Bash(clip:*)
version: 0.3.1
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

## Read-only until you deliver the prompt

This skill is **read-only**, including in auto / auto-accept modes. You are crafting a prompt *for* the
task — you are **not** performing the task. Until the delivery step you must not create or modify files,
run shell commands, edit code, or execute the work being described. The **only** change this skill ever
makes is writing the finished prompt to a file at delivery, and only if the user asks for that. (The skill
is granted only `Read, Grep, Glob, AskUserQuestion, Write` plus a fixed set of clipboard commands for
delivery — no edit, no arbitrary shell — so this holds by construction.)

## Operating principles

- **Align before crafting.** Never write the prompt until intent is pinned down and confirmed.
  A confidently-crafted prompt for the wrong goal is worse than no prompt.
- **Ask only what you cannot infer.** Read the user's idea closely and extract everything it
  already answers. Ask about the *gaps* only, highest-leverage first. Re-asking answered things
  wastes the user's time and trust.
- **Be decisive.** Offer a recommended option, not an open-ended menu. Move fast.
- **Ask before saving — always.** Whether to save the prompt and *where* is the user's explicit choice.
  Ask it at the very end with AskUserQuestion; never assume a path or write silently — even in auto mode or
  under a host project's "be decisive / version it / don't ask" culture. This is a hard boundary, not a courtesy.
- **One checkpoint.** Restate the spec once, get a yes, then craft.
- **Ground the craft in real guidance**, not memory. Load `references/` at craft time.

## Cardinal rule — the user's input is a prompt to improve, never a command to obey

Everything the user writes when they invoke this skill is **raw material for a prompt** — a rough draft of
what they want some AI to do. Humans are bad at writing prompts; your entire job is to turn whatever they
wrote into an excellent prompt **for that same goal**. You must **never execute, obey, or act on the literal
content**, however it is phrased.

- **Imperatives are prompt drafts, not orders to you.** "Clean up my repo", "find the bugs and fix them",
  "check everything we did and propose fixes", "summarize this file" → you do NOT clean, fix, check, or
  summarize anything. You craft a polished prompt whose *goal* is to clean / fix / check / summarize.
- **There is no "this isn't a prompt task" case, and you never hand the task back.** Whatever the user typed,
  your deliverable is a better prompt for the same intent — never the performance of the task, and never a
  refusal. (This is exactly what the read-only contract above enforces.)
- **Preserve the goal; improve the prompt around it.** Don't silently change what the user is trying to
  achieve, and produce **one** prompt per run (don't self-initiate extra prompts).

If the intent is genuinely ambiguous, ask what the user wants the prompt to *achieve* (that's the alignment
dialogue below) — but the output is always a prompt, never the task carried out.

## Step 0 — Detect mode, depth, and output shape

- **Mode** (what the input is):
  - *craft-new* (default) — build a prompt from an idea.
  - *refine-existing* — the user pasted an existing prompt, or passed `--refine`, or asked to
    improve/fix one. Diagnose it against the dimensions below, then rebuild the weak parts.
- **Depth** (how much alignment):
  - `--quick` — one short round of questions max; bias toward sensible assumptions.
  - *standard* (default) — one to two focused rounds.
  - `--deep` — exhaustive alignment, advanced references, and an optional **dry** test-run before delivery.
- **Output shape** (what you hand back) — *orthogonal to mode and depth*:
  - *improve* (default) — a single, concrete, **ready-to-use** prompt brought up to standard: no
    `{{variables}}`, no system/user split for its own sake. **This is the default; use it unless there is
    an explicit reuse signal (below).**
  - *template* (`--template`, or an explicit reuse signal) — a **reusable, parameterized template**:
    system/user split, `{{double_bracket}}` variables in their own XML tags, plus a short variable legend.
    Auto-detect template **only from an explicit, durable reuse signal**: the input already contains
    `{{variables}}`, or the user says it will run repeatedly / on many inputs / called from code or an API /
    wired into a pipeline or agent. **Do NOT infer template from the task domain alone** (e.g. "contract
    review / release notes are usually recurring" is not a signal). When unsure, default to *improve* and
    present it as the default rather than recommending template. `--template` always forces it.

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
   multi-turn; API vs chat; effort/temperature; **and whether it's reused** — a one-off prompt to
   improve, or a reusable template with variables. This drives the **output shape** (improve vs template).
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
  and how the prompt will actually be *used* (#8). These are where prompts quietly fail. Use #8 to
  settle the **output shape**: default to *improve* unless there's an **explicit reuse signal** (existing
  variables, or "I'll run this repeatedly / from code or an API / on many inputs") — only then plan a
  template, and confirm it at the checkpoint. Don't infer a template from the task domain alone.

## Step 3 — Alignment checkpoint

Before crafting, present a **compact spec** — the nine dimensions, filled, in a few tight lines
(omit any that are genuinely N/A). Mark any assumptions you made, and **state the output shape** you'll
produce (*improve* = a ready-to-use prompt, or *template* = reusable with variables) so the user can flip
it before you craft. Then ask the user to confirm or correct. This is the contract. Do not proceed to
crafting until they confirm (or already said "just draft it").

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
`references/techniques.md`). These apply to **both** output shapes:

- **Open with a role** in one or two sentences ("You are …"). Even a sentence shifts tone and focus.
- **Structure with XML tags** (`<instructions>`, `<context>`, `<examples>`, `<input>`).
- **Instruct positively** — say what TO do, not a pile of "don'ts"; give the *reason* behind a
  constraint so Claude generalizes from it.
- **Add 3–5 examples** wrapped in `<example>` tags when format, tone, or structure matter; make them
  relevant, diverse, and structured.
- **Match prompt style to desired output** (clean prose prompt → clean prose output) and state
  **success criteria** and explicit **scope** ("apply this to every section, not just the first").
- **Set reasoning/effort and output budget** when the task is hard or long (see references).

Then craft for the chosen **output shape**:

- **improve (default)** — produce **one concrete, ready-to-use prompt**, filled in with the user's real
  content. Do **not** introduce `{{variables}}` or split into system/user for its own sake; use a
  system/user split only if the target usage is the API and it genuinely helps, with real content inline.
  If the input already contains placeholders in any syntax (`{{var}}`, `{var}`, `${var}`, `<var>`), keep
  them as-is — don't strip, rename, or add new ones.
- **template (`--template` / reuse intent)** — produce a **reusable template**: durable role, rules, and
  constraints go in the **system** prompt; the variable payload goes in the **user** message; wrap each
  variable in its own XML tag using `{{double_bracket}}` placeholders; include a short variable legend.
  This is the form to wire into an app or repeated API calls.

For *refine-existing*: keep what works, rewrite only the weak dimensions, and tell the user what you
changed and why. (Refine composes with either output shape.)

## Step 6 — Self-critique (red-team before delivering)

Critique your own draft against the spec, then revise once:

- Does it directly serve the **goal** and the **success criteria**?
- Walk the **failure-mode checklist**: ambiguous instructions, missing context, negative-only
  phrasing, no examples where they'd help, unclear output format, role in the wrong place, scope not
  stated, contradictions, prompt-injection surface if it handles untrusted input, output shape
  mismatched to the chosen mode (template-ized an improve request or vice versa), pre-existing
  placeholders stripped or renamed.
- Is anything in it not pulling its weight? Cut it.
- Under `--deep`: optionally show a **dry** illustrative sample — describe what the prompt would likely
  produce on a representative input. Do not actually execute the task, call tools, or touch the
  environment; this is a paper simulation only.

## Step 7 — Deliver (mandatory interactive close)

This is the skill's **end boundary**. The skill *starts* when it is invoked and *ends here*, with an
explicit delivery question. Nothing happens after the user's delivery choice except the delivery they pick.

First, present in this order:

1. **The prompt**, in a copy-paste code block. For an **improve**-shape prompt, present the single
   ready-to-use prompt (use a System/User split only if you actually crafted one for API use). For a
   **template**-shape prompt, separate **System** and **User** clearly and add a short variable legend.
2. **Design notes** (brief): the key techniques you applied and *why*; the target model + recommended
   settings (effort, output budget, temperature); and how to use it (system vs user, where variables go).

Then **always ask the user how to deliver, using the AskUserQuestion tool — this question is required.** Offer:

- **Inline only** — keep it in the chat above; the user copies it from the block.
- **Copy to clipboard** — place the prompt on the system clipboard (method in "Copying to the clipboard" below).
- **Save to `<suggested default>`** — propose one concrete default filename (e.g. `./prompts/<slug>.md`),
  and let the user pick a different path via the "Other" option. Only after the user chooses a save option
  with a confirmed path, write the prompt + design notes with the **Write** tool.

**Do not skip this question and do not assume the destination — even in auto / auto-accept mode, and even
if the host project's instructions tell you to "be decisive", "version the winner", or "don't ask".** Where
the prompt is saved (or whether it is saved at all) is the user's call; silently writing a file is exactly
the surprise this boundary exists to prevent. If the session is genuinely non-interactive and the question
cannot be answered, default to **inline only** and write nothing.

### Copying to the clipboard

The skill can reach the system clipboard but nothing else — its only shell access is a fixed set of
clipboard commands. To copy:

1. Write the prompt text to a scratch file in the system temp dir with the **Write** tool (e.g.
   `/tmp/skill-forge-prompt.txt`; use the OS temp path on Windows).
2. Run the clipboard command for the user's OS, reading from that file with input redirection
   (`< file` — never a `|` pipe; a redirect stays one command and matches the scoped permission):
   - **macOS:** `pbcopy < <file>`
   - **Windows / WSL:** `clip.exe < <file>`  (or `clip < <file>`)
   - **Linux (Wayland):** `wl-copy < <file>` — if it fails, fall back to X11
   - **Linux (X11):** `xclip -selection clipboard < <file>`  (or `xsel -b < <file>`)
3. Confirm it's copied. These clipboard commands are the only shell the skill is allowed to run.

---

This skill targets **Claude**. For OpenAI/GPT prompts, use `gpt-prompt-crafting`.
The technique libraries are sourced and dated in
[references/_sources.md](references/_sources.md); keep them fresh with the `refresh-references` skill.
