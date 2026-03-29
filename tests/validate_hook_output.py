#!/usr/bin/env python3

import json
import os
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HOOK = ROOT / "hooks" / "session-start"


def run_hook(extra_env: dict[str, str] | None = None) -> dict:
    env = os.environ.copy()
    if extra_env:
        env.update(extra_env)

    result = subprocess.run(
        [str(HOOK)],
        check=True,
        capture_output=True,
        text=True,
        env=env,
        cwd=ROOT,
    )
    return json.loads(result.stdout)


def main() -> None:
    default_payload = run_hook()
    hook_output = default_payload["hookSpecificOutput"]
    assert hook_output["hookEventName"] == "SessionStart"
    assert hook_output["additionalContext"]
    assert "begin your reply with an insight block in this format" in hook_output[
        "additionalContext"
    ], "Expected SessionStart prompt to describe the insight block as a format, not a literal block"
    assert "Replace the placeholder line with 2-3 brief educational points" in hook_output[
        "additionalContext"
    ], "Expected SessionStart prompt to explain how to replace the placeholder line"
    assert "Do not say that you'll include an insight block later" in hook_output[
        "additionalContext"
    ], "Expected SessionStart prompt to forbid promising the block instead of rendering it"

    for env_name in ("CLAUDE_PLUGIN_ROOT", "CURSOR_PLUGIN_ROOT"):
        env_payload = run_hook({env_name: str(ROOT)})
        env_hook_output = env_payload["hookSpecificOutput"]
        assert env_hook_output["hookEventName"] == "SessionStart"
        assert env_hook_output["additionalContext"] == hook_output["additionalContext"], (
            f"Expected {env_name} to preserve the Codex SessionStart output contract"
        )


if __name__ == "__main__":
    main()
