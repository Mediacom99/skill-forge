<!--
last-verified: 2026-10-12
sources: _sources.md #10 — prompting-claude-sonnet-5-5 (dedicated Sonnet 5.5 page, current Sonnet flagship)
         _sources.md #6 — prompting-claude-sonnet-5 (previous Sonnet generation; deltas in a dedicated section)
scope: Per-model tuning for Claude Sonnet 5.5 (current Sonnet flagship, claude-sonnet-5-5). Loaded at craft time
only when the target model is Sonnet. Sonnet 5 deltas are in their own section below.
-->

# Tuning for Claude Sonnet 5.5

Claude Sonnet 5.5 is the current Sonnet flagship — the balanced, agentic workhorse for coding and production
work. Existing **Sonnet 5 prompts run well unchanged**; for the hardest long-horizon work, an Opus model
(`models/opus.md`) is still the better choice. The deltas below are where tuning pays.

## Effort — recalibrated, and workload-dependent
- Ladder unchanged: `max` · `xhigh` · `high` · `medium` · `low`. **Levels are recalibrated** — a level does not
  produce the same amount of thinking as the same level on Sonnet 5; re-sweep against your own evals rather
  than porting the Sonnet 5 setting.
- **`high`** is the API default, but pick a starting point by workload rather than defaulting blindly:
  agentic coding / multistep tool use → start at `medium` for well-specified tasks, `high` for harder/longer
  ones; chat / latency-sensitive work → start at `medium` or `low` (higher effort means a longer wait before
  the reply starts). Raise effort if quality needs it.
- Lower effort changes how the model finishes agentic work, not just how much it thinks: at `low` it can skip
  verifying a change (see Verification below); at `low`/`medium` on long agentic tasks it's more likely to stop
  and check in before finishing (see Initiative below).
