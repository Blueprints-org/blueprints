"""Standard GU sheet pile profiles."""

from __future__ import annotations

from typing import NamedTuple

from blueprints.structural_sections.steel.profile_definitions.sheetpile_u_profile import SheetpileUProfile
from blueprints.structural_sections.steel.standard_profiles._data.gu.gu6 import GU6_GEOMETRY
from blueprints.structural_sections.steel.standard_profiles._data.gu.gu7 import GU7_GEOMETRY
from blueprints.structural_sections.steel.standard_profiles._data.gu.gu8 import GU8_GEOMETRY
from blueprints.structural_sections.steel.standard_profiles._data.gu.gu10 import GU10_GEOMETRY
from blueprints.structural_sections.steel.standard_profiles._data.gu.gu11 import GU11_GEOMETRY
from blueprints.structural_sections.steel.standard_profiles._data.gu.gu12 import GU12_GEOMETRY
from blueprints.structural_sections.steel.standard_profiles._data.gu.gu13 import GU13_GEOMETRY
from blueprints.structural_sections.steel.standard_profiles._data.gu.gu14 import GU14_GEOMETRY
from blueprints.structural_sections.steel.standard_profiles._data.gu.gu15 import GU15_GEOMETRY
from blueprints.structural_sections.steel.standard_profiles._data.gu.gu16 import GU16_GEOMETRY
from blueprints.structural_sections.steel.standard_profiles._data.gu.gu18 import GU18_GEOMETRY
from blueprints.structural_sections.steel.standard_profiles._data.gu.gu18_400 import GU18_400_GEOMETRY
from blueprints.structural_sections.steel.standard_profiles._data.gu.gu20 import GU20_GEOMETRY
from blueprints.structural_sections.steel.standard_profiles._data.gu.gu21 import GU21_GEOMETRY
from blueprints.structural_sections.steel.standard_profiles._data.gu.gu22 import GU22_GEOMETRY
from blueprints.structural_sections.steel.standard_profiles._data.gu.gu23 import GU23_GEOMETRY
from blueprints.structural_sections.steel.standard_profiles._data.gu.gu27 import GU27_GEOMETRY
from blueprints.structural_sections.steel.standard_profiles._data.gu.gu28 import GU28_GEOMETRY
from blueprints.structural_sections.steel.standard_profiles._data.gu.gu30 import GU30_GEOMETRY
from blueprints.structural_sections.steel.standard_profiles._data.gu.gu31 import GU31_GEOMETRY
from blueprints.structural_sections.steel.standard_profiles._data.gu.gu32 import GU32_GEOMETRY
from blueprints.structural_sections.steel.standard_profiles._data.gu.gu33 import GU33_GEOMETRY
from blueprints.structural_sections.steel.standard_profiles.utils import StandardProfileMeta
from blueprints.type_alias import MM


class __GUProfileParameters(NamedTuple):
    """Parameters for defining a GU profile."""

    name: str
    """Name of the GU profile."""
    coordinates: list[tuple[float, float]]
    """List of (x, y) coordinate tuples defining the profile geometry."""
    web_thickness: MM
    """Thickness of the web [mm]."""
    flange_thickness: MM
    """Thickness of the flanges [mm]."""
    interlocking_ctc: MM
    """Center to center distance of the sheets (interlocking distance) [mm]."""


GU_PROFILES_DATABASE = {
    "GU6N": __GUProfileParameters("GU 6N", GU6_GEOMETRY, 6.0, 6.0, 600),
    "GU7S": __GUProfileParameters("GU 7S", GU7_GEOMETRY, 6.9, 7.2, 600),
    "GU8S": __GUProfileParameters("GU 8S", GU8_GEOMETRY, 7.5, 8.0, 600),
    "GU10N": __GUProfileParameters("GU 10N", GU10_GEOMETRY, 6.8, 9.0, 600),
    "GU11N": __GUProfileParameters("GU 11N", GU11_GEOMETRY, 7.4, 10.0, 600),
    "GU12N": __GUProfileParameters("GU 12N", GU12_GEOMETRY, 8.0, 11.0, 600),
    "GU13N": __GUProfileParameters("GU 13N", GU13_GEOMETRY, 7.4, 9.0, 600),
    "GU14N": __GUProfileParameters("GU 14N", GU14_GEOMETRY, 8.0, 10.0, 600),
    "GU15N": __GUProfileParameters("GU 15N", GU15_GEOMETRY, 8.6, 11.0, 600),
    "GU16N": __GUProfileParameters("GU 16N", GU16_GEOMETRY, 8.4, 10.2, 600),
    "GU18N": __GUProfileParameters("GU 18N", GU18_GEOMETRY, 9.0, 11.2, 600),
    "GU18_400": __GUProfileParameters("GU 18-400", GU18_400_GEOMETRY, 9.7, 15.0, 400),
    "GU20N": __GUProfileParameters("GU 20N", GU20_GEOMETRY, 9.5, 12.2, 600),
    "GU21N": __GUProfileParameters("GU 21N", GU21_GEOMETRY, 9.0, 11.1, 600),
    "GU22N": __GUProfileParameters("GU 22N", GU22_GEOMETRY, 9.5, 12.1, 600),
    "GU23N": __GUProfileParameters("GU 23N", GU23_GEOMETRY, 10.0, 13.1, 600),
    "GU27N": __GUProfileParameters("GU 27N", GU27_GEOMETRY, 9.7, 14.2, 600),
    "GU28N": __GUProfileParameters("GU 28N", GU28_GEOMETRY, 10.1, 15.2, 600),
    "GU30N": __GUProfileParameters("GU 30N", GU30_GEOMETRY, 10.5, 16.2, 600),
    "GU31N": __GUProfileParameters("GU 31N", GU31_GEOMETRY, 10.6, 18.5, 600),
    "GU32N": __GUProfileParameters("GU 32N", GU32_GEOMETRY, 11.0, 19.5, 600),
    "GU33N": __GUProfileParameters("GU 33N", GU33_GEOMETRY, 11.4, 20.5, 600),
}


class GU(metaclass=StandardProfileMeta):
    """Geometrical representation of standard GU sheet pile profiles.

    GU profiles are a standardized form of U-shaped sheet piles. This class provides
    access to standard GU sheet pile profiles from a predefined database. Profiles
    can be accessed as class attributes using their standardized names. Each accessed
    profile returns a SheetpileUProfile instance.

    Usage example
    -------------
        >>> profile = GU.GU18
        >>> print(isinstance(profile, SheetpileUProfile))  # True
        >>>
        >>> # To iterate over all available GU profiles:
        >>> for profile in GU:
        ...     print(isinstance(profile, SheetpileUProfile))  # True
    """

    _factory = SheetpileUProfile
    _database = GU_PROFILES_DATABASE
