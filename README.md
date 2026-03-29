# codex-explanatory-style

A distributable Codex plugin that recreates a Claude-like explanatory output style through a `SessionStart` hook.

## What it does

Once installed, the plugin injects additional developer context at session start and resume so Codex is nudged to include a short branded `★ Insight` block in substantive answers.

The insight block is meant to explain:

- implementation choices
- codebase patterns
- tradeoffs and design decisions
- educational takeaways that help the user learn from the work

The plugin keeps the guidance narrow so Codex still answers directly and does not turn every reply into a lecture. The goal is collaborative teaching, not textbook narration.

## Example

```text
★ Insight ─────────────────────────────────────
I used a startup hook here because Codex officially supports adding
developer context on SessionStart, which makes the style active from the
first turn instead of relying on an opt-in skill.

That also gives us a good place to encourage learning-oriented explanations
about tradeoffs and codebase patterns without changing the code itself.
─────────────────────────────────────────────────

Created the plugin manifest and wired the startup hook.
```

## Installation

Codex installs plugins through marketplaces rather than by pointing directly at a repo root. In practice, there are two steps:

1. Register the plugin locally so Codex can discover it in a marketplace.
2. Install the plugin from that marketplace in Codex App or Codex CLI so Codex enables it for use.

### Quick install

If you want Codex to handle the local registration steps for you, paste the prompt below into Codex. This prepares the plugin so it appears in Codex's plugin directory. You still need to restart Codex and enable it afterward from Codex App or Codex CLI.

```text
Register the codex-explanatory-style plugin as a local Codex plugin.

Only do the local registration steps so the plugin appears in Codex's Plugins UI.
Do not install or enable it inside Codex.

Tasks:
1. Clone https://github.com/5amfung/codex-explanatory-style into ~/.codex/plugins/codex-explanatory-style if it is not already present
2. Create or update ~/.agents/plugins/marketplace.json
3. Preserve any existing marketplace entries and unrelated plugins
4. Ensure marketplace.json contains a local plugin entry for codex-explanatory-style pointing to ./.codex/plugins/codex-explanatory-style
5. Verify that the cloned plugin contains .codex-plugin/plugin.json
6. When finished, tell me to restart Codex and enable the plugin from Plugins in Codex App or from /plugins in Codex CLI

If you need a reference, use https://raw.githubusercontent.com/5amfung/codex-explanatory-style/main/README.md
Do not delete, replace, or rewrite unrelated marketplace entries.
```

### Configure a local marketplace

If you do not already have `~/.agents/plugins/marketplace.json`, create it with the example below.

If you already have that file, use this section as the reference for the plugin object you need to add to its top-level `plugins` array.

Example `~/.agents/plugins/marketplace.json`:

```json
{
  "name": "local-plugins",
  "interface": {
    "displayName": "Local Plugins"
  },
  "plugins": [
    {
      "name": "codex-explanatory-style",
      "source": {
        "source": "local",
        "path": "./.codex/plugins/codex-explanatory-style"
      },
      "policy": {
        "installation": "AVAILABLE",
        "authentication": "ON_INSTALL"
      },
      "category": "Coding"
    }
  ]
}
```

The `source.path` is resolved relative to your home directory for a personal local marketplace, so `./.codex/plugins/codex-explanatory-style` points at `~/.codex/plugins/codex-explanatory-style`.

Adding the plugin to `marketplace.json` does not install it by itself. That file only makes the plugin appear in Codex's plugin directory. You still need the install step in Codex so the plugin is actually installed and enabled.

### Install in Codex App

1. Restart Codex after creating or updating the marketplace file.
2. Open `Plugins`.
3. Open the `Local Plugins` marketplace, or whatever `interface.displayName` you used in `marketplace.json`.
4. Select `codex-explanatory-style`.
5. Install or enable the plugin.
6. Start a new thread. This plugin uses a `SessionStart` hook, so the behavior is applied on new or resumed sessions.

### Install in Codex CLI

1. Restart your Codex CLI session after creating or updating the marketplace file.
2. Run `codex`.
3. Open the plugin directory with `/plugins`.
4. Open the `Local Plugins` marketplace, or whatever `interface.displayName` you used in `marketplace.json`.
5. Select `codex-explanatory-style`.
6. Install or enable the plugin.
7. Start a new thread so the `SessionStart` hook can apply.

### Troubleshooting

- If the plugin does not appear, make sure you copied the entire repository directory, including `.codex-plugin/plugin.json`, `hooks.json`, and `hooks/session-start`.
- If the marketplace loads but the plugin is missing, check that `marketplace.json` is valid JSON and that the plugin entry is inside the top-level `plugins` array.
- If Codex cannot resolve the local path, confirm that `./.codex/plugins/codex-explanatory-style` exists under your home directory.
- Verify the plugin in a new interactive Codex App or Codex CLI session. In local testing on March 28, 2026 with `codex-cli 0.117.0`, `codex exec` did not run the `SessionStart` hook command, so it was not a reliable end-to-end smoke test for this plugin.
- The official build-plugin docs also describe repo-local marketplaces if you want to test the plugin from another repository instead of copying it into `~/.codex/plugins`.

## Token cost

This plugin adds startup instructions and tends to produce slightly longer responses. Only install it if that tradeoff matches how you like Codex to work.

## Releases

This repository uses Google's `release-please` GitHub Action to manage release PRs, GitHub releases, and `CHANGELOG.md`.

- Merges to `main` can trigger a release PR.
- The release PR updates `CHANGELOG.md`, `.release-please-manifest.json`, and the version field in `.codex-plugin/plugin.json`.
- Merge commit titles should follow Conventional Commits such as `fix: ...`, `feat: ...`, or `feat!: ...` because release versions are derived from those commit types.

## Implementation Notes

- The plugin uses Codex's documented `SessionStart` hook.
- The hook emits runtime-aware JSON on `stdout`: `hookSpecificOutput.additionalContext` for Claude-style runtimes and `additional_context` as the fallback for other runtimes.
- The instructions explicitly skip the insight block for trivial replies to reduce noise.
- The prompt now explicitly asks for educational and learning-oriented insights, not just reasoning transparency.

## Verification Notes

- The local JSON and shell validation commands in this repo verify the plugin manifest, hook wiring, and hook output contract.
- Those checks do not prove that Codex is actively applying the injected context in a live session.
- For a true smoke test, install or enable the plugin, start a new interactive Codex App or Codex CLI session, and then ask a substantive software question that should trigger the `★ Insight` block.

## References

- [Codex hooks](https://developers.openai.com/codex/hooks)
- [Build plugins for Codex](https://developers.openai.com/codex/plugins/build)
- [Claude explanatory output style plugin](https://github.com/anthropics/claude-code/tree/main/plugins/explanatory-output-style)
