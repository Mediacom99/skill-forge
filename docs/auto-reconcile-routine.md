# Automated reference reconcile — claude.ai routine → PR

This closes the last manual gap in the freshness system. Today:

- **`check-sources.yml`** (weekly) detects when an Anthropic source doc changes, refreshes
  `.source-hashes.json`, and opens a **drift issue** — *detection*, automated.
- **`/refresh-references`** reconciles the distilled prose against the changed docs — *reconciliation*,
  **manual** until now.

A **claude.ai scheduled routine** runs the reconcile automatically and delivers the result as a **pull
request** (never a push to `main`), so a human still reviews the LLM-edited prose before it ships. When a
needed change is **beyond what it can safely do on its own** (an ambiguous judgment call, a moved/new source,
or a change outside its allowed scope), it doesn't guess — it opens a **notification issue** for the
maintainer instead. Either way, the email it produces links straight to the PR or issue.

> **Why a PR, not a push to main?** The cloud routine previously stalled because its *"allow unrestricted
> branch pushes to `main`"* permission wouldn't save (a likely product bug). Opening a PR pushes to a
> **feature branch**, which should not require that toggle — so PR-mode is expected to sidestep the bug.
> This is the main thing to confirm on the first run.

Billing: the routine runs on the **Claude subscription** (no `ANTHROPIC_API_KEY`, no per-run API cost).

---

## The routine prompt

> **The prompt does not contain the procedure.** The reconcile steps live in
> [`plugins/maintenance/skills/refresh-references/SKILL.md`](../plugins/maintenance/skills/refresh-references/SKILL.md)
> — the same file behind `/refresh-references` — and the routine reads it from the repo at run time. This
> prompt carries only what's specific to running unattended: scope, delivery, and notification.
>
> **So: to change how the reconcile works, edit the skill.** The routine picks it up on the next run with no
> re-paste. Only re-paste this prompt when the *delivery* rules change. (These two used to be independent
> copies and had drifted apart — the skill was still telling maintainers they could hand-refresh
> `.source-hashes.json`, which the routine correctly forbids.)

Paste this into the scheduled routine (targeting `Mediacom99/skill-forge`):

```text
You are the reference-freshness bot for the GitHub repo Mediacom99/skill-forge. On each scheduled run, keep
the distilled reference libraries faithful to their official Anthropic source docs. Deliver any reconcile you
can do as a pull request for review (never by pushing to main); when a needed change is beyond what you can
safely do yourself, notify the maintainer with a GitHub issue instead (see Deliver for both paths).

You run unattended on a schedule with no one watching. Proceed on reversible, in-scope actions (fetching
docs, editing reference files, opening a PR or a notification issue) without pausing to ask, and finish the
job with tool calls rather than stopping at a plan or a promise. The PR (or issue) is the review gate.

Procedure — do not improvise one:

Read plugins/maintenance/skills/refresh-references/SKILL.md in the repo and follow it exactly. That file is
the authoritative reconcile procedure (it is the same content behind the /refresh-references skill; read it
from the repo rather than assuming the plugin is installed here). You are its "Unattended" mode throughout:
don't pause for approval on in-scope reversible work, and escalate anything ambiguous instead of guessing.
Its Hard boundaries are binding — in particular, never edit any references/.source-hashes.json.

One scope rule this run adds on top of the skill: edit only files under references/** and CHANGELOG.md. Any
other repo file — including a SKILL.md — is out of scope and becomes a path-C notification below. This
narrows the skill's Step 6: do the last-verified bumps and the CHANGELOG entry as written, but a version bump
(plugin.json + SKILL.md frontmatter) is out of scope — mention it in the PR body for the maintainer instead.
(Opening or updating a GitHub PR or issue is of course allowed.)

Before you start, make sure your branch is cut from CURRENT origin/main (git fetch origin, then branch from
origin/main). Two past runs branched from a stale base and reproduced work that had already shipped; both PRs
were closed as superseded.

Deliver — the skill's Step 4 sorts your findings into A, B, or C. Here is what each one means for delivery:

A) Nothing to do. Stop and open nothing.

B) A reconcile you can do faithfully. Make the minimal faithful edits and open a PR (details below).

C) Something the maintainer must decide or do. NOTIFY, don't go silent: open (or update) a GitHub issue
   titled "Reference reconcile — needs maintainer <YYYY-MM-DD>" containing exactly what the skill's Step 4C
   tells you to state — what needs doing, why you couldn't, the quoted source text, the affected reference
   files — ending with "cc @Mediacom99", and assign Mediacom99. If you also completed a partial reconcile,
   open the path-B PR too and cross-link the two.

For the PR in path B:
- If an open PR from an auto/refresh-references-* branch already exists, update it instead of opening a duplicate.
- Otherwise open a PR from a new branch auto/refresh-references-<YYYY-MM-DD> based on current origin/main, with:
  - title: "chore: refresh references against current Anthropic docs";
  - a body summarizing exactly what changed and why, listing each source URL you checked, and flagging
    anything ambiguous for a human;
  - "Closes #<n>" if an open issue titled "Source docs changed" exists;
  - a line "cc @Mediacom99", and a review request to Mediacom99.

Always end your run with a short summary whose FIRST line is the PR URL (path B) or the issue URL (path C), so
the email you generate links straight to it — the maintainer opens it to review and merge (PR) or to act
(issue). If you opened nothing (path A), say so in one line.
```

