"""Fatigue strength curve value from EN 1993-1-9:2025: Chapter 8 - Fatigue resistance."""

from typing import Literal

from blueprints.codes.eurocode.en_1993_1_9_2025 import EN_1993_1_9_2025
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_scientific
from blueprints.type_alias import DIMENSIONLESS, MPA
from blueprints.validations import raise_if_less_or_equal_to_zero

# Latex subscripts of the reference and target points of the fatigue strength curve for each variant.
# point "D": constant amplitude fatigue limit, derived from the detail category C with the first slope m1.
# point "L": cut-off limit, derived from the constant amplitude fatigue limit D with the second slope m2.
_POINT_SYMBOLS: dict[str, dict[str, str]] = {
    "D": {"out": "D", "ref": "C", "slope": "1"},
    "L": {"out": "L", "ref": "D", "slope": "2"},
}


class Form8FatigueStrengthCurveValue(Formula):
    r"""Class representing the relation that gives a fatigue strength on the fatigue strength curve [$\Delta\sigma_D$] or [$\Delta\sigma_L$].

    This relation is not stated explicitly in EN 1993-1-9:2025, but follows directly from the constant-slope fatigue strength curves of
    chapter 8. The same expression yields:

    - the constant amplitude fatigue limit [$\Delta\sigma_D$] from the detail category [$\Delta\sigma_C$] with the first slope [$m_1$], and
    - the cut-off limit [$\Delta\sigma_L$] from the constant amplitude fatigue limit [$\Delta\sigma_D$] with the second slope [$m_2$].

    The variant is selected through the ``point`` argument.
    """

    label = "Figures 8.1-8.4 (fatigue strength curve value)"
    source_document = EN_1993_1_9_2025

    def __init__(
        self,
        delta_sigma_ref: MPA,
        n_ref: DIMENSIONLESS,
        n_target: DIMENSIONLESS,
        m: DIMENSIONLESS,
        point: Literal["D", "L"],
    ) -> None:
        r"""[$\Delta\sigma_D$] or [$\Delta\sigma_L$] Fatigue strength at a reference point of the fatigue strength curve [$MPa$].

        EN 1993-1-9:2025 - Chapter 8 - Fatigue resistance (derived from the fatigue strength curves)

        [$\Delta\sigma_{out} = \Delta\sigma_{ref} \left( \frac{N_{ref}}{N_{out}} \right)^{1 / m}$]

        With ``point="D"`` the constant amplitude fatigue limit is obtained from the detail category
        ([$\Delta\sigma_D = \Delta\sigma_C \left( N_C / N_D \right)^{1 / m_1}$]).
        With ``point="L"`` the cut-off limit is obtained from the constant amplitude fatigue limit
        ([$\Delta\sigma_L = \Delta\sigma_D \left( N_D / N_L \right)^{1 / m_2}$]).

        Parameters
        ----------
        delta_sigma_ref : MPA
            [$\Delta\sigma_{ref}$] Reference fatigue strength: the detail category [$\Delta\sigma_C$] for ``point="D"``,
            or the constant amplitude fatigue limit [$\Delta\sigma_D$] for ``point="L"`` [$MPa$].
        n_ref : DIMENSIONLESS
            [$N_{ref}$] Number of cycles at the reference point: [$N_C$] for ``point="D"`` or [$N_D$] for ``point="L"`` [$-$].
        n_target : DIMENSIONLESS
            [$N_{out}$] Number of cycles at the target point: [$N_D$] for ``point="D"`` or [$N_L$] for ``point="L"`` [$-$].
        m : DIMENSIONLESS
            [$m$] Slope of the relevant part of the fatigue strength curve: [$m_1$] for ``point="D"`` or [$m_2$] for ``point="L"`` [$-$].
        point : Literal["D", "L"]
            Reference point to compute. ``"D"`` for the constant amplitude fatigue limit [$\Delta\sigma_D$],
            ``"L"`` for the cut-off limit [$\Delta\sigma_L$].

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

    @staticmethod
    def _evaluate(
        delta_sigma_ref: MPA,
        n_ref: DIMENSIONLESS,
        n_target: DIMENSIONLESS,
        m: DIMENSIONLESS,
        point: Literal["D", "L"],
    ) -> MPA:
        """Evaluates the formula, for more information see the __init__ method."""
        if point not in _POINT_SYMBOLS:
            raise ValueError(f"Invalid point: {point}. Must be 'D' or 'L'.")
        # delta_sigma_ref is the numerator reference strength; a zero would give a nonsensical zero strength, so require it > 0 too.
        raise_if_less_or_equal_to_zero(n_ref=n_ref, n_target=n_target, m=m, delta_sigma_ref=delta_sigma_ref)
        return delta_sigma_ref * (n_ref / n_target) ** (1 / m)

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for the fatigue strength curve value."""
        symbols = _POINT_SYMBOLS[self.point]
        out, ref, slope = symbols["out"], symbols["ref"], symbols["slope"]
        # The slope m is an integer (m1 = 3, m2 = 5), so trailing zeros are stripped to keep the exponent clean.
        m_str = f"{self.m:.{n}f}"
        if "." in m_str:
            m_str = m_str.rstrip("0").rstrip(".")
        return LatexFormula(
            return_symbol=rf"\Delta\sigma_{{{out}}}",
            result=f"{self:.{n}f}",
            equation=rf"\Delta\sigma_{{{ref}}} \left( \frac{{N_{{{ref}}}}}{{N_{{{out}}}}} \right)^{{1 / m_{{{slope}}}}}",
            numeric_equation=(
                rf"{self.delta_sigma_ref:.{n}f} \left( \frac{{{latex_scientific(self.n_ref)}}}{{{latex_scientific(self.n_target)}}} \right)"
                rf"^{{1 / {m_str}}}"
            ),
            comparison_operator_label="=",
            unit="MPa",
        )
