<!--
last-verified: 2026-07-03
source: _sources.md #4 — prompting-claude-fable-5 (dedicated Fable 5 / Mythos 5 page)
scope: Per-model tuning for Claude Fable 5 and Claude Mythos 5 (current frontier — long-horizon, agentic,
ambiguity-tolerant). Loaded at craft time only when the target model is Fable/Mythos. Applies on top of
techniques.md. Agentic-scaffolding items are flagged; skip them for one-shot/chat prompts.
-->

# Tuning for Claude Fable 5 / Mythos 5

Fable 5 takes on problems that were too complex, long-running, or ambiguous for prior models — end-to-end
work that takes a person hours, days, or weeks. It's a **strong instruction-follower**, so the guiding
principle inverts the usual advice: **brief, outcome-led instructions beat enumerating every behavior.**
Over-prescriptive prompts (especially ones ported from older models) can *degrade* its output.

## Effort
- **`high` = default** for most tasks. **`xhigh`** for the most capability-sensitive work. **`medium`/`low`**
  for routine work — lower effort on Fable 5 still performs well and often exceeds `xhigh` on prior models.
- Reduce effort if a task completes but takes longer than needed, or when you want a quicker, interactive feel.

## Steer with brief instructions, not enumerations
- One short instruction steers most behaviors. To cut over-elaboration (surveying options it won't pursue,
  narrating next steps, over-structured PR text), a brevity line works as well as listing each pattern:
  *"Lead with the outcome — your first sentence answers 'what happened / what did you find.' Supporting
  detail after. Be selective about what you include rather than compressing into fragments or arrow-chains."*
- Same for **checkpoints** in long workflows: *"Pause for the user only when the work genuinely requires them
  — a destructive/irreversible action, a real scope change, or input only they can provide."*
- At higher effort it can over-deliver (unrequested tidying/refactoring). One line reins it in: *"Do the
  simplest thing that works; don't add features, refactors, abstractions, or error handling for cases that
  can't happen. Only validate at system boundaries."*

## Give the reason, not only the request
- It connects a task to relevant context better when it knows the intent: *"I'm working on [larger task] for
  [who]. They need [what the output enables]. With that in mind: [request]."* Especially valuable for
  long-running agents drawing on multiple workstreams.

## State the boundaries
- It can occasionally take unrequested actions (drafting an email, making defensive git backups). Define what
  it should and shouldn't do: when the user is describing a problem or thinking out loud, **the deliverable is
  your assessment — report findings and stop; don't apply a fix until asked.** Check evidence before running
  any state-changing command.

## Reasoning — critical gotcha
- **Do NOT ask Fable 5 to reproduce, echo, transcribe, or explain its internal reasoning as response text.**
  Such "show your thinking / reflect on your reasoning" instructions can trigger the **`reasoning_extraction`
  refusal** and cause elevated fallbacks to Opus 4.8. If the app needs reasoning visibility, read the
  structured `thinking` blocks from adaptive thinking instead. **Audit ported prompts/skills** for
  show-your-work language before targeting Fable 5.
- Fable 5 is **adaptive-thinking-only** with **summarized-only** thinking output and **no extended-thinking
  budgets**; effort is the depth control.

## Safety & fallback (API)
- Runs safety classifiers targeting **offensive cybersecurity**, **biology/life-sciences**, and
  **reasoning-extraction**; benign work in those areas can also trip them. Declined requests return
  `stop_reason: "refusal"`. Configure **server- or client-side fallback to Opus 4.8** to auto-reroute.

## Long-horizon / agentic scaffolding *(only if the prompt drives an agent or long autonomous run)*
- **Longer turns by default:** hard requests can run many minutes at higher effort; autonomous runs for hours.
  Expect the harness (not the prompt) to adjust timeouts/streaming/progress and check runs asynchronously.
  Anti-overplanning line: *"When you have enough information to act, act. If weighing a choice, give a
  recommendation, not an exhaustive survey. (Does not apply to thinking blocks.)"*
- **Ground progress claims:** *"Before reporting progress, audit each claim against a tool result from this
  session. Report only work you can point to evidence for; if unverified, say so."* Nearly eliminates
  fabricated status.
- **Memory system:** give it a place to record lessons — even a Markdown file, **one lesson per file, a
  one-line summary at top**; record corrections and confirmed approaches with *why*; update rather than
  duplicate; delete wrong notes. It performs particularly well when it can reference past-run lessons.
- **Parallel subagents:** it delegates readily — *"Delegate independent subtasks to subagents and keep working
  while they run; intervene if one goes off track."* Prefer async orchestrator↔subagent communication and
  long-lived subagents (cache reads, no bottleneck on the slowest).
- **`send_to_user` tool:** for async agents, a client-side tool that surfaces a message verbatim mid-turn
  (partial deliverable, direct answer) without ending the turn. **Defining it isn't enough** — pair it with an
  elicitation line ("when you have content the user must read verbatim, call `send_to_user`") and use it only
  for user-facing content, not narration.
- **Autonomous pipelines:** add a reminder that no human is watching, so it shouldn't ask "Want me to…?" for
  reversible in-scope actions, and shouldn't end a turn on a plan/promise — do the work with tool calls.
- **Context-budget calm:** if the harness shows a remaining-token countdown it may offer to hand off/summarize;
  avoid surfacing counts, or add *"You have ample context remaining; do not stop or suggest a new session."*
- **Communication style:** in long tool-heavy runs its final summary can be dense shorthand — instruct it to
  drop working shorthand, write complete sentences, and open with the outcome for a reader who saw none of it.

## Migration note
- Skills/prompts tuned for prior models are often **too prescriptive** for Fable 5 and can hurt quality.
  Review and remove older instructions when default performance is already better; keep instructions brief and
  outcome-led.
