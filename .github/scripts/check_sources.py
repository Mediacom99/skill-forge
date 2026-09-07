#!/usr/bin/env python3
"""Detect drift in the official source docs behind each skill's reference library.

For every plugins/**/references/.source-hashes.json it fetches each source URL, hashes the content,
and compares to the stored hash:
  - stored == null  -> capture a baseline (no drift reported)
  - stored != hash  -> DRIFT (record it)
  - stored == hash  -> unchanged

It rewrites the hash files with current values, and writes drift.md + sets has_drift in $GITHUB_OUTPUT
when any source changed. The workflow then commits the refreshed hashes and opens/updates an issue.

No LLM, no secrets — just fetch + sha256. Only the page's article body is hashed, so site nav and
footer churn don't register; a substantive edit inside the article still can be cosmetic (acceptable).

Changing normalize() invalidates every stored hash: null the `sources` values in the same commit so
the next run re-baselines (a baseline is not drift, so no issue is opened).

Run locally: python .github/scripts/check_sources.py [--selftest]
"""
import datetime
import hashlib
import json
import os
import re
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
UA = {"User-Agent": "skill-forge-check-sources/1.0 (+https://github.com/Mediacom99/skill-forge)"}
drift = []
baselined = []
failed = []


def normalize(raw):
    """Reduce a page to the visible text of its *article body* before hashing, so cosmetic
    re-renders (markup churn, changed asset-hash URLs, whitespace) and site chrome don't trip
    the detector. Stdlib only — imperfect HTML stripping, but far less flappy than raw bytes.

    Scoping to the article matters more than the tag-stripping: the docs shell puts the full
    left nav, the cookie banner and the marketing footer in every page's visible text, so one
    new nav entry (or a footer link) used to flip *every* tracked URL at once. Adding the
    Fable 5.1 page to the nav did exactly that."""
    text = raw.decode("utf-8", "ignore")
    text = re.sub(r"(?is)<(script|style)\b[^>]*>.*?</\1>", " ", text)  # drop scripts/styles
    body = re.search(r"(?is)<article\b[^>]*>(.*)</article>", text) or \
        re.search(r"(?is)<main\b[^>]*>(.*)</main>", text)              # article body, not chrome
    text = body.group(1) if body else text                             # unknown shell: hash it all
    text = re.sub(r"(?s)<[^>]+>", " ", text)                           # strip remaining tags
    text = re.sub(r"\s+", " ", text).strip()                           # collapse whitespace
    return text


def selftest():
    """Offline check of the one piece of real logic here. Run: check_sources.py --selftest"""
    page = b"""<html><head><style>a{}</style><script>var x=1</script></head><body>
        <div id="consent-banner">Cookie settings Accept</div>
        <nav>Overview Prompting Claude Fable 5.1 Careers</nav>
        <article id="content-container"><h1>Title</h1><p>Real   body</p></article>
        <footer>Privacy policy</footer></body></html>"""
    got = normalize(page)
    assert got == "Title Real body", got
    for chrome in ("Cookie settings", "Careers", "Privacy policy", "var x=1", "a{}"):
        assert chrome not in got, f"chrome leaked into hash: {chrome}"
    # <main> is the fallback when there's no <article>
    assert normalize(b"<html><body><nav>Nav</nav><main><p>Body</p></main></body></html>") == "Body"
    # neither container: hash the whole document rather than nothing
    assert normalize(b"<html><body><p>Bare</p></body></html>") == "Bare"
    print("selftest ok")


def fetch_hash(url):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=45) as r:  # noqa: S310 (trusted, owner-curated URLs)
        return hashlib.sha256(normalize(r.read()).encode("utf-8")).hexdigest()


def process(hashes_file):
    data = json.loads(hashes_file.read_text())
    sources = data.get("sources", {})
    skill = hashes_file.parent.parent.name
    changed = False
    for url, stored in sources.items():
        try:
            current = fetch_hash(url)
        except Exception as e:  # noqa: BLE001
            failed.append(f"- ⚠ fetch failed ({skill}): {url} — {e}")
            continue
        if stored is None:
            baselined.append(f"- baseline ({skill}): {url}")
            sources[url] = current
            changed = True
        elif stored != current:
            drift.append(f"- **changed** ({skill}): {url}")
            sources[url] = current
            changed = True
    if changed:
        data["sources"] = sources
        data["last_updated"] = datetime.date.today().isoformat()
        hashes_file.write_text(json.dumps(data, indent=2) + "\n")


def main():
    if "--selftest" in sys.argv:
        return selftest()
    files = sorted(ROOT.glob("plugins/**/references/.source-hashes.json"))
    if not files:
        print("no .source-hashes.json files found")
        return
    for f in files:
        process(f)

    for line in baselined:
        print(line)
    for line in failed:
        print(line)
    for line in drift:
        print(line)

    if drift or failed:
        report = ROOT / "drift.md"
        body = [
            "## 📡 Source docs changed",
            "",
            "The official docs behind one or more reference libraries changed — or could not be fetched — "
            "since the last check.",
            "Run `/refresh-references` on the affected skill(s) to reconcile, then bump the "
            "`last-verified` dates and update `CHANGELOG.md`.",
            "",
        ]
        if drift:
            body += drift
        if failed:
            body += ["", "### Fetch failures (may be moved/removed URLs — verify)", *failed]
        report.write_text("\n".join(body) + "\n")

    out = os.environ.get("GITHUB_OUTPUT")
    if out:
        with open(out, "a") as fh:
            fh.write(f"has_drift={'true' if (drift or failed) else 'false'}\n")

    print(f"\nsummary: {len(drift)} changed, {len(baselined)} baselined, {len(failed)} failed")


if __name__ == "__main__":
    sys.exit(main())
