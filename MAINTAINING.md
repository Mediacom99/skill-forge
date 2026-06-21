# Maintaining skill-forge

This repo is a Claude Code **marketplace** that hosts multiple **plugins**, each bundling one or more
**skills**. It's built to grow — adding skills is mechanical.

## Add a skill to an existing plugin

1. Create the skill folder:
   ```
   plugins/<plugin>/skills/<skill-name>/SKILL.md
   ```
2. Write `SKILL.md` with YAML frontmatter — at minimum `name` (kebab-case, **must equal the folder
   name**) and a `description`. Make the description specific about *what it does* and *when to trigger*
   (slightly "pushy" wording helps — skills tend to under-trigger). Bundle heavy material under
   `references/` and load it on demand (progressive disclosure) rather than inlining everything.
3. Skills auto-discover from a plugin's `skills/` directory — no marketplace edit needed for a new skill
   inside an existing plugin.
4. Run validation locally (below) and open a PR.

## Add a new plugin (new theme)

1. Scaffold:
   ```
   plugins/<new-plugin>/.claude-plugin/plugin.json
   plugins/<new-plugin>/skills/<skill>/SKILL.md
   ```
   `plugin.json` needs at least `name` + `description` (add `version`, `author`).
2. Register it in `.claude-plugin/marketplace.json` — add an entry to `plugins[]` with a local `source`:
   ```json
   { "name": "<new-plugin>", "description": "…", "author": { "name": "Mediacom99" },
     "category": "productivity", "source": "./plugins/<new-plugin>",
     "homepage": "https://github.com/Mediacom99/skill-forge/tree/main/plugins/<new-plugin>" }
   ```
3. Validate and PR. Users install with `/plugin install <new-plugin>@skill-forge`.

## The sourced-reference convention (`_sources.md`)

Any skill whose content distills external docs should be **sourced**:

- Put distilled docs in `references/`. Add a header comment with `last-verified: <date>`.
- Keep a `references/_sources.md` manifest: the canonical URLs, a one-line "what it covers" per URL, a
  `last-verified` date, and a **volatile items** list (facts that change — model IDs, parameters, etc.).
- Separate stable principles from the small, clearly-flagged volatile facts so updates touch little.
- Add a `references/.source-hashes.json` seeded with the same URLs and `null` hashes; the drift workflow
  captures the baseline on its first run.

### Keeping references fresh

1. **`/refresh-references`** (the `maintenance` plugin) — point it at a skill; it re-fetches each source,
   diffs against the distilled reference, proposes targeted edits, and bumps the dates.
2. **`check-sources.yml`** — runs weekly (and on demand via *Run workflow*). It hashes each source and, on
   change, opens/updates an issue. Then you run `/refresh-references` to reconcile.
3. After any reference change: bump `last-verified` in `_sources.md` and the file headers, and add a
   `CHANGELOG.md` entry.

## Run the checks locally

```bash
pip install pyyaml
python .github/scripts/validate.py        # manifests + skill frontmatter + relative links
python .github/scripts/check_sources.py   # fetch + hash the sources, report drift (writes drift.md)
```

`validate.py` must exit clean before merging — it's the same gate CI runs.

## Versioning & releases

- Bump the affected `plugin.json` `version` (semver) when a plugin's behavior changes.
- Record changes in `CHANGELOG.md` (Keep a Changelog style).
- Marketplace installs track the repo, so users pick up changes on update — no separate publish step.
- A `release.yml` (tag + GitHub Release from the changelog) can be added later if desired.
