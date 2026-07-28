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

Paste this into the scheduled routine (targeting `Mediacom99/skill-forge`):

```text
You are the reference-freshness bot for the GitHub repo Mediacom99/skill-forge. On each scheduled run, keep
the distilled reference libraries faithful to their official Anthropic source docs. Deliver any reconcile you
can do as a pull request for review (never by pushing to main); when a needed change is beyond what you can
safely do yourself, notify the maintainer with a GitHub issue instead (see Deliver for both paths).

You run unattended on a schedule with no one watching. Proceed on reversible, in-scope actions (fetching
docs, editing reference files, opening a PR or a notification issue) without pausing to ask, and finish the
job with tool calls rather than stopping at a plan or a promise. The PR (or issue) is the review gate.

Procedure:

1. Find every references/_sources.md in the repo. For each, read its source-URL list, its last-verified date,
   and the reference files it governs (techniques.md, techniques-advanced.md, models/*.md, examples.md).
2. Fetch each source URL and compare it against what those reference files currently claim. Concentrate on the
   volatile items each _sources.md flags: model IDs and versions, effort/reasoning parameters and their
   enums/defaults, feature availability (prefill, adaptive thinking), refusal categories, API surface, and any
   moved or 404'd URLs. If a source can't be fetched, note it — never delete content over a failed fetch.
3. Only where something is genuinely out of date, make the minimal faithful edit: correct changed facts; add a
   genuinely new high-leverage technique sparingly (keep the core lean); remove what is no longer true; fix
   moved URLs in _sources.md. Bump last-verified in _sources.md and in the header of every file you touch, and
   add a dated CHANGELOG.md entry describing what changed.

Hard boundaries:
- Edit only files under references/** and CHANGELOG.md — no other file edits. (Opening or updating a GitHub PR
  or issue for review/notification is allowed; changing any other repo file is not.)
- Never edit any references/.source-hashes.json — the check-sources GitHub Action owns it. If a source needs
  to be added to or retired from tracking, that's a maintainer action: notify, don't edit it.
- Never commit or push to main; every change goes on a branch and ships via PR.

Deliver — pick the path that matches what you found:

A) Nothing to do — references already current, or the pages only re-rendered cosmetically with every tracked
   fact still matching. Stop and open nothing.

B) A reconcile you CAN do fully — facts to correct, a genuinely new high-leverage technique to distill, or a
   moved URL to fix in _sources.md. This is the normal path: make the minimal faithful edits and open a PR
   (details below).

C) An action the maintainer needs that you CANNOT do yourself — NOTIFY, don't go silent. Cases include: a
   change whose faithful distillation is genuinely ambiguous or a judgment call; a source that 404'd or
   redirected, or a new model / new dedicated page, where deciding what to track is the maintainer's call; a
   needed change outside your allowed scope (anything beyond references/** and CHANGELOG.md — e.g. adding or
   retiring a tracked URL in .source-hashes.json, or a SKILL.md edit); or anything you cannot edit with
   confidence. Open (or update) a GitHub issue titled "Reference reconcile — needs maintainer <YYYY-MM-DD>"
   that states exactly what needs doing and why you couldn't, quotes the relevant source text, lists the
   affected reference file(s), ends with "cc @Mediacom99", and assigns Mediacom99. If you also completed a
   partial reconcile, open the PR (path B) as well and cross-link the two.

For the PR in path B:
- If an open PR from an auto/refresh-references-* branch already exists, update it instead of opening a duplicate.
- Otherwise open a PR from a new branch auto/refresh-references-<YYYY-MM-DD> based on main, with:
  - title: "chore: refresh references against current Anthropic docs";
  - a body summarizing exactly what changed and why, listing each source URL you checked, and flagging
    anything ambiguous for a human;
  - "Closes #<n>" if an open issue titled "Source docs changed" exists;
  - a line "cc @Mediacom99", and a review request to Mediacom99.

Before opening the PR, re-read your edits to confirm every changed fact traces to a fetched source and that
you bumped the matching last-verified dates. Be conservative — if a change is a judgment call, prefer path C
(notify) over guessing in a PR. The goal is references that are current and faithful, not bigger.

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
