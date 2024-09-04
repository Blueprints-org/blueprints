"""Constants for the calculation of nominal concrete cover according to NEN-EN 1992-1-1+C2:2011."""

from blueprints.checks.nominal_concrete_cover.definitions import AbrasionClass, CastingSurface
from blueprints.type_alias import MM

# According to art. 4.4.1.2 (11) from NEN-EN 1992-1-1+C2:2011
COVER_INCREASE_FOR_UNEVEN_SURFACE: MM = 5

# According to art. 4.4.1.2 (13) from NEN-EN 1992-1-1+C2:2011
COVER_INCREATSE_FOR_ABRASION_CLASS: dict[AbrasionClass, MM] = {
    AbrasionClass.NA: 0,
    AbrasionClass.XM1: 0,
    AbrasionClass.XM2: 0,
    AbrasionClass.XM3: 0,
}

# According to art. 4.4.1.3 (1) from NEN-EN 1992-1-1+C2:2011
DEFAULT_DELTA_C_DEV: MM = 5


def minimum_cover_with_regard_to_casting_surface(c_min_dur: MM, casting_surface: CastingSurface) -> MM:
    """Calculate the minimum cover with regard to casting surface according to art. 4.4.1.3 (4) from NEN-EN 1992-1-1+C2:2011."""
    match casting_surface:
        case CastingSurface.PERMANENTLY_EXPOSED | CastingSurface.FORMWORK:
            return 0  # No additional requirements
        case CastingSurface.PREPARED_GROUND:
            return c_min_dur + 10  # k1 ≥ c_min,dur + 10
        case CastingSurface.DIRECTLY_AGAINST_SOIL:
            return c_min_dur + 50  # k2 ≥ c_min,dur + 50
