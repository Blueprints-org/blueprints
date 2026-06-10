"""Standard AZ sheet pile profiles."""

from __future__ import annotations

from typing import NamedTuple

from blueprints.structural_sections.steel.profile_definitions.az_profile import AZProfile
from blueprints.structural_sections.steel.standard_profiles._data.az.az12_700 import AZ12_700_GEOMETRY
from blueprints.structural_sections.steel.standard_profiles._data.az.az12_770 import AZ12_770_GEOMETRY
from blueprints.structural_sections.steel.standard_profiles._data.az.az13_700 import AZ13_700_GEOMETRY
from blueprints.structural_sections.steel.standard_profiles._data.az.az13_700_10_10 import AZ13_700_10_10_GEOMETRY
from blueprints.structural_sections.steel.standard_profiles._data.az.az13_770 import AZ13_770_GEOMETRY
from blueprints.structural_sections.steel.standard_profiles._data.az.az14_700 import AZ14_700_GEOMETRY
from blueprints.structural_sections.steel.standard_profiles._data.az.az14_770 import AZ14_770_GEOMETRY
from blueprints.structural_sections.steel.standard_profiles._data.az.az14_770_10_10 import AZ14_770_10_10_GEOMETRY
from blueprints.structural_sections.steel.standard_profiles._data.az.az17_700 import AZ17_700_GEOMETRY
from blueprints.structural_sections.steel.standard_profiles._data.az.az18 import AZ18_GEOMETRY
from blueprints.structural_sections.steel.standard_profiles._data.az.az18_10_10 import AZ18_10_10_GEOMETRY
from blueprints.structural_sections.steel.standard_profiles._data.az.az18_700 import AZ18_700_GEOMETRY
from blueprints.structural_sections.steel.standard_profiles._data.az.az18_800 import AZ18_800_GEOMETRY
from blueprints.structural_sections.steel.standard_profiles._data.az.az19_700 import AZ19_700_GEOMETRY
from blueprints.structural_sections.steel.standard_profiles._data.az.az20_700 import AZ20_700_GEOMETRY
from blueprints.structural_sections.steel.standard_profiles._data.az.az22_800 import AZ22_800_GEOMETRY
from blueprints.structural_sections.steel.standard_profiles._data.az.az24_700 import AZ24_700_GEOMETRY
from blueprints.structural_sections.steel.standard_profiles._data.az.az25_800 import AZ25_800_GEOMETRY
from blueprints.structural_sections.steel.standard_profiles._data.az.az26 import AZ26_GEOMETRY
from blueprints.structural_sections.steel.standard_profiles._data.az.az26_700 import AZ26_700_GEOMETRY
from blueprints.structural_sections.steel.standard_profiles._data.az.az27_800 import AZ27_800_GEOMETRY
from blueprints.structural_sections.steel.standard_profiles._data.az.az28_700 import AZ28_700_GEOMETRY
from blueprints.structural_sections.steel.standard_profiles._data.az.az28_750 import AZ28_750_GEOMETRY
from blueprints.structural_sections.steel.standard_profiles._data.az.az30_750 import AZ30_750_GEOMETRY
from blueprints.structural_sections.steel.standard_profiles._data.az.az32_750 import AZ32_750_GEOMETRY
from blueprints.structural_sections.steel.standard_profiles._data.az.az36_700n import AZ36_700N_GEOMETRY
from blueprints.structural_sections.steel.standard_profiles._data.az.az38_700n import AZ38_700N_GEOMETRY
from blueprints.structural_sections.steel.standard_profiles._data.az.az40_700n import AZ40_700N_GEOMETRY
from blueprints.structural_sections.steel.standard_profiles._data.az.az42_700n import AZ42_700N_GEOMETRY
from blueprints.structural_sections.steel.standard_profiles._data.az.az44_700n import AZ44_700N_GEOMETRY
from blueprints.structural_sections.steel.standard_profiles._data.az.az46_700n import AZ46_700N_GEOMETRY
from blueprints.structural_sections.steel.standard_profiles._data.az.az48_700 import AZ48_700_GEOMETRY
from blueprints.structural_sections.steel.standard_profiles._data.az.az50_700 import AZ50_700_GEOMETRY
from blueprints.structural_sections.steel.standard_profiles._data.az.az52_700 import AZ52_700_GEOMETRY
from blueprints.structural_sections.steel.standard_profiles.utils import StandardProfileMeta
from blueprints.type_alias import MM


class __AZProfileParameters(NamedTuple):
    """Parameters for defining an AZ profile."""

    name: str
    """Name of the AZ profile."""
    coordinates: list[tuple[float, float]]
    """List of (x, y) coordinate tuples defining the profile geometry."""
    web_thickness: MM
    """Thickness of the web [mm]."""
    flange_thickness: MM
    """Thickness of the flanges [mm]."""
    interlocking_ctc: MM
    """Center to center distance of the sheets (interlocking distance) [mm]."""


