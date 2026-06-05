"""Fatigue life (number of cycles to failure) on a standard fatigue strength curve from EN 1993-1-9:2025: Chapter 8."""

from dataclasses import dataclass

from blueprints.codes.eurocode.en_1993_1_9_2025 import EN_1993_1_9_2025
from blueprints.codes.eurocode.en_1993_1_9_2025.chapter_8_fatigue_resistance.fatigue_strength_curve import FatigueStrengthCurve, StressType
from blueprints.codes.eurocode.en_1993_1_9_2025.chapter_8_fatigue_resistance.fatigue_strength_curve_limits import FatigueStrengthCurveLimits
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_scientific
from blueprints.type_alias import DIMENSIONLESS, MPA
from blueprints.validations import raise_if_negative


@dataclass(frozen=True)
class _GoverningBranch:
    r"""The branch of a fatigue strength curve that governs a given applied stress range.

    Bundles the reference anchor of the governing branch so both the fatigue life and its LaTeX
    representation can be derived from a single source. ``m`` is ``None`` when the applied stress
    range falls below the cut-off limit [$\Delta\sigma_L$], for which the life is infinite.
    """

    point: str  # reference point of the governing branch: "C" (first branch), "D" (second branch) or "L" (below cut-off)
    delta_sigma_ref: MPA  # fatigue strength at the reference point [MPa]
    n_ref: DIMENSIONLESS  # number of cycles at the reference point [-]
    m: DIMENSIONLESS | None  # slope of the governing branch [-], None below the cut-off limit (infinite life)


def _governing_branch(delta_sigma_r: MPA, delta_sigma_c: MPA, curve: FatigueStrengthCurve) -> _GoverningBranch:
    r"""Select the branch of ``curve`` that governs an applied stress range [$\Delta\sigma_R$].

    The fatigue strength curve is piecewise (see :class:`Form8FatigueLife`); the governing branch is
    the one whose stress range covers [$\Delta\sigma_R$].
    """
    limits = FatigueStrengthCurveLimits(delta_sigma_c=delta_sigma_c, curve=curve)
    delta_sigma_d = float(limits.delta_sigma_d)
    if delta_sigma_r >= delta_sigma_d:
        # first branch (slope m1), anchored at the detail category point (N_C, Δσ_C)
        return _GoverningBranch(point="C", delta_sigma_ref=delta_sigma_c, n_ref=curve.n_c, m=curve.m1)

    delta_sigma_l = limits.delta_sigma_l
    if delta_sigma_l is not None and curve.m2 is not None and delta_sigma_r >= float(delta_sigma_l):
        # second branch (slope m2), anchored at the constant amplitude fatigue limit point (N_D, Δσ_D)
        return _GoverningBranch(point="D", delta_sigma_ref=delta_sigma_d, n_ref=curve.n_d, m=curve.m2)

    # below the cut-off limit Δσ_L (or below Δτ_D for the single-slope shear curve): infinite life, no damage
    reference = delta_sigma_d if delta_sigma_l is None else float(delta_sigma_l)
    return _GoverningBranch(point="L", delta_sigma_ref=reference, n_ref=curve.n_l or curve.n_d, m=None)


