"""Eurocode EN 1993-1-9:2005."""

from blueprints.utils.lazy_imports import lazy_import_get_attr

__all__ = [
    "annex_a_determination_of_fatigue_load_parameters_and_verification_formats",
]


def __getattr__(name: str) -> object:
    """Override the getattr method, so we can lazily import the functions in this module."""
    return lazy_import_get_attr(__package__, name, __all__)


EN_1993_1_9_2005 = "EN 1993-1-9:2005"