---

## One-time setup (your side, in the UI)

1. **Install the Claude GitHub App with write access** on `Mediacom99/skill-forge`
   (github.com/settings/installations). This is **distinct from the OAuth connector** and was the untried
   fix last time — the App needs `contents: write` + `pull_requests: write` (to open the reconcile PR) and
   `issues: write` (to open a path-C notification issue) on the repo.
2. **Create the scheduled routine** in claude.ai: connect it to `Mediacom99/skill-forge`, paste the prompt
   above, and set the schedule to **weekly, ~1 hour after `check-sources`** (that Action runs Mondays 09:00
   UTC, so pick Mondays ~10:00 UTC — the drift issue and refreshed hashes will already exist).
3. **Confirm PR-mode dodges the permission bug.** Because the routine opens a PR from a feature branch, you
   should *not* be asked for the "unrestricted branch pushes to `main`" permission that wouldn't save. If it
   still demands a main-push permission, PR-mode isn't dodging it → use the fallback below.
4. **Validate with one manual run** ("Run now"): confirm a PR appears, the diff is sane, and **you receive an
   email** (see next section). Then let the schedule take over.

**Fallback if the cloud routine still can't open a PR:** run the *same prompt* via `claude -p "<prompt>"
--permission-mode acceptEdits` on a **VPS + Coolify weekly job** or a **self-hosted GitHub Actions runner**
(both subscription-billed, no API key), ending in `gh pr create`. See the doc-freshness-automation notes.

---

## Making sure you get an email (with the link) when the routine acts

GitHub emails you about a PR or issue **only if it's authored by a different identity than yours** (it
suppresses notifications about your own actions). Two layers cover both cases, and both carry the link:

**Layer 1 — zero setup (works if the routine acts as the Claude App / a bot):**
- The prompt makes the PR (path B) **`cc @Mediacom99`** + **request your review**, and the notification issue
  (path C) **`cc @Mediacom99`** + **assign you** — each triggers a notification email that includes the
  PR/issue link.
- The routine also ends its run with the PR/issue URL as the first line of its summary, so claude.ai's
  **native run notification** carries the link too.
- Confirm email delivery is on: github.com/settings/notifications → *Email* enabled, and **watch** the repo
  (Watch → *Participating and @mentions* covers @mentions, review requests, and assignments).

**Layer 2 — guaranteed (use if the first run's PR is authored under *your* identity, so Layer 1 stays silent):**
A ready-to-use notifier already lives at [`.github/workflows/notify-pr.yml`](../.github/workflows/notify-pr.yml).
It emails you on any `auto/refresh*` PR regardless of GitHub's notification rules — no `ANTHROPIC_API_KEY`,
just SMTP. It's committed **inert**: until the secrets exist it logs a skip and passes green; once they're
set it emails. Activate it by adding these repo secrets (Settings → Secrets and variables → Actions):

- `MAIL_SERVER` — e.g. `smtp.gmail.com`
- `MAIL_USERNAME` — the sending account
- `MAIL_PASSWORD` — an app password (Gmail: **not** your login password)
- `MAIL_TO` — where to send the alert

Filtering on the `auto/refresh*` head branch keeps it quiet for ordinary PRs. Its email body already includes
the **PR URL** (`html_url`). Note this SMTP layer is **PR-only**; path-C notification *issues* are covered by
Layer 1 (@mention + assignment) and the routine's native run summary, not by this workflow.
