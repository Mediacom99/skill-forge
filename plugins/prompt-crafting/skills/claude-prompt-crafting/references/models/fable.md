<!--
last-verified: 2026-09-07
sources: _sources.md #8 — prompting-claude-fable-5-1 (Fable 5.1 / Mythos 5.1 — the default target here)
         _sources.md #4 — prompting-claude-fable-5 (Fable 5 / Mythos 5 — the base this builds on)
scope: Per-model tuning for the Fable family (frontier — long-horizon, agentic, ambiguity-tolerant).
Written for Claude Fable 5.1 / Mythos 5.1; what differs on Claude Fable 5 / Mythos 5 is in the last
section. Loaded at craft time only when the target model is Fable/Mythos. Applies on top of techniques.md.
Agentic-scaffolding items are flagged; skip them for one-shot/chat prompts.
-->

# Tuning for Claude Fable 5.1 / Mythos 5.1

The Fable tier takes on problems that were too complex, long-running, or ambiguous for prior models —
end-to-end work that takes a person hours, days, or weeks. It's a **strong instruction-follower**, so the
guiding principle inverts the usual advice: **brief, outcome-led instructions beat enumerating every
behavior.** Over-prescriptive prompts (especially ones ported from older models) can *degrade* output.

Fable 5 prompts run well on Fable 5.1 unchanged. The deltas in **What changed in 5.1** are where tuning pays.

## Effort
- **`high` = default.** Sweep all five levels (`low`…`max`) against your own evals — and **re-sweep even if
  you swept on Fable 5**: effort names don't map to the same amount of thinking across models.
- 5.1's gains show at every level and are largest at the top. At **`medium`** it roughly matches Fable 5 at
  lower cost — step down where quality holds. At **`low`** it's often competitive with Opus/Sonnet on cost
  per task while scoring higher, so include it wherever you'd otherwise run a smaller model at high effort.
- Two effort-specific behaviors have their own items below: less search-tool triggering at `low`, and longer
  pre-writing thinking at `xhigh`/`max`.

## Steer with brief instructions, not enumerations
- One short instruction steers most behaviors. For **checkpoints** in long workflows: *"Pause for the user
  only when the work genuinely requires them — a destructive/irreversible action, a real scope change, or
  input only they can provide. Ask and end the turn rather than ending on a promise."*
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
- **Do NOT ask the model to reproduce, echo, transcribe, or explain its internal reasoning as response text.**
  Such "show your thinking / reflect on your reasoning" instructions can trigger the **`reasoning_extraction`
  refusal** and cause elevated fallbacks to Opus 4.8. If the app needs reasoning visibility, read the
  structured `thinking` blocks from adaptive thinking instead. **Audit ported prompts/skills** for
  show-your-work language before targeting this family.
- Fable is **adaptive-thinking-only** with no extended-thinking budgets; effort is the depth control.

## Safety & fallback (API)
- Runs safety classifiers targeting **offensive cybersecurity**, **biology/life-sciences**, and
  **reasoning-extraction**; declined requests return `stop_reason: "refusal"`. Configure **server- or
  client-side fallback to Opus 4.8** to auto-reroute.
- 5.1 produces **fewer false positives** than Fable 5 did at launch, and **finding vulnerabilities in source
  code is permitted**. Three things still raise the odds: **compile-check phrasing** (ask *"are there any bugs
  in this program?"*, not *"does this compile without errors?"*), **lesser-known languages** (give the model
  the language's docs/context), and **base64 in tool output** (strip it).

## What changed in 5.1 — the tuning that pays

- **It narrates less.** Fewer user-facing updates during long tool-calling turns, more so at high effort and
  in long chains; users see minutes of silence. First check your client is *receiving* them — the between-call
  notes arrive as progress-update `thinking` blocks, empty under the default `display: "omitted"` (set
  `display: "updates"`, beta, or `"summarized"`). Then **delete legacy lines that suppress narration**
  ("hold all findings for the final response"). Only then add: *"Before you start, say in a line what you're
  about to do; brief updates while you work help the user follow along. Close with a short recap that stands
  on its own — what you found, what you did, and what's next."*
- **One tool call per turn in coding / computer-use loops** (where the next calls are implied rather than
  asked for). Nudge: *"First privately list what you need next; then request every item that doesn't depend
  on another's result in this one response."* Re-send it each turn as a **turn-scoped system message**
  (`clear_at: "next_user_message"`, beta) after the tool results — appended fresh, earlier copies left
  untouched.
- **Keep the conversation history append-only.** Replay each assistant turn exactly as returned, thinking
  blocks included. Editing earlier turns — injecting/removing per-turn reminders, summarizing in place,
  rebuilding `system` or `tools` — invalidates every later thinking block (a 400 for accounts created on or
  after **2026-08-31**, and expected to become universal). Send reminders as turn-scoped system messages,
  change instructions via mid-conversation system messages, and let server-side compaction do the trimming.
  *(Harness constraint, not prompt text — but it decides whether a per-turn reminder is safe to write.)*
- **Denser prose.** Longer sentences, fewer breaks. Name the anti-pattern: *"Please remove all mannered
  prose"* — or the long form defining mannered prose as metaphor and flourish substituted for direct
  statement ("a dial worth turning" for "a parameter worth varying"), which makes the reader work so the
  writer can perform, and drags in connotations the writer didn't choose.
- **It under-formats in chat** (less bold, fewer headers/lists) — the opposite of older models. **Remove
  anti-formatting rules** you inherited; replace with a when-to rule: *"Use lists and bullet points when
  asked to, or when the content is multifaceted enough that they aid clarity; plain prose for conversational,
  personal, or emotional exchanges."*
- **Unmarked quoting** when summarizing retrieved documents. Fix with **one complete worked example** in the
  system prompt — request, response, and a `<rationale>` saying why it's correct (own indirect speech, at most
  a short marked phrase, everything else reworded). Template the tool-call lines so they read as tool output.
