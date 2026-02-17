"""HEB Steel Profiles."""

from typing import NamedTuple

from blueprints.structural_sections.steel.profile_definitions.i_profile import IProfile
from blueprints.structural_sections.steel.standard_profiles.utils import StandardProfileMeta
from blueprints.type_alias import MM


class __HEBProfileParameters(NamedTuple):
    """Parameters for defining a HEB profile."""

    name: str
    """Name of the HEB profile."""
    top_flange_width: MM
    """Top flange width of the HEB profile."""
    top_flange_thickness: MM
    """Top flange thickness of the HEB profile."""
    bottom_flange_width: MM
    """Bottom flange width of the HEB profile."""
    bottom_flange_thickness: MM
    """Bottom flange thickness of the HEB profile."""
    total_height: MM
    """Total height of the HEB profile."""
    web_thickness: MM
    """Web thickness of the HEB profile."""
    top_radius: MM
    """Top radius of the HEB profile."""
    bottom_radius: MM
    """Bottom radius of the HEB profile."""


HEB_PROFILES_DATABASE = {
    "HEB100": __HEBProfileParameters("HEB100", 100, 10, 100, 10, 100, 6, 12, 12),
    "HEB120": __HEBProfileParameters("HEB120", 120, 11, 120, 11, 120, 6.5, 12, 12),
    "HEB140": __HEBProfileParameters("HEB140", 140, 12, 140, 12, 140, 7, 12, 12),
    "HEB160": __HEBProfileParameters("HEB160", 160, 13, 160, 13, 160, 8, 15, 15),
    "HEB180": __HEBProfileParameters("HEB180", 180, 14, 180, 14, 180, 8.5, 15, 15),
    "HEB200": __HEBProfileParameters("HEB200", 200, 15, 200, 15, 200, 9, 18, 18),
    "HEB220": __HEBProfileParameters("HEB220", 220, 16, 220, 16, 220, 9.5, 18, 18),
    "HEB240": __HEBProfileParameters("HEB240", 240, 17, 240, 17, 240, 10, 21, 21),
    "HEB260": __HEBProfileParameters("HEB260", 260, 17.5, 260, 17.5, 260, 10, 24, 24),
    "HEB280": __HEBProfileParameters("HEB280", 280, 18, 280, 18, 280, 10.5, 24, 24),
    "HEB300": __HEBProfileParameters("HEB300", 300, 19, 300, 19, 300, 11, 27, 27),
    "HEB320": __HEBProfileParameters("HEB320", 300, 20.5, 300, 20.5, 320, 11.5, 27, 27),
    "HEB340": __HEBProfileParameters("HEB340", 300, 21.5, 300, 21.5, 340, 12, 27, 27),
    "HEB360": __HEBProfileParameters("HEB360", 300, 22.5, 300, 22.5, 360, 12.5, 27, 27),
    "HEB400": __HEBProfileParameters("HEB400", 300, 24, 300, 24, 400, 13.5, 27, 27),
    "HEB450": __HEBProfileParameters("HEB450", 300, 26, 300, 26, 450, 14, 27, 27),
    "HEB500": __HEBProfileParameters("HEB500", 300, 28, 300, 28, 500, 14.5, 27, 27),
    "HEB550": __HEBProfileParameters("HEB550", 300, 29, 300, 29, 550, 15, 27, 27),
    "HEB600": __HEBProfileParameters("HEB600", 300, 30, 300, 30, 600, 15.5, 27, 27),
    "HEB650": __HEBProfileParameters("HEB650", 300, 31, 300, 31, 650, 16, 27, 27),
    "HEB700": __HEBProfileParameters("HEB700", 300, 32, 300, 32, 700, 17, 27, 27),
    "HEB800": __HEBProfileParameters("HEB800", 300, 33, 300, 33, 800, 17.5, 30, 30),
    "HEB900": __HEBProfileParameters("HEB900", 300, 35, 300, 35, 900, 18.5, 30, 30),
    "HEB1000": __HEBProfileParameters("HEB1000", 300, 36, 300, 36, 1000, 19, 30, 30),
}


class HEB(metaclass=StandardProfileMeta):
    """Geometrical representation of HEB steel profiles.

    This class provides access to standard HEB profiles from a predefined database.
    Profiles can be accessed as class attributes using their standardized names.
    Each accessed profile returns a IProfile instance.

    Usage example
    -------------
        >>> profile = HEB.HEB200
        >>> print(isinstance(profile, IProfile))  # True
        >>>
        >>> # To iterate over all available HEB profiles:
        >>> for profile in HEB:
        >>>     print(isinstance(profile, IProfile))  # True
    """

    _factory = IProfile
    """Factory class for creating standard HEB profiles."""
    _database = HEB_PROFILES_DATABASE
    """Database of standard HEB profile parameters."""
