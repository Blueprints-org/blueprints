r"""Corner point of a standard EN 1993-1-9:2025 fatigue strength curve.

A fatigue strength curve is piecewise-linear on log-log [$N$] - [$\Delta\sigma$] axes; its shape is fixed by a
handful of corner points: the detail category ``C`` at [$N_C$], the constant amplitude fatigue limit ``D`` at
[$N_D$] and the cut-off limit ``L`` at [$N_L$]. The :func:`form8_curve_corner_points` helper returns these points
(as :class:`FatigueStrengthCurvePoint` instances) for a given detail category, so callers can read the whole curve
geometry without re-deriving the EN power law per branch.
"""

from dataclasses import dataclass
from typing import Literal

from blueprints.type_alias import DIMENSIONLESS, MPA


@dataclass(frozen=True)
class FatigueStrengthCurvePoint:
    r"""One corner point of a standard EN 1993-1-9 fatigue strength curve on the [$N$] - [$\Delta\sigma$] plane.

    Parameters
    ----------
    point : Literal["C", "D", "L"]
        The corner label: ``"C"`` (detail category at [$N_C$]), ``"D"`` (constant amplitude fatigue limit at [$N_D$])
        or ``"L"`` (cut-off limit, the end of the curve).
    n_cycles : DIMENSIONLESS
        [$N$] Number of cycles at the corner [$-$].
    delta_sigma : MPA
        Stress range at the corner: a normal [$\Delta\sigma$] or a shear [$\Delta\tau$], matching the curve [$MPa$].
    """

    point: Literal["C", "D", "L"]
    n_cycles: DIMENSIONLESS
    delta_sigma: MPA
