"""Fatigue life curve value from EN 1993-1-9:2025: Chapter 8 - Fatigue resistance."""

from typing import Literal

from blueprints.codes.eurocode.en_1993_1_9_2025 import EN_1993_1_9_2025
from blueprints.codes.eurocode.en_1993_1_9_2025.chapter_8_fatigue_resistance.fatigue_strength_curve import StressType
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_scientific
from blueprints.type_alias import DIMENSIONLESS, MPA
from blueprints.validations import raise_if_less_or_equal_to_zero

# Latex slope subscript of the governing branch for each reference point.
# point "C": first branch, anchored at the detail category C with the first slope m1.
# point "D": second branch, anchored at the constant amplitude fatigue limit D with the second slope m2.
_SLOPE_SUBSCRIPT: dict[str, str] = {"C": "1", "D": "2"}


class Form8FatigueLifeCurveValue(Formula):
    r"""Class representing the relation that gives the fatigue life [$N_R$] on a branch of a fatigue strength curve.

    This relation is the inverse of
    :class:`~blueprints.codes.eurocode.en_1993_1_9_2025.chapter_8_fatigue_resistance.fatigue_strength_curve_value.Form8FatigueStrengthCurveValue`:
    where that relation reads a strength off the curve at a number of cycles, this one reads the number of cycles
    [$N_R$] at which an applied stress range [$\Delta\sigma_R$] meets a single (constant-slope) branch of the curve.
    Like its inverse it is not stated explicitly in EN 1993-1-9:2025, but follows directly from the constant-slope
    fatigue strength curves of chapter 8. The same expression yields the life on either branch:

    - the first branch (slope [$m_1$]) anchored at the detail category [$\Delta\sigma_C$] (point ``"C"``), and
    - the second branch (slope [$m_2$]) anchored at the constant amplitude fatigue limit [$\Delta\sigma_D$] (point ``"D"``).

    The variant is selected through the ``point`` argument. The branch below the cut-off limit gives infinite life and
    is therefore not a curve value; it is handled by the caller (see :class:`Form8FatigueLife`).
    """

    label = "Figures 8.1-8.4 (fatigue life curve value)"
    source_document = EN_1993_1_9_2025

    def __init__(
        self,
        delta_sigma_ref: MPA,
        n_ref: DIMENSIONLESS,
        m: DIMENSIONLESS,
        delta_sigma_r: MPA,
        point: Literal["C", "D"],
        stress_type: StressType,
    ) -> None:
        r"""[$N_R$] Fatigue life of an applied stress range on a single branch of the fatigue strength curve [$-$].

        EN 1993-1-9:2025 - Chapter 8 - Fatigue resistance (derived from the fatigue strength curves)

        [$N_R = N_{ref} \left( \frac{\Delta\sigma_{ref}}{\Delta\sigma_R} \right)^{m}$]

        With ``point="C"`` the life is read on the first branch from the detail category
        ([$N_R = N_C \left( \Delta\sigma_C / \Delta\sigma_R \right)^{m_1}$]).
        With ``point="D"`` the life is read on the second branch from the constant amplitude fatigue limit
        ([$N_R = N_D \left( \Delta\sigma_D / \Delta\sigma_R \right)^{m_2}$]).

        Parameters
        ----------
        delta_sigma_ref : MPA
            [$\Delta\sigma_{ref}$] Reference fatigue strength of the branch: the detail category [$\Delta\sigma_C$] for
            ``point="C"``, or the constant amplitude fatigue limit [$\Delta\sigma_D$] for ``point="D"`` [$MPa$].
        n_ref : DIMENSIONLESS
            [$N_{ref}$] Number of cycles at the reference point: [$N_C$] for ``point="C"`` or [$N_D$] for ``point="D"`` [$-$].
        m : DIMENSIONLESS
            [$m$] Slope of the branch: [$m_1$] for ``point="C"`` or [$m_2$] for ``point="D"`` [$-$].
        delta_sigma_r : MPA
            [$\Delta\sigma_R$] Applied constant-amplitude stress range to find the fatigue life for [$MPa$].
            For shear curves this is the applied shear stress range [$\Delta\tau_R$].
        point : Literal["C", "D"]
            Reference point of the governing branch. ``"C"`` for the first branch (slope [$m_1$]),
            ``"D"`` for the second branch (slope [$m_2$]).
        stress_type : StressType
            Whether the curve is a normal-stress or shear-stress curve. Only affects the rendered symbol
            ([$\Delta\sigma$] vs [$\Delta\tau$]); the value is the same.

        Returns
        -------
        None
        """
        super().__init__()
        self.delta_sigma_ref: MPA = delta_sigma_ref
        self.n_ref: DIMENSIONLESS = n_ref
        self.m: DIMENSIONLESS = m
        self.delta_sigma_r: MPA = delta_sigma_r
        self.point: Literal["C", "D"] = point
        self.stress_type: StressType = stress_type

    @staticmethod
    def _evaluate(
        delta_sigma_ref: MPA,
        n_ref: DIMENSIONLESS,
        m: DIMENSIONLESS,
        delta_sigma_r: MPA,
        point: Literal["C", "D"],
        stress_type: StressType,  # noqa: ARG004
    ) -> DIMENSIONLESS:
        """Evaluates the formula, for more information see the __init__ method."""
        if point not in _SLOPE_SUBSCRIPT:
            raise ValueError(f"Invalid point: {point}. Must be 'C' or 'D'.")
        # delta_sigma_ref is the numerator reference strength; a zero would give a nonsensical N_R = 0, so require it > 0 too.
        raise_if_less_or_equal_to_zero(n_ref=n_ref, m=m, delta_sigma_r=delta_sigma_r, delta_sigma_ref=delta_sigma_ref)
        return n_ref * (delta_sigma_ref / delta_sigma_r) ** m

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for the fatigue life curve value (Δτ symbol for shear curves)."""
        # Unlike the strength curve value (which is only ever rendered for normal-stress limits), this engine is
        # delegated to for the shear curve as well, so it carries the stress type to switch the rendered symbol.
        symbol = r"\Delta\tau" if self.stress_type == StressType.SHEAR else r"\Delta\sigma"
        ref = self.point
        slope_sub = _SLOPE_SUBSCRIPT[self.point]
        # The slope m is an integer (m1, m2 in {3, 5, 9}), so trailing zeros are stripped to keep the exponent clean.
        slope_str = f"{self.m:.{n}f}"
        if "." in slope_str:
            slope_str = slope_str.rstrip("0").rstrip(".")
        return LatexFormula(
            return_symbol="N_{R}",
            result=f"{self:.0f}",
            equation=rf"N_{{{ref}}} \left( \frac{{{symbol}_{{{ref}}}}}{{{symbol}_{{R}}}} \right)^{{m_{{{slope_sub}}}}}",
            numeric_equation=(
                rf"{latex_scientific(self.n_ref)} \left( \frac{{{self.delta_sigma_ref:.{n}f}}}{{{self.delta_sigma_r:.{n}f}}} \right)"
                rf"^{{{slope_str}}}"
            ),
            comparison_operator_label="=",
        )
