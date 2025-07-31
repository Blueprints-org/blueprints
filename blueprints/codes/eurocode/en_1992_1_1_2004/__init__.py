"""Eurocode EN 1992-1-1:2004."""

from blueprints.utils.lazy_imports import lazy_import_get_attr

__all__ = [
    "chapter_3_materials",
    "chapter_4_durability_and_cover",
    "chapter_5_structural_analysis",
    "chapter_6_ultimate_limit_state",
    "chapter_7_serviceability_limit_state",
    "chapter_8_detailing_of_reinforcement_and_prestressing_tendons",
    "chapter_9_detailling_and_specific_rules",
    "chapter_10_precast_concrete_elements_and_structures",
    "chapter_11_lightweight_aggregate_concrete_structures",
    "chapter_12_plain_and_lightly_reinforced_concrete_structures",
]


def __getattr__(name: str) -> object:
    """Override the getattr method, so we can lazily import the functions in this module."""
    return lazy_import_get_attr(__package__, name, __all__)


EN_1992_1_1_2004 = "EN 1992-1-1:2004"
