<!--
last-verified: 2026-11-16
sources: _sources.md #13 — prompting-claude-fable-5-2 (Fable 5.2 / Mythos 5.2 — the default target here, current frontier)
         _sources.md #8 — prompting-claude-fable-5-1 (Fable 5.1 / Mythos 5.1 — now legacy, previous generation)
         _sources.md #4 — prompting-claude-fable-5 (Fable 5 / Mythos 5 — the base Fable 5.1 built on)
         _sources.md #14 — whats-new-fable-5-2 (untracked, cited only for the refusal-fallback targets and breaking API changes)
scope: Per-model tuning for the Fable family (frontier — long-horizon, agentic, ambiguity-tolerant).
Written for Claude Fable 5.2 / Mythos 5.2; what differs on the legacy Fable 5.1 / Mythos 5.1 and
Fable 5 / Mythos 5 generations is in the sections below. Loaded at craft time only when the target
model is Fable/Mythos. Applies on top of techniques.md. Agentic-scaffolding items are flagged;
skip them for one-shot/chat prompts.
-->

# Tuning for Claude Fable 5.2 / Mythos 5.2

The Fable tier takes on problems that were too complex, long-running, or ambiguous for prior models —
end-to-end work that takes a person hours, days, or weeks. It's a **strong instruction-follower**, so the
guiding principle inverts the usual advice: **brief, outcome-led instructions beat enumerating every
behavior.** Over-prescriptive prompts (especially ones ported from older models) can *degrade* output.

Fable 5.1 prompts run well on Fable 5.2 unchanged — start there, then apply the deltas below. Fable 5.2
**costs less** than Fable 5.1 (roughly 20% lower input/output price) and is the current Fable flagship;
Fable 5.1 is now a legacy model.

## Effort — recalibrate, don't port
- **`high` = default** on the API. Re-sweep against your own evals even if you swept on Fable 5.1 — effort
  names don't map to the same amount of thinking across generations. Most of the capability gain is already
  present at `high`; the step from `medium` to `high` is the single biggest jump on most coding and
  knowledge-work evals.
- At **`low`**, 5.2 scores close to what 5.1 needed higher effort for — a real cost lever for high-volume
  work (e.g. fast subagents). `medium` suits interactive coding/chat/everyday knowledge work. `xhigh` is for
  measured gains on your hardest long-running coding/agentic work; `max` is for measuring the ceiling or
  open-ended problems (scientific discovery, math) where time and tokens don't matter — reserve both for
  where you've confirmed a gain, since gains above `high` are uneven and task-dependent.
- At `high` and above it **thinks before almost every reply, including a greeting.** "Answer directly without
  deliberating" does not stop this at `medium` and above — if basic turns cost more than they should, lower
  effort for those turns instead. Effort has little effect on reply *length*; use prompting for length/tone.
- Mix levels in one workflow with a **per-message effort change** (beta, `mid-conversation-output-config-2026-07-01`
  header) — e.g. plan/iterate at `medium`, raise to `high`/`xhigh` for the long unattended stretch — without
  losing the prompt cache. A top-level `effort` change between requests does lose it.

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

## Finish the whole task
- On long, multistep tasks it can end a turn before the work is done: listing what's left, offering to
  continue, or stopping at an ordinary obstacle (a timeout, an empty result, a locked file) — more often at
  `low`/`medium`. Add to the system prompt, distinguishing **ordinary obstacles** (diagnose and work through
  them with the access you have) from **deliberate blockers** (a file marked off-limits, withheld access, a
  safety guardrail — leave these alone and report them):
  *"Please avoid stopping while you still owe work the user asked for. Be persistent and do not stop unless
  needed. While status notes are welcome, as is clarifying with the user on open decisions, carry on with
  work that does not depend on the user's answer without unnecessary stops. If you notice yourself inviting
  the user to redirect you or offering to wait, instead proceed on the next part of the task. You may meet
  ordinary obstacles like errors, timeouts, locked files, empty results or failing tools — diagnose them
  first, and when they are not real blockers, work through them (wait and retry, fix the request, use
  another tool or source) rather than stopping unnecessarily. If someone clearly decided something is a hard
  blocker, leave it alone, say plainly what you found, and look for another safe way to finish the task. This
  does not override the need for confirmation on risky or destructive actions."* Roughly halves unfinished
  endings in testing; output tokens rise ~30%. Keep your own confirmation step for risky/irreversible actions
  — it asks less often with this text, not never.
- **Approvals:** when telling it to continue, say exactly what you're approving ("Yes, run the migration on
  staging"), not a bare "go"/"continue". Be specific about which actions need approval in your own rules —
  a broad category like "sending messages to people outside this conversation" made it hold back about half
  of routine, harmless requests to colleagues in testing.

