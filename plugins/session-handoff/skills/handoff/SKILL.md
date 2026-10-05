---
name: handoff
description: >
  End a long session cleanly before /clear: persist everything worth keeping into the project's
  own state files (progress, TODO, decisions, session log), then produce a short, copy-ready
  handoff prompt for a fresh session and put it on the clipboard. Use when the user says the
  context is full, wants to restart / start a new session, asks to "persist state", "update the
  state files", "save progress", or asks for a handoff / resume / continuation prompt — in any
  language (e.g. "riparto in una nuova sessione, dammi l'handoff prompt").
argument-hint: "[optional: what the next session should focus on]"
allowed-tools: Read, Grep, Glob, Edit, Write, Bash(git status:*), Bash(git diff:*), Bash(git log:*), Bash(git worktree list:*), Bash(pbcopy:*), Bash(wl-copy:*), Bash(xclip:*), Bash(xsel:*), Bash(clip.exe:*), Bash(clip:*)
version: 0.1.0
metadata:
  tags: session, handoff, context, progress, state, resume, clear
---

# Handoff

The user is about to `/clear`. Everything that lives only in this conversation is about to be
lost. Your job: **move what matters into files, then hand over a prompt that lets a fresh session
with zero memory continue without asking anything.** Do it fast — the context is already full, so
every token you spend here is expensive.

**Speed rules:** no questions to the user, no subagents, no re-exploring the codebase. You already
know what happened in this session; read only the files you are about to update. If the user
passed an argument, it sets the next session's focus.

## 1. Find where state lives (one pass)

1. **The project's own rules come first.** Project instruction files (`CLAUDE.md`, `AGENTS.md`,
   and anything they point to) usually say where state lives, how it is written, what language,
   size limits, and what is forbidden (e.g. "no tool memory, state lives only in PROGRESS.md").
   They are already in your context: follow them exactly. They override everything below.
2. If the rules don't name the state files, glob the repo root and `docs/` for the usual ones:
   `PROGRESS.md`, `STATUS.md`, `TODO.md`, `HANDOFF.md`, `NOTES.md`, `SESSION-NOTES.md`,
   `ROADMAP.md`, `CHANGELOG.md`, a `progress/` or `sessions/` folder.
3. Run `git status --short` and `git diff --stat` (plus `git worktree list` if worktrees were used)
   to see what is uncommitted.

If no state file exists at all, create one `PROGRESS.md` at the repo root (where we are + next
steps) and say so in the final report.

## 2. Update the state files

Write what a fresh session needs and **cannot recover from the code or git history**:

- **Where we are**: what works now, what is half-done (exact file, function, step), what is broken.
- **Decisions and why**, with the alternative rejected — the "why" is what dies with the context.
  Put them where the project keeps decisions, not in the progress file, if it has such a place.
- **Next steps**, concrete and in order; remove the TODOs that got done.
- **Traps found**: things that cost time this session (a flaky test, a wrong assumption, a command
  that must be run a certain way).
- **Open questions** for the user, if any were left unanswered.

How to write it:

- **Replace stale state, don't append forever.** The "current state" section describes now; the old
  version goes away. If the project keeps a per-session history (a `progress/` folder, a log), add
  this session's entry there, short, following the existing entries' format.
- Absolute dates (`2026-10-05`), never "today" or "yesterday".
- Match the existing files' language, tone, and structure. Respect size limits; split if the project
  says to.
- Use tool memory (auto-memory, `MEMORY.md`) only if the project already uses it and its rules
  allow it.
- **Don't commit or push** unless the project rules or the user say to. Uncommitted work goes in the
  prompt instead.

### What dies with the session — persist it or name it

- Files in a session-scoped scratchpad or temp dir: move anything worth keeping into the repo (or
  where the project says), otherwise state that it's disposable.
- Git worktrees, branches, stashes created this session; background processes or servers still
  running; pending reviews, open PRs, agents you launched.
- Something the user is editing right now, or a change you proposed and they haven't applied yet.
- Facts you verified by running things (a measurement, a reproduced bug) that aren't written down.

## 3. Write the handoff prompt

A prompt for a model that knows nothing. Rules:

- **In the user's language**, addressed to the next session ("Riprendi...", "Resume...").
- **Point to files, don't copy them.** The state is in the files now; the prompt says what to read
  and in what order, and carries only what isn't in any file.
- Don't repeat instruction files the new session loads automatically (`CLAUDE.md`); do name the
  ones it must read by hand (e.g. `AGENTS.md`, `PROGRESS.md`) if the project rules say so.
- **Short**: about 10–25 lines. Structure:
  1. one line: project and what we're doing;
  2. files to read first, in order;
  3. where we are, in 1–3 lines;
  4. **the next action**, concrete enough to start without asking (file, function, command);
  5. uncommitted or ephemeral state (branch, worktree, running process, unapplied change);
  6. traps and constraints that aren't obvious from the files — only if there are any.
- Every path, name, and number in it must be real: you wrote or read it this session.

Self-check before delivering: *with only this prompt and the repo, would a fresh session know the
next action and not redo or undo anything?* If not, fix the prompt or the files.

## 4. Deliver

1. Print the prompt in **one fenced code block** (use `~~~~` fences if it contains backticks) so it
   copies cleanly.
2. Copy it to the clipboard with a single clipboard command fed by a quoted here-doc, no temp file:
   `pbcopy << 'HANDOFF_CLIP_EOF'` … `HANDOFF_CLIP_EOF` on macOS; `wl-copy` (Wayland),
   `xclip -selection clipboard` or `xsel -b` (X11), `clip.exe` (WSL) elsewhere. If it fails, say so
   and move on — the code block is enough.
3. Close with at most three lines: which files you updated (or created), what is left uncommitted,
   and "copied — `/clear`, then paste". Nothing else: no recap of the session, no offers.

You cannot run `/clear` yourself; the user does.
