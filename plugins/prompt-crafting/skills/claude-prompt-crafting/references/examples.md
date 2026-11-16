<!--
last-verified: 2026-11-16
scope: Worked before/after examples for the Claude craft step. Illustrative, not exhaustive.
-->

# Worked examples (Claude)

## Example A — craft-new (vague idea → production prompt)

**User's rough idea:** "I want something that takes customer support emails and tells me how angry
they are and what they want."

**Spec after alignment (compact):**
- Goal: triage inbound support emails. Output: JSON with `sentiment`, `urgency`, `primary_request`,
  `suggested_owner`. Audience: a routing script (machine-consumed). Success: correct routing fields,
  no invented categories. Failure modes: hallucinated category, missing the real ask, leaking PII into
  notes. Context: fixed category lists. Constraints: strict schema, English. Target: Sonnet via API,
  system+user, Structured Outputs on. Examples: 3 labeled emails available.

**Crafted prompt:**

```
SYSTEM:
You are a support-triage classifier. Read one customer email and extract routing fields for an
automated system. Accuracy matters more than nuance: a wrong field misroutes a real customer.

<categories>
  <urgency>low | normal | high | critical</urgency>
  <owner>billing | technical | account | other</owner>
</categories>

<rules>
- Choose urgency from the customer's stated impact and deadline, not their tone alone.
- primary_request: one sentence, in your own words, describing what they actually want.
- Never invent a category outside the lists. If unsure, use "other" and explain in notes.
- Do not copy personal data (emails, card numbers) into notes.
</rules>

<examples>
  <example>
    <input>My card was charged twice and I need this fixed before payroll runs Friday.</input>
    <output>{"sentiment":"frustrated","urgency":"high","owner":"billing",
    "primary_request":"Refund a duplicate charge before Friday","notes":"Deadline-driven"}</output>
  </example>
  <!-- 2 more diverse examples: a calm technical question, an angry churn threat -->
</examples>

USER:
<email>{{email_body}}</email>
```

**Why:** role + reason in system; fixed category lists prevent hallucination (failure mode #1);
positive rules; 3 diverse examples lock the schema; variable payload isolated in the user turn;
Structured Outputs enforces the JSON.

---

## Example B — refine-existing (weak prompt → stronger)

**Before:**
```
Write a blog post about our new feature. Don't make it boring and don't use too much jargon.
Make it good.
```

**Diagnosis against the dimensions:** no role, no audience, negative-only instructions ("don't…"),
no success criteria, no structure, no length, no context about the feature. "Make it good" is unsteerable.

**After:**
```
SYSTEM:
You are a product writer for {{company}}. Write for {{audience}} — smart, busy, not deeply technical.
Your job: make them understand one new feature and want to try it.

Write in clear, flowing prose. Lead with the concrete problem it solves, show one realistic example,
then how to start. Define any necessary term in one short clause. Aim for 500–700 words.

A great post: a reader who skims the first paragraph still gets the value; every claim is specific
(no "powerful, seamless, robust"); it ends with one obvious next step.

USER:
<feature_brief>{{feature_brief}}</feature_brief>
```

**Why:** added role + audience; converted "don'ts" into positive direction and a concrete success bar;
gave structure and length; isolated the variable brief. Kept the user's intent, rebuilt the weak dimensions.

---

## Example C — per-model tuning (an agentic prompt tuned for Fable 5.2)

Shows how the craft changes once the **target model** is pinned — here Fable 5.2 / Mythos 5.2, the current
Fable flagship (load `models/fable.md`).

**User's rough idea:** "A system prompt for an autonomous agent that triages our failing CI tests overnight
and fixes the flaky ones."

**Spec after alignment (compact):** Goal: overnight autonomous agent that triages failing CI tests and fixes
flaky ones. Output: fixes as commits + a morning summary. Target: **Fable 5.2** via API, agentic/long-horizon,
`high` effort. Success: real flaky tests fixed, no false "done" claims. Failure modes: fabricated progress,
unrequested refactors, asking permission mid-run when no one's watching, stopping before the work is done.

**Crafted prompt (Fable 5.2 idiom):**

```
You are the owner and long-term maintainer of this CI suite, and its design is up to you. Overnight, find
failing tests, separate genuinely flaky ones from real regressions, and fix the flaky ones.

I'm running this so the team starts the day with a green build and a short report — that's what the output
is for. When you have enough information to act, act; give a recommendation, not an exhaustive survey.

Before reporting progress, audit each claim against a tool result from this session. Report only work you
can point to evidence for; if a fix is unverified, say so.

If you spot an unrelated bug, report it as a follow-up instead of fixing it. You are operating
autonomously — no one is watching, so proceed on reversible, in-scope actions without unnecessary stops;
pause only for a destructive or irreversible action. You may meet ordinary obstacles like flaky
infrastructure, timeouts, or a test that fails to even start — diagnose them first, and work through them
with the access you have rather than stopping to report. If something is a deliberate blocker (a test
explicitly marked do-not-touch, access withheld on purpose), leave it alone and say so.

Keep a notes file (one lesson per file, a one-line summary on top) recording which tests were flaky and
why, and reference it on future runs.

Write the morning report for someone who saw none of the run: put the key points in the first few
sentences, use plain words and complete sentences, and keep bullets only for genuinely separate items.
```

**Why (model-specific):** the Fable family is a strong instruction-follower, so the prompt stays **brief and
outcome-led** instead of enumerating every behavior; it **gives the reason**, **grounds progress claims**,
and adds a **memory file** — all still true of 5.2. Four pieces come straight from `models/fable.md`'s
Fable-5.2-specific guidance: the **ownership sentence** (without it, 5.2 tends to report problems around the
test suite instead of fixing them, treating it as someone else's code — the trade-off is more unasked-for
cleanup, which the follow-up rule bounds), the **obstacles-vs-blockers distinction** (replaces the older
"check your last paragraph for a promise" line that was specific to Fable 5.1, since 5.2's failure mode is
stopping at an *ordinary* obstacle rather than ending the turn on a plan), and the **plain-language report
instruction** (5.2's reports can otherwise run dense for a reader who saw none of the work). It **never asks
the agent to echo or explain its reasoning** (that risks the `reasoning_extraction` refusal, which falls back
to Opus 4.8 or Opus 5 on both Fable 5.2 and the legacy Fable 5.1); effort is `high`, 5.2's default. Tuned for
Haiku instead, the same spec would get a tighter, example-led classification prompt; for Opus, explicit scope
statements.
