"""Standard PAU sheet pile profiles."""

from __future__ import annotations

from typing import NamedTuple

from blueprints.structural_sections.steel.profile_definitions.sheetpile_u_profile import SheetpileUProfile
from blueprints.structural_sections.steel.standard_profiles._data.pau.pau2240 import PAU2240_GEOMETRY
from blueprints.structural_sections.steel.standard_profiles._data.pau.pau2250 import PAU2250_GEOMETRY
from blueprints.structural_sections.steel.standard_profiles._data.pau.pau2260 import PAU2260_GEOMETRY
from blueprints.structural_sections.steel.standard_profiles._data.pau.pau2440 import PAU2440_GEOMETRY
from blueprints.structural_sections.steel.standard_profiles._data.pau.pau2450 import PAU2450_GEOMETRY
from blueprints.structural_sections.steel.standard_profiles._data.pau.pau2460 import PAU2460_GEOMETRY
from blueprints.structural_sections.steel.standard_profiles._data.pau.pau2770 import PAU2770_GEOMETRY
from blueprints.structural_sections.steel.standard_profiles._data.pau.pau2780 import PAU2780_GEOMETRY
from blueprints.structural_sections.steel.standard_profiles.utils import StandardProfileMeta
from blueprints.type_alias import MM


class __PAUProfileParameters(NamedTuple):
    """Parameters for defining a PAU profile."""

    name: str
    """Name of the PAU profile."""
    coordinates: list[tuple[float, float]]
    """List of (x, y) coordinate tuples defining the profile geometry."""
    web_thickness: MM
    """Thickness of the web [mm]."""
    flange_thickness: MM
    """Thickness of the flanges [mm]."""
    interlocking_ctc: MM
    """Center to center distance of the sheets (interlocking distance) [mm]."""


PAU_PROFILES_DATABASE = {
    "PAU2240": __PAUProfileParameters("PAU 22-40", PAU2240_GEOMETRY, 4.0, 4.0, 922),
    "PAU2250": __PAUProfileParameters("PAU 22-50", PAU2250_GEOMETRY, 5.0, 5.0, 921),
    "PAU2260": __PAUProfileParameters("PAU 22-60", PAU2260_GEOMETRY, 6.0, 6.0, 921),
    "PAU2440": __PAUProfileParameters("PAU 24-40", PAU2440_GEOMETRY, 4.0, 4.0, 813),
    "PAU2450": __PAUProfileParameters("PAU 24-50", PAU2450_GEOMETRY, 5.0, 5.0, 813),
    "PAU2460": __PAUProfileParameters("PAU 24-60", PAU2460_GEOMETRY, 6.0, 6.0, 813),
    "PAU2770": __PAUProfileParameters("PAU 27-70", PAU2770_GEOMETRY, 7.0, 7.0, 804),
    "PAU2780": __PAUProfileParameters("PAU 27-80", PAU2780_GEOMETRY, 8.0, 8.0, 804),
}


class PAU(metaclass=StandardProfileMeta):
    """Geometrical representation of standard PAU sheet pile profiles.

    PAU profiles are a standardized form of combined U-shaped sheet piles. This class provides
    access to standard PAU sheet pile profiles from a predefined database. Profiles
    can be accessed as class attributes using their standardized names. Each accessed
    profile returns a SheetpileUProfile instance.

    Usage example
    -------------
        >>> profile = PAU.PAU2450
        >>> print(isinstance(profile, SheetpileUProfile))  # True
        >>>
        >>> # To iterate over all available PAU profiles:
        >>> for profile in PAU:
        ...     print(isinstance(profile, SheetpileUProfile))  # True
    """

    _factory = SheetpileUProfile
    _database = PAU_PROFILES_DATABASE