AZ_PROFILES_DATABASE = {
    "AZ12_700": __AZProfileParameters("AZ 12-700", AZ12_700_GEOMETRY, 8.5, 8.5, 700),
    "AZ12_770": __AZProfileParameters("AZ 12-770", AZ12_770_GEOMETRY, 8.5, 8.5, 770),
    "AZ13_700": __AZProfileParameters("AZ 13-700", AZ13_700_GEOMETRY, 9.5, 9.5, 700),
    "AZ13_700_10_10": __AZProfileParameters("AZ 13-700-10/10", AZ13_700_10_10_GEOMETRY, 10.0, 10.0, 700),
    "AZ13_770": __AZProfileParameters("AZ 13-770", AZ13_770_GEOMETRY, 9.0, 9.0, 770),
    "AZ14_700": __AZProfileParameters("AZ 14-700", AZ14_700_GEOMETRY, 10.5, 10.5, 700),
    "AZ14_770": __AZProfileParameters("AZ 14-770", AZ14_770_GEOMETRY, 9.5, 9.5, 770),
    "AZ14_770_10_10": __AZProfileParameters("AZ 14-770-10/10", AZ14_770_10_10_GEOMETRY, 10.0, 10.0, 770),
    "AZ17_700": __AZProfileParameters("AZ 17-700", AZ17_700_GEOMETRY, 8.5, 8.5, 700),
    "AZ18": __AZProfileParameters("AZ 18", AZ18_GEOMETRY, 9.5, 9.5, 630),
    "AZ18_10_10": __AZProfileParameters("AZ 18-10/10", AZ18_10_10_GEOMETRY, 10.0, 10.0, 630),
    "AZ18_700": __AZProfileParameters("AZ 18-700", AZ18_700_GEOMETRY, 9.0, 9.0, 700),
    "AZ18_800": __AZProfileParameters("AZ 18-800", AZ18_800_GEOMETRY, 8.5, 8.5, 800),
    "AZ19_700": __AZProfileParameters("AZ 19-700", AZ19_700_GEOMETRY, 9.5, 9.5, 700),
    "AZ20_700": __AZProfileParameters("AZ 20-700", AZ20_700_GEOMETRY, 10.0, 10.0, 700),
    "AZ22_800": __AZProfileParameters("AZ 22-800", AZ22_800_GEOMETRY, 10.5, 10.5, 800),
    "AZ24_700": __AZProfileParameters("AZ 24-700", AZ24_700_GEOMETRY, 11.2, 11.2, 700),
    "AZ25_800": __AZProfileParameters("AZ 25-800", AZ25_800_GEOMETRY, 10.0, 12.5, 800),
    "AZ26": __AZProfileParameters("AZ 26", AZ26_GEOMETRY, 12.2, 13.0, 630),
    "AZ26_700": __AZProfileParameters("AZ 26-700", AZ26_700_GEOMETRY, 12.2, 12.2, 700),
    "AZ27_800": __AZProfileParameters("AZ 27-800", AZ27_800_GEOMETRY, 11.0, 13.5, 800),
    "AZ28_700": __AZProfileParameters("AZ 28-700", AZ28_700_GEOMETRY, 13.2, 13.2, 700),
    "AZ28_750": __AZProfileParameters("AZ 28-750", AZ28_750_GEOMETRY, 10.0, 12.0, 750),
    "AZ30_750": __AZProfileParameters("AZ 30-750", AZ30_750_GEOMETRY, 11.0, 13.0, 750),
    "AZ32_750": __AZProfileParameters("AZ 32-750", AZ32_750_GEOMETRY, 12.0, 14.0, 750),
    "AZ36_700N": __AZProfileParameters("AZ 36-700N", AZ36_700N_GEOMETRY, 11.2, 15.0, 700),
    "AZ38_700N": __AZProfileParameters("AZ 38-700N", AZ38_700N_GEOMETRY, 12.2, 16.0, 700),
    "AZ40_700N": __AZProfileParameters("AZ 40-700N", AZ40_700N_GEOMETRY, 13.2, 17.0, 700),
    "AZ42_700N": __AZProfileParameters("AZ 42-700N", AZ42_700N_GEOMETRY, 14.0, 18.0, 700),
    "AZ44_700N": __AZProfileParameters("AZ 44-700N", AZ44_700N_GEOMETRY, 15.0, 19.0, 700),
    "AZ46_700N": __AZProfileParameters("AZ 46-700N", AZ46_700N_GEOMETRY, 16.0, 20.0, 700),
    "AZ48_700": __AZProfileParameters("AZ 48-700", AZ48_700_GEOMETRY, 15.0, 22.0, 700),
    "AZ50_700": __AZProfileParameters("AZ 50-700", AZ50_700_GEOMETRY, 16.0, 23.0, 700),
    "AZ52_700": __AZProfileParameters("AZ 52-700", AZ52_700_GEOMETRY, 17.0, 24.0, 700),
}


class AZ(metaclass=StandardProfileMeta):
    """Geometrical representation of standard AZ sheet pile profiles.

    This class provides access to standard AZ sheet pile profiles
    from a predefined database. Profiles can be accessed as class attributes using
    their standardized names. Each accessed profile returns an AZProfile instance.

    Usage example
    -------------
        >>> profile = AZ.AZ18
        >>> print(isinstance(profile, AZProfile))  # True
        >>>
        >>> # To iterate over all available AZ profiles:
        >>> for profile in AZ:
        ...     print(isinstance(profile, AZProfile))  # True
    """

    _factory = AZProfile
    _database = AZ_PROFILES_DATABASE
