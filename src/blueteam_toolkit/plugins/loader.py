import importlib.util
from pathlib import Path

from .sdk import ToolkitPlugin


def load_plugins(plugin_dir: str | Path) -> list[ToolkitPlugin]:
    plugins = []
    directory = Path(plugin_dir)
    if not directory.exists():
        return plugins

    for plugin_file in directory.glob("*.py"):
        spec = importlib.util.spec_from_file_location(plugin_file.stem, plugin_file)
        if spec is None or spec.loader is None:
            continue
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        for attr_name in dir(module):
            attr = getattr(module, attr_name)
            if (
                isinstance(attr, type)
                and issubclass(attr, ToolkitPlugin)
                and attr is not ToolkitPlugin
            ):
                plugins.append(attr())
    return plugins
