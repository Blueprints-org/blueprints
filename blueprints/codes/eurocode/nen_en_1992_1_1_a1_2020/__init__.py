"""Eurocode NEN-EN 1992-1-1:2005+A1:2015+NB:2016+A1:2020."""

from blueprints.utils.lazy_imports import lazy_import_get_attr

__all__ = ["chapter_4_durability_and_cover", "chapter_8_detailing_of_reinforcement_and_prestressing_tendons"]


def __getattr__(name: str) -> object:
    """Override the getattr method, so we can lazily import the functions in this module."""
    return lazy_import_get_attr(__package__, name, __all__)


NEN_EN_1992_1_1_A1_2020 = "NEN-EN 1992-1-1:2005+A1:2015+NB:2016+A1:2020"
