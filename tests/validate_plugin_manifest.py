#!/usr/bin/env python3

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PLUGIN_MANIFEST = ROOT / ".codex-plugin" / "plugin.json"


def main() -> None:
    payload = json.loads(PLUGIN_MANIFEST.read_text())
    interface = payload["interface"]
    assert (
        "defaultPrompt" not in interface
    ), "Expected plugin manifest to omit interface.defaultPrompt so the plugin does not seed a starter conversation"


if __name__ == "__main__":
    main()