class Form8FatigueLife(Formula):
    r"""Class representing the number of cycles to failure [$N_R$] for an applied stress range on a standard fatigue strength curve.

    This is the inverse of :class:`~blueprints.codes.eurocode.en_1993_1_9_2025.chapter_8_fatigue_resistance.fatigue_strength.Form8FatigueStrength`:
    given a constant-amplitude applied stress range [$\Delta\sigma_R$] (or [$\Delta\tau_R$]) and a detail category
    [$\Delta\sigma_C$], it returns the number of cycles [$N_R$] at which [$\Delta\sigma_R$] meets the characteristic
    fatigue strength curve (EN 1993-1-9:2025, Figures 8.1 - 8.4). It provides the denominator [$N_R$] of the partial
    damage [$n / N_R$] of a Palmgren-Miner accumulation. The curve is piecewise:

    - first branch (slope [$m_1$]), [$\Delta\sigma_R \geq \Delta\sigma_D$]: [$N_R = N_C (\Delta\sigma_C / \Delta\sigma_R)^{m_1}$],
    - second branch (slope [$m_2$]), [$\Delta\sigma_L \leq \Delta\sigma_R < \Delta\sigma_D$]: [$N_R = N_D (\Delta\sigma_D / \Delta\sigma_R)^{m_2}$],
    - below the cut-off limit, [$\Delta\sigma_R < \Delta\sigma_L$]: infinite life [$N_R = \infty$] (no fatigue damage).

    For the shear curve (Figure 8.4) there is a single slope and the constant amplitude fatigue limit [$\Delta\tau_D$]
    acts as the cut-off, so any [$\Delta\tau_R < \Delta\tau_D$] gives infinite life.
    """

    label = "Figures 8.1-8.4 (fatigue life)"
    source_document = EN_1993_1_9_2025

    def __init__(self, delta_sigma_r: MPA, delta_sigma_c: MPA, curve: FatigueStrengthCurve) -> None:
        r"""[$N_R$] Number of cycles to failure for an applied stress range on a standard fatigue strength curve [$-$].

        EN 1993-1-9:2025 - Chapter 8 - Fatigue resistance (Figures 8.1 - 8.4)

        Parameters
        ----------
        delta_sigma_r : MPA
            [$\Delta\sigma_R$] Applied constant-amplitude stress range to find the fatigue life for [$MPa$].
            For shear curves this is the applied shear stress range [$\Delta\tau_R$].
        delta_sigma_c : MPA
            [$\Delta\sigma_C$] Detail category: the reference fatigue strength at [$N_C = 2 \cdot 10^6$] cycles [$MPa$].
            For shear curves this is the shear detail category [$\Delta\tau_C$].
        curve : FatigueStrengthCurve
            The standard fatigue strength curve to read from (one of Figures 8.1 - 8.4), fixing the slopes
            [$m_1$], [$m_2$] and the reference cycle numbers [$N_C$], [$N_D$], [$N_L$].

        Returns
        -------
        None
        """
        super().__init__()
        self.delta_sigma_r: MPA = delta_sigma_r
        self.delta_sigma_c: MPA = delta_sigma_c
        self.curve: FatigueStrengthCurve = curve

    @staticmethod
    def _evaluate(delta_sigma_r: MPA, delta_sigma_c: MPA, curve: FatigueStrengthCurve) -> DIMENSIONLESS:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(delta_sigma_r=delta_sigma_r, delta_sigma_c=delta_sigma_c)

        branch = _governing_branch(delta_sigma_r, delta_sigma_c, curve)
        if branch.m is None:
            # below the cut-off limit: infinite life (the division below is never reached for Δσ_R = 0)
            return float("inf")
        return branch.n_ref * (branch.delta_sigma_ref / delta_sigma_r) ** branch.m

    @property
    def detailed_result(self) -> dict:
        r"""Reference anchor of the governing branch, so callers can label [$N_R$] without re-deriving the branch.

        Returns
        -------
        dict
            ``reference_point`` ("C", "D" or "L"), the governing reference strength ``delta_sigma_ref`` [$MPa$]
            ([$\Delta\sigma_C$], [$\Delta\sigma_D$] or [$\Delta\sigma_L$]), its cycle number ``n_ref`` [$-$], the
            governing slope ``m`` [$-$] (``None`` below the cut-off) and the fatigue life ``n_r`` [$-$].
        """
        branch = _governing_branch(self.delta_sigma_r, self.delta_sigma_c, self.curve)
        return {
            "reference_point": branch.point,
            "delta_sigma_ref": branch.delta_sigma_ref,
            "n_ref": branch.n_ref,
            "m": branch.m,
            "n_r": float(self),
        }

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for the fatigue life at the applied stress range."""
        branch = _governing_branch(self.delta_sigma_r, self.delta_sigma_c, self.curve)
        symbol = r"\Delta\tau" if self.curve.stress_type == StressType.SHEAR else r"\Delta\sigma"

        if branch.m is None:
            # below the cut-off limit: the life is infinite, so there is no fraction to evaluate
            return LatexFormula(
                return_symbol="N_{R}",
                result=r"\infty",
                comparison_operator_label="=",
            )

        ref, slope_sub = branch.point, "1" if branch.point == "C" else "2"
        # The slope m is an integer (m1, m2 in {3, 5, 9}), so trailing zeros are stripped to keep the exponent clean.
        slope_str = f"{branch.m:.{n}f}"
        if "." in slope_str:
            slope_str = slope_str.rstrip("0").rstrip(".")

        return LatexFormula(
            return_symbol="N_{R}",
            result=f"{self:.0f}",
            equation=rf"N_{{{ref}}} \left( \frac{{{symbol}_{{{ref}}}}}{{{symbol}_{{R}}}} \right)^{{m_{{{slope_sub}}}}}",
            numeric_equation=(
                rf"{latex_scientific(branch.n_ref)} \left( \frac{{{branch.delta_sigma_ref:.{n}f}}}{{{self.delta_sigma_r:.{n}f}}} \right)"
                rf"^{{{slope_str}}}"
            ),
            comparison_operator_label="=",
        )