- **Finishing the whole task.** On async work it may describe next steps instead of doing them, or ask
  permission for something already in scope. Two system-prompt blocks, in order of value: (1) *"You are
  operating autonomously. The user is not watching and cannot answer mid-task… For reversible actions that
  follow from the original request, proceed without asking. Before ending your turn, check your last
  paragraph: if it is a plan, a question, or a promise ('I'll…'), do that work now with tool calls."*
  (2) a **delivering-work** block — the request sets the scope and the scope is the deliverable; don't
  narrow, widen, or swap it; do the parts that don't depend on an open question first; if one part is
  blocked, finish the rest and say what you left out.
- **Scope and test sprawl** on open-ended features (fixing nearby code, committing more tests than the change
  warrants): *"If you find a pre-existing bug or unrelated concern, report it as a follow-up rather than
  fixing it. Commit tests only where the task asks or the repo already keeps them for this kind of change…
  This is about extras only: implement every behavior the task asks for, completely."*
- **Search triggering at `low`.** It answers from memory more than Fable 5 did. Raise effort for the affected
  turns, or tell it that recognizing a name isn't knowing its current state: search fast-moving names *as the
  user wrote them* before answering, because partial background is what makes a stale answer sound
  authoritative.
- **Whole-file rewrites** for small edits: *"The number of tokens used to edit files is best minimized, all
  else being equal. Therefore, when it will not affect the end result, try to surgically edit a file rather
  than rewrite the entire thing."*
- **Long outputs at `xhigh`/`max`.** It can draft the deliverable in thinking and then write it again. Run
  these at `high`; if you don't, leave `max_tokens` headroom for thinking *and* reply, and append a note that
  both share one limit of about `[max_tokens]` tokens, so it should *"use the reasoning space to reason and
  the output space to write an output."*
- **Client-side compaction:** it responds well to being told exactly what a summary must keep — problems and
  how they were resolved, options tried or set aside, anything asked/decided/ruled out stated exactly, where
  things stand, what's still open, and hard-to-reconstruct specifics; keep the user's words close to verbatim
  and condense your own reasoning. (Server-side compaction already does this.)

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
  while they run; intervene if one goes off track."* On 5.1, **don't force the lead agent to block**: have the
  spawn tool return immediately, deliver results in a later `user` message, and give the lead a separate
  "wait" tool. Prefer long-lived subagents (cache reads, no bottleneck on the slowest).
- **`send_to_user` tool:** for async agents, a client-side tool that surfaces a message verbatim mid-turn
  (partial deliverable, direct answer) without ending the turn. **Defining it isn't enough** — pair it with an
  elicitation line ("when you have content the user must read verbatim, call `send_to_user`") and use it only
  for user-facing content, not narration.
- **Context-budget calm:** if the harness shows a remaining-token countdown it may offer to hand off/summarize;
  avoid surfacing counts, or add *"You have ample context remaining; do not stop or suggest a new session."*
- **Vision:** 5.1 does its best work on dense charts/screenshots when it can **crop and zoom** — run it with a
  container holding the raw images plus PIL/OpenCV, or at minimum a crop tool returning an enlarged region.
- **Aim higher than you would for prior models.** Pick a task at the top of your difficulty range and let it
  scope, ask clarifying questions, and execute — testing it only on simpler workloads undersells its range.
- **Self-verification beats self-critique:** for long-running tasks, prefer separate, fresh-context verifier
  subagents over asking it to check its own work: *"Establish a method for checking your own work at an
  interval of [X] as you build. Run this every [X interval], verifying your work with subagents against the
  specification."*

## If the target is Claude Fable 5 / Mythos 5
Everything above applies **except the "What changed in 5.1" items**, which are 5.1-specific — and two of them
invert:
- **Fable 5 over-elaborates** rather than going quiet (surveying options it won't pursue, narrating next
  steps, over-structured PR text, heavily-formatted output). Add a brevity line instead of a narration one:
  *"Lead with the outcome — your first sentence answers 'what happened / what did you find.' Supporting detail
  after. Be selective about what you include rather than compressing into fragments or arrow-chains."*
- **Readability after long runs:** its final summary can be dense working shorthand — instruct it to drop the
  shorthand, write complete sentences, and open with the outcome for a reader who saw none of it.
- Preserved thinking, turn-scoped batching nudges, mannered prose, low-effort search triggering, whole-file
  rewrites, and the `xhigh`/`max` output-headroom note are **not** Fable 5 behaviors — don't port them.

## Migration note
- Skills/prompts tuned for **prior generations** are often too prescriptive for this family and can hurt
  quality. Keep instructions brief and outcome-led. Coming from **Fable 5**, the reverse risk applies: lines
  written to hold down its over-elaboration and over-formatting now suppress behavior 5.1 doesn't have.
