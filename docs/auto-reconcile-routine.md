# Automated reference reconcile — claude.ai routine → PR

This closes the last manual gap in the freshness system. Today:

- **`check-sources.yml`** (weekly) detects when an Anthropic source doc changes, refreshes
  `.source-hashes.json`, and opens a **drift issue** — *detection*, automated.
- **`/refresh-references`** reconciles the distilled prose against the changed docs — *reconciliation*,
  **manual** until now.

A **claude.ai scheduled routine** runs the reconcile automatically and delivers the result as a **pull
request** (never a push to `main`), so a human still reviews the LLM-edited prose before it ships.

> **Why a PR, not a push to main?** The cloud routine previously stalled because its *"allow unrestricted
> branch pushes to `main`"* permission wouldn't save (a likely product bug). Opening a PR pushes to a
> **feature branch**, which should not require that toggle — so PR-mode is expected to sidestep the bug.
> This is the main thing to confirm on the first run.

Billing: the routine runs on the **Claude subscription** (no `ANTHROPIC_API_KEY`, no per-run API cost).

---

## The routine prompt

Paste this into the scheduled routine (targeting `Mediacom99/skill-forge`):

```text
You are the skill-forge reference-freshness bot for the repo Mediacom99/skill-forge. Your job each run:
keep the distilled reference libraries faithful to their official Anthropic source docs, and deliver any
updates as a pull request for review — never by pushing to main.

1. Find every references/_sources.md in the repo. For each, read its source-URL list, its last-verified
   date, and the reference files it governs (techniques.md, techniques-advanced.md, models/*.md, examples.md).
2. Fetch each source URL and compare it against what those reference files currently claim. Focus on the
   volatile items each _sources.md flags: model IDs and versions, effort/reasoning parameters and their
   enums/defaults, feature availability (prefill, adaptive thinking), refusal categories, API surface, and
   any moved or 404'd URLs.
3. Only if something is genuinely out of date, make the minimal faithful edits: correct changed facts; add a
   genuinely new high-leverage technique sparingly (keep the core lean); remove what is no longer true; fix
   moved URLs in _sources.md. Bump last-verified in _sources.md and in the header of every file you touch.
   Add a dated CHANGELOG.md entry describing what changed.
4. Do NOT edit any references/.source-hashes.json — the check-sources GitHub Action owns that file.
5. If you made no edits (references already current), stop and open nothing.
6. If you made edits, open a pull request from a new branch named auto/refresh-references-<YYYY-MM-DD> with:
   - title: "chore: refresh references against current Anthropic docs";
   - a body that summarizes exactly what changed and why, lists each source URL you checked, and explicitly
     flags anything ambiguous for human judgement;
   - "Closes #<n>" if an open issue titled "Source docs changed" exists;
   - a line "cc @Mediacom99" in the body, and request a review from Mediacom99.
   Never push to main; the PR is the review gate.

Be conservative: every factual claim in a reference file must trace to a source URL. Surface uncertainty in
the PR body rather than guessing. The goal is current and faithful references, not bigger ones.
```

---

## One-time setup (your side, in the UI)

1. **Install the Claude GitHub App with write access** on `Mediacom99/skill-forge`
   (github.com/settings/installations). This is **distinct from the OAuth connector** and was the untried
   fix last time — PR creation needs the App to hold `contents: write` + `pull_requests: write` on the repo.
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

## Making sure you get an email when the PR opens

GitHub emails you for a PR **only if the PR is authored by a different identity than yours** (it suppresses
notifications about your own actions). Two layers cover both cases:

**Layer 1 — zero setup (works if the routine opens the PR as the Claude App / a bot):**
- The prompt makes the PR **`cc @Mediacom99`** and **request your review** — both trigger a notification email.
- Confirm email delivery is on: github.com/settings/notifications → *Email* enabled, and **watch** the repo
  (Watch → *Participating and @mentions* is enough for @mentions + review requests).

**Layer 2 — guaranteed (use if the first run's PR is authored under *your* identity, so Layer 1 stays silent):**
A ready-to-use notifier already lives at [`.github/workflows/notify-pr.yml`](../.github/workflows/notify-pr.yml).
It emails you on any `auto/refresh*` PR regardless of GitHub's notification rules — no `ANTHROPIC_API_KEY`,
just SMTP. It's committed **inert**: until the secrets exist it logs a skip and passes green; once they're
set it emails. Activate it by adding these repo secrets (Settings → Secrets and variables → Actions):

- `MAIL_SERVER` — e.g. `smtp.gmail.com`
- `MAIL_USERNAME` — the sending account
- `MAIL_PASSWORD` — an app password (Gmail: **not** your login password)
- `MAIL_TO` — where to send the alert

Filtering on the `auto/refresh*` head branch keeps it quiet for ordinary PRs.
