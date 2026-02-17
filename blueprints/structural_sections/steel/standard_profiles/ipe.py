"""IPE Steel Profiles."""

from typing import NamedTuple

from blueprints.structural_sections.steel.profile_definitions.i_profile import IProfile
from blueprints.structural_sections.steel.standard_profiles.utils import StandardProfileMeta
from blueprints.type_alias import MM


class __IPEProfileParameters(NamedTuple):
    """Parameters for defining a IPE profile."""

    name: str
    """Name of the IPE profile."""
    top_flange_width: MM
    """Top flange width of the IPE profile."""
    top_flange_thickness: MM
    """Top flange thickness of the IPE profile."""
    bottom_flange_width: MM
    """Bottom flange width of the IPE profile."""
    bottom_flange_thickness: MM
    """Bottom flange thickness of the IPE profile."""
    total_height: MM
    """Total height of the IPE profile."""
    web_thickness: MM
    """Web thickness of the IPE profile."""
    top_radius: MM
    """Top radius of the IPE profile."""
    bottom_radius: MM
    """Bottom radius of the IPE profile."""


IPE_PROFILES_DATABASE = {
    "IPE80": __IPEProfileParameters("IPE80", 46, 5.2, 46, 5.2, 80, 3.8, 5, 5),
    "IPE100": __IPEProfileParameters("IPE100", 55, 5.7, 55, 5.7, 100, 4.1, 7, 7),
    "IPE120": __IPEProfileParameters("IPE120", 64, 6.3, 64, 6.3, 120, 4.4, 7, 7),
    "IPE140": __IPEProfileParameters("IPE140", 73, 6.9, 73, 6.9, 140, 4.7, 7, 7),
    "IPE160": __IPEProfileParameters("IPE160", 82, 7.4, 82, 7.4, 160, 5.0, 9, 9),
    "IPE180": __IPEProfileParameters("IPE180", 91, 8.0, 91, 8.0, 180, 5.3, 9, 9),
    "IPE200": __IPEProfileParameters("IPE200", 100, 8.5, 100, 8.5, 200, 5.6, 12, 12),
    "IPE220": __IPEProfileParameters("IPE220", 110, 9.2, 110, 9.2, 220, 5.9, 12, 12),
    "IPE240": __IPEProfileParameters("IPE240", 120, 9.8, 120, 9.8, 240, 6.2, 15, 15),
    "IPE270": __IPEProfileParameters("IPE270", 135, 10.2, 135, 10.2, 270, 6.6, 15, 15),
    "IPE300": __IPEProfileParameters("IPE300", 150, 10.7, 150, 10.7, 300, 7.1, 15, 15),
    "IPE330": __IPEProfileParameters("IPE330", 160, 11.5, 160, 11.5, 330, 7.5, 18, 18),
    "IPE360": __IPEProfileParameters("IPE360", 170, 12.7, 170, 12.7, 360, 8.0, 18, 18),
    "IPE400": __IPEProfileParameters("IPE400", 180, 13.5, 180, 13.5, 400, 8.6, 21, 21),
    "IPE450": __IPEProfileParameters("IPE450", 190, 14.6, 190, 14.6, 450, 9.4, 21, 21),
    "IPE500": __IPEProfileParameters("IPE500", 200, 16.0, 200, 16.0, 500, 10.2, 21, 21),
    "IPE550": __IPEProfileParameters("IPE550", 210, 17.2, 210, 17.2, 550, 11.1, 24, 24),
    "IPE600": __IPEProfileParameters("IPE600", 220, 19.0, 220, 19.0, 600, 12.0, 24, 24),
}


class IPE(metaclass=StandardProfileMeta):
    """Geometrical representation of IPE steel profiles.

    This class provides access to standard IPE profiles from a predefined database.
    Profiles can be accessed as class attributes using their standardized names.
    Each accessed profile returns a IProfile instance.

    Usage example
    -------------
        >>> profile = IPE.IPE200
        >>> print(isinstance(profile, IProfile))  # True
        >>>
        >>> # To iterate over all available IPE profiles:
        >>> for profile in IPE:
        >>>     print(isinstance(profile, IProfile))  # True
    """

    _factory = IProfile
    """Factory class for creating standard IPE profiles."""
    _database = IPE_PROFILES_DATABASE
    """Database of standard IPE profile parameters."""
