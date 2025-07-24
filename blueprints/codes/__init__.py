"""Codes package."""

import importlib
import sys

# all active packages in the codes
_all_packages = ["eurocode", "cur"]

# iterate through a copy of the list
for sub_module in _all_packages[:]:
    # Extend the _all_packages list with the submodule's __all__
    module = importlib.import_module(f".{sub_module}", package=__name__)
    _all_packages.extend(module.__all__)

    # write alisases for each submodule
    for alias in module.__all__:
        alias_modname = f"{__name__}.{alias}"
        if alias_modname not in sys.modules:
            mod = importlib.import_module(f".{alias}", package=f"{__name__}.{sub_module}")
            sys.modules[alias_modname] = mod
            setattr(sys.modules[__name__], alias, mod)


def __getattr__(name):
    if name in __all__:
        # Determine which submodule the name comes from (you can map it dynamically if needed)
        for sub_module in ["eurocode", "cur"]:
            try:
                return importlib.import_module(f".{sub_module}.{name}", __name__)
            except ModuleNotFoundError:
                continue
        raise AttributeError(f"Module {name} not found in known submodules.")
    raise AttributeError(f"module {__name__} has no attribute {name}")

# set all generated packages to __all__
__all__ = list(_all_packages)
