"""Standard PU sheet pile profiles."""

from __future__ import annotations

from typing import NamedTuple

from blueprints.structural_sections.steel.profile_definitions.sheetpile_u_profile import SheetpileUProfile
from blueprints.structural_sections.steel.standard_profiles._data.pu.pu12 import PU12_GEOMETRY
from blueprints.structural_sections.steel.standard_profiles._data.pu.pu18 import PU18_GEOMETRY
from blueprints.structural_sections.steel.standard_profiles._data.pu.pu22 import PU22_GEOMETRY
from blueprints.structural_sections.steel.standard_profiles._data.pu.pu28 import PU28_GEOMETRY
from blueprints.structural_sections.steel.standard_profiles._data.pu.pu32 import PU32_GEOMETRY
from blueprints.structural_sections.steel.standard_profiles.utils import StandardProfileMeta
from blueprints.type_alias import MM


class __PUProfileParameters(NamedTuple):
    """Parameters for defining a PU profile."""

    name: str
    """Name of the PU profile."""
    coordinates: list[tuple[float, float]]
    """List of (x, y) coordinate tuples defining the profile geometry."""
    web_thickness: MM
    """Thickness of the web [mm]."""
    flange_thickness: MM
    """Thickness of the flanges [mm]."""
    interlocking_ctc: MM
    """Center to center distance of the sheets (interlocking distance) [mm]."""


PU_PROFILES_DATABASE = {
    "PU12": __PUProfileParameters("PU 12", PU12_GEOMETRY, 9.0, 9.8, 600),
    "PU18": __PUProfileParameters("PU 18", PU18_GEOMETRY, 9.0, 11.2, 600),
    "PU22": __PUProfileParameters("PU 22", PU22_GEOMETRY, 9.5, 12.1, 600),
    "PU28": __PUProfileParameters("PU 28", PU28_GEOMETRY, 10.1, 15.2, 600),
    "PU32": __PUProfileParameters("PU 32", PU32_GEOMETRY, 11.0, 19.5, 600),
}


class PU(metaclass=StandardProfileMeta):
    """Geometrical representation of standard PU sheet pile profiles.

    PU profiles are a standardized form of U-shaped sheet piles. This class provides
    access to standard PU sheet pile profiles from a predefined database. Profiles
    can be accessed as class attributes using their standardized names. Each accessed
    profile returns a SheetpileUProfile instance.

    Usage example
    -------------
        >>> profile = PU.PU18
        >>> print(isinstance(profile, SheetpileUProfile))  # True
        >>>
        >>> # To iterate over all available PU profiles:
        >>> for profile in PU:
        ...     print(isinstance(profile, SheetpileUProfile))  # True
    """

    _factory = SheetpileUProfile
    _database = PU_PROFILES_DATABASE
