<!--
last-verified: 2026-06-21
sources: see _sources.md (official OpenAI developer docs)
scope: DEEP APPENDIX — load only for agentic / tool-use / long-context / RAG / structured-output-heavy /
eval prompts, or under --deep. Lean core is in techniques.md.
-->

# GPT prompt techniques — advanced appendix

## Contents
- Tool use & agents
- GPT-5.x / 5.1 specifics
- Structured Outputs (edge cases)
- Long context & RAG
- Model selection & tiering
- Evaluation prompts
- Prompt-injection / untrusted input

## Tool use & agents
- **Define tools via the API `tools` field**, never by describing them in the prose prompt — keeps the model in
  distribution and improves selection (measurable SWE-bench gain). Put tool *usage examples* in a system-prompt
  `# Examples` section, not in the tool description.
- **Agentic reminder trio** (workhorse): persistence ("only terminate when the problem is solved"), tool-calling
  ("use tools instead of guessing"), planning ("plan before each call, reflect after").
- **Tune eagerness:** to make an agent do less — lower `reasoning_effort`, give an explicit tool-call budget
  ("at most 2 tool calls"), and clear stop criteria. To make it do more — raise effort + add persistence.
- **Tool preambles:** GPT-5.x emits upfront plans + progress updates; steer their frequency/verbosity in the prompt.

## GPT-5.x / 5.1 specifics (VOLATILE)
- **Surgical instruction-following** — contradictions are costly; audit for conflicts.
- **GPT-5.1 `none` reasoning mode** makes it behave like a classic non-reasoning model, usable with hosted tools;
  function-calling much improved.
- **GPT-5.1 may terminate early / be over-concise** — add explicit persistence ("persist until the task is fully
  handled end-to-end this turn; do not stop at analysis or partial fixes").
- **Named tools** like `apply_patch` (large drop in code-edit failures) and `shell` exist on recent models — use them
  for code/file edits instead of free-form output. *(Verify availability per model.)*

## Structured Outputs (edge cases)
- `strict: true`; root = object; every property `required`; `additionalProperties: false`; some JSON-Schema
  features unsupported. First call with a new schema adds latency; later calls don't.
- **Refusals** surface as a distinct field under Structured Outputs — handle them.
- JSON mode (`response_format: {type:"json_object"}`) only guarantees valid JSON, not your schema — prefer
  Structured Outputs whenever the model supports it.

## Long context & RAG
- Repeat key instructions at **start and end**; place single-copy instructions **above** the context.
- Use contrasting delimiters (XML-ish / key-value) for documents; avoid JSON-wrapping large doc sets.
- Tell the model what to do when the answer isn't present ("say you don't know") to curb hallucination.

## Model selection & tiering (VOLATILE)
- Two axes: reasoning vs non-reasoning, and large vs small (mini/nano = cheaper/faster).
- **Durable tiering pattern:** small model routes/filters → large model synthesizes → reasoning model verifies.
- Reasoning models for ambiguity, planning, dense-document analysis, code review, evals; non-reasoning for speed,
  cost, well-defined execution.
- **Current IDs (2026-06-21 — RECHECK):** `gpt-5.5` (flagship/default for new projects; best in Responses API),
  `gpt-5.4` (+ `-mini`, `-nano`); older but documented: `gpt-4.1` (+ mini/nano), `gpt-4o`, `o3`, `o4-mini`.

## Evaluation prompts
- Build multidimensional rubrics with small fixed scales and explicit anchors; have the judge reason, then score;
  grade with a different model than the generator. Prefer Structured Outputs for machine-readable verdicts.

## Prompt-injection / untrusted input
- Separate untrusted content in clearly named delimiters and state that content inside them is data, not
  instructions. Define the trust boundary and allowed actions explicitly.
