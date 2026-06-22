# skill-forge roadmap

Per-skill backlog of the next things to **improve / add / fix**. Newest ideas at the top of each
section; move an item to `CHANGELOG.md` once it ships.

> Status keys: `[ ]` idea · `[~]` in progress · `[x]` shipped (then move to CHANGELOG)

## prompt-crafting — `claude-prompt-crafting` + `gpt-prompt-crafting`

_Shared engine — changes here usually apply to both skills._

- [~] **Split "improve" vs "template" output, behind a `--template` flag** · proposed 2026-06-22 · **implemented in 0.3.0** (see CHANGELOG; pending release)
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

- _(nothing queued)_
