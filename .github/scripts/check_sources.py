#!/usr/bin/env python3
"""Detect drift in the official source docs behind each skill's reference library.

For every plugins/**/references/.source-hashes.json it fetches each source URL, hashes the content,
and compares to the stored hash:
  - stored == null  -> capture a baseline (no drift reported)
  - stored != hash  -> DRIFT (record it)
  - stored == hash  -> unchanged

It rewrites the hash files with current values, and writes drift.md + sets has_drift in $GITHUB_OUTPUT
when any source changed. The workflow then commits the refreshed hashes and opens/updates an issue.

No LLM, no secrets — just fetch + sha256. Cosmetic page edits can cause false positives (acceptable).
Run locally: python .github/scripts/check_sources.py
"""
import datetime
import hashlib
import json
import os
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
UA = {"User-Agent": "skill-forge-check-sources/1.0 (+https://github.com/Mediacom99/skill-forge)"}
drift = []
baselined = []
failed = []


def fetch_hash(url):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=45) as r:  # noqa: S310 (trusted, owner-curated URLs)
        return hashlib.sha256(r.read()).hexdigest()


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

    if drift:
        report = ROOT / "drift.md"
        body = [
            "## 📡 Source docs changed",
            "",
            "The official docs behind one or more reference libraries changed since the last check.",
            "Run `/refresh-references` on the affected skill(s) to reconcile, then bump the "
            "`last-verified` dates and update `CHANGELOG.md`.",
            "",
            *drift,
        ]
        if failed:
            body += ["", "### Fetch failures (may be moved/removed URLs — verify)", *failed]
        report.write_text("\n".join(body) + "\n")

    out = os.environ.get("GITHUB_OUTPUT")
    if out:
        with open(out, "a") as fh:
            fh.write(f"has_drift={'true' if drift else 'false'}\n")

    print(f"\nsummary: {len(drift)} changed, {len(baselined)} baselined, {len(failed)} failed")


if __name__ == "__main__":
    sys.exit(main())
