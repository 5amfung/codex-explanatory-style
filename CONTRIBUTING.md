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
python3 -m json.tool .codex-plugin/plugin.json >/dev/null
python3 -m json.tool hooks.json >/dev/null
sh -n hooks/session-start
python3 tests/validate_plugin_manifest.py
python3 tests/validate_hook_output.py
```

Those commands validate the plugin files and hook payload, but they are not a full end-to-end behavior test.

For an end-to-end smoke test, install or enable the plugin, start a new interactive Codex App or Codex CLI session, and ask a substantive software question that should trigger the `★ Insight` block. In local testing on March 28, 2026 with `codex-cli 0.117.0`, `codex exec` did not run the `SessionStart` hook command, so it was not a reliable smoke test for this plugin.

## Pull request guidelines

- Describe the user-facing change clearly.
- Mention any tradeoffs or follow-up work.
- Include docs updates in the same pull request when needed.
- Keep PRs reviewable. If a change spans multiple concerns, split it up.
- Use Conventional Commit style for the final merged commit title when possible, for example `fix: ...`, `feat: ...`, or `feat!: ...`, because releases are managed by `release-please`.

## Development notes

This repo is intentionally small:

- `.codex-plugin/plugin.json` defines plugin metadata.
- `hooks.json` wires the Codex `SessionStart` hook.
- `hooks/session-start` emits the additional startup context.

Please preserve that simplicity unless a change clearly needs more structure.
