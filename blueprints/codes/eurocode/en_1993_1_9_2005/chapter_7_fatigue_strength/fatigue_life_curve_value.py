"""Fatigue life curve value from EN 1993-1-9:2005: Chapter 7 - Fatigue strength."""

from typing import Literal

from blueprints.codes.eurocode.en_1993_1_9_2005 import EN_1993_1_9_2005
from blueprints.codes.eurocode.en_1993_1_9_2005.chapter_7_fatigue_strength.fatigue_strength_curve import StressType
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_scientific
from blueprints.type_alias import DIMENSIONLESS, MPA
from blueprints.validations import raise_if_less_or_equal_to_zero

# Reference points that can anchor a branch of the fatigue strength curves.
# Direct stress (Figure 7.1): the first branch is anchored at the detail category C, the second branch at the
# constant amplitude fatigue limit D. Shear stress (Figure 7.2): the single slope is anchored at C; there is no D.
_ANCHOR_POINTS: dict[tuple[str, StressType], str] = {
    ("C", StressType.DIRECT): "C",
    ("D", StressType.DIRECT): "D",
    ("C", StressType.SHEAR): "C",
}


class Form7FatigueLifeCurveValue(Formula):
    r"""Class representing the relation that gives the fatigue life [$N_R$] on a branch of a fatigue strength curve.

    This relation is the rearranged form of the fatigue strength curve relations of EN 1993-1-9:2005, 7.1(2) and
    7.1(3) ([$\Delta\sigma_R^m \: N_R = \Delta\sigma_C^m \: 2 \cdot 10^6$]): it reads the number of cycles [$N_R$]
    at which an applied stress range [$\Delta\sigma_R$] meets a single (constant-slope) branch of the curve. The
    same expression yields the life on either branch:

    - the first branch anchored at the detail category [$\Delta\sigma_C$] (point ``"C"``, both curves), and
    - the second branch anchored at the constant amplitude fatigue limit [$\Delta\sigma_D$] (point ``"D"``,
      direct stress only, 7.1(3)).

    The variant is selected through the ``point`` argument. The branch below the cut-off limit gives infinite life
    and is therefore not a curve value; it is handled by the caller (see :class:`Form7FatigueLife`).
    """

    label = "Figures 7.1-7.2 (fatigue life curve value)"
    source_document = EN_1993_1_9_2005

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

        EN 1993-1-9:2005 - Chapter 7 - Fatigue strength (rearranged from the relations in 7.1(2) and 7.1(3))

        [$N_R = N_{ref} \left( \frac{\Delta\sigma_{ref}}{\Delta\sigma_R} \right)^{m}$]

        With ``point="C"`` the life is read on the first branch from the detail category
        ([$N_R = N_C \left( \Delta\sigma_C / \Delta\sigma_R \right)^{m}$]).
        With ``point="D"`` the life is read on the second branch of the direct stress curve from the constant
        amplitude fatigue limit ([$N_R = N_D \left( \Delta\sigma_D / \Delta\sigma_R \right)^{m}$]).

        Parameters
        ----------
        delta_sigma_ref : MPA
            [$\Delta\sigma_{ref}$] Reference fatigue strength of the branch: the detail category [$\Delta\sigma_C$]
            for ``point="C"``, or the constant amplitude fatigue limit [$\Delta\sigma_D$] for ``point="D"`` [$MPa$].
        n_ref : DIMENSIONLESS
            [$N_{ref}$] Number of cycles at the reference point: [$N_C$] for ``point="C"`` or [$N_D$] for ``point="D"`` [$-$].
        m : DIMENSIONLESS
            [$m$] Slope of the branch [$-$].
        delta_sigma_r : MPA
            [$\Delta\sigma_R$] Applied constant-amplitude stress range to find the fatigue life for [$MPa$].
            For the shear curve this is the applied shear stress range [$\Delta\tau_R$].
        point : Literal["C", "D"]
            Reference point of the governing branch. ``"C"`` for the first branch, ``"D"`` for the second branch
            of the direct stress curve.
        stress_type : StressType
            Whether the curve is a direct-stress or shear-stress curve. Only affects the rendered symbol
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
        stress_type: StressType,
    ) -> DIMENSIONLESS:
        """Evaluates the formula, for more information see the __init__ method."""
        if (point, stress_type) not in _ANCHOR_POINTS:
            raise ValueError(
                f"Invalid point: {point} for {stress_type}. Must be 'C' or, for the direct stress curve only, 'D' "
                "(the shear curve of Figure 7.2 has a single branch)."
            )
        # delta_sigma_ref is the numerator reference strength; a zero would give a nonsensical N_R = 0, so require it > 0 too.
        raise_if_less_or_equal_to_zero(n_ref=n_ref, m=m, delta_sigma_r=delta_sigma_r, delta_sigma_ref=delta_sigma_ref)
        return n_ref * (delta_sigma_ref / delta_sigma_r) ** m

    def latex(self, n: int = 3) -> LatexFormula:
        r"""Returns LatexFormula object for the fatigue life curve value ([$\Delta\tau$] symbol for the shear curve)."""
        symbol = r"\Delta\tau" if self.stress_type == StressType.SHEAR else r"\Delta\sigma"
        ref = self.point
        # The slope m is an integer (3 or 5), so trailing zeros are stripped to keep the exponent clean.
        slope_str = f"{self.m:.{n}f}"
        if "." in slope_str:
            slope_str = slope_str.rstrip("0").rstrip(".")
        return LatexFormula(
            return_symbol="N_{R}",
            result=f"{self:.0f}",
            equation=rf"N_{{{ref}}} \left( \frac{{{symbol}_{{{ref}}}}}{{{symbol}_{{R}}}} \right)^{{m}}",
            numeric_equation=(
                rf"{latex_scientific(self.n_ref)} \left( \frac{{{self.delta_sigma_ref:.{n}f}}}{{{self.delta_sigma_r:.{n}f}}} \right)"
                rf"^{{{slope_str}}}"
            ),
            comparison_operator_label="=",
        )
