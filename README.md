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

Codex installs plugins through marketplaces rather than by pointing directly at a repo root.

For local testing, follow the manual local-plugin flow from the Codex plugin docs:

1. Copy this plugin folder into `~/.codex/plugins/codex-explanatory-style`.
2. Add or update `~/.agents/plugins/marketplace.json` so it points to `./.codex/plugins/codex-explanatory-style` relative to your home directory.
3. Restart Codex and install or enable the plugin from that marketplace.

The official build-plugin docs also describe repo-local marketplaces if you want to test the plugin from another repository.

Example `~/.agents/plugins/marketplace.json` entry:

```json
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
```

## Token cost

This plugin adds startup instructions and tends to produce slightly longer responses. Only install it if that tradeoff matches how you like Codex to work.

## Implementation Notes

- The plugin uses Codex's documented `SessionStart` hook.
- The hook emits `hookSpecificOutput.additionalContext` as JSON on `stdout`.
- The instructions explicitly skip the insight block for trivial replies to reduce noise.
- The prompt now explicitly asks for educational and learning-oriented insights, not just reasoning transparency.

## References

- [Codex hooks](https://developers.openai.com/codex/hooks)
- [Build plugins for Codex](https://developers.openai.com/codex/plugins/build)
- [Claude explanatory output style plugin](https://github.com/anthropics/claude-code/tree/main/plugins/explanatory-output-style)
