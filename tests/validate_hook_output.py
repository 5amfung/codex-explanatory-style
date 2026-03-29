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
    assert "additional_context" in default_payload, (
        "Expected additional_context fallback when no Claude-specific env is set"
    )
    assert default_payload["additional_context"], (
        "Expected additional_context fallback to be non-empty"
    )
    assert "MUST begin your reply with the exact block below" in default_payload[
        "additional_context"
    ], "Expected default prompt to explicitly require the insight block first"
    assert "Do not describe the insight block or mention it abstractly" in default_payload[
        "additional_context"
    ], "Expected default prompt to forbid describing the block instead of rendering it"

    claude_payload = run_hook({"CLAUDE_PLUGIN_ROOT": str(ROOT)})
    hook_output = claude_payload["hookSpecificOutput"]
    assert hook_output["hookEventName"] == "SessionStart"
    assert hook_output["additionalContext"]
    assert "MUST begin your reply with the exact block below" in hook_output[
        "additionalContext"
    ], "Expected Claude-specific prompt to explicitly require the insight block first"
    assert "Do not describe the insight block or mention it abstractly" in hook_output[
        "additionalContext"
    ], "Expected Claude-specific prompt to forbid describing the block instead of rendering it"


if __name__ == "__main__":
    main()
