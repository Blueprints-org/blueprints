"""Formula 8.4 from NEN-EN 1992-1-1+C2:2011: Chapter 8: Detailing of reinforcement and prestressing tendons."""

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011 import NEN_EN_1992_1_1_C2_2011
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_max_curly_brackets
from blueprints.type_alias import DIMENSIONLESS, MM
from blueprints.validations import raise_if_negative


class Form8Dot4DesignAnchorageLength(Formula):
    """Class representing formula 8.4 for the calculation of the design anchorage length :math:`l_{bd}` [mm]."""

    label = "8.4"
    source_document = NEN_EN_1992_1_1_C2_2011

    def __init__(
        self,
        alpha_1: DIMENSIONLESS,
        alpha_2: DIMENSIONLESS,
        alpha_3: DIMENSIONLESS,
        alpha_4: DIMENSIONLESS,
        alpha_5: DIMENSIONLESS,
        l_b_rqd: MM,
        l_b_min: MM,
    ) -> None:
        """[:math:`l_{bd}`] Design anchorage length [:math:`mm`].

        NEN-EN 1992-1-1+C2:2011 art.8.4.4(1) - Formula (8.4)

        Parameters
        ----------
        alpha_1 : DIMENSIONLESS
            [:math:`α_{1}`] Coefficient for the effect of the form of the bars assuming adequate cover (see figure 8.1) [-].

            :math:`= 1.0` for bars in compression.

            :math:`= 1.0` for straight bars in tension.

            :math:`= 1.0 if c_{d} <= 3 ⋅ Ø` for bars other than straight in tension (see figure 8.1 (b), (c) and (d)).

            :math:`= 0.7 if c_{d} > 3 ⋅ Ø` for bars other than straight in tension (see figure 8.1 (b), (c) and (d)).

            Note: see figure 8.3 for values of :math:`c_{d}`.
        alpha_2 : DIMENSIONLESS
            [:math:`α_{2}`] Coefficient for the effect of minimum concrete cover (see figure 8.3) [-].

            :math:`= 1.0` for bars in compression.

            :math:`= 1 - 0.15 ⋅ (c_{d} - Ø) / Ø <= 1` with a minimum of 0.7 for straight bars in tension.

            :math:`= 1 - 0.15 ⋅ (c_{d} - 3 ⋅ Ø) / Ø <= 1` with a minimum of 0.7 for bars other than
            straight in tension (see figure 8.1 (b), (c) and (d)).

            Note: see figure 8.3 for values of :math:`c_{d}`.
        alpha_3 : DIMENSIONLESS
            [:math:`α_{3}`] Coefficient for the effect of confinement by transverse reinforcement [-].

            :math:`= 1.0` for bars in compression.

            :math:`= 1 - K ⋅ λ <= 1` with a minimum of 0.7 for bars in tension.

            Where: :math:`λ = (ΣA_{st} - ΣA_{st,min}) / A_{s}`.

            Where: :math:`ΣA_{st,min}` = cross-sectional area of the minimum transverse
            reinforcement :math:`= 0,25 ⋅ A_{s}` for beams and 0 for slabs.

            Note: see figure 8.4 for values of :math:`K, A_{s} and A_{st}`.
        alpha_4 : DIMENSIONLESS
            [:math:`α_{4}`] Coefficient for the influence of one or more welded transverse bars :math:`(Ø_{t} > 0,6 Ø)` along the design anchorage
            length :math:`l_{bd}` (see 8.6) [-].

            :math:`= 0.7` for all types, position and size as specified in figure 8.6 (e) in both tension and compression.

        alpha_5 : DIMENSIONLESS
            [:math:`α_{5}`] Coefficient for the effect of the pressure transverse to the plane of splitting
            along the design anchorage length :math:`l_{bd}` (see 8.6) [-].

            :math:`= 1 - 0.04 ⋅ p <= 1` with a minimum of 0.7 for all types of anchorage in compression.

            Where: p = transverse pressure at ultimate limit state along :math:`l_{bd}` [MPa].
        l_b_rqd: MM
            [:math:`l_{b,rqd}`] Basic required anchorage length, for anchoring the force As⋅σsd in a straight bar assuming constant
            bond stress (formula 8.3) [:math:`mm`].

            Use your own implementation for this value or use the :class:`Form8Dot3RequiredAnchorageLength` class.
        l_b_min : MM
            [:math:`l_{b,min}`] Minimum anchorage length if no other limitation is applied [:math:`mm`].

            :math:`= max(0.3 ⋅ l_{b,rqd}, 10 ⋅ Ø, 100)` for tension anchorage (formula 8.6).
            :math:`= max(0.6 ⋅ l_{b,rqd}, 10 ⋅ Ø, 100)` for compression anchorage (formula 8.7).

            Use your own implementation of this formula or use the :class:`Form8Dot6MinimumTensionAnchorage` class for tension or
            :class:`Form8Dot7MinimumCompressionAnchorage` for compression.

        Notes
        -----
        NEN-EN 1992-1-1+C2:2011 art.8.4.4(1) - Formula (8.5) prescribes that :math:`(α_{2} ⋅ α_{3} ⋅ α_{5}) >= 0.7`.
        """
        super().__init__()
        self.alpha_1 = alpha_1
        self.alpha_2 = alpha_2
        self.alpha_3 = alpha_3
        self.alpha_4 = alpha_4
        self.alpha_5 = alpha_5
        self.l_b_rqd = l_b_rqd
        self.l_b_min = l_b_min

    @staticmethod
    def _evaluate(
        alpha_1: DIMENSIONLESS,
        alpha_2: DIMENSIONLESS,
        alpha_3: DIMENSIONLESS,
        alpha_4: DIMENSIONLESS,
        alpha_5: DIMENSIONLESS,
        l_b_rqd: MM,
        l_b_min: MM,
    ) -> MM:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(
            alpha_1=alpha_1,
            alpha_2=alpha_2,
            alpha_3=alpha_3,
            alpha_4=alpha_4,
            alpha_5=alpha_5,
            l_b_rqd=l_b_rqd,
            l_b_min=l_b_min,
        )
        return max(alpha_1 * alpha_2 * alpha_3 * alpha_4 * alpha_5 * l_b_rqd, l_b_min)

    def latex(self) -> LatexFormula:
        """Returns a LatexFormula representation of the formula."""
        return LatexFormula(
            return_symbol=r"l_{bd}",
            result=f"{self:.2f}",
            equation=latex_max_curly_brackets(r"\alpha_1 \cdot \alpha_2 \cdot \alpha_3 \cdot \alpha_4 \cdot \alpha_5 \cdot l_{b,rqd}", r"l_{b,min}"),
            numeric_equation=latex_max_curly_brackets(
                rf"{self.alpha_1} \cdot {self.alpha_2} \cdot {self.alpha_3} \cdot {self.alpha_4} \cdot {self.alpha_5} \cdot {self.l_b_rqd:.2f}",
                self.l_b_min,
            ),
            comparison_operator_label="=",
        )