- Set `max_tokens` with headroom for thinking + reply — thinking counts toward it even when not returned to
  you. For agentic coding, 128,000 (the model's max) with streaming is a good default. Reserve `xhigh`/`max`
  for measured quality gains; thinking and replies get much longer there, and `between_tools` (below) isn't
  accepted at those levels. To get less thinking, lower effort first — asking in the prompt for less thinking
  doesn't reliably work from `medium` up.
- Changing the top-level `effort` value between requests invalidates the prompt cache; use a per-message
  effort change (beta) to vary it mid-conversation without losing the cache. Per-message effort changes need
  adaptive thinking — with `between_tools` set, a per-message change returns a 400.

## Steer initiative and scope
- **Checkpointing at low/medium effort:** on agentic coding tasks it can pause to confirm a plan, ask something
  it could answer itself, or stop mid-multipart-task to ask whether to continue. Try raising effort first; to
  keep it working at the same effort, add: *"Keep working until everything the user asked for is done, and only
  stop to ask when you can't go on without the user or before a risky step. When the work the user asked for is
  done and checked, stop and report. Don't add features, tests, files, docs or refactors that weren't asked
  for. If you think one would help, mention it at the end instead of doing it."* This makes it carry more work
  through at low/medium effort — sessions run longer and cost more.
- **Unrequested additions when coding:** it adds tests, docs, and small supporting files that fit repo
  convention, unasked, at every effort level (more at higher effort) — though the requested change itself stays
  close to what was asked. Most teams will welcome this; if not, the second paragraph above (starting "When the
  work the user asked for is done") curbs it, most effectively at `xhigh`/`max`.
- **Thoroughness at `xhigh`/`max`:** it can start its own review/verification rounds after finishing (sometimes
  with subagents) and make related fixes it noticed — more time and tokens for rarely-needed depth. Run routine
  work at `high` or below. To keep the thoroughness but aim it only at the task: *"When the work the user asked
  for is done and its checks pass, stop and report. Don't start extra rounds of review or hardening on your
  own, and don't launch reviewer sub-agents unless the user asked for a review. If you think a deeper review is
  worth doing, say so at the end."* (Cut subagent-reviewer launches and ~1/3 of session cost at `max` effort in
  Anthropic's testing, no quality loss — reduces but doesn't eliminate self-started review.)
- **Open-ended requests** ("show me what you can do with this") can jump straight to building when you wanted
  ideas: *"When the user asks for ideas, options or a plan, give them that and stop. Don't start building or
  changing anything until they say to go ahead."*

## Running without up-front thinking: `between_tools`
- The lowest thinking setting on Sonnet 5.5 is `thinking: {"type": "between_tools"}` — distinct from
  `"disabled"` (which this model doesn't accept). Accepted at `high` effort or below only; a 400 at `xhigh`/
  `max`. With it set, effort can't change mid-conversation (a differing per-message `output_config.effort`
  returns a 400) — use adaptive thinking instead if you need that.
- With `between_tools`, don't add "don't think" instructions — they increase internal-tag leakage, as on other
  models' thinking-disabled modes.
- **Read responses by block type, not position** — a response can open with a `thinking` block under adaptive
  thinking, or a progress-update `thinking` block under `between_tools`.
- **Pass `thinking` blocks back unchanged.** Under `between_tools`, notes written between tool calls longer
  than a sentence or two come back as `thinking` blocks carrying a summary; sending the block back (not just
  the summary) gives the model the full note it wrote.
- **For reasoning tasks without tools, use adaptive thinking, not `between_tools`** — in a toolless request,
  `between_tools` means the model answers with no thinking first at all. See JSON output below.

## Reasoning tasks with JSON output
- On tasks needing a few steps of working out (totaling figures, applying a rule, ranking) with a JSON answer,
  the model often skips thinking, especially at `low`/`medium` — accuracy suffers because, with **structured
  outputs**, the response text holds only the JSON, so it can only work the problem out in thinking.
- **With adaptive thinking:** add *"Think the problem through before you answer."* to the end of the system
  prompt — at `high` this closes most of the gap to `xhigh`-level accuracy for a modest token increase; at
  `low`/`medium` it still helps but less. Or just run at `xhigh` (highest accuracy, no line needed, but more
  tokens). `between_tools` doesn't think first on toolless requests, so use adaptive thinking for this pattern.
- With structured outputs at `low`/`medium`, the model can occasionally keep thinking until `max_tokens`; treat
  `stop_reason: "max_tokens"` as a failed attempt (even with valid-looking JSON in the text) and retry — this is
  rare from `high` up.
- **Without structured outputs** (JSON requested in the prompt), the model often reasons in the response text
  and writes JSON at the end — parse the **last** JSON value in the response (scan for `{`/`[`, parse, continue
  past it; a response whose `stop_reason` is `max_tokens` is a failed attempt). `xhigh` + adaptive thinking
  moves the working-out into thinking so the reply is usually JSON alone, at about the same total tokens as
  `high`.

## User-facing progress updates
- Notes longer than a sentence or two come back as progress-update `thinking` blocks, empty text under the
  default `display: "omitted"`. Set `display: "updates"` (beta, `thinking-display-updates-2026-08-18` header)
  to see them. Under `between_tools`, the summary text comes back automatically — no `display` field needed
  (and `between_tools` rejects `display`, `budget_tokens`, or `block_binding` with a 400).
- For content the user must see verbatim mid-turn, give a simple send-to-user-style tool, declared from the
  first request of the session.
- Remove old "hold all findings for the final response" scaffolding; for updates at predictable points, ask for
  them explicitly in the system prompt.
- If long turns still go quiet, have the harness count consecutive silent tool-calling steps and, after several
  (e.g. 5), append a one-turn reminder as a turn-scoped system message; stop after 2–3 if it stays quiet. Keep
  this occasional — frequent harness text right after tool results risks the prompt-injection misread below.

## Tool use in chat and knowledge work
- It can answer from training knowledge where a search would catch changed details (what's allowed, required,
  charged). Remove language that discourages tool use ("only use tools when strictly necessary"); for
  search-enabled products, add: *"Use the search tool to check specifics that may have changed since your
  training, such as what is allowed, required or charged, even when you feel confident. For researched work
  such as a report or a comparison, gather current sources rather than writing from your training knowledge."*

## Mid-turn user messages — a new prompt-injection-resistance gotcha
- Sonnet 5.5 resists indirect prompt injection well enough that it can **misread a genuine user message as
  injected text** when that text arrives right after a tool result — e.g. a mid-task message delivered as a
  mid-conversation system message placed directly after a `tool_result`, or text placed inside a `tool_result`
  block itself. It may then tell the user the tool result "contained text posing as" them and ignore it or ask
  for confirmation. A per-step token/budget countdown or per-step harness instructions after every tool result
  can trigger this every turn; an occasional reminder (see above) triggers it far less.
- **Never put user-authored text inside a `tool_result` block.** Deliver mid-turn user input as a text block
  in the user message carrying the `tool_result` blocks, after the last one. Keep harness notices in a
  *separate* mid-conversation system message after the user's words — never share a block with them. Avoid
  your own token/budget countdown after tool results in sessions where users can type mid-turn; [task
  budgets](https://platform.claude.com/docs/en/build-with-claude/task-budgets) (beta) have not been seen to
  cause this.

## Verification on coding tasks
- At `low` effort it sometimes reports a code change done without a check that exercises it (e.g. skipping
  tests because dependencies aren't installed). Add: *"When you change code that can be run, built, or
  type-checked, run a real check that exercises the change before reporting it done: the project's tests,
  type-checker, or build, or the changed command itself. A syntax-only check, or a check command that failed to
  start, does not count; if all that is missing is the project's declared dependencies, install them with its
  own package manager and lockfile (e.g. npm install, pip install -r requirements.txt), never via sudo or the
  system package manager, unless told not to. Only if no real check can run here, say which one you did not run
  and why instead of reporting the change as done."* Makes skipped/superficial checks rare at `low` effort, for
  a small cost increase.

## Tolerant tool-call handling
- It occasionally calls a declared tool with the wrong letter case (`bash` for `Bash`) or passes a known
  parameter under a slightly different name. Have the harness accept an unambiguous case-insensitive match, or
  return a `tool_result` with `is_error: true` naming the exact expected name — it usually self-corrects next
  turn.

## Vision
- For dense charts/technical drawings, give it crop/zoom/code tools. Tools help charts at **every** effort
  level; for technical drawings they help only from `high` up, most at `xhigh`/`max`. For charts, tools beat
  raising effort: tools at `high` out-read no-tools-at-`max`, for a fraction of the cost.

## Safeguard refusals
- Runs safety classifiers; a decline is a normal response with `stop_reason: "refusal"` and
  `stop_details.category` naming one of: **`cyber`** (vuln-finding in source code allowed; high-risk dual-use
  not), **`bio`** (everyday health/education unaffected), **`frontier_llm`** (assisting a competing model's
  development), **`reasoning_extraction`** (asking the model to reproduce its reasoning as response text — drop
  such instructions and read `display: "summarized"` thinking instead), **`general_harms`** (another
  usage-policy area; can trigger on benign work).
- **Server-side fallback (beta) retries only `cyber` and `frontier_llm`**, on Sonnet 5 — it does **not** retry
  `bio`, `reasoning_extraction`, or `general_harms` declines. This fallback scope differs by model family; see
  `models/opus.md` and `models/haiku.md` for theirs — don't assume parity.
- Apply to the Cyber Verification Program / Life Sciences Verification Program if a classifier blocks
  legitimate work in those areas.

## If the target is Claude Sonnet 5 (previous generation)
Sonnet 5's own tuning still applies where 5.5 didn't change it. What differs targeting Sonnet 5 specifically:
- **Effort is simpler:** `high` default (same as Sonnet 4.6), no recalibration caveat; `xhigh` for the hardest
  coding/agentic work; cross-model mapping from 4.6: Sonnet 5 `medium` ≈ 4.6 `high`, Sonnet 5 `high` ≈ 4.6
  `max`. Strict scoping at `low` carries real under-thinking risk on moderately complex tasks.
- **Adaptive thinking is on by default, disable-able at any effort** via `thinking: {type: "disabled"}` (no
  `between_tools` mode exists on Sonnet 5) — a flip from Sonnet 4.6, where the same request ran with thinking
  off. `max_tokens` is a hard cap on thinking + response combined; revisit budgets ported from 4.6.
- **Manual extended thinking (`budget_tokens`) is removed** (400). **New tokenizer** produces ~30% more tokens
  for the same text than 4.6's — raise `max_tokens` or drop effort if you see `stop_reason: "max_tokens"` with a
  mostly-thinking, truncated response.
- **`temperature`/`top_p`/`top_k` at non-default values return 400.** Use system-prompt instructions for output
  variety instead (e.g. "propose N distinct directions, then commit to one").
- **More agentic than 4.6 by default**; with thinking disabled it's less likely to reach for tools (add an
  explicit nudge if you rely on tool calls with thinking off). `high`/`xhigh` effort shows substantially more
  tool use in agentic search/coding. Gives good interim progress updates on its own — remove forced
  "summarize every N calls" scaffolding.
- **Interactive coding products:** run at `xhigh`/`high`, front-load task/intent/constraints in the first user
  turn.
- **Code-review harnesses:** follows "only report high-severity / be conservative" faithfully and may
  under-report low-severity bugs (precision up, recall down) — ask it to report everything with
  confidence + severity and filter downstream for coverage.
- **Literal instruction-following:** state scope explicitly for broad instructions ("apply this to every
  section, not just the first").
- **Design & frontend defaults:** can settle into one default visual style; break it with a concrete alternative
  spec or "propose 4 distinct visual directions first, then implement the one picked" (not `temperature`, which
  is rejected). Pair with an anti-"AI slop" directive against generic fonts/palettes/layouts.
- **Computer use:** `computer_toolset_20260801` (Claude API + Google Cloud) plus the earlier `computer_20251124`,
  and the `browser_toolset_20260801` browser-use tool. Up to 2576px / 3.75MP; 1080p balances cost/performance,
  720p/1366×768 for cost-sensitive work.

## When to pick Sonnet
- Default for balanced production prompts, API pipelines, and coding/agentic tasks. Step **up to Opus 5.5**
  (current Opus flagship — see `models/opus.md`) for the hardest agentic-coding / enterprise / long-horizon
  work (or **Fable 5.1** for frontier capability); step **down to Haiku 5.5** for high-volume, latency-sensitive,
  well-scoped tasks.
