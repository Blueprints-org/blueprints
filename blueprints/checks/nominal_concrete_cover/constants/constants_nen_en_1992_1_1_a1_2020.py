"""Constants for the calculation of nominal concrete cover according to NEN-EN 1992-1-1:2005+A1:2015+NB:2016+A1:2020."""

from dataclasses import dataclass, field

from blueprints.checks.nominal_concrete_cover.constants.base import NominalConcreteCoverConstantsBase
from blueprints.checks.nominal_concrete_cover.definitions import AbrasionClass, CastingSurface
from blueprints.type_alias import MM


@dataclass(frozen=True)
class NominalConcreteCoverConstants2020A1(NominalConcreteCoverConstantsBase):
    """Constants for the calculation of nominal concrete cover according to NEN-EN 1992-1-1:2005+A1:2015+NB:2016+A1:2020."""

    CODE_SUFFIX: str = field(default=":2005+A1:2015+NB:2016+A1:2020", init=False)

    # According to art. 4.4.1.2 (11) from NEN-EN 1992-1-1:2005+A1:2015+NB:2016+A1:2020
    COVER_INCREASE_FOR_UNEVEN_SURFACE: MM = field(default=5, init=False)

    # According to art. 4.4.1.3 (1) from NEN-EN 1992-1-1:2005+A1:2015+NB:2016+A1:2020
    DEFAULT_DELTA_C_DEV: MM = field(default_factory=int)

    # According to art. 4.4.1.2 (13) from NEN-EN 1992-1-1:2005+A1:2015+NB:2016+A1:2020
    COVER_INCREASE_FOR_ABRASION_CLASS: dict[AbrasionClass, MM] = field(default_factory=dict)

    def __post_init__(self) -> None:
        """Post-initialization method to set default values."""
        if not self.COVER_INCREASE_FOR_ABRASION_CLASS:
            abrasion_class_cover_increase = {
                AbrasionClass.NA: 0,
                AbrasionClass.XM1: 0,  # k1 according to art. 4.4.1.2 (13)
                AbrasionClass.XM2: 0,  # k2 according to art. 4.4.1.2 (13)
                AbrasionClass.XM3: 0,  # k3 according to art. 4.4.1.2 (13)
            }
            object.__setattr__(self, "COVER_INCREASE_FOR_ABRASION_CLASS", abrasion_class_cover_increase)
        if not self.DEFAULT_DELTA_C_DEV:
            object.__setattr__(self, "DEFAULT_DELTA_C_DEV", 5)

    @staticmethod
    def minimum_cover_with_regard_to_casting_surface(c_min_dur: MM, casting_surface: CastingSurface) -> MM:
        """Calculate the minimum cover with regard to casting surface
        according to art. 4.4.1.3 (4) from NEN-EN 1992-1-1:2005+A1:2015+NB:2016+A1:2020.
        """
        match casting_surface:
            case CastingSurface.PERMANENTLY_EXPOSED | CastingSurface.FORMWORK:
                return 0  # No additional requirements
            case CastingSurface.PREPARED_GROUND:
                return c_min_dur + 10  # k1 ≥ c_min,dur + 10
            case CastingSurface.DIRECTLY_AGAINST_SOIL:
                return c_min_dur + 50  # k2 ≥ c_min,dur + 50

    @staticmethod
    def minimum_cover_with_regard_to_casting_surface_latex(casting_surface: CastingSurface) -> str:
        """LateX representation of minimum cover with regard to casting surface
        according to art. 4.4.1.3 (4) from NEN-EN 1992-1-1:2005+A1:2015+NB:2016+A1:2020.
        """
        match casting_surface:
            case CastingSurface.PERMANENTLY_EXPOSED | CastingSurface.FORMWORK:
                return f"0 (No additional requirements for {casting_surface.value})"
            case CastingSurface.PREPARED_GROUND:
                return f"k1 \\ge c_{{min,dur}} + 10 mm for {casting_surface.value}"
            case CastingSurface.DIRECTLY_AGAINST_SOIL:
                return f"k2 \\ge c_{{min,dur}} + 50 mm for {casting_surface.value}"
