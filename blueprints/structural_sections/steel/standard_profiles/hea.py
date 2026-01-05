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
    "HEA100": __HEAProfileParameters("HEA100", 96, 8, 96, 8, 100, 5, 12, 12),
    "HEA120": __HEAProfileParameters("HEA120", 114, 8, 114, 8, 120, 5, 12, 12),
    "HEA140": __HEAProfileParameters("HEA140", 133, 8.5, 133, 8.5, 140, 5.5, 12, 12),
    "HEA160": __HEAProfileParameters("HEA160", 152, 9, 152, 9, 160, 6, 15, 15),
    "HEA180": __HEAProfileParameters("HEA180", 171, 9.5, 171, 9.5, 180, 6, 15, 15),
    "HEA200": __HEAProfileParameters("HEA200", 190, 10, 190, 10, 200, 6.5, 18, 18),
    "HEA220": __HEAProfileParameters("HEA220", 210, 11, 210, 11, 220, 7, 18, 18),
    "HEA240": __HEAProfileParameters("HEA240", 230, 12, 230, 12, 240, 7.5, 21, 21),
    "HEA260": __HEAProfileParameters("HEA260", 250, 12.5, 250, 12.5, 260, 7.5, 24, 24),
    "HEA280": __HEAProfileParameters("HEA280", 270, 13, 270, 13, 280, 8, 24, 24),
    "HEA300": __HEAProfileParameters("HEA300", 290, 14, 290, 14, 300, 8.5, 27, 27),
    "HEA320": __HEAProfileParameters("HEA320", 310, 15.5, 310, 15.5, 320, 9, 27, 27),
    "HEA340": __HEAProfileParameters("HEA340", 330, 16.5, 330, 16.5, 340, 9.5, 27, 27),
    "HEA360": __HEAProfileParameters("HEA360", 350, 17.5, 350, 17.5, 360, 10, 27, 27),
    "HEA400": __HEAProfileParameters("HEA400", 390, 19, 390, 19, 400, 11, 27, 27),
    "HEA450": __HEAProfileParameters("HEA450", 440, 21, 440, 21, 450, 11.5, 27, 27),
    "HEA500": __HEAProfileParameters("HEA500", 490, 23, 490, 23, 500, 12, 27, 27),
    "HEA550": __HEAProfileParameters("HEA550", 540, 24, 540, 24, 550, 12.5, 27, 27),
    "HEA600": __HEAProfileParameters("HEA600", 590, 25, 590, 25, 600, 13, 27, 27),
    "HEA650": __HEAProfileParameters("HEA650", 640, 26, 640, 26, 650, 13.5, 27, 27),
    "HEA700": __HEAProfileParameters("HEA700", 690, 27, 690, 27, 700, 14.5, 27, 27),
    "HEA800": __HEAProfileParameters("HEA800", 790, 28, 790, 28, 800, 15, 30, 30),
    "HEA900": __HEAProfileParameters("HEA900", 890, 30, 890, 30, 900, 16, 30, 30),
    "HEA1000": __HEAProfileParameters("HEA1000", 990, 31, 990, 31, 1000, 16.5, 30, 30),
}


class HEA(metaclass=StandardProfileMeta):
    """Geometrical representation of HEA steel profiles.

    This class provides access to standard HEA profiles from a predefined database.
    Profiles can be accessed as class attributes using their standardized names.
    Each accessed profile returns a IProfile instance.

    Usage example
    -------------
        >>> profile = HEA.HEA200
    """

    _factory = IProfile
    """Factory class for creating standard HEA profiles."""
    _database = HEA_PROFILES_DATABASE
    """Database of standard HEA profile parameters."""
