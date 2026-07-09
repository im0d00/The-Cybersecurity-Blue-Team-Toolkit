# Plugin Guide

Implement a class that inherits `ToolkitPlugin` and place it in a plugin directory.

Example plugin contract:
- `name`: plugin identifier
- `run(payload: dict) -> dict`: execution entrypoint

Use `load_plugins("plugins")` to discover and execute installed plugins.
