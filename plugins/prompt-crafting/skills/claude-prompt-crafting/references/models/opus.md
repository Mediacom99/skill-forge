<!--
last-verified: 2026-07-28
source: _sources.md #3 — prompting-claude-opus-5 (dedicated Opus 5 page) + models overview
scope: Per-model tuning for Claude Opus 5 (current Opus flagship, claude-opus-5). Loaded at craft time only
when the target model is Opus. Applies on top of techniques.md; Opus 4.8 (now legacy) deltas noted inline.
-->

# Tuning for Claude Opus 5

Claude Opus 5 (`claude-opus-5`) is built for **complex agentic coding and enterprise work**, with particular
strength on long-horizon agentic tasks; the docs say to **start with Opus 5** for that work (step up to
**Fable 5** only when you need the highest available capability). It has a **1M-token context window** (both
default and max) and **128k** max output, and performs well out of the box on existing Opus 4.8 prompts. The
biggest levers are `effort`, whether thinking is on, and telling it the length/scope you want — it now runs
**longer and more autonomously** by default than prior Opus models.

## Effort — the primary cost/latency lever
- Ladder (intelligence ↔ latency/cost): `max` · `xhigh` · `high` · `medium` · `low`. **Default is `high`**
  (on the Claude API and Claude Code).
  - **`high`** — the default; the balanced starting point.
  - **`xhigh`** — step up for **demanding coding and agentic** work.
  - **`low` / `medium`** — now genuinely strong: they deliver good quality at a fraction of the tokens and
    latency, so use them **liberally** as your primary control for cost and response time wherever quality
    holds. (This is a shift from Opus 4.8, which recommended `xhigh` for coding/agentic and warned of
    under-thinking at `low`.)
  - **`max`** — the most intelligence-demanding tasks; diminishing returns on token spend.
- If you carried effort defaults over from a prior model, **re-run an effort sweep on your own evals** — the
  cost/quality curve moved. If reasoning looks shallow on a hard problem, raise effort rather than prompting
  around it.

## Thinking — ON by default now (the key migration change)
- Opus 5 uses **adaptive thinking, on by default**: omit the `thinking` field and it runs with adaptive
  thinking. (This is a flip from Opus 4.8, where thinking was **off** unless you set `thinking: {type:
  "adaptive"}`.)
- **You can disable thinking only at effort `high` or lower** (`thinking: {type: "disabled"}`); at `xhigh`
  and `max`, thinking is always on. Manual extended-thinking budgets (`budget_tokens`) are not supported (400).
- **Prefer keeping thinking on at a lower effort** over disabling it — for most tasks, thinking on at `low`
  beats thinking off at similar cost. With thinking **disabled**, two artifacts can leak into visible output:
  the model occasionally writes a **tool call as plain text** (it never runs) on tool-heavy work, and it can
  emit **internal `<thinking>`/XML tags**. Don't add rules like "do not think/do not reason" — they *increase*
  tag leakage. If you must disable thinking, one combined instruction mitigates both: allow a brief sentence
  before a tool call, allow saying "no tool fits" instead of forcing a call, and forbid internal tags.

## Length, narration, and written output run long — rein them in explicitly
- **Verbosity:** Opus 5's default user-facing responses run **longer** than prior Opus. Effort controls how
  much it *thinks*, **not** how much it *says* — lowering effort won't reliably shorten the reply. Ask for
  concision directly, e.g. *"Keep responses focused and concise; spend most of the response on the main
  answer; give a high-level summary unless more depth is requested."*
- **Progress narration:** it narrates readily in agentic runs (announcing what it's about to do; longer
  per-message output). Describe the cadence you want, e.g. one sentence before the first tool call, brief
  updates only on important findings or direction changes, outcome-first at the end. Positive examples of the
  style beat "don't" instructions.
- **Written deliverables:** files it writes to disk (reports, docs) also run long — add length calibration
  (*"match length to what the task needs; don't pad with filler sections or boilerplate"*).

## Scope and self-verification — remove old scaffolding
- **It verifies its own work without being told.** If your prompt carries explicit verification steps
  ("include a final verification step", "use a subagent to verify", "double-check before responding"),
  **remove them** — on Opus 5 they cause *over-verification* (wasted tokens/latency) with no quality gain.
  Same for legacy harness scaffolding that adds a separate verify pass.
- **It can widen scope** (adding unrequested steps, transforming the task). For narrow work, constrain
  explicitly: *"Deliver what was asked, at the scope intended; make routine judgment calls yourself; if a
  better approach exists, say so in a sentence and continue with the task as asked rather than quietly
  widening or transforming it."*
- **Self-correction:** it catches and fixes its own mistakes well; avoid re-check instructions. It also
  narrates corrections more than prior models — if that's noisy in a product, tell it to only surface
  corrections that change the user's code/conclusions and otherwise fix silently.

## Subagents
- Opus 5 **delegates to subagents readily**, which pays off on genuinely independent, sizeable tracks but
  multiplies cost/time on small ones. Cap it: *"Delegate only for large, genuinely independent, parallelizable
  work; don't delegate what you can finish in a few tool calls; don't use subagents to verify your own work;
  keep spawn counts low."* Deterministic caps also help. (It coordinates writer-verifier teams well.)

## Literal instruction-following → state scope
- Like current Sonnet/Fable, Opus 5 follows instructions literally and won't silently generalize one to
  other items. When an instruction should apply broadly, say so ("Apply this to every section, not just the
  first"). Great for structured extraction and pipelines. In **code-review** harnesses it follows "only report
  high-severity / be conservative" faithfully (precision up, measured recall down) — for coverage, tell it to
  report everything with confidence + severity and filter in a separate pass.

## Vision
- Strong on charts, documents, diagrams, and UI/frontend replication. Vision is best when it has **tools to
  iteratively analyze, crop, and visually verify** — tool use is a more cost-effective lever than thinking
  alone here. Re-validate prompt-side vision workarounds tuned for older models; they may no longer be needed.

## Version deltas
- **Opus 4.8 / 4.7 / 4.6 are now legacy** (each has its own page). Migrating **4.8 → 5**: thinking is now on
  by default; disabling it is capped at `high` effort; and the effort cost/quality curve moved (re-sweep).
- The **Opus 4.8** page documented two things the Opus 5 page does **not** carry: a persistent design house
  style (warm cream/off-white ~`#F4F1EA`, serif display type, terracotta/amber accents, and the two ways to
  break it) and computer-use resolution guidance (up to 2576px / 3.75MP; 1080p balance). If you're targeting
  **Opus 4.8**, see its page (`prompting-claude-opus-4-8`) for those; don't assume they carry to Opus 5.
