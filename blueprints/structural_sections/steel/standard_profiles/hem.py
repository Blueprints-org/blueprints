"""HEM Steel Profiles."""

from typing import NamedTuple

from blueprints.structural_sections.steel.profile_definitions.i_profile import IProfile
from blueprints.structural_sections.steel.standard_profiles.utils import StandardProfileMeta
from blueprints.type_alias import MM


class __HEMProfileParameters(NamedTuple):
    """Parameters for defining a HEM profile."""

    name: str
    """Name of the HEM profile."""
    top_flange_width: MM
    """Top flange width of the HEM profile."""
    top_flange_thickness: MM
    """Top flange thickness of the HEM profile."""
    bottom_flange_width: MM
    """Bottom flange width of the HEM profile."""
    bottom_flange_thickness: MM
    """Bottom flange thickness of the HEM profile."""
    total_height: MM
    """Total height of the HEM profile."""
    web_thickness: MM
    """Web thickness of the HEM profile."""
    top_radius: MM
    """Top radius of the HEM profile."""
    bottom_radius: MM
    """Bottom radius of the HEM profile."""


HEM_PROFILES_DATABASE = {
    "HEM100": __HEMProfileParameters("HEM100", 106, 20, 106, 20, 120, 12, 12, 12),
    "HEM120": __HEMProfileParameters("HEM120", 126, 21, 126, 21, 140, 12.5, 12, 12),
    "HEM140": __HEMProfileParameters("HEM140", 146, 22, 146, 22, 160, 13, 12, 12),
    "HEM160": __HEMProfileParameters("HEM160", 166, 23, 166, 23, 180, 14, 15, 15),
    "HEM180": __HEMProfileParameters("HEM180", 186, 24, 186, 24, 200, 14.5, 15, 15),
    "HEM200": __HEMProfileParameters("HEM200", 206, 25, 206, 25, 220, 15, 18, 18),
    "HEM220": __HEMProfileParameters("HEM220", 226, 26, 226, 26, 240, 15.5, 18, 18),
    "HEM240": __HEMProfileParameters("HEM240", 248, 32, 248, 32, 270, 18, 21, 21),
    "HEM260": __HEMProfileParameters("HEM260", 268, 32.5, 268, 32.5, 290, 18, 24, 24),
    "HEM280": __HEMProfileParameters("HEM280", 288, 39, 288, 39, 310, 18.5, 24, 24),
    "HEM300": __HEMProfileParameters("HEM300", 310, 39, 310, 39, 340, 21, 27, 27),
    "HEM320": __HEMProfileParameters("HEM320", 309, 40, 309, 40, 359, 21, 27, 27),
    "HEM340": __HEMProfileParameters("HEM340", 309, 40, 309, 40, 377, 21, 27, 27),
    "HEM360": __HEMProfileParameters("HEM360", 308, 40, 308, 40, 395, 21, 27, 27),
    "HEM400": __HEMProfileParameters("HEM400", 307, 40, 307, 40, 432, 21, 27, 27),
    "HEM450": __HEMProfileParameters("HEM450", 307, 40, 307, 40, 478, 21, 27, 27),
    "HEM500": __HEMProfileParameters("HEM500", 306, 40, 306, 40, 524, 21, 27, 27),
    "HEM550": __HEMProfileParameters("HEM550", 306, 40, 306, 40, 572, 21, 27, 27),
    "HEM600": __HEMProfileParameters("HEM600", 305, 40, 305, 40, 620, 21, 27, 27),
    "HEM650": __HEMProfileParameters("HEM650", 305, 40, 305, 40, 668, 21, 27, 27),
    "HEM700": __HEMProfileParameters("HEM700", 304, 40, 304, 40, 716, 21, 27, 27),
    "HEM800": __HEMProfileParameters("HEM800", 303, 40, 303, 40, 814, 21, 30, 30),
    "HEM900": __HEMProfileParameters("HEM900", 302, 40, 302, 40, 910, 21, 30, 30),
    "HEM1000": __HEMProfileParameters("HEM1000", 302, 40, 302, 40, 1008, 21, 30, 30),
}


class HEM(metaclass=StandardProfileMeta):
    """Geometrical representation of HEM steel profiles.

    This class provides access to standard HEM profiles from a predefined database.
    Profiles can be accessed as class attributes using their standardized names.
    Each accessed profile returns a IProfile instance.

    Usage example
    -------------
        >>> profile = HEM.HEM200
        >>> print(isinstance(profile, IProfile))  # True
        >>>
        >>> # To iterate over all available HEM profiles:
        >>> for profile in HEM:
        >>>     print(isinstance(profile, IProfile))  # True
    """

    _factory = IProfile
    """Factory class for creating standard HEM profiles."""
    _database = HEM_PROFILES_DATABASE
    """Database of standard HEM profile parameters."""
