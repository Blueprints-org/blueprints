"""Standard PAZ sheet pile profiles."""

from __future__ import annotations

from typing import NamedTuple

from blueprints.structural_sections.steel.profile_definitions.sheetpile_z_profile import SheetpileZProfile
from blueprints.structural_sections.steel.standard_profiles._data.paz.paz4350 import PAZ4350_GEOMETRY
from blueprints.structural_sections.steel.standard_profiles._data.paz.paz4360 import PAZ4360_GEOMETRY
from blueprints.structural_sections.steel.standard_profiles._data.paz.paz4370 import PAZ4370_GEOMETRY
from blueprints.structural_sections.steel.standard_profiles._data.paz.paz4450 import PAZ4450_GEOMETRY
from blueprints.structural_sections.steel.standard_profiles._data.paz.paz4460 import PAZ4460_GEOMETRY
from blueprints.structural_sections.steel.standard_profiles._data.paz.paz4470 import PAZ4470_GEOMETRY
from blueprints.structural_sections.steel.standard_profiles._data.paz.paz4550 import PAZ4550_GEOMETRY
from blueprints.structural_sections.steel.standard_profiles._data.paz.paz4560 import PAZ4560_GEOMETRY
from blueprints.structural_sections.steel.standard_profiles._data.paz.paz4570 import PAZ4570_GEOMETRY
from blueprints.structural_sections.steel.standard_profiles._data.paz.paz4660 import PAZ4660_GEOMETRY
from blueprints.structural_sections.steel.standard_profiles._data.paz.paz4670 import PAZ4670_GEOMETRY
from blueprints.structural_sections.steel.standard_profiles._data.paz.paz5360 import PAZ5360_GEOMETRY
from blueprints.structural_sections.steel.standard_profiles._data.paz.paz5370 import PAZ5370_GEOMETRY
from blueprints.structural_sections.steel.standard_profiles._data.paz.paz5380 import PAZ5380_GEOMETRY
from blueprints.structural_sections.steel.standard_profiles._data.paz.paz5390 import PAZ5390_GEOMETRY
from blueprints.structural_sections.steel.standard_profiles._data.paz.paz5460 import PAZ5460_GEOMETRY
from blueprints.structural_sections.steel.standard_profiles._data.paz.paz5470 import PAZ5470_GEOMETRY
from blueprints.structural_sections.steel.standard_profiles._data.paz.paz5480 import PAZ5480_GEOMETRY
from blueprints.structural_sections.steel.standard_profiles._data.paz.paz5490 import PAZ5490_GEOMETRY
from blueprints.structural_sections.steel.standard_profiles._data.paz.paz5560 import PAZ5560_GEOMETRY
from blueprints.structural_sections.steel.standard_profiles._data.paz.paz5570 import PAZ5570_GEOMETRY
from blueprints.structural_sections.steel.standard_profiles._data.paz.paz5580 import PAZ5580_GEOMETRY
from blueprints.structural_sections.steel.standard_profiles._data.paz.paz5590 import PAZ5590_GEOMETRY
from blueprints.structural_sections.steel.standard_profiles._data.paz.paz5660 import PAZ5660_GEOMETRY
from blueprints.structural_sections.steel.standard_profiles._data.paz.paz5670 import PAZ5670_GEOMETRY
from blueprints.structural_sections.steel.standard_profiles._data.paz.paz5680 import PAZ5680_GEOMETRY
from blueprints.structural_sections.steel.standard_profiles._data.paz.paz5690 import PAZ5690_GEOMETRY
from blueprints.structural_sections.steel.standard_profiles._data.paz.paz54100 import PAZ54100_GEOMETRY
from blueprints.structural_sections.steel.standard_profiles._data.paz.paz55100 import PAZ55100_GEOMETRY
from blueprints.structural_sections.steel.standard_profiles._data.paz.paz56100 import PAZ56100_GEOMETRY
from blueprints.structural_sections.steel.standard_profiles.utils import StandardProfileMeta
from blueprints.type_alias import MM


class __PAZProfileParameters(NamedTuple):
    """Parameters for defining a PAZ profile."""

    name: str
    """Name of the PAZ profile."""
    coordinates: list[tuple[float, float]]
    """List of (x, y) coordinate tuples defining the profile geometry."""
    web_thickness: MM
    """Thickness of the web [mm]."""
    flange_thickness: MM
    """Thickness of the flanges [mm]."""
    interlocking_ctc: MM
    """Center to center distance of the sheets (interlocking distance) [mm]."""


