"""Standard fatigue strength curves from EN 1993-1-9:2005: Chapter 7 - Fatigue strength (Figures 7.1 - 7.2)."""

from enum import Enum

from blueprints.type_alias import DIMENSIONLESS

# Number of cycles at the detail category reference point, shared by both fatigue strength curves [-].
N_C: DIMENSIONLESS = 2e6


class StressType(Enum):
    """Type of nominal stress range a fatigue strength curve applies to."""

    DIRECT = "direct stress"  # [$\Delta\sigma$]
    SHEAR = "shear stress"  # [$\Delta\tau$]


class FatigueStrengthCurve(Enum):
    r"""Standard characteristic fatigue strength curves of EN 1993-1-9:2005, Figures 7.1 - 7.2.

    Each member bundles the fixed geometry of one curve: the slope [$m_1$] of the first branch, the
    number of cycles [$N_D$] at the constant amplitude fatigue limit (when one exists), the slope
    [$m_2$] of the second branch (when one exists) and the number of cycles [$N_L$] at the cut-off
    limit. The detail category reference point [$N_C$] is shared by both curves (see [$N_C$]).

    Every member is defined as a tuple ``(stress_type, description, m1, n_d, m2, n_l)``. For shear
    (Figure 7.2) there is a single slope running straight to the cut-off limit [$\Delta\tau_L$] at
    [$N_L$], so there is no constant amplitude fatigue limit and ``n_d`` and ``m2`` are ``None``.
    """

    FIG_7_1 = (StressType.DIRECT, "Direct stress ranges (Figure 7.1)", 3.0, 5e6, 5.0, 1e8)
    FIG_7_2 = (StressType.SHEAR, "Shear stress ranges (Figure 7.2)", 5.0, None, None, 1e8)

    def __init__(
        self,
        stress_type: StressType,
        description: str,
        m1: DIMENSIONLESS,
        n_d: DIMENSIONLESS | None,
        m2: DIMENSIONLESS | None,
        n_l: DIMENSIONLESS,
    ) -> None:
        self.stress_type = stress_type
        self.description = description
        self.m1 = m1
        self.n_d = n_d
        self.m2 = m2
        self.n_l = n_l

    @property
    def n_c(self) -> DIMENSIONLESS:
        """[$N_C$] Number of cycles at the detail category reference point [-]."""
        return N_C

    @property
    def has_constant_amplitude_fatigue_limit(self) -> bool:
        r"""Whether the curve has a constant amplitude fatigue limit [$\Delta\sigma_D$] at [$N_D$] cycles.

        ``False`` for the shear curve (Figure 7.2), which has a single slope running straight to its
        cut-off limit [$\Delta\tau_L$] at [$N_L$].
        """
        return self.n_d is not None
