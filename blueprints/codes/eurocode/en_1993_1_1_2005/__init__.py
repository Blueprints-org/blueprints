"""EN 1993-1-1:2005."""

from blueprints.utils.lazy_imports import lazy_import_get_attr

__all__ = ["chapter_2_basic_of_design", "chapter_3_materials", "chapter_5_structural_analysis", "chapter_6_ultimate_limit_state"]


def __getattr__(name: str) -> object:
    """Override the getattr method, so we can lazily import the functions in this module."""
    return lazy_import_get_attr(__package__, name, __all__)


EN_1993_1_1_2005 = "EN 1993-1-1:2005"
