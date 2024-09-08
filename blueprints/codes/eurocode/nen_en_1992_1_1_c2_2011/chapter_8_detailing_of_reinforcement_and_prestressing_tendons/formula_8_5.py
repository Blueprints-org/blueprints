"""Formula 8.5 from NEN-EN 1992-1-1+C2:2011: Chapter 8: Detailing of reinforcement and prestressing tendons."""

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011 import NEN_EN_1992_1_1_C2_2011
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula
from blueprints.type_alias import RATIO
from blueprints.validations import raise_if_negative


class Form8Dot5ProductAlphas235(Formula):
    """Class representing formula 8.5 for the calculating the product of α_{2}, α_{3} α_{5} [-]."""

    label = "8.5"
    source_document = NEN_EN_1992_1_1_C2_2011

    def __init__(
        self,
        alpha_2: RATIO,
        alpha_3: RATIO,
        alpha_5: RATIO,
    ) -> None:
        """Calculate the product of α_{2}, α_{3} and α_{5} [:math:`-`].

        NEN-EN 1992-1-1+C2:2011 art.8.4.4(1) - Formula (8.5) prescribes that :math:`(α_{2} ⋅ α_{3} ⋅ α_{5}) ≥ 0.7`.
        Used by NEN-EN 1992-1-1+C2:2011 art.8.4.4(1) - Formula (8.4)

        Parameters
        ----------
        alpha_2 : RATIO
            [:math:`α_{2}`] Coefficient for the effect of minimum concrete cover (see figure 8.3) [-].

            :math:`= 1.0` for bars in compression.

            :math:`= 1 - 0.15 ⋅ (c_{d} - Ø) / Ø <= 1` with a minimum of 0.7 for straight bars in tension.

            :math:`= 1 - 0.15 ⋅ (c_{d} - 3 ⋅ Ø) / Ø <= 1` with a minimum of 0.7 for bars other than
            straight in tension (see figure 8.1 (b), (c) and (d)).

            Note: see figure 8.3 for values of :math:`c_{d}`.
        alpha_3 : RATIO
            [:math:`α_{3}`] Coefficient for the effect of confinement by transverse reinforcement [-].

            :math:`= 1.0` for bars in compression.

            :math:`= 1 - K ⋅ λ <= 1` with a minimum of 0.7 for bars in tension.

            Where: :math:`λ = (ΣA_{st} - ΣA_{st,min}) / A_{s}`.

            Where: :math:`ΣA_{st,min}` = cross-sectional area of the minimum transverse
            reinforcement :math:`= 0,25 ⋅ A_{s}` for beams and 0 for slabs.

            Note: see figure 8.4 for values of :math:`K, A_{s} and A_{st}`.

        alpha_5 : RATIO
            [:math:`α_{5}`] Coefficient for the effect of the pressure transverse to the plane of splitting
            along the design anchorage length :math:`l_{bd}` (see 8.6) [-].

            :math:`= 1 - 0.04 ⋅ p <= 1` with a minimum of 0.7 for all types of anchorage in compression.

            Where: p = transverse pressure at ultimate limit state along :math:`l_{bd}` [MPa].
        """
        super().__init__()
        self.alpha_2 = alpha_2
        self.alpha_3 = alpha_3
        self.alpha_5 = alpha_5

    @staticmethod
    def _evaluate(
        alpha_2: RATIO,
        alpha_3: RATIO,
        alpha_5: RATIO,
    ) -> RATIO:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(
            alpha_2=alpha_2,
            alpha_3=alpha_3,
            alpha_5=alpha_5,
        )

        # The product of alpha values 2, 3, 5 can't be smaller than 0.7
        return max(alpha_2 * alpha_3 * alpha_5, 0.7)

    def latex(self) -> LatexFormula:
        """Returns a LatexFormula representation of the formula."""
        return LatexFormula(
            return_symbol="",
            result=f"{self:.2f}",
            equation=r"\alpha_2 \cdot \alpha_3 \cdot \alpha_5 \ge 0.7",
            numeric_equation=rf"{self.alpha_2} \cdot {self.alpha_3} \cdot {self.alpha_5} \ge 0.7",
            comparison_operator_label="\\to",
        )
