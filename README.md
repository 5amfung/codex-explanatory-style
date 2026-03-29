# codex-explanatory-style

A `SessionStart` hook for Codex that adds an explanatory output style to every session.

## What it does

Once installed, the hook injects additional developer context at session start and resume so Codex is nudged to include a short branded `★ Insight` block in substantive answers.

The insight block is meant to explain:

- implementation choices
- codebase patterns
- tradeoffs and design decisions
- educational takeaways that help the user learn from the work

The hook keeps the guidance narrow so Codex still answers directly and does not turn every reply into a lecture. The goal is collaborative teaching, not textbook narration.

## Example

```text
★ Insight ─────────────────────────────────────
I used a startup hook here because Codex officially supports adding
developer context on SessionStart, which makes the style active from the
first turn instead of relying on an opt-in skill.

That also gives us a good place to encourage learning-oriented explanations
about tradeoffs and codebase patterns without changing the code itself.
─────────────────────────────────────────────────

Created the hook and wired it into the Codex config.
```

## Prerequisites

Codex hooks are an experimental feature. Enable them by adding the following to your Codex configuration:

```toml
[features]
codex_hooks = true
```

## Installation

The hook is installed by copying two files into `~/.codex/`: the hook script and its wiring in `hooks.json`.

### Quick install

Paste the prompt below into Codex and it will handle the installation for you.

```text
Install the codex-explanatory-style SessionStart hook.

Tasks:
1. Clone https://github.com/5amfung/codex-explanatory-style into a temp directory
2. Create ~/.codex/hooks/ if it does not exist
3. Copy hooks/session-start from the cloned repo to ~/.codex/hooks/session-start
4. Make ~/.codex/hooks/session-start executable (chmod +x)
5. If ~/.codex/hooks.json already exists, merge the SessionStart entry from the repo's hooks.json into the existing file without removing other hooks
6. If ~/.codex/hooks.json does not exist, copy the repo's hooks.json to ~/.codex/hooks.json
7. Remove the temp clone
8. Check that codex_hooks is enabled in the Codex config. If not, tell me how to enable it
9. Tell me to start a new Codex session so the hook takes effect

Do not delete, replace, or rewrite any existing hooks in ~/.codex/hooks.json.
```

### Manual install

1. Clone or download this repository.

2. Copy the hook script:

   ```bash
   mkdir -p ~/.codex/hooks
   cp hooks/session-start ~/.codex/hooks/session-start
   chmod +x ~/.codex/hooks/session-start
   ```

3. Add the hook wiring to `~/.codex/hooks.json`. If the file does not exist, copy it directly:

   ```bash
   cp hooks.json ~/.codex/hooks.json
   ```

   If `~/.codex/hooks.json` already exists, merge the `SessionStart` entry from this repo's `hooks.json` into your existing file. The hook entry to add:

   ```json
   {
     "matcher": "startup|resume",
     "hooks": [
       {
         "type": "command",
         "command": "~/.codex/hooks/session-start",
         "statusMessage": "Loading explanatory style"
       }
     ]
   }
   ```

   This object goes inside the `hooks.SessionStart` array in your `hooks.json`.

4. Start a new Codex session. The hook fires on session start and resume.

### Uninstall

1. Remove the `SessionStart` entry for `session-start` from `~/.codex/hooks.json`. If it is the only hook, you can delete the file entirely.
2. Delete the hook script:

   ```bash
   rm ~/.codex/hooks/session-start
   ```

### Troubleshooting

- If the insight block does not appear, confirm that `codex_hooks = true` is set in your Codex configuration.
- If the hook does not fire, check that `~/.codex/hooks/session-start` exists and is executable (`chmod +x`).
- If you see a JSON parse error, validate your `~/.codex/hooks.json` with `python3 -m json.tool ~/.codex/hooks.json`.
- The hook only fires on new or resumed sessions. It will not apply mid-session.

## Token cost

This hook adds startup instructions and tends to produce slightly longer responses. Only install it if that tradeoff matches how you like Codex to work.

## Releases

This repository uses Google's `release-please` GitHub Action to manage release PRs, GitHub releases, and `CHANGELOG.md`.

- Merges to `main` can trigger a release PR.
- The release PR updates `CHANGELOG.md` and `.release-please-manifest.json`.
- Merge commit titles should follow Conventional Commits such as `fix: ...`, `feat: ...`, or `feat!: ...` because release versions are derived from those commit types.

## Implementation Notes

- The hook uses Codex's documented `SessionStart` event.
- The hook emits `hookSpecificOutput.additionalContext` as JSON on `stdout`.
- The instructions explicitly skip the insight block for trivial replies to reduce noise.
- The prompt explicitly asks for educational and learning-oriented insights, not just reasoning transparency.

## References

- [Codex hooks](https://developers.openai.com/codex/hooks)
- [Claude explanatory output style plugin](https://github.com/anthropics/claude-code/tree/main/plugins/explanatory-output-style)
