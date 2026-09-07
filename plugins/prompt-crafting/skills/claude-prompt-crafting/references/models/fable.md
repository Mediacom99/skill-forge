<!--
last-verified: 2026-09-07
source: _sources.md #8 — prompting-claude-fable-5-1 (dedicated Fable 5.1 / Mythos 5.1 page, current frontier);
#4 — prompting-claude-fable-5 (prior-gen Fable 5 / Mythos 5 page, baseline guidance still valid)
scope: Per-model tuning for Claude Fable 5.1 / Mythos 5.1 (current frontier — long-horizon, agentic,
ambiguity-tolerant), with Fable 5 / Mythos 5 deltas called out. Loaded at craft time only when the target
model is Fable/Mythos. Applies on top of techniques.md. Agentic-scaffolding items are flagged; skip them for
one-shot/chat prompts.
-->

# Tuning for Claude Fable 5.1 / Mythos 5.1 (and Fable 5 / Mythos 5)

Fable takes on problems that were too complex, long-running, or ambiguous for prior models — end-to-end work
that takes a person hours, days, or weeks. It's a **strong instruction-follower**, so the guiding principle
inverts the usual advice: **brief, outcome-led instructions beat enumerating every behavior.**
Over-prescriptive prompts (especially ones ported from older models) can *degrade* its output. **Fable 5.1 is
the current release**; existing Fable 5 prompts carry over without changes, but the deltas below (progress
updates, tool-call batching, conversation-history binding, writing density, formatting, edit style, safeguard
false positives) are worth checking against your own evals.

## Effort
- **`high` = default** for most tasks. **`xhigh`** for the most capability-sensitive work. **`medium`/`low`**
  for routine work — lower effort still performs well and often exceeds `xhigh` on prior models.
- Reduce effort if a task completes but takes longer than needed, or when you want a quicker, interactive feel.
- **Fable 5.1 delta:** re-run your effort sweep even if you already tuned it for Fable 5 — effort-level names
  don't map to the same amount of thinking across models. Gains over Fable 5 are largest at higher effort; at
  `medium` it roughly matches Fable 5 quality at lower cost, and at `low` it's often cost-competitive with
  Opus/Sonnet at a higher effort while scoring better — include it in that comparison rather than defaulting
  up. Two effort-specific gotchas: at `low`, it's less likely to call search/retrieval tools (see below); at
  `xhigh`/`max` on a long deliverable, it can draft the output once in thinking and again in the reply,
  doubling length and latency — for long single-shot deliverables, start at `high` and only raise effort where
  you've measured a quality gain; if you do run `xhigh`/`max`, leave headroom in `max_tokens` for both passes
  and tell it explicitly not to compose the full deliverable twice.

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
- **Do NOT ask Fable to reproduce, echo, transcribe, or explain its internal reasoning as response text.**
  Such "show your thinking / reflect on your reasoning" instructions can trigger the **`reasoning_extraction`
  refusal**. If the app needs reasoning visibility, read the structured `thinking` blocks from adaptive
  thinking instead. **Audit ported prompts/skills** for show-your-work language before targeting Fable.
- Fable is **adaptive-thinking-only** with **summarized-only** thinking output and **no extended-thinking
  budgets**; effort is the depth control.

## Safety & fallback (API)
- Runs safety classifiers targeting **offensive cybersecurity**, **biology/life-sciences**, and
  **reasoning-extraction**; benign work in those areas can also trip them. Declined requests return
  `stop_reason: "refusal"`. The Fable 5 page documents **server- or client-side fallback to Opus 4.8** to
  auto-reroute declines — the Fable 5.1 page reconfirms the same refusal categories with **fewer false
  positives** at launch than Fable 5 had, but doesn't restate the fallback target on-page (it's on the
  untracked `whats-new-fable-5-1` page), so treat "still falls back to Opus 4.8" as likely but unconfirmed for
  5.1 specifically.
- **Three residual false-positive triggers on Fable 5.1:** compile-check phrasing ("does this compile?" — ask
  "are there bugs in this program?" instead), lesser-known programming languages (give it doc context), and
  base64-encoded data in tool output (avoid passing it through).

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
- **Aim higher than you would for prior models.** Pick a task at the top of your difficulty range and let it
  scope, ask clarifying questions, and execute — testing it only on simpler workloads undersells its range.
- **Self-verification beats self-critique:** for long-running tasks, prefer separate, fresh-context verifier
  subagents over asking it to check its own work: *"Establish a method for checking your own work at an
  interval of [X] as you build. Run this every [X interval], verifying your work with subagents against the
  specification."*

## Fable 5.1 deltas vs Fable 5
- **Fewer user-facing progress updates by default**, more pronounced at higher effort and in long tool chains
  — it can go quiet for minutes then summarize only the last step. First check your client actually surfaces
  progress-update `thinking` blocks (empty by default under `thinking.display: "omitted"`; set `"updates"` or
  `"summarized"`, both beta). If updates are reaching you and you still want more, add an explicit cadence +
  a self-contained closing recap instruction (a reader who saw none of the run should still get the full
  picture from the last message).
- **Tool-call batching can regress to one-per-turn** specifically in coding/computer-use loops where the next
  calls are implied rather than explicitly requested (custom bash-and-editor harnesses). A one-line nudge —
  "list what you need next, then request every independent item in this one response" — fixes it; in long
  agent loops, resend that nudge as a **turn-scoped system message** each round rather than only once.
- **Conversation history must be append-only.** For newer accounts, a thinking block replayed after its
  prefix (system prompt, tool list, or an earlier message) changed now returns a 400 or drops the block. Don't
  edit earlier turns, rewrite `system`/`tools` mid-session, or summarize in place; use turn-scoped/mid-
  conversation system messages or server-side compaction instead, or replace the whole history with one
  summary + the new turn if compacting client-side. See `_sources.md`'s volatile-items entry for the current
  scope of enforcement.
- **Denser prose by default** — longer sentences, fewer paragraph breaks, more metaphor/flourish ("mannered
  prose") than Fable 5. If output reads ornate, add a short instruction naming and forbidding that pattern, or
  as a one-liner: *"Please remove all mannered prose."*
- **Less structure in chat by default** (fewer bullets/headers/bold than Fable 5) — remove old anti-formatting
  instructions written for chattier prior models; if you want structure back, say when it's appropriate rather
  than banning it outright.
- **More likely to rewrite whole files for small changes** (the reverse of Fable 5's tendency). Add: *"Prefer
  a surgical edit over rewriting the whole file when it won't affect the result — minimize edit tokens."*
- **Scope creep on open-ended feature work:** may fix nearby code, extend unrequested behavior, or over-commit
  test files. State explicitly that unrequested fixes/extensions become a follow-up note, not an in-scope
  change, and that tests should match the task's own ask plus the repo's existing test density.
- **Weaker search triggering at `low` effort** — more likely to answer fast-moving-topic questions from
  memory. Either raise effort for those turns or add a rule: recognizing a name isn't the same as knowing its
  current state, so search names as written rather than skipping on familiarity.
- **Lead agent can idle while subagents run.** If your harness supports it, make subagent-launch tools return
  immediately and give the lead agent a separate "wait for result" tool so it can keep working meanwhile.

## Migration note
- Fable 5 prompts and skills carry over to Fable 5.1 largely unchanged; check them against the deltas above
  rather than rewriting from scratch.
- Skills/prompts tuned for pre-Fable models are often **too prescriptive** for Fable and can hurt quality.
  Review and remove older instructions when default performance is already better; keep instructions brief and
  outcome-led.
