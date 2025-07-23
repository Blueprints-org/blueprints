"""Codes package."""

import importlib
import importlib.util
import sys

_all_packages = ["eurocode", "cur"]

for sub_module in _all_packages[:]:
    try:
        module = importlib.import_module(f".{sub_module}", package=__name__)
    except ModuleNotFoundError:
        # Optional: log warning
        continue

    _all_packages.extend(module.__all__)

    for alias in module.__all__:
        real_modname = f"blueprints.codes.{sub_module}.{alias}"
        alias_modname = f"{__name__}.{alias}"

        if alias_modname not in sys.modules:
            if importlib.util.find_spec(real_modname) is None:
                # Skip non-existent submodule
                continue
            mod = importlib.import_module(real_modname)
            sys.modules[alias_modname] = mod
            setattr(sys.modules[__name__], alias, mod)

__all__ = list(_all_packages)
