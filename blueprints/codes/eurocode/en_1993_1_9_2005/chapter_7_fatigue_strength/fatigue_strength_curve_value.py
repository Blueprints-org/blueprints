"""Fatigue strength curve value from EN 1993-1-9:2005: Chapter 7 - Fatigue strength."""

from typing import Literal

from blueprints.codes.eurocode.en_1993_1_9_2005 import EN_1993_1_9_2005
from blueprints.codes.eurocode.en_1993_1_9_2005.chapter_7_fatigue_strength.fatigue_strength_curve import StressType
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_scientific
from blueprints.type_alias import DIMENSIONLESS, MPA
from blueprints.validations import raise_if_less_or_equal_to_zero

# Latex subscript of the reference point for each (target point, stress type) pair of the fatigue strength curves.
# Direct stress (Figure 7.1): D is reached from the detail category C along the first branch, and L from D along the
# second branch. Shear stress (Figure 7.2): the single-slope curve runs straight from C to the cut-off limit L, so
# there is no point D.
_REF_POINTS: dict[tuple[str, StressType], str] = {
    ("D", StressType.DIRECT): "C",
    ("L", StressType.DIRECT): "D",
    ("L", StressType.SHEAR): "C",
}


class Form7FatigueStrengthCurveValue(Formula):
    r"""Class representing the relation that gives a fatigue strength on the fatigue strength curve [$\Delta\sigma_D$] or [$\Delta\sigma_L$].

    This relation is the rearranged form of the fatigue strength curve relations of EN 1993-1-9:2005, 7.1(2) and 7.1(3)
    ([$\Delta\sigma_R^m \: N_R = \Delta\sigma_C^m \: 2 \cdot 10^6$]). The same expression yields:

    - the constant amplitude fatigue limit [$\Delta\sigma_D = (2/5)^{1/3} \Delta\sigma_C$] from the detail category
      [$\Delta\sigma_C$] (direct stress, 7.1(2)),
    - the cut-off limit [$\Delta\sigma_L = (5/100)^{1/5} \Delta\sigma_D$] from the constant amplitude fatigue limit
      [$\Delta\sigma_D$] (direct stress, 7.1(3)), and
    - the cut-off limit [$\Delta\tau_L = (2/100)^{1/5} \Delta\tau_C$] from the detail category [$\Delta\tau_C$]
      (shear stress, 7.1(2)).

    The variant is selected through the ``point`` and ``stress_type`` arguments.
    """

    label = "Figures 7.1-7.2 (fatigue strength curve value)"
    source_document = EN_1993_1_9_2005

    def __init__(
        self,
        delta_sigma_ref: MPA,
        n_ref: DIMENSIONLESS,
        n_target: DIMENSIONLESS,
        m: DIMENSIONLESS,
        point: Literal["D", "L"],
        stress_type: StressType,
    ) -> None:
        r"""[$\Delta\sigma_D$] or [$\Delta\sigma_L$] Fatigue strength at a reference point of the fatigue strength curve [$MPa$].

        EN 1993-1-9:2005 - Chapter 7 - Fatigue strength (rearranged from the relations in 7.1(2) and 7.1(3))

        [$\Delta\sigma_{out} = \Delta\sigma_{ref} \left( \frac{N_{ref}}{N_{out}} \right)^{1 / m}$]

        With ``point="D"`` the constant amplitude fatigue limit is obtained from the detail category
        ([$\Delta\sigma_D = \Delta\sigma_C \left( N_C / N_D \right)^{1 / m}$], direct stress only).
        With ``point="L"`` the cut-off limit is obtained from the constant amplitude fatigue limit for direct stress
        ([$\Delta\sigma_L = \Delta\sigma_D \left( N_D / N_L \right)^{1 / m}$]) or straight from the detail category
        for shear stress ([$\Delta\tau_L = \Delta\tau_C \left( N_C / N_L \right)^{1 / m}$]).

        Parameters
        ----------
        delta_sigma_ref : MPA
            [$\Delta\sigma_{ref}$] Reference fatigue strength: the detail category [$\Delta\sigma_C$] or, for the
            direct-stress cut-off limit, the constant amplitude fatigue limit [$\Delta\sigma_D$] [$MPa$].
        n_ref : DIMENSIONLESS
            [$N_{ref}$] Number of cycles at the reference point: [$N_C$] or, for the direct-stress cut-off limit,
            [$N_D$] [$-$].
        n_target : DIMENSIONLESS
            [$N_{out}$] Number of cycles at the target point: [$N_D$] for ``point="D"`` or [$N_L$] for ``point="L"`` [$-$].
        m : DIMENSIONLESS
            [$m$] Slope of the relevant branch of the fatigue strength curve [$-$].
        point : Literal["D", "L"]
            Reference point to compute. ``"D"`` for the constant amplitude fatigue limit [$\Delta\sigma_D$]
            (direct stress only), ``"L"`` for the cut-off limit [$\Delta\sigma_L$] or [$\Delta\tau_L$].
        stress_type : StressType
            Whether the curve is a direct-stress or shear-stress curve. Fixes the reference point the target is
            derived from and the rendered symbol ([$\Delta\sigma$] vs [$\Delta\tau$]).

        Returns
        -------
        None
        """
        super().__init__()
        self.delta_sigma_ref: MPA = delta_sigma_ref
        self.n_ref: DIMENSIONLESS = n_ref
        self.n_target: DIMENSIONLESS = n_target
        self.m: DIMENSIONLESS = m
        self.point: Literal["D", "L"] = point
        self.stress_type: StressType = stress_type

    @staticmethod
    def _evaluate(
        delta_sigma_ref: MPA,
        n_ref: DIMENSIONLESS,
        n_target: DIMENSIONLESS,
        m: DIMENSIONLESS,
        point: Literal["D", "L"],
        stress_type: StressType,
    ) -> MPA:
        """Evaluates the formula, for more information see the __init__ method."""
        if (point, stress_type) not in _REF_POINTS:
            raise ValueError(
                f"Invalid point: {point} for {stress_type}. Must be 'D' (direct stress only, the shear curve of "
                "Figure 7.2 has no constant amplitude fatigue limit) or 'L'."
            )
        # delta_sigma_ref is the numerator reference strength; a zero would give a nonsensical zero strength, so require it > 0 too.
        raise_if_less_or_equal_to_zero(n_ref=n_ref, n_target=n_target, m=m, delta_sigma_ref=delta_sigma_ref)
        return delta_sigma_ref * (n_ref / n_target) ** (1 / m)

    def latex(self, n: int = 3) -> LatexFormula:
        r"""Returns LatexFormula object for the fatigue strength curve value ([$\Delta\tau$] symbol for shear curves)."""
        symbol = r"\Delta\tau" if self.stress_type == StressType.SHEAR else r"\Delta\sigma"
        ref = _REF_POINTS[(self.point, self.stress_type)]
        # The slope m is an integer (3 or 5), so trailing zeros are stripped to keep the exponent clean.
        m_str = f"{self.m:.{n}f}"
        if "." in m_str:
            m_str = m_str.rstrip("0").rstrip(".")
        return LatexFormula(
            return_symbol=rf"{symbol}_{{{self.point}}}",
            result=f"{self:.{n}f}",
            equation=rf"{symbol}_{{{ref}}} \left( \frac{{N_{{{ref}}}}}{{N_{{{self.point}}}}} \right)^{{1 / m}}",
            numeric_equation=(
                rf"{self.delta_sigma_ref:.{n}f} \left( \frac{{{latex_scientific(self.n_ref)}}}{{{latex_scientific(self.n_target)}}} \right)"
                rf"^{{1 / {m_str}}}"
            ),
            comparison_operator_label="=",
            unit="MPa",
        )
