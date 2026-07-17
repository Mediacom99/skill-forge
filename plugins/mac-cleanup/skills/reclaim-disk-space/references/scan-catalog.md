<!-- verified against macOS 26.3 (build 25D125) · Apple Silicon (arm64) · 2026-07-17 — re-verify on a major macOS update -->

# Scan catalog — what to measure in Phase 1

Loaded at the start of Phase 1. This is the **catalog of candidates**; the **Absolute safety rules**
and *Phase 1 command safety* in `SKILL.md` still govern everything here. Measure real sizes with
`du -sh`; **never assume** a size or that a path exists. Probe each tool with `command -v` first and
silently skip absent ones. Apply the **~100 MB reporting floor** (roll small caches into one
aggregate row). **Verify reclaimability before listing** (predicates below).

Handy sizing idioms (read-only):
- One path: `du -sh "$path" 2>/dev/null`
- Several subfolders ranked: `du -sh "$dir"/* 2>/dev/null | sort -rh | head -20`
- Bounded home overview (depth 1, no full-tree walk, skip iCloud): `du -sh -d 1 "$HOME" 2>/dev/null | sort -rh | head -25` — but **exclude** `~/Library/Mobile Documents` and any synced Desktop/Documents.

---

## Tier A — Regenerable, low-risk (highest priority)

Mark which reclaims are **PERMANENT** (rule 6) vs Trash-reversible.

### Caches & logs
- `~/Library/Caches` — clear cache **subfolders** only; size the big ones: `du -sh ~/Library/Caches/* 2>/dev/null | sort -rh | head`.
- `~/Library/Logs` — old logs.
- **App caches — delete ONLY the `Cache` / `Code Cache` / `GPUCache` subfolder, NEVER the whole**
  `~/Library/Application Support/<app>` (that holds logins, profiles, local databases). Owning app
  **quit first** (rule 9). Common ones:
  - Chrome: `~/Library/Caches/Google/Chrome`
  - Slack: `~/Library/Application Support/Slack/{Cache,Code Cache,Service Worker/CacheStorage}`
  - Spotify: `~/Library/Caches/com.spotify.client`
  - JetBrains: `~/Library/Caches/JetBrains`; VS Code: `~/Library/Application Support/Code/{Cache,CachedData,Code Cache,GPUCache}`

### Xcode / dev
- **DerivedData:** `~/Library/Developer/Xcode/DerivedData` — pure build output, high yield, safe.
- **Old iOS DeviceSupport:** `~/Library/Developer/Xcode/iOS DeviceSupport` — per-OS-version symbols; old versions are re-generated on next device connect.
- **CoreSimulator caches:** `~/Library/Developer/CoreSimulator/Caches`.
- **Unused simulator RUNTIMES** — `xcrun simctl runtime list` (PERMANENT delete via `runtime delete`). ⚠️ `xcrun simctl` may provision/update CoreSimulator components on first run **even with Xcode installed** (expect a possible one-time "Install Started/Succeeded"); guard on `xcode-select -p` and treat its output cautiously.
- **Stale simulator devices:** `xcrun simctl delete unavailable` (PERMANENT).
- JetBrains / VS Code caches (above); old **nvm / pyenv / fnm** toolchains.

### Package & language caches
- pip: `~/Library/Caches/pip` · Yarn: `~/Library/Caches/Yarn` · CocoaPods: `~/Library/Caches/CocoaPods`
- npm: `~/.npm/_cacache` · Cargo: `~/.cargo/registry` · Gradle: `~/.gradle/caches` · conda (if present)
- **pnpm store** — resolve robustly, don't hardcode: prefer `pnpm config get store-dir` (avoids the Corepack-download side effect of `pnpm store path`); it's `~/Library/pnpm/store` (e.g. `…/store/v10`), **not** `~/Library/Caches/pnpm`. Reclaim via `pnpm store prune` (PERMANENT).
- **Go module cache** — resolve with `go env GOMODCACHE` (usually `~/go/pkg/mod`); its files are **read-only**, so plain `rm` fails — reclaim via `go clean -modcache` (PERMANENT).
- **Maven** — only `~/.m2/repository` (exclude `settings.xml`); flag **SNAPSHOT / locally-installed** artifacts as maybe-irreplaceable.
- **Homebrew** — reclaim via `brew cleanup` (PERMANENT); size the downloads cache first: `du -sh "$(brew --cache)" 2>/dev/null` and preview with `brew cleanup -n`.