## Say who owns the code
- Without a statement of ownership, it tends to **add to existing structure (even duplicating code) and
  report nearby problems instead of fixing them**, treating the codebase as someone else's. Telling it the
  codebase is its own flips this: *"You are the owner and long-term maintainer of this codebase, and its
  design is up to you."* raised duplicate-code consolidation from under 10% of runs to about 75% in testing.
  Trade-off: output tokens rise 70–80%, it adds unrequested tests/docs/fixes, and its own PR summaries can
  omit small changes it made — review the actual diff, not just the summary. Leave the sentence out where
  the user owns the code and wants minimal change; a scope rule like "no drive-by refactors" alone didn't
  fully cancel the effect (it still consolidated duplicated code in over half of runs with the rule alone).

## Keep users informed during long turns
- Long runs of tool calls can pass with little user-facing text, including the very first call. Updates
  between tool calls arrive as **progress-update `thinking` blocks**, empty under the default
  `display: "omitted"` — first confirm your client isn't just silently dropping them (`display: "updates"`,
  beta, or `"summarized"`). Three levers, in order of effort to wire up:
  1. **Harness reminder:** count consecutive tool-calling steps with no `text`/progress-update content; after
     several (e.g. 5), append as a **turn-scoped system message** (`clear_at: "next_user_message"`, beta):
     *"The user hasn't heard from you in a while: say in a few words what you're doing, then continue."*
     Roughly halved the longest silent stretch in testing with no real token/time cost. Stop after 2–3 if it
     stays quiet.
  2. **Opening line + recap**, for human-in-the-loop work (costs ~20% more output tokens): *"Before you
     start, say in a line what you're about to do; brief updates while you work help the user follow along.
     Close with a short recap that stands on its own (what you found, what you did, and what's next), so a
     reader who only sees the last message has the full picture."*
  3. **Lighter fallback** when your platform has no turn-scoped system messages: add *"Every few tool calls,
     give the user a one-line update on where things stand."* to the system prompt directly.

## Set expectations for subagents
- How much it delegates depends on your harness: rarely starts one with a minimal subagent tool on short
  tasks; delegates readily where the harness/prompts already invite it (e.g. an agentic coding product). At
  `xhigh`/`max` it can spawn subagents to **review its own work**, unprompted — Fable 5.1 didn't do this on
  the same tasks. Works well as a planner/orchestrator for other models. Subagents can be a large share of
  session cost — check what model they default to.
- Only rewrite your subagent tool's description if it over-delegates: state what a subagent costs in your
  harness, when delegation is and isn't worth it, and how to brief one. A longer, cost-aware description
  roughly halved subagent count at `high` effort in testing, vs. a short one.

## Keep caution from piling up
- Cautious instructions accumulated across sessions (memory, notes, instruction files) — some the model wrote
  itself — can make it over-ask for approval on routine work, especially with multiple agents. Fixes: delete
  stale notes ("never retry") once their reason no longer holds; **name the specific steps that need no
  approval** rather than a vague "act more freely"; re-examine blanket validation gates like "stop and review
  at the first error"; and prefer "ask for approval before deleting files" over "never delete files" if you
  actually want exceptions — it treats "never" as absolute. Keep your own confirmation step for genuinely
  risky/irreversible actions regardless.

## Migrating prompts/harnesses built for earlier models
- **Standing delegate instructions** in system prompts, skills, or agent files can now over-trigger — remove
  if it delegates more than the task needs (see subagents, above).
- **A token budget shown to the model** changes how much it spends; removing a large one lowered cost with
  equivalent performance on coding tasks in testing (counter to the usual intuition) — test without it. This
  is about budget text in the *prompt*, not the API's task-budgets beta feature.
- **Harness code that edits earlier turns** invalidates the thinking blocks after the edited point (see
  Preserved thinking, below) — use context editing or compaction that drops no earlier turns, or accept the
  `drop_block` cost as a stopgap.
- **"Treat that answer as done" lines** (from Opus 5.5's chat tuning) measurably reduce follow-up-turn
  thinking on Fable 5.2 too, but also make it far less likely to flag its own earlier mistakes — test before
  porting, and leave out where self-correction on long analyses/agentic work matters.
- **"Think less" instructions no longer work** at `medium`+ — lower effort instead (see Effort, above).
- **Hard style rules** (e.g. a strict sentence-length cap) now read as choppy prose, since it follows them
  closely — relax before adding the reports guidance below.
- Audit memory/notes/instruction files for absolute rules and stale cautions before migrating (ties to
  "Keep caution from piling up", above); a system stuck on over-caution may need its memory trimmed and
  restarted.

## Make reports easy to follow
- People reading a final report or handoff after a long agentic run usually haven't seen the tool calls or
  files behind it. For reports/handoffs, add and adapt to your product:
  *"Write for an intelligent but low-context reader. The person reading has not seen your tool calls, your
  reasoning or the files you opened, and may be switching in from other work. Put the key points in the
  first few sentences; don't use an undefined reference in line 1 that only makes sense by line 12. Use
  plain words and clear, complete sentences — short sentences, one idea per sentence, active voice, the same
  word for the same thing each time. Use flowing prose where ideas connect; keep bullets for lists of
  separate items. Leave out unnecessary detail unless asked, but keep the key context."* Made final reports
  less dense (fewer semicolons) and shortened sentences on workflow-automation tasks in testing.

## Safeguard refusals & fallback — taxonomy widened to match Sonnet 5.5
- Now names **five** categories (up from Fable 5.1's three) plus an uncategorized fallback: **`cyber`**
  (vuln-finding in source code allowed; high-risk dual-use not), **`bio`** (everyday health/education
  unaffected), **`frontier_llm`** (assisting a competing model's development — new to the Fable family this
  generation), **`reasoning_extraction`** (don't ask the model to reproduce its reasoning as response text —
  read `display: "summarized"` thinking instead), **`general_harms`** (another usage-policy area; can trigger
  on benign work), and **`null`** (refusal doesn't map to a named category). A decline returns
  `stop_reason: "refusal"` with a `stop_details` object.
- **Fallback targets are Claude Opus 4.8 and Claude Opus 5** (confirmed on the untracked whats-new page, #14
  — the dedicated prompting page still doesn't name a model itself). Server-side fallback (beta) retries on
  the recommended target per category; categories with no recommended fallback, such as
  `reasoning_extraction`, return the refusal to you instead.
- False positives are down vs. 5.1's launch and source-code vulnerability finding is permitted; the three
  triggers that raise odds on the Fable family persist: compile-check phrasing (ask *"are there any bugs in
  this program?"*, not *"does this compile without errors?"*), lesser-known languages (give the model the
  language's docs/context), and base64 in tool output (strip it).

## Breaking API changes vs. Fable 5.1 worth knowing when porting a prompt/harness
- **Thinking can't be disabled** (`{"type": "disabled"}` and manual `budget_tokens` both 400) — adaptive
  thinking is the only mode, same as 5.1.
- **Forced tool use isn't supported** — `tool_choice: {"type": "any"}` or naming a specific tool both 400.
  For schema-valid JSON, use `tool_choice: {"type": "auto"}` with strict tool use or Structured Outputs
  instead (unavailable under customer-managed encryption keys).
- **`computer_20251124` is retired** in favor of the `computer_toolset_20260801` toolset (except on Amazon
  Bedrock, which still accepts the older tool).

## If the target is Claude Fable 5.1 / Mythos 5.1 (legacy, previous generation)
Everything above still describes the Fable family's character, but several specific behaviors and the
guidance for them are 5.1-specific — don't port 5.2's wording verbatim:
- **Narrates less than Fable 5** during long tool-calling turns, more so at high effort and in long chains —
  the opposite complaint from 5.2's occasional silent stretches, but the fix is the same shape: confirm your
  client renders progress-update `thinking` blocks (`display: "updates"`/`"summarized"`), then delete legacy
  narration-suppressing lines, then add an opening-line-and-recap instruction.
- **One tool call per turn in coding/computer-use loops** where later calls are implied rather than asked
  for — re-send a turn-scoped system message nudging batching after each round of tool results. This issue
  is **not mentioned on the Fable 5.2 page** — likely resolved; re-test before porting the workaround forward.
- **Denser prose, less chat formatting** than earlier models by default (not the same as 5.2, which follows
  *your* style rules closely but isn't dense by default) — name the anti-pattern directly ("remove mannered
  prose") or add a when-to formatting rule rather than blanket anti-formatting lines.
- **Unmarked quoting** when summarizing retrieved documents — fix with one complete worked example (request,
  response, `<rationale>`) in the system prompt.
- **Search triggering at `low`** is lower than Fable 5 — raise effort for affected turns, or note that
  recognizing a name isn't knowing its current state.
- **Whole-file rewrites for small edits** — ask it to surgically edit rather than rewrite when the end result
  is unaffected.
- **Long outputs at `xhigh`/`max`** can get drafted once in thinking, then written again in the reply — run
  these at `high`, or leave `max_tokens` headroom for both and say thinking and output share one budget.
- **Safeguard refusals: three categories** (`cyber`, `bio`, `reasoning_extraction`, no `frontier_llm` /
  `general_harms`) — narrower than 5.2's five. Fallback targets are the same (Claude Opus 4.8 and Claude
  Opus 5), confirmed on the linked, untracked "What's new in Claude Fable 5.1" page (#12) — the dedicated
  prompting page doesn't name a model itself.
- **Client-side compaction:** tell it exactly what a summary must keep — problems and how they were
  resolved, options tried or set aside, anything asked/decided/ruled out stated exactly, where things stand,
  what's open, hard-to-reconstruct specifics — keep the user's words near-verbatim, condense your own
  reasoning. (Server-side compaction already does this.)

## Preserved thinking / append-only history (shared across the current family)
Editing earlier turns invalidates later thinking blocks — a 400 for accounts created on or after
**2026-08-31** on Claude Fable 5.2, Mythos 5.2, Fable 5.1, Mythos 5.1, Opus 5.5, Sonnet 5.5, and Haiku 5.5
(not Fable 5/Mythos 5, Opus 5, or Sonnet 5). Keep the conversation append-only: per-turn reminders as
turn-scoped system messages, instruction/tool changes via mid-conversation system messages, no rewriting
`system`/`tools` or summarizing older turns in place; let server-side compaction or context editing trim
instead. The opt-in `thinking.block_binding.prefix_mismatch_behavior: "drop_block"` (beta,
`thinking-binding-controls-2026-08-01`) drops the affected blocks instead of erroring, as a stopgap — expect
higher output tokens while you rely on it, since dropped-thinking turns re-think from scratch.

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
  duplicate; delete wrong notes (see also "Keep caution from piling up", above — memory is exactly where
  stale over-caution accumulates). It performs particularly well when it can reference past-run lessons.
- **`send_to_user` tool:** for async agents, a client-side tool that surfaces a message verbatim mid-turn
  (partial deliverable, direct answer) without ending the turn. **Defining it isn't enough** — pair it with an
  elicitation line ("when you have content the user must read verbatim, call `send_to_user`") and use it only
  for user-facing content, not narration.
- **Context-budget calm:** if the harness shows a remaining-token countdown it may offer to hand off/summarize;
  avoid surfacing counts, or add *"You have ample context remaining; do not stop or suggest a new session."*
- **Vision:** does its best work on dense charts/screenshots when it can **crop and zoom** — run it with a
  container holding the raw images plus PIL/OpenCV, or at minimum a crop tool returning an enlarged region.
- **Aim higher than you would for prior models.** Pick a task at the top of your difficulty range and let it
  scope, ask clarifying questions, and execute — testing it only on simpler workloads undersells its range.
- **Self-verification beats self-critique:** for long-running tasks, prefer separate, fresh-context verifier
  subagents over asking it to check its own work: *"Establish a method for checking your own work at an
  interval of [X] as you build. Run this every [X interval], verifying your work with subagents against the
  specification."*

## If the target is Claude Fable 5 / Mythos 5
The 5.1/5.2 deltas above don't apply; two behaviors **invert** relative to 5.1/5.2:
- **Fable 5 over-elaborates** rather than going quiet (surveying options it won't pursue, narrating next
  steps, over-structured PR text, heavily-formatted output). Add a brevity line instead of a narration one:
  *"Lead with the outcome — your first sentence answers 'what happened / what did you find.' Supporting detail
  after. Be selective about what you include rather than compressing into fragments or arrow-chains."*
- **Readability after long runs:** its final summary can be dense working shorthand — instruct it to drop the
  shorthand, write complete sentences, and open with the outcome for a reader who saw none of it.
- Preserved thinking, turn-scoped batching nudges, mannered prose, low-effort search triggering, whole-file
  rewrites, the `xhigh`/`max` output-headroom note, the widened refusal taxonomy, and the "say who owns the
  code" / "make reports easy to follow" additions are **not** Fable 5 behaviors or options — don't port them.
  Fallback target is Claude Opus 4.8 (stated directly on the Fable 5 page).

## Migration note
- Skills/prompts tuned for **prior generations** are often too prescriptive for this family and can hurt
  quality. Keep instructions brief and outcome-led. Coming from **Fable 5**, the reverse risk applies: lines
  written to hold down its over-elaboration and over-formatting now suppress behavior neither 5.1 nor 5.2 has.
  Coming from **Fable 5.1**, re-sweep effort rather than porting a tuned value, and re-test any workaround for
  the one-tool-call-per-turn and narration issues before carrying them forward — 5.2's page doesn't repeat
  either, which is evidence (not proof) they've improved.
