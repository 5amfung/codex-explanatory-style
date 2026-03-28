## Summary

Describe the change and why it is needed.

## Validation

- [ ] `python3 -m json.tool .codex-plugin/plugin.json >/dev/null`
- [ ] `python3 -m json.tool hooks.json >/dev/null`
- [ ] `sh -n hooks/session-start`
- [ ] `./hooks/session-start | python3 -c 'import json,sys; data=json.load(sys.stdin); assert data["hookSpecificOutput"]["hookEventName"] == "SessionStart"; assert data["hookSpecificOutput"]["additionalContext"]'`

## Checklist

- [ ] Docs updated if installation or behavior changed
- [ ] Scope is focused and reviewable
- [ ] No unrelated files changed