### Project artifacts (verify each — see predicates)
- `node_modules` — only where a sibling `package.json` exists; regenerable via `npm/pnpm/yarn install`.
- `build` / `dist` / `target` / `.next` / `.turbo` — only if the build config is present, the source to regenerate exists, and git shows the dir ignored/clean (not holding uncommitted or only-copy output).

### Python
- `.venv` / `venv` — only if a `requirements*.txt` / `poetry.lock` / `Pipfile.lock` / `pyproject.toml` is present to recreate it.
- `__pycache__` directories; conda envs (only if a lock/environment file exists).

### Media libraries (re-downloadable)
- GarageBand / Logic **sound libraries & Apple loops** — often tens of GB; `~/Library/Application Support/{GarageBand,Logic}` and `~/Library/Audio/Apple Loops`.

### Docker (daemon RUNNING — rule 9)
- Size first: `docker system df` (and `docker system df -v` for detail). Run `docker ps -a` first and **warn** that `prune` deletes stopped containers, whose writable layer can be the only copy of their data. Reclaim **only dangling images / build cache** (PERMANENT); **never** `-a` or `--volumes` unless the user explicitly asks.

### Installers
- Old `Install macOS *.app` in `/Applications` (~12–15 GB, re-downloadable).

---

## Tier B — Personal / high-value, for the user's judgment (never removed without them reading each one)

- **Downloads** — especially large `.dmg` / `.pkg` / `.zip` / `.ipsw` installers the user can re-download: `du -sh ~/Downloads/* 2>/dev/null | sort -rh | head -20`.
- **Large media & documents** — rank the biggest by size; never pre-select.
- **Local LLM weights** — `~/.ollama/models`, `~/.cache/huggingface`, LM Studio (`~/.lmstudio/models`): regenerable but tens–hundreds of GB and slow/gated to re-download; **list, don't assume**.
- **iOS device backups** — `~/Library/Application Support/MobileSync/Backup`: may be the **ONLY** copy of a phone. Show each backup's **device name + date** and confirm a newer / iCloud backup exists before proposing anything.
- **Time Machine local snapshots** — `tmutil listlocalsnapshots /`; reclaim via `tmutil deletelocalsnapshots <date>` (PERMANENT; see rule 8).
- **VM / container disk images — REPORT-ONLY (rule 4).** Show existence + size but **never propose deleting**: OrbStack `~/.orbstack/data`, UTM `~/Library/Containers/com.utmapp.UTM/…`, Parallels `~/Parallels/*.pvm`, `Docker.raw` under `~/Library/Containers/com.docker.docker/Data/…`. Never match by `*.img` / `*.qcow2` extension.

---

## Tier C — Deep (higher effort, needs care)

- **Duplicate files** — match by size then content hash, but **first exclude APFS clones and
  hardlinks** (same inode / link-count > 1 via `stat` — deleting those frees ≈0), and report the
  **TRUE extra bytes** a deletion frees. Show both paths and let the **user** choose which to keep;
  default to keeping the copy in the more canonical/protected location. Never auto-pick.
- **Unused apps** and their orphaned `Application Support` / `Preferences` / `Caches` leftovers.

---

## Verify-before-listing predicates (quick reference)

| Candidate | List it only if |
|-----------|-----------------|
| `node_modules` | a sibling `package.json` exists |
| `build`/`dist`/`target`/`.next` | build config present **and** source present **and** git shows it ignored/clean |
| `.venv`/`venv` | a `requirements*.txt` / lockfile / `pyproject.toml` is present |
| any cache | the user owns it (and the owning app is quit before a file-level delete) |
| Maven `~/.m2` | excluding `settings.xml`; SNAPSHOT/local artifacts flagged maybe-irreplaceable |
| VM/container image | **never** — report size only (rule 4) |
| iCloud stub | **never** — `du`≈0, deleting can wipe the only copy (rule 8) |
