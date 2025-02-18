r"""Formula 8.4 from NEN-EN 1992-1-1+C2:2011: Chapter 8: Detailing of reinforcement and prestressing tendons."""

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011 import NEN_EN_1992_1_1_C2_2011
from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011.chapter_8_detailing_of_reinforcement_and_prestressing_tendons.formula_8_5 import (
    Form8Dot5ProductAlphas235,
)
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_max_curly_brackets
from blueprints.type_alias import MM, RATIO
from blueprints.validations import raise_if_negative


class Form8Dot4DesignAnchorageLength(Formula):
    r"""Class representing formula 8.4 for the calculation of the design anchorage length [$l_{bd}$] [$mm$]."""

    label = "8.4"
    source_document = NEN_EN_1992_1_1_C2_2011

    def __init__(
        self,
        alpha_1: RATIO,
        alpha_2: RATIO,
        alpha_3: RATIO,
        alpha_4: RATIO,
        alpha_5: RATIO,
        l_b_rqd: MM,
        l_b_min: MM,
        min_product_alpha_2_3_5: RATIO | None = None,
    ) -> None:
        r"""[$l_{bd}$] Design anchorage length [$mm$].

        NEN-EN 1992-1-1+C2:2011 art.8.4.4(1) - Formula (8.4)

        Parameters
        ----------
        alpha_1 : RATIO
            [$α_{1}$] Coefficient for the effect of the form of the bars assuming adequate cover (see figure 8.1) [$-$].
            [$= 1.0$] for bars in compression.
            [$= 1.0$] for straight bars in tension.
            [$= 1.0 \text{ if } c_{d} \leq 3 ⋅ Ø$] for bars other than straight in tension (see figure 8.1 (b), (c) and (d)).
            [$= 0.7 \text{ if } c_{d} > 3 ⋅ Ø$] for bars other than straight in tension (see figure 8.1 (b), (c) and (d)).
            Note: see figure 8.3 for values of [$c_{d}$].
        alpha_2 : RATIO
            [$α_{2}$] Coefficient for the effect of minimum concrete cover (see figure 8.3) [$-$].
            [$= 1.0$] for bars in compression.
            [$= 1 - 0.15 ⋅ (c_{d} - Ø) / Ø \leq 1$] with a minimum of 0.7 for straight bars in tension.
            [$= 1 - 0.15 ⋅ (c_{d} - 3 ⋅ Ø) / Ø \leq 1$] with a minimum of 0.7 for bars other than
            straight in tension (see figure 8.1 (b), (c) and (d)).
            Note: see figure 8.3 for values of [$c_{d}$].
        alpha_3 : RATIO
            [$α_{3}$] Coefficient for the effect of confinement by transverse reinforcement [$-$].
            [$= 1.0$] for bars in compression.
            [$= 1 - K ⋅ λ \leq 1$] with a minimum of 0.7 for bars in tension.
            Where: [$λ = (\Sigma A_{st} - \Sigma A_{st,min}) / A_{s}$].
            Where: [$\Sigma A_{st,min}$] = cross-sectional area of the minimum transverse
            reinforcement [$= 0,25 ⋅ A_{s}$] for beams and 0 for slabs.
            Note: see figure 8.4 for values of [$K, A_{s}$] and [$A_{st}$].
        alpha_4 : RATIO
            [$α_{4}$] Coefficient for the influence of one or more welded transverse bars [$Ø_{t} > 0,6 Ø$] along the design anchorage
            length [$l_{bd}$] (see 8.6) [$-$].
            [$= 0.7$] for all types, position and size as specified in figure 8.6 (e) in both tension and compression.
        alpha_5 : RATIO
            [$α_{5}$] Coefficient for the effect of the pressure transverse to the plane of splitting
            along the design anchorage length [$l_{bd}$] (see 8.6) [$-$].
            [$= 1 - 0.04 ⋅ p \leq 1$] with a minimum of 0.7 for all types of anchorage in compression.
            Where: p = transverse pressure at ultimate limit state along [$l_{bd}$] [$MPa$].
        l_b_rqd: MM
            [$l_{b,rqd}$] Basic required anchorage length, for anchoring the force [$A_{s}⋅σ_{sd}$] in a straight bar assuming constant
            bond stress (formula 8.3) [$mm$].
            Use your own implementation for this value or use the :class:`Form8Dot3RequiredAnchorageLength` class.
        l_b_min : MM
            [$l_{b,min}$] Minimum anchorage length if no other limitation is applied [$mm$].
            [$= \max(0.3 ⋅ l_{b,rqd}, 10 ⋅ Ø, 100)$] for tension anchorage (formula 8.6).
            [$= \max(0.6 ⋅ l_{b,rqd}, 10 ⋅ Ø, 100)$] for compression anchorage (formula 8.7).
            Use your own implementation of this formula or use the :class:`Form8Dot6MinimumTensionAnchorage` class for tension or
            :class:`Form8Dot7MinimumCompressionAnchorage` for compression.
        min_product_alpha_2_3_5: RATIO | None
            Minimum value of the product of factors [$α_{2}$], [$α_{3}$] and [$α_{5}$].
            When this argument is None, :class: `Form8Dot5ProductAlphas235` is used for this condition.
            When this argument is given, the condition [$\max(α_{2}⋅α_{3}⋅α_{5}) \geq$] min_product_alpha_2_3_5 is used.

        Notes
        -----
        NEN-EN 1992-1-1+C2:2011 art.8.4.4(1) - Formula (8.5) prescribes that [$α_{2} ⋅ α_{3} ⋅ α_{5} \geq 0.7$].
        """
        super().__init__()
        self.alpha_1 = alpha_1
        self.alpha_2 = alpha_2
        self.alpha_3 = alpha_3
        self.alpha_4 = alpha_4
        self.alpha_5 = alpha_5
        self.l_b_rqd = l_b_rqd
        self.l_b_min = l_b_min
        self.min_product_alpha_2_3_5 = min_product_alpha_2_3_5

    @staticmethod
    def _evaluate(
        alpha_1: RATIO,
        alpha_2: RATIO,
        alpha_3: RATIO,
        alpha_4: RATIO,
        alpha_5: RATIO,
        l_b_rqd: MM,
        l_b_min: MM,
        min_product_alpha_2_3_5: RATIO | None = None,
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

        if min_product_alpha_2_3_5 is None:
            product_alphas_2_3_5: float = Form8Dot5ProductAlphas235(alpha_2=alpha_2, alpha_3=alpha_3, alpha_5=alpha_5)
        else:
            product_alphas_2_3_5 = max(alpha_2 * alpha_3 * alpha_5, min_product_alpha_2_3_5)

        return max(alpha_1 * alpha_4 * product_alphas_2_3_5 * l_b_rqd, l_b_min)

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
