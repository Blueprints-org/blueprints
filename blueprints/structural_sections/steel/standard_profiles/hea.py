"""HEA Steel Profiles."""

from typing import NamedTuple

from blueprints.structural_sections.steel.profile_definitions.i_profile import IProfile
from blueprints.structural_sections.steel.standard_profiles.utils import StandardProfileMeta
from blueprints.type_alias import MM


class __HEAProfileParameters(NamedTuple):
    """Parameters for defining a HEA profile."""

    name: str
    """Name of the HEA profile."""
    top_flange_width: MM
    """Top flange width of the HEA profile."""
    top_flange_thickness: MM
    """Top flange thickness of the HEA profile."""
    bottom_flange_width: MM
    """Bottom flange width of the HEA profile."""
    bottom_flange_thickness: MM
    """Bottom flange thickness of the HEA profile."""
    total_height: MM
    """Total height of the HEA profile."""
    web_thickness: MM
    """Web thickness of the HEA profile."""
    top_radius: MM
    """Top radius of the HEA profile."""
    bottom_radius: MM
    """Bottom radius of the HEA profile."""


HEA_PROFILES_DATABASE = {
    "HEA100": __HEAProfileParameters("HEA100", 100, 8, 100, 8, 96, 5, 12, 12),
    "HEA120": __HEAProfileParameters("HEA120", 120, 8, 120, 8, 114, 5, 12, 12),
    "HEA140": __HEAProfileParameters("HEA140", 140, 8.5, 140, 8.5, 133, 5.5, 12, 12),
    "HEA160": __HEAProfileParameters("HEA160", 160, 9, 160, 9, 152, 6, 15, 15),
    "HEA180": __HEAProfileParameters("HEA180", 180, 9.5, 180, 9.5, 171, 6, 15, 15),
    "HEA200": __HEAProfileParameters("HEA200", 200, 10, 200, 10, 190, 6.5, 18, 18),
    "HEA220": __HEAProfileParameters("HEA220", 220, 11, 220, 11, 210, 7, 18, 18),
    "HEA240": __HEAProfileParameters("HEA240", 240, 12, 240, 12, 230, 7.5, 21, 21),
    "HEA260": __HEAProfileParameters("HEA260", 260, 12.5, 260, 12.5, 250, 7.5, 24, 24),
    "HEA280": __HEAProfileParameters("HEA280", 280, 13, 280, 13, 270, 8, 24, 24),
    "HEA300": __HEAProfileParameters("HEA300", 300, 14, 300, 14, 290, 8.5, 27, 27),
    "HEA320": __HEAProfileParameters("HEA320", 300, 15.5, 300, 15.5, 310, 9, 27, 27),
    "HEA340": __HEAProfileParameters("HEA340", 300, 16.5, 300, 16.5, 330, 9.5, 27, 27),
    "HEA360": __HEAProfileParameters("HEA360", 300, 17.5, 300, 17.5, 350, 10, 27, 27),
    "HEA400": __HEAProfileParameters("HEA400", 300, 19, 300, 19, 390, 11, 27, 27),
    "HEA450": __HEAProfileParameters("HEA450", 300, 21, 300, 21, 440, 11.5, 27, 27),
    "HEA500": __HEAProfileParameters("HEA500", 300, 23, 300, 23, 490, 12, 27, 27),
    "HEA550": __HEAProfileParameters("HEA550", 300, 24, 300, 24, 540, 12.5, 27, 27),
    "HEA600": __HEAProfileParameters("HEA600", 300, 25, 300, 25, 590, 13, 27, 27),
    "HEA650": __HEAProfileParameters("HEA650", 300, 26, 300, 26, 640, 13.5, 27, 27),
    "HEA700": __HEAProfileParameters("HEA700", 300, 27, 300, 27, 690, 14.5, 27, 27),
    "HEA800": __HEAProfileParameters("HEA800", 300, 28, 300, 28, 790, 15, 30, 30),
    "HEA900": __HEAProfileParameters("HEA900", 300, 30, 300, 30, 890, 16, 30, 30),
    "HEA1000": __HEAProfileParameters("HEA1000", 300, 31, 300, 31, 990, 16.5, 30, 30),
}


class HEA(metaclass=StandardProfileMeta):
    """Geometrical representation of HEA steel profiles.

    This class provides access to standard HEA profiles from a predefined database.
    Profiles can be accessed as class attributes using their standardized names.
    Each accessed profile returns an IProfile instance.

    Usage example
    -------------
        >>> profile = HEA.HEA200
        >>> print(isinstance(profile, IProfile))  # True
        >>>
        >>> # To iterate over all available HEA profiles:
        >>> for profile in HEA:
        ...     print(isinstance(profile, IProfile))  # True
    """

    _factory = IProfile
    """Factory class for creating standard HEA profiles."""
    _database = HEA_PROFILES_DATABASE
    """Database of standard HEA profile parameters."""
