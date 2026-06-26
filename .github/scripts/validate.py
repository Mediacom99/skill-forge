#!/usr/bin/env python3
"""Validate skill-forge manifests and skills so `main` stays installable.

Checks:
  - .claude-plugin/marketplace.json: valid JSON, has name/owner/plugins[], each plugin has name+source.
  - plugins/*/.claude-plugin/plugin.json: valid JSON, has name+description.
  - plugins/*/skills/*/SKILL.md: frontmatter has name+description; name is kebab-case and matches the
    skill directory; relative markdown links to bundled files actually exist.

Exits non-zero (printing every problem) if anything is wrong. Run locally: python .github/scripts/validate.py
"""
import json
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("PyYAML required: pip install pyyaml", file=sys.stderr)
    sys.exit(2)

ROOT = Path(__file__).resolve().parents[2]
KEBAB = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
errors = []

# Prompt-crafting skills are read-only by contract (see their SKILL.md): they may declare only these
# tools. A regression that adds Edit or an unscoped Bash would silently break that guarantee, so the
# install-safety gate enforces it here.
READONLY_PROMPT_TOOLS = {
    "Read", "Grep", "Glob", "AskUserQuestion", "Write",
    "Bash(pbcopy:*)", "Bash(wl-copy:*)", "Bash(xclip:*)", "Bash(xsel:*)",
    "Bash(clip.exe:*)", "Bash(clip:*)",
}


def load_json(path):
    try:
        return json.loads(path.read_text())
    except Exception as e:  # noqa: BLE001
        errors.append(f"{path.relative_to(ROOT)}: invalid JSON ({e})")
        return None


def check_marketplace():
    mp = ROOT / ".claude-plugin" / "marketplace.json"
    if not mp.exists():
        errors.append(".claude-plugin/marketplace.json: missing")
        return
    data = load_json(mp)
    if data is None:
        return
    for key in ("name", "owner", "plugins"):
        if key not in data:
            errors.append(f"marketplace.json: missing '{key}'")
    for i, plugin in enumerate(data.get("plugins", [])):
        if "name" not in plugin:
            errors.append(f"marketplace.json: plugins[{i}] missing 'name'")
        if "source" not in plugin:
            errors.append(f"marketplace.json: plugin '{plugin.get('name', i)}' missing 'source'")


def parse_frontmatter(path):
    text = path.read_text()
    if not text.startswith("---"):
        errors.append(f"{path.relative_to(ROOT)}: missing YAML frontmatter")
        return None
    parts = text.split("---", 2)
    if len(parts) < 3:
        errors.append(f"{path.relative_to(ROOT)}: malformed frontmatter")
        return None
    try:
        return yaml.safe_load(parts[1]) or {}
    except Exception as e:  # noqa: BLE001
        errors.append(f"{path.relative_to(ROOT)}: frontmatter not valid YAML ({e})")
        return None


def check_links(skill_md):
    body = skill_md.read_text()
    for target in re.findall(r"\]\(([^)]+)\)", body):
        link = target.split("#")[0].strip()
        if not link or link.startswith(("http://", "https://", "mailto:")):
            continue
        if not (skill_md.parent / link).exists():
            errors.append(f"{skill_md.relative_to(ROOT)}: broken relative link '{link}'")


def check_plugins():
    plugins_dir = ROOT / "plugins"
    if not plugins_dir.exists():
        errors.append("plugins/: missing")
        return
    for plugin_json in plugins_dir.glob("*/.claude-plugin/plugin.json"):
        data = load_json(plugin_json)
        if data is None:
            continue
        for key in ("name", "description"):
            if key not in data:
                errors.append(f"{plugin_json.relative_to(ROOT)}: missing '{key}'")
    for skill_md in plugins_dir.glob("*/skills/*/SKILL.md"):
        fm = parse_frontmatter(skill_md)
        if fm is None:
            continue
        name = fm.get("name")
        if not name:
            errors.append(f"{skill_md.relative_to(ROOT)}: frontmatter missing 'name'")
        else:
            if not KEBAB.match(str(name)):
                errors.append(f"{skill_md.relative_to(ROOT)}: name '{name}' is not kebab-case")
            if str(name) != skill_md.parent.name:
                errors.append(
                    f"{skill_md.relative_to(ROOT)}: name '{name}' != directory '{skill_md.parent.name}'"
                )
        if not fm.get("description"):
            errors.append(f"{skill_md.relative_to(ROOT)}: frontmatter missing 'description'")
        if name and str(name).endswith("-prompt-crafting"):
            declared = {t.strip() for t in str(fm.get("allowed-tools", "")).split(",") if t.strip()}
            extra = declared - READONLY_PROMPT_TOOLS
            if extra:
                errors.append(
                    f"{skill_md.relative_to(ROOT)}: read-only contract violated — "
                    f"allowed-tools grants {sorted(extra)} beyond the permitted set"
                )
        check_links(skill_md)


def main():
    check_marketplace()
    check_plugins()
    if errors:
        print(f"❌ validation failed ({len(errors)} problem(s)):")
        for e in errors:
            print(f"  - {e}")
        sys.exit(1)
    print("✅ validation passed: manifests and skills look good.")


if __name__ == "__main__":
    main()
