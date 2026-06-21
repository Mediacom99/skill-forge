<!--
last-verified: 2026-06-21
scope: Worked before/after examples for the GPT craft step. Illustrative, not exhaustive.
-->

# Worked examples (GPT)

## Example A — craft-new, non-reasoning workhorse (vague idea → production prompt)

**User's rough idea:** "an agent that fixes failing tests in our repo automatically."

**Spec (compact):** Goal: autonomously fix failing tests. Output: code edits + a summary. Audience: a dev
reviewing a PR. Success: tests pass, minimal diff, no unrelated changes. Failure modes: gives up early,
guesses file contents, edits unrelated code. Target: GPT-4.1 (workhorse) as an agent, developer+user,
Responses API, tools defined via API. Examples: n/a.

**Crafted prompt (developer message):**
```
# Role and Objective
You are a coding agent that makes failing tests pass with the smallest correct change.

# Instructions
- Persistence: keep going until all targeted tests pass. Only end your turn when you are sure the
  problem is solved.
- Tool-calling: if you are unsure about file contents or repo structure, read them with your tools.
  Do NOT guess or fabricate code.
- Planning: plan before each tool call and reflect on the result of the previous one.
- Make the minimal diff. Do not touch unrelated code or reformat files.

# Reasoning Steps
1. Run the failing tests and read the errors. 2. Locate the cause. 3. Make the smallest fix.
4. Re-run tests. 5. Repeat until green.

# Output Format
When done: a short summary of the root cause and the change, then the final diff.
```
**User message:** `Failing tests: {{test_command_output}}`

**Why:** workhorse → explicit planning + the agentic reminder trio (persistence/tool-calling/planning);
minimal-diff rule targets the failure modes; tools via API, not described in prose.

---

## Example B — craft-new, reasoning model (same goal, different prompt)

For **GPT-5.x thinking / o-series**, the *same* task is prompted very differently:
```
# Objective
Make the failing tests pass with the smallest correct change. Do not modify unrelated code.

Use your tools to inspect the repo rather than guessing. Persist until all targeted tests pass.
When done, summarize the root cause and show the final diff.
```
**Why:** no "think step by step", no hand-written Reasoning Steps — the model reasons internally; brief,
goal-first instructions; set `reasoning_effort: high` via the API, not the prompt. Over-instructing a
reasoning model degrades it.

---

## Example C — refine-existing (remove the CoT footgun)

**Before (aimed at o-series):** "Let's think step by step. First, carefully reason through each clause of
the contract one by one, showing all your work, then..."

**Diagnosis:** explicit chain-of-thought prompting on a reasoning model — redundant and can hurt; also
over-long. **After:** "Review the contract for clauses that expose us to uncapped liability. List each
risky clause, the risk, and a suggested edit." Brief, goal-first; let the model reason internally; set
`reasoning_effort` to match difficulty.
