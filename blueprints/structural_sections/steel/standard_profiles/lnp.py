"""LNP Steel Profiles."""

from typing import NamedTuple

from blueprints.structural_sections.steel.profile_definitions.lnp_profile import LNPProfile
from blueprints.structural_sections.steel.standard_profiles.utils import StandardProfileMeta
from blueprints.type_alias import MM


class __LNPProfileParameters(NamedTuple):
    """Parameters for defining a LNP profile."""

    name: str
    """Name of the LNP profile."""
    total_height: MM
    """Total height of the LNP profile."""
    total_width: MM
    """Total width of the LNP profile."""
    web_thickness: MM
    """Web thickness of the LNP profile."""
    base_thickness: MM
    """Base thickness of the LNP profile."""
    root_radius: MM
    """Inner radius of the web-base corner of the LNP profile."""
    back_radius: MM
    """Outer radius of the web-base corner of the LNP profile."""
    web_toe_radius: MM
    """Radius of the toe in the web of the LNP profile."""
    base_toe_radius: MM
    """Radius of the toe in the base of the LNP profile."""


LNP_PROFILES_DATABASE = {
    "LNP40x40x4": __LNPProfileParameters("LNP 40x40x4", 40, 40, 4, 4, 6, 0, 3, 3),
    "LNP40x40x5": __LNPProfileParameters("LNP 40x40x5", 40, 40, 5, 5, 6, 0, 3, 3),
    "LNP45x45x5": __LNPProfileParameters("LNP 45x45x5", 45, 45, 5, 5, 7, 0, 3.5, 3.5),
    "LNP50x50x5": __LNPProfileParameters("LNP 50x50x5", 50, 50, 5, 5, 7, 0, 3.5, 3.5),
    "LNP50x50x6": __LNPProfileParameters("LNP 50x50x6", 50, 50, 6, 6, 7, 0, 3.5, 3.5),
    "LNP50x50x8": __LNPProfileParameters("LNP 50x50x8", 50, 50, 8, 8, 7, 0, 3.5, 3.5),
    "LNP50x30x4": __LNPProfileParameters("LNP 50x30x4", 50, 30, 4, 4, 5, 0, 2.5, 2.5),
    "LNP50x30x5": __LNPProfileParameters("LNP 50x30x5", 50, 30, 5, 5, 5, 0, 2.5, 2.5),
    "LNP55x55x6": __LNPProfileParameters("LNP 55x55x6", 55, 55, 6, 6, 8, 0, 4, 4),
    "LNP60x60x6": __LNPProfileParameters("LNP 60x60x6", 60, 60, 6, 6, 8, 0, 4, 4),
    "LNP60x60x8": __LNPProfileParameters("LNP 60x60x8", 60, 60, 8, 8, 8, 0, 4, 4),
    "LNP60x60x10": __LNPProfileParameters("LNP 60x60x10", 60, 60, 10, 10, 8, 0, 4, 4),
    "LNP60x30x5": __LNPProfileParameters("LNP 60x30x5", 60, 30, 5, 5, 5, 0, 2.5, 2.5),
    "LNP60x30x7": __LNPProfileParameters("LNP 60x30x7", 60, 30, 7, 7, 5, 0, 2.5, 2.5),
    "LNP60x40x5": __LNPProfileParameters("LNP 60x40x5", 60, 40, 5, 5, 6, 0, 3, 3),
    "LNP60x40x6": __LNPProfileParameters("LNP 60x40x6", 60, 40, 6, 6, 6, 0, 3, 3),
    "LNP60x40x7": __LNPProfileParameters("LNP 60x40x7", 60, 40, 7, 7, 6, 0, 3, 3),
    "LNP65x65x7": __LNPProfileParameters("LNP 65x65x7", 65, 65, 7, 7, 9, 0, 4.5, 4.5),
    "LNP70x70x7": __LNPProfileParameters("LNP 70x70x7", 70, 70, 7, 7, 9, 0, 4.5, 4.5),
    "LNP70x70x9": __LNPProfileParameters("LNP 70x70x9", 70, 70, 9, 9, 9, 0, 4.5, 4.5),
    "LNP70x50x6": __LNPProfileParameters("LNP 70x50x6", 70, 50, 6, 6, 7, 0, 3.5, 3.5),
    "LNP75x75x8": __LNPProfileParameters("LNP 75x75x8", 75, 75, 8, 8, 9, 0, 4.5, 4.5),
    "LNP75x50x6": __LNPProfileParameters("LNP 75x50x6", 75, 50, 6, 6, 7, 0, 3.5, 3.5),
    "LNP75x50x7": __LNPProfileParameters("LNP 75x50x7", 75, 50, 7, 7, 7, 0, 3.5, 3.5),
    "LNP80x80x8": __LNPProfileParameters("LNP 80x80x8", 80, 80, 8, 8, 10, 0, 5, 5),
    "LNP80x80x10": __LNPProfileParameters("LNP 80x80x10", 80, 80, 10, 10, 10, 0, 5, 5),
    "LNP80x80x12": __LNPProfileParameters("LNP 80x80x12", 80, 80, 12, 12, 10, 0, 5, 5),
    "LNP80x40x6": __LNPProfileParameters("LNP 80x40x6", 80, 40, 6, 6, 7, 0, 3.5, 3.5),
    "LNP80x40x8": __LNPProfileParameters("LNP 80x40x8", 80, 40, 8, 8, 7, 0, 3.5, 3.5),
    "LNP90x90x9": __LNPProfileParameters("LNP 90x90x9", 90, 90, 9, 9, 11, 0, 5.5, 5.5),
    "LNP90x60x6": __LNPProfileParameters("LNP 90x60x6", 90, 60, 6, 6, 7, 0, 3.5, 3.5),
    "LNP90x60x8": __LNPProfileParameters("LNP 90x60x8", 90, 60, 8, 8, 7, 0, 3.5, 3.5),
    "LNP100x100x10": __LNPProfileParameters("LNP 100x100x10", 100, 100, 10, 10, 12, 0, 6, 6),
    "LNP100x100x12": __LNPProfileParameters("LNP 100x100x12", 100, 100, 12, 12, 12, 0, 6, 6),
    "LNP100x100x14": __LNPProfileParameters("LNP 100x100x14", 100, 100, 14, 14, 12, 0, 6, 6),
    "LNP100x50x6": __LNPProfileParameters("LNP 100x50x6", 100, 50, 6, 6, 8, 0, 4, 4),
    "LNP100x50x8": __LNPProfileParameters("LNP 100x50x8", 100, 50, 8, 8, 8, 0, 4, 4),
    "LNP100x50x10": __LNPProfileParameters("LNP 100x50x10", 100, 50, 10, 10, 8, 0, 4, 4),
    "LNP100x65x7": __LNPProfileParameters("LNP 100x65x7", 100, 65, 7, 7, 10, 0, 5, 5),
    "LNP100x65x9": __LNPProfileParameters("LNP 100x65x9", 100, 65, 9, 9, 10, 0, 5, 5),
    "LNP100x65x11": __LNPProfileParameters("LNP 100x65x11", 100, 65, 11, 11, 10, 0, 5, 5),
    "LNP100x75x9": __LNPProfileParameters("LNP 100x75x9", 100, 75, 9, 9, 10, 0, 5, 5),
    "LNP110x110x10": __LNPProfileParameters("LNP 110x110x10", 110, 110, 10, 10, 12, 0, 6, 6),
    "LNP120x120x10": __LNPProfileParameters("LNP 120x120x10", 120, 120, 10, 10, 13, 0, 6.5, 6.5),
    "LNP120x120x12": __LNPProfileParameters("LNP 120x120x12", 120, 120, 12, 12, 13, 0, 6.5, 6.5),
    "LNP120x120x15": __LNPProfileParameters("LNP 120x120x15", 120, 120, 15, 15, 13, 0, 6.5, 6.5),
    "LNP120x80x8": __LNPProfileParameters("LNP 120x80x8", 120, 80, 8, 8, 11, 0, 5.5, 5.5),
    "LNP120x80x10": __LNPProfileParameters("LNP 120x80x10", 120, 80, 10, 10, 11, 0, 5.5, 5.5),
    "LNP120x80x12": __LNPProfileParameters("LNP 120x80x12", 120, 80, 12, 12, 11, 0, 5.5, 5.5),
    "LNP130x130x12": __LNPProfileParameters("LNP 130x130x12", 130, 130, 12, 12, 14, 0, 7, 7),
    "LNP130x65x8": __LNPProfileParameters("LNP 130x65x8", 130, 65, 8, 8, 11, 0, 5.5, 5.5),
    "LNP130x65x10": __LNPProfileParameters("LNP 130x65x10", 130, 65, 10, 10, 11, 0, 5.5, 5.5),
    "LNP130x65x12": __LNPProfileParameters("LNP 130x65x12", 130, 65, 12, 12, 11, 0, 5.5, 5.5),
    "LNP140x140x13": __LNPProfileParameters("LNP 140x140x13", 140, 140, 13, 13, 15, 0, 7.5, 7.5),
    "LNP140x140x15": __LNPProfileParameters("LNP 140x140x15", 140, 140, 15, 15, 15, 0, 7.5, 7.5),
    "LNP150x150x14": __LNPProfileParameters("LNP 150x150x14", 150, 150, 14, 14, 16, 0, 8, 8),
    "LNP150x150x16": __LNPProfileParameters("LNP 150x150x16", 150, 150, 16, 16, 16, 0, 8, 8),
    "LNP150x75x9": __LNPProfileParameters("LNP 150x75x9", 150, 75, 9, 9, 12, 0, 6, 6),
    "LNP150x75x11": __LNPProfileParameters("LNP 150x75x11", 150, 75, 11, 11, 10.5, 0, 5.5, 5.5),
    "LNP150x100x10": __LNPProfileParameters("LNP 150x100x10", 150, 100, 10, 10, 12, 0, 6, 6),
    "LNP150x100x12": __LNPProfileParameters("LNP 150x100x12", 150, 100, 12, 12, 12, 0, 6, 6),
    "LNP150x100x14": __LNPProfileParameters("LNP 150x100x14", 150, 100, 14, 14, 13, 0, 6.5, 6.5),
    "LNP160x160x15": __LNPProfileParameters("LNP 160x160x15", 160, 160, 15, 15, 17, 0, 8.5, 8.5),
    "LNP160x160x17": __LNPProfileParameters("LNP 160x160x17", 160, 160, 17, 17, 17, 0, 8.5, 8.5),
    "LNP160x160x20": __LNPProfileParameters("LNP 160x160x20", 160, 160, 20, 20, 17, 0, 8.5, 8.5),
    "LNP160x80x10": __LNPProfileParameters("LNP 160x80x10", 160, 80, 10, 10, 13, 0, 6.5, 6.5),
    "LNP160x80x12": __LNPProfileParameters("LNP 160x80x12", 160, 80, 12, 12, 13, 0, 6.5, 6.5),
    "LNP160x80x14": __LNPProfileParameters("LNP 160x80x14", 160, 80, 14, 14, 13, 0, 6.5, 6.5),
    "LNP180x180x16": __LNPProfileParameters("LNP 180x180x16", 180, 180, 16, 16, 18, 0, 9, 9),
    "LNP180x180x18": __LNPProfileParameters("LNP 180x180x18", 180, 180, 18, 18, 18, 0, 9, 9),
    "LNP180x180x20": __LNPProfileParameters("LNP 180x180x20", 180, 180, 20, 20, 18, 0, 9, 9),
    "LNP200x200x16": __LNPProfileParameters("LNP 200x200x16", 200, 200, 16, 16, 18, 0, 9, 9),
    "LNP200x200x18": __LNPProfileParameters("LNP 200x200x18", 200, 200, 18, 18, 18, 0, 9, 9),
    "LNP200x200x20": __LNPProfileParameters("LNP 200x200x20", 200, 200, 20, 20, 18, 0, 9, 9),
    "LNP200x200x22": __LNPProfileParameters("LNP 200x200x22", 200, 200, 22, 22, 18, 0, 9, 9),
    "LNP200x200x24": __LNPProfileParameters("LNP 200x200x24", 200, 200, 24, 24, 18, 0, 9, 9),
    "LNP200x200x26": __LNPProfileParameters("LNP 200x200x26", 200, 200, 26, 26, 18, 0, 9, 9),
    "LNP200x100x10": __LNPProfileParameters("LNP 200x100x10", 200, 100, 10, 10, 15, 0, 7.5, 7.5),
    "LNP200x100x12": __LNPProfileParameters("LNP 200x100x12", 200, 100, 12, 12, 15, 0, 7.5, 7.5),
    "LNP200x100x14": __LNPProfileParameters("LNP 200x100x14", 200, 100, 14, 14, 15, 0, 7.5, 7.5),
    "LNP200x100x16": __LNPProfileParameters("LNP 200x100x16", 200, 100, 16, 16, 15, 0, 7.5, 7.5),
}


class LNP(metaclass=StandardProfileMeta):
    r"""Geometrical representation of LNP steel profiles.

                       ↓-- Web thickness
                      ┌──\ <-- Toe radius
                      │  │
                      │  │
                      │  │
                      │  │
        Height -----> │   \ <-- Root radius
                      │    \_____
                      │          \ <-- Base thickness
                      └───────────┘
                          ^ Width


    The horizontal leg is at the top, the vertical leg descends from the left.

    This class provides access to standard LNP profiles from a predefined database.
    Profiles can be accessed as class attributes using their standardized names.
    Each accessed profile returns a LNPProfile instance.

    Usage example
    -------------
        >>> profile = LNP.LNP40x40x4
        >>> print(isinstance(profile, LNPProfile))  # True
        >>>
        >>> # To iterate over all available LNP profiles:
        >>> for profile in LNP:
        ...     print(isinstance(profile, LNPProfile))  # True
    """

    _factory = LNPProfile
    """Factory class for creating standard LNP profiles."""
    _database = LNP_PROFILES_DATABASE
    """Database of standard LNP profile parameters."""
