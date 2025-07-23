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
        real_modname = f"blueprints.codes.{sub_module}.{alias}"
        alias_modname = f"{__name__}.{alias}"

        if alias_modname not in sys.modules:
            mod = importlib.import_module(real_modname)
            sys.modules[alias_modname] = mod
            setattr(sys.modules[__name__], alias, mod)

# set all generated packages to __all__
__all__ = list(_all_packages)
