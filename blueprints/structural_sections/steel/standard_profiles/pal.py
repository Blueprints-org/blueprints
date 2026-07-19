"""Standard PAL sheet pile profiles."""

from __future__ import annotations

from typing import NamedTuple

from blueprints.structural_sections.steel.profile_definitions.sheetpile_u_profile import SheetpileUProfile
from blueprints.structural_sections.steel.standard_profiles._data.pal.pal3030 import PAL3030_GEOMETRY
from blueprints.structural_sections.steel.standard_profiles._data.pal.pal3040 import PAL3040_GEOMETRY
from blueprints.structural_sections.steel.standard_profiles._data.pal.pal3050 import PAL3050_GEOMETRY
from blueprints.structural_sections.steel.standard_profiles._data.pal.pal3130 import PAL3130_GEOMETRY
from blueprints.structural_sections.steel.standard_profiles._data.pal.pal3140 import PAL3140_GEOMETRY
from blueprints.structural_sections.steel.standard_profiles._data.pal.pal3150 import PAL3150_GEOMETRY
from blueprints.structural_sections.steel.standard_profiles.utils import StandardProfileMeta
from blueprints.type_alias import MM


class __PALProfileParameters(NamedTuple):
    """Parameters for defining a PAL profile."""

    name: str
    """Name of the PAL profile."""
    coordinates: list[tuple[float, float]]
    """List of (x, y) coordinate tuples defining the profile geometry."""
    web_thickness: MM
    """Thickness of the web [mm]."""
    flange_thickness: MM
    """Thickness of the flanges [mm]."""
    interlocking_ctc: MM
    """Center to center distance of the sheets (interlocking distance) [mm]."""


PAL_PROFILES_DATABASE = {
    "PAL3030": __PALProfileParameters("PAL 30-30", PAL3030_GEOMETRY, 3.0, 3.0, 660),
    "PAL3040": __PALProfileParameters("PAL 30-40", PAL3040_GEOMETRY, 4.0, 4.0, 660),
    "PAL3050": __PALProfileParameters("PAL 30-50", PAL3050_GEOMETRY, 5.0, 5.0, 660),
    "PAL3130": __PALProfileParameters("PAL 31-30", PAL3130_GEOMETRY, 3.0, 3.0, 711),
    "PAL3140": __PALProfileParameters("PAL 31-40", PAL3140_GEOMETRY, 4.0, 4.0, 711),
    "PAL3150": __PALProfileParameters("PAL 31-50", PAL3150_GEOMETRY, 5.0, 5.0, 711),
}


class PAL(metaclass=StandardProfileMeta):
    """Geometrical representation of standard PAL sheet pile profiles.

    PAL profiles are a standardized form of large U-shaped sheet piles. This class provides
    access to standard PAL sheet pile profiles from a predefined database. Profiles
    can be accessed as class attributes using their standardized names. Each accessed
    profile returns a SheetpileUProfile instance.

    Usage example
    -------------
        >>> profile = PAL.PAL3040
        >>> print(isinstance(profile, SheetpileUProfile))  # True
        >>>
        >>> # To iterate over all available PAL profiles:
        >>> for profile in PAL:
        ...     print(isinstance(profile, SheetpileUProfile))  # True
    """

    _factory = SheetpileUProfile
    _database = PAL_PROFILES_DATABASE
