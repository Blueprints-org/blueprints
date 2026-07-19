"""Standard AU sheet pile profiles."""

from __future__ import annotations

from typing import NamedTuple

from blueprints.structural_sections.steel.profile_definitions.sheetpile_u_profile import SheetpileUProfile
from blueprints.structural_sections.steel.standard_profiles._data.au.au14 import AU14_GEOMETRY
from blueprints.structural_sections.steel.standard_profiles._data.au.au16 import AU16_GEOMETRY
from blueprints.structural_sections.steel.standard_profiles._data.au.au18 import AU18_GEOMETRY
from blueprints.structural_sections.steel.standard_profiles._data.au.au20 import AU20_GEOMETRY
from blueprints.structural_sections.steel.standard_profiles._data.au.au23 import AU23_GEOMETRY
from blueprints.structural_sections.steel.standard_profiles._data.au.au25 import AU25_GEOMETRY
from blueprints.structural_sections.steel.standard_profiles.utils import StandardProfileMeta
from blueprints.type_alias import MM


class __AUProfileParameters(NamedTuple):
    """Parameters for defining an AU profile."""

    name: str
    """Name of the AU profile."""
    coordinates: list[tuple[float, float]]
    """List of (x, y) coordinate tuples defining the profile geometry."""
    web_thickness: MM
    """Thickness of the web [mm]."""
    flange_thickness: MM
    """Thickness of the flanges [mm]."""
    interlocking_ctc: MM
    """Center to center distance of the sheets (interlocking distance) [mm]."""


AU_PROFILES_DATABASE = {
    "AU14": __AUProfileParameters("AU 14", AU14_GEOMETRY, 8.3, 10.0, 750),
    "AU16": __AUProfileParameters("AU 16", AU16_GEOMETRY, 9.3, 11.5, 750),
    "AU18": __AUProfileParameters("AU 18", AU18_GEOMETRY, 9.1, 10.5, 750),
    "AU20": __AUProfileParameters("AU 20", AU20_GEOMETRY, 10.0, 12.0, 750),
    "AU23": __AUProfileParameters("AU 23", AU23_GEOMETRY, 9.5, 13.0, 750),
    "AU25": __AUProfileParameters("AU 25", AU25_GEOMETRY, 10.2, 14.5, 750),
}


class AU(metaclass=StandardProfileMeta):
    """Geometrical representation of standard AU sheet pile profiles.

    AU profiles are a standardized form of U-shaped sheet piles. This class provides
    access to standard AU sheet pile profiles from a predefined database. Profiles
    can be accessed as class attributes using their standardized names. Each accessed
    profile returns a SheetpileUProfile instance.

    Usage example
    -------------
        >>> profile = AU.AU18
        >>> print(isinstance(profile, SheetpileUProfile))  # True
        >>>
        >>> # To iterate over all available AU profiles:
        >>> for profile in AU:
        ...     print(isinstance(profile, SheetpileUProfile))  # True
    """

    _factory = SheetpileUProfile
    _database = AU_PROFILES_DATABASE
