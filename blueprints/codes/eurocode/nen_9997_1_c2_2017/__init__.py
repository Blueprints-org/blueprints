"""NEN 9997-1-C2:2017."""

from blueprints.utils.lazy_imports import lazy_import_get_attr

__all__ = ["chapter_1_general_rules", "chapter_2_basic_of_geotechnical_design"]


def __getattr__(name: str) -> object:
    """Override the getattr method, so we can lazily import the functions in this module."""
    return lazy_import_get_attr(__package__, name, __all__)


NEN_9997_1_C2_2017 = "NEN 9997-1-C2:2017"
