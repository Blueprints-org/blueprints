"""Import bootstrap for the benchmark scripts.

Blueprints pulls in a few optional-at-runtime reporting dependencies at import
time (``googletrans``, ``latex2mathml``, ``mathml2omml``).  They play no role in
section-property calculations, so when they are absent this module installs a
minimal stub for them.  That keeps the benchmarks runnable in a bare
environment without mutating the interpreter's site-packages.

Import this module *before* importing anything from ``blueprints``.
"""

from __future__ import annotations

import importlib
import sys
import types
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[1]


def _ensure_repo_on_path() -> None:
    """Make sure the checked-out blueprints package wins over any installed copy."""
    root = str(_REPO_ROOT)
    if sys.path[:1] != [root]:
        sys.path.insert(0, root)


def _stub(name: str, attributes: dict[str, object]) -> None:
    """Register a stub module when the real one is not installed."""
    try:
        importlib.import_module(name)
    except ModuleNotFoundError:
        module = types.ModuleType(name)
        for attr, value in attributes.items():
            setattr(module, attr, value)
        sys.modules[name] = module


def _unavailable(name: str):
    def _raise(*_args: object, **_kwargs: object) -> None:
        msg = f"{name} is stubbed out for benchmarking and cannot be used"
        raise RuntimeError(msg)

    return _raise


class _Translator:
    """Stand-in for :class:`googletrans.Translator`."""

    def translate(self, *_args: object, **_kwargs: object) -> None:
        msg = "googletrans is stubbed out for benchmarking"
        raise RuntimeError(msg)


def install() -> None:
    """Install the import shims and put the repo first on ``sys.path``."""
    _ensure_repo_on_path()
    _stub("googletrans", {"Translator": _Translator})
    _stub("latex2mathml", {})
    _stub("latex2mathml.converter", {"convert": _unavailable("latex2mathml")})
    _stub("mathml2omml", {"convert": _unavailable("mathml2omml")})


install()
