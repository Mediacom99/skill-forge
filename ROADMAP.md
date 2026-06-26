# skill-forge roadmap

Per-skill backlog of the next things to **improve / add / fix**. Newest ideas at the top of each
section; move an item to `CHANGELOG.md` once it ships.

> Status keys: `[ ]` idea · `[~]` in progress · `[x]` shipped (then move to CHANGELOG)

## prompt-crafting — `claude-prompt-crafting`

_Backlog for the prompt-crafting skill (Claude-only as of 0.4.0)._

- [x] ~~**Trim the skill `description:` frontmatter — it's over the listing budget**~~ · **done in 0.3.1** (trimmed both + added API framing; re-check the listing warning after install)
  - Claude Code warns the skill descriptions exceed `skillListingBudgetFraction` (1.1% / 1% of context), so
    `gpt-prompt-crafting`'s description gets **dropped from the listing** → weaker/no auto-triggering for
    GPT-prompt requests. Real discoverability bug.
  - **Fix on our side, not the user's:** ship a **tighter description**, do NOT tell users to raise
    `skillListingBudgetFraction` (costs them ~2k tokens every session + faster rate limits). A good
    marketplace skill fits the default budget.
  - Both descriptions are ~10 verbose lines now. Rewrite each to a tight 3–4 lines: what it does + when +
    key trigger phrases + the claude-vs-gpt disambiguation. **Do this in the same pass as the
    API/programmatic item below** — add those terms *while* trimming, so it nets shorter, not longer.

- [x] ~~**Position the skill for API / programmatic prompt creation (marketing + discovery)**~~ · descriptions done in 0.3.1; **README "Why" + differentiators added 2026-06-26**
  - Make explicit that this crafts **production-ready prompts for API / programmatic use**, not just chat:
    `--template` yields a parameterized system/user template with `{{variables}}` you drop straight into code
    (validated by T10), and the craft already applies API-aware guidance (effort/output budget, Structured
    Outputs, role split; the GPT skill is API-native — developer message, Responses API, `reasoning_effort`).
  - **Where:** README "Why" / "What you get"; consider adding "API / programmatic / production" terms to the
    skill `description:` frontmatter (also improves auto-triggering for those users) and `marketplace.json`.
  - **Guardrail:** claim "production-ready prompt *templates* for your API calls," NOT "builds your
    integration" — it crafts the prompt, not the code. Keep the claim accurate.

- [ ] **Clean up the clipboard scratch file after a successful copy** · proposed 2026-06-25
  - Clipboard delivery writes the prompt to a scratch file (`/tmp/skill-forge-prompt.txt`) then `pbcopy < file`;
    the file is left behind. Currently no removal step.
  - **Constraint:** the read-only safety model scopes shell to clipboard commands only — **no `rm`** — so we
    can't delete it via shell without widening `allowed-tools` (which we won't). Safe options:
    - Keep the **fixed filename** (already the case) so scratch files never accumulate — only one stale file.
    - **Overwrite it with empty content** via Write right after the copy, so the prompt text doesn't linger
      (the only cleanup the current `allowed-tools` actually permit).
    - Rely on OS temp-dir cleanup as a backstop.
  - Pick one, add the step to Step 7 "Copying to the clipboard" in **both** skills.

- [ ] **Adaptive depth for the alignment dialogue — go deeper when the task warrants it** · proposed 2026-06-25
  - Today depth is mostly flag-driven (`--quick` / standard / `--deep`). The standard path can stay too
    shallow on complex, high-stakes, or ambiguous specs. Make the questionnaire **auto-scale its depth** to
    the task — more/deeper rounds when the spec is underspecified, destructive, multi-part, or agentic; stay
    light when it's simple — without the user having to pass `--deep`.
  - **Design notes:**
    - Keep the "ask only the gaps, highest-leverage first" principle — deeper ≠ more redundant questions.
    - Signals to deepen: many *unknown/partial* dimensions, a destructive/irreversible goal, conflicting
      requirements, an agentic/tool-using target, or a user answer that opens new gaps.
    - `--quick` / `--deep` stay as explicit overrides; this just makes the *default* depth adaptive.
    - Touch points: Step 0 (depth), Step 2 (dialogue), Step 3 (checkpoint). Apply to **both** skills.

- [x] ~~**Split "improve" vs "template" output, behind a `--template` flag**~~ · **shipped 0.3.0**, calibration fixed in **0.3.1** (F2)
  - 📋 **Full scope:** [`docs/template-and-delivery-spec.md`](docs/template-and-delivery-spec.md)
  - **Default (no flag):** improve the user's prompt and bring it up to the target vendor's current
    guideline standard — do **not** auto-build a reusable, parameterized template (no forced
    system/user split, no `{{variable}}` scaffolding). Return a clean, ready-to-use prompt.
  - **`--template`:** produce a reusable prompt template — system/user split, `{{double_bracket}}`
    variables, XML structure — for wiring into an app or pipeline.
  - **Design notes / open questions:**
    - Output shape (improve vs template) is **orthogonal** to mode (`--refine` = input is an existing
      prompt vs. a raw idea). Make sure the two compose cleanly.
    - Consider **auto-detecting** template intent during alignment (e.g. "I'll reuse this with
      different inputs / call it from code"), with `--template` as the explicit override — mirrors how
      `--refine` is auto-detected.
    - "Improve" mode must stay **fully technique-grounded** (still loads `references/`, still applies the
      right techniques); it just skips the template/reusability scaffolding unless the spec calls for it.
    - Touch points: SKILL dimension #8 (target model + usage), Step 5 (craft), Step 7 (deliver), the
      Flags & modes table, and README "Flags & modes". Apply to **both** skills.

- [x] ~~**"Use it now in this session" delivery option**~~ — **won't do** (verified 2026-06-22)
  - Claude Code has no primitive for a skill to queue its output as the next task, and `allowed-tools` lift
    on the next turn anyway — so an automated handoff is impossible and a manual one adds nothing over
    inline/clipboard. See [`docs/template-and-delivery-spec.md`](docs/template-and-delivery-spec.md); revisit
    only if a turn-queuing primitive appears.

## maintenance — `refresh-references`

- [ ] **Reduce `check-sources` false positives — hash normalized content, not raw bytes** · proposed 2026-06-26
  - Both drift issues were partly cosmetic: #2 (06-22) flipped all 5 hashes at once from a site-wide
    re-render with **no content change**. `check_sources.py` hashes raw response bytes, so any docs-site
    rebuild trips it. Normalize before hashing (extract main content / strip boilerplate + whitespace) to cut
    false-positive issues. Pairs well with the `/schedule` auto-reconcile routine (fewer no-op runs).
