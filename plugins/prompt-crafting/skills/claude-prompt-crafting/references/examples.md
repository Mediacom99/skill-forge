<!--
last-verified: 2026-06-21
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
