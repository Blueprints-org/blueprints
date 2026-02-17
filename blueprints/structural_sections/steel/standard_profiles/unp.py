"""UNP Steel Profiles."""

from typing import NamedTuple

from blueprints.structural_sections.steel.profile_definitions.unp_profile import UNPProfile
from blueprints.structural_sections.steel.standard_profiles.utils import StandardProfileMeta
from blueprints.type_alias import MM, PERCENTAGE


class __UNPProfileParameters(NamedTuple):
    """Parameters for defining a UNP profile."""

    name: str
    top_flange_total_width: MM
    top_flange_thickness: MM
    bottom_flange_total_width: MM
    bottom_flange_thickness: MM
    total_height: MM
    web_thickness: MM
    top_root_fillet_radius: MM
    bottom_root_fillet_radius: MM
    top_toe_radius: MM
    bottom_toe_radius: MM
    top_slope: PERCENTAGE
    bottom_slope: PERCENTAGE


UNP_PROFILES_DATABASE = {
    "UNP80": __UNPProfileParameters("UNP80", 45, 8, 45, 8, 80, 6, 8, 8, 4, 4, 8, 8),
    "UNP100": __UNPProfileParameters("UNP100", 50, 8.5, 50, 8.5, 100, 6, 8.5, 8.5, 4.5, 4.5, 8, 8),
    "UNP120": __UNPProfileParameters("UNP120", 55, 9, 55, 9, 120, 7, 9, 9, 4.5, 4.5, 8, 8),
    "UNP140": __UNPProfileParameters("UNP140", 60, 10, 60, 10, 140, 7, 10, 10, 5, 5, 8, 8),
    "UNP160": __UNPProfileParameters("UNP160", 65, 10.5, 65, 10.5, 160, 7.5, 10.5, 10.5, 5.5, 5.5, 8, 8),
    "UNP180": __UNPProfileParameters("UNP180", 70, 11, 70, 11, 180, 8, 11, 11, 5.5, 5.5, 8, 8),
    "UNP200": __UNPProfileParameters("UNP200", 75, 11.5, 75, 11.5, 200, 8.5, 11.5, 11.5, 6, 6, 8, 8),
    "UNP220": __UNPProfileParameters("UNP220", 80, 12.5, 80, 12.5, 220, 9, 12.5, 12.5, 6.5, 6.5, 8, 8),
    "UNP240": __UNPProfileParameters("UNP240", 85, 13, 85, 13, 240, 9.5, 13, 13, 6.5, 6.5, 8, 8),
    "UNP260": __UNPProfileParameters("UNP260", 90, 14, 90, 14, 260, 10, 14, 14, 7, 7, 8, 8),
    "UNP280": __UNPProfileParameters("UNP280", 95, 15, 95, 15, 280, 10, 15, 15, 7.5, 7.5, 8, 8),
    "UNP300": __UNPProfileParameters("UNP300", 100, 16, 100, 16, 300, 10, 16, 16, 8, 8, 8, 8),
    "UNP320": __UNPProfileParameters("UNP320", 100, 17.5, 100, 17.5, 320, 14, 17.5, 17.5, 8.75, 8.75, 5, 5),
    "UNP350": __UNPProfileParameters("UNP350", 100, 16, 100, 16, 350, 14, 16, 16, 8, 8, 5, 5),
    "UNP380": __UNPProfileParameters("UNP380", 102, 16, 102, 16, 380, 13.5, 16, 16, 8, 8, 5, 5),
    "UNP400": __UNPProfileParameters("UNP400", 110, 18, 110, 18, 400, 14, 18, 18, 9, 9, 5, 5),
}


class UNP(metaclass=StandardProfileMeta):
    """Geometrical representation of UNP profiles.

    This class provides access to standard UNP profiles from a predefined database.
    Profiles can be accessed as class attributes using their standardized names.
    Each accessed profile returns a UNPProfile instance.

    Usage example
    -------------
        >>> profile = UNP.UNP200
        >>> print(isinstance(profile, UNPProfile))  # True
        >>>
        >>> # To iterate over all available UNP profiles:
        >>> for profile in UNP:
        >>>     print(isinstance(profile, UNPProfile))  # True

    """

    _factory = UNPProfile
    """Factory class for creating standard UNP profiles."""
    _database = UNP_PROFILES_DATABASE
    """Database of standard UNP profile parameters."""
