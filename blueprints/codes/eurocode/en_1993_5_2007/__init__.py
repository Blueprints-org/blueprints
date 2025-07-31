"""Eurocode EN 1993-5:2007."""

from blueprints.utils.lazy_imports import lazy_import_get_attr

__all__ = [
    "chapter_5_ultimate_limit_states",
]


def __getattr__(name: str) -> object:
    """Override the getattr method, so we can lazily import the functions in this module."""
    return lazy_import_get_attr(__package__, name, __all__)


EN_1993_5_2007 = "EN 1993-5:2007"