PAZ_PROFILES_DATABASE = {
    "PAZ4350": __PAZProfileParameters("PAZ 43-50", PAZ4350_GEOMETRY, 5.0, 5.0, 770),
    "PAZ4360": __PAZProfileParameters("PAZ 43-60", PAZ4360_GEOMETRY, 6.0, 6.0, 770),
    "PAZ4370": __PAZProfileParameters("PAZ 43-70", PAZ4370_GEOMETRY, 7.0, 7.0, 770),
    "PAZ4450": __PAZProfileParameters("PAZ 44-50", PAZ4450_GEOMETRY, 5.0, 5.0, 725),
    "PAZ4460": __PAZProfileParameters("PAZ 44-60", PAZ4460_GEOMETRY, 6.0, 6.0, 725),
    "PAZ4470": __PAZProfileParameters("PAZ 44-70", PAZ4470_GEOMETRY, 7.0, 7.0, 725),
    "PAZ4550": __PAZProfileParameters("PAZ 45-50", PAZ4550_GEOMETRY, 5.0, 5.0, 676),
    "PAZ4560": __PAZProfileParameters("PAZ 45-60", PAZ4560_GEOMETRY, 6.0, 6.0, 676),
    "PAZ4570": __PAZProfileParameters("PAZ 45-70", PAZ4570_GEOMETRY, 7.0, 7.0, 676),
    "PAZ4660": __PAZProfileParameters("PAZ 46-60", PAZ4660_GEOMETRY, 5.0, 5.0, 621),
    "PAZ4670": __PAZProfileParameters("PAZ 46-70", PAZ4670_GEOMETRY, 6.0, 6.0, 621),
    "PAZ5360": __PAZProfileParameters("PAZ 53-60", PAZ5360_GEOMETRY, 6.0, 6.0, 857),
    "PAZ5370": __PAZProfileParameters("PAZ 53-70", PAZ5370_GEOMETRY, 7.0, 7.0, 857),
    "PAZ5380": __PAZProfileParameters("PAZ 53-80", PAZ5380_GEOMETRY, 8.0, 8.0, 857),
    "PAZ5390": __PAZProfileParameters("PAZ 53-90", PAZ5390_GEOMETRY, 9.0, 9.0, 857),
    "PAZ54100": __PAZProfileParameters("PAZ 54-100", PAZ54100_GEOMETRY, 10.0, 10.0, 808),
    "PAZ5460": __PAZProfileParameters("PAZ 54-60", PAZ5460_GEOMETRY, 6.0, 6.0, 807),
    "PAZ5470": __PAZProfileParameters("PAZ 54-70", PAZ5470_GEOMETRY, 7.0, 7.0, 807),
    "PAZ5480": __PAZProfileParameters("PAZ 54-80", PAZ5480_GEOMETRY, 8.0, 8.0, 807),
    "PAZ5490": __PAZProfileParameters("PAZ 54-90", PAZ5490_GEOMETRY, 9.0, 9.0, 807),
    "PAZ55100": __PAZProfileParameters("PAZ 55-100", PAZ55100_GEOMETRY, 10.0, 10.0, 745),
    "PAZ5560": __PAZProfileParameters("PAZ 55-60", PAZ5560_GEOMETRY, 6.0, 6.0, 743),
    "PAZ5570": __PAZProfileParameters("PAZ 55-70", PAZ5570_GEOMETRY, 7.0, 7.0, 743),
    "PAZ5580": __PAZProfileParameters("PAZ 55-80", PAZ5580_GEOMETRY, 8.0, 8.0, 744),
    "PAZ5590": __PAZProfileParameters("PAZ 55-90", PAZ5590_GEOMETRY, 9.0, 9.0, 744),
    "PAZ56100": __PAZProfileParameters("PAZ 56-100", PAZ56100_GEOMETRY, 10.0, 10.0, 673),
    "PAZ5660": __PAZProfileParameters("PAZ 56-60", PAZ5660_GEOMETRY, 6.0, 6.0, 671),
    "PAZ5670": __PAZProfileParameters("PAZ 56-70", PAZ5670_GEOMETRY, 7.0, 7.0, 671),
    "PAZ5680": __PAZProfileParameters("PAZ 56-80", PAZ5680_GEOMETRY, 8.0, 8.0, 672),
    "PAZ5690": __PAZProfileParameters("PAZ 56-90", PAZ5690_GEOMETRY, 9.0, 9.0, 672),
}


class PAZ(metaclass=StandardProfileMeta):
    """Geometrical representation of standard PAZ sheet pile profiles.

    PAZ (Pile and AZ) profiles are a standardized form of combined Z-shaped sheet piles.
    This class provides access to standard PAZ sheet pile profiles from a predefined
    database. Profiles can be accessed as class attributes using their standardized names.
    Each accessed profile returns a SheetpileZProfile instance configured with 2 sheets.

    Note
    ----
    PAZ profiles consist of two interlocked Z-sections forming a combined pile.

    Usage example
    -------------
        >>> profile = PAZ.PAZ4350
        >>> print(isinstance(profile, SheetpileZProfile))  # True
        >>> print(profile.number_of_sheets)
        >>>
        >>> # To iterate over all available PAZ profiles:
        >>> for profile in PAZ:
        ...     print(isinstance(profile, SheetpileZProfile))  # True
    """

    _factory = SheetpileZProfile
    _database = PAZ_PROFILES_DATABASE
