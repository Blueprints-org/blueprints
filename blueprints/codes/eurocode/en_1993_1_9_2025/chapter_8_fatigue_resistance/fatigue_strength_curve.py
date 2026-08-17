"""Standard fatigue strength curves from EN 1993-1-9:2025: Chapter 8 - Fatigue resistance (Figures 8.1 - 8.4)."""

from enum import Enum

from blueprints.type_alias import DIMENSIONLESS

# Number of cycles at the detail category reference point, shared by every fatigue strength curve [-].
N_C: DIMENSIONLESS = 2e6


class StressType(Enum):
    """Type of nominal stress range a fatigue strength curve applies to."""

    NORMAL = "normal stress"  # [$\Delta\sigma$]
    SHEAR = "shear stress"  # [$\Delta\tau$]


class FatigueStrengthCurve(Enum):
    r"""Standard characteristic fatigue strength curves of EN 1993-1-9:2025, Figures 8.1 - 8.4.

    Each member bundles the fixed geometry of one curve: the slope [$m_1$] of the first branch, the
    number of cycles [$N_D$] at the constant amplitude fatigue limit, and (when a second branch exists)
    the slope [$m_2$] and the number of cycles [$N_L$] at the cut-off limit. The detail category reference
    point [$N_C$] is shared by all curves (see [$N_C$]).

    Every member is defined as a tuple ``(stress_type, description, m1, n_d, m2, n_l)``. For shear
    (Figure 8.4) there is a single slope and no separate cut-off branch, so ``m2`` and ``n_l`` are ``None``.
    """

    FIG_8_1A = (StressType.NORMAL, "Non-welded details, light notch effect (Figure 8.1a)", 5.0, 2e6, 9.0, 1e8)
    FIG_8_1B = (StressType.NORMAL, "Non-welded details, sharp notch effect (Figure 8.1b)", 3.0, 2e6, 5.0, 1e8)
    FIG_8_2A = (StressType.NORMAL, "Welded details, detail category 71 and above (Figure 8.2a)", 3.0, 5e6, 5.0, 1e8)
    FIG_8_2B = (StressType.NORMAL, "Welded details, detail category below 71 (Figure 8.2b)", 3.0, 1e7, 5.0, 1e8)
    FIG_8_3 = (StressType.NORMAL, "Lattice girder joints of hollow sections, Table 10.8 (Figure 8.3)", 5.0, 1e7, 9.0, 1e8)
    FIG_8_4 = (StressType.SHEAR, "Constructional details subject to shear stress (Figure 8.4)", 5.0, 1e8, None, None)

    def __init__(
        self,
        stress_type: StressType,
        description: str,
        m1: DIMENSIONLESS,
        n_d: DIMENSIONLESS,
        m2: DIMENSIONLESS | None,
        n_l: DIMENSIONLESS | None,
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
    def has_cutoff_segment(self) -> bool:
        r"""Whether the curve has a second branch ending at a separate cut-off limit [$\Delta\sigma_L$].

        ``False`` for the shear curve (Figure 8.4), which has a single slope and whose constant amplitude
        fatigue limit [$\Delta\tau_D$] is also its cut-off limit.
        """
        return self.m2 is not None
