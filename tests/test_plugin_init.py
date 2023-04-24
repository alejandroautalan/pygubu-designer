import importlib
import traceback
from pygubu.component.plugin_manager import PluginManager


def main():
    all_modules = []
    for plugin in PluginManager.builder_plugins():
        all_modules.extend(plugin.get_all_modules())
    for _module in all_modules:
        try:
            importlib.import_module(_module)
        except (ModuleNotFoundError, ImportError):
            msg = f"Failed to load widget module: '{_module}'"
            det = traceback.format_exc()
            print(msg)
            print(det)


if __name__ == "__main__":
    main()
