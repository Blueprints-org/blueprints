"""Eurocode EN 1995-1-1:2004."""

from blueprints.utils.lazy_imports import lazy_import_get_attr

__all__ = [
    "chapter_7_serviceability_limit_states",
]


def __getattr__(name: str) -> object:
    """Override the getattr method, so we can lazily import the functions in this module."""
    return lazy_import_get_attr(__package__, name, __all__)


EN_1995_1_1_2004 = "EN 1995-1-1:2004"
