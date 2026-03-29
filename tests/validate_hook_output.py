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

    claude_payload = run_hook({"CLAUDE_PLUGIN_ROOT": str(ROOT)})
    hook_output = claude_payload["hookSpecificOutput"]
    assert hook_output["hookEventName"] == "SessionStart"
    assert hook_output["additionalContext"]


if __name__ == "__main__":
    main()
