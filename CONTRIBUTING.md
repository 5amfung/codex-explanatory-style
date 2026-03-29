# Contributing

Thanks for helping improve `codex-explanatory-style`.

## Ways to contribute

- Report bugs with clear reproduction steps
- Suggest improvements to the prompt, install flow, or docs
- Submit pull requests for focused fixes or enhancements

## Before you open a pull request

1. Read the README and confirm the change fits the plugin's scope.
2. Keep changes small and targeted.
3. Update docs when behavior or installation changes.
4. Run the local validation commands below.

## Local validation

```bash
python3 -m json.tool hooks.json >/dev/null
sh -n hooks/session-start
./hooks/session-start | python3 -c 'import json,sys; data=json.load(sys.stdin); assert data["hookSpecificOutput"]["hookEventName"] == "SessionStart"; assert data["hookSpecificOutput"]["additionalContext"]'
```

## Pull request guidelines

- Describe the user-facing change clearly.
- Mention any tradeoffs or follow-up work.
- Include docs updates in the same pull request when needed.
- Keep PRs reviewable. If a change spans multiple concerns, split it up.
- Use Conventional Commit style for the final merged commit title when possible, for example `fix: ...`, `feat: ...`, or `feat!: ...`, because releases are managed by `release-please`.

## Development notes

This repo is intentionally small:

- `hooks.json` wires the Codex `SessionStart` hook.
- `hooks/session-start` emits the additional startup context.

Please preserve that simplicity unless a change clearly needs more structure.
