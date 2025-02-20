r"""Formula 8.10 from NEN-EN 1992-1-1+C2:2011: Chapter 8: Detailing of reinforcement and prestressing tendons."""

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011 import NEN_EN_1992_1_1_C2_2011
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_max_curly_brackets, latex_min_curly_brackets
from blueprints.type_alias import DIMENSIONLESS, MM
from blueprints.validations import raise_if_negative


class Form8Dot10DesignLapLength(Formula):
    r"""Class representing formula 8.10 for the calculation of the design lap length [$l_{0}$] [$mm$]."""

    label = "8.10"
    source_document = NEN_EN_1992_1_1_C2_2011

    def __init__(
        self,
        alpha_1: DIMENSIONLESS,
        alpha_2: DIMENSIONLESS,
        alpha_3: DIMENSIONLESS,
        alpha_5: DIMENSIONLESS,
        alpha_6: DIMENSIONLESS,
        l_b_rqd: MM,
        l_0_min: MM,
    ) -> None:
        r"""[$l_{0}$] Design lap length [$mm$].

        NEN-EN 1992-1-1+C2:2011 art.8.7.3(1) - Formula (8.10)

        Parameters
        ----------
        alpha_1 : DIMENSIONLESS
            [$α_{1}$] Coefficient for the effect of the form of the bars assuming adequate cover (see figure 8.1) [$-$].

            [$= 1.0$] for bars in compression.

            [$= 1.0$] for straight bars in tension.

            [$= 1.0$] if [$c_{d} <= 3 ⋅ Ø$] for bars other than straight in tension (see figure 8.1 (b), (c) and (d)).

            [$= 0.7$] if [$c_{d} > 3 ⋅ Ø$] for bars other than straight in tension (see figure 8.1 (b), (c) and (d)).

            Note: see figure 8.3 for values of [$c_{d}$].
        alpha_2 : DIMENSIONLESS
            [$α_{2}$] Coefficient for the effect of minimum concrete cover (see figure 8.3) [$-$].

            [$= 1.0$] for bars in compression.

            [$= 1 - 0.15 ⋅ (c_{d} - Ø) / Ø <= 1$] with a minimum of 0.7 for straight bars in tension.

            [$= 1 - 0.15 ⋅ (c_{d} - 3 ⋅ Ø) / Ø <= 1$] with a minimum of 0.7 for bars other than straight in tension
            (see figure 8.1 (b), (c) and (d)).

            Note: see figure 8.3 for values of [$c_{d}$].
        alpha_3 : DIMENSIONLESS
            [$α_{3}$] Coefficient for the effect of confinement by transverse reinforcement [$-$].

            [$= 1.0$] for bars in compression.

            [$= 1 - K ⋅ λ <= 1$] with a minimum of 0.7 for bars in tension.

            Where: [$λ = (ΣA_{st} - ΣA_{st,min}) / A_{s}$].

            Where: [$ΣA_{st,min} = A_{s} ⋅ (σ_{sd}/f_{yd})$]

            With [$A_{s}$] = area of one lapped bar [$mm²$].

            Note: see figure 8.4 for values of [$K, A_{s}$] and [$A_{st}$].
        alpha_5 : DIMENSIONLESS
            [$α_{5}$] Coefficient for the effect of the pressure transverse to the plane of splitting along the design
            anchorage length [$l_{bd}$] (see 8.6) [$-$].

            [$= 1 - 0.04 ⋅ p <= 1$] with a minimum of 0.7 for all types of anchorage in compression.

            Where: p = transverse pressure at ultimate limit state along [$l_{bd}$] [$MPa$].
        alpha_6 : DIMENSIONLESS
            [$α_{6}$] Coefficient for the effect of reinforcement ratio [$-$].

            [$= (ρ_{1}/25)^{0.5} <= 1.5$] with a minimum of 1.0.

            Where: [$ρ_{1}$] = reinforcement percentage lapped within [$0,65 ⋅ l_{0}$] from the centre of the lap length
            considered (see figure 8.8) [$-$].

            Use your own implementation of this formula or use the :class:`SubForm8Dot10Alpha6` class.
        l_b_rqd : MM
            [$l_{b,rqd}$] Basic required anchorage length, for anchoring the force [$A_{s} ⋅ σ_{sd}$] in a straight bar assuming constant
            bond stress (formula 8.3) [$mm$].

            Use your own implementation for this value or use the :class:`Form8Dot3RequiredAnchorageLength` class.
        l_0_min : MM
            [$l_{0,min}$] Minimum design lap length [$mm$].

            [$= max(0.3 ⋅ α_{6} ⋅ l_{b,rqd}, 15 ⋅ Ø, 200)$] (formula 8.11).

            Use your own implementation of this formula or use :class:`Form8Dot11MinimumDesignLapLength` class.
        """
        super().__init__()
        self.alpha_1 = alpha_1
        self.alpha_2 = alpha_2
        self.alpha_3 = alpha_3
        self.alpha_5 = alpha_5
        self.alpha_6 = alpha_6
        self.l_b_rqd = l_b_rqd
        self.l_0_min = l_0_min

    @staticmethod
    def _evaluate(
        alpha_1: DIMENSIONLESS,
        alpha_2: DIMENSIONLESS,
        alpha_3: DIMENSIONLESS,
        alpha_5: DIMENSIONLESS,
        alpha_6: DIMENSIONLESS,
        l_b_rqd: MM,
        l_0_min: MM,
    ) -> MM:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(
            alpha_1=alpha_1,
            alpha_2=alpha_2,
            alpha_3=alpha_3,
            alpha_5=alpha_5,
            alpha_6=alpha_6,
            l_b_rqd=l_b_rqd,
            l_0_min=l_0_min,
        )
        return max(alpha_1 * alpha_2 * alpha_3 * alpha_5 * alpha_6 * l_b_rqd, l_0_min)

    def latex(self) -> LatexFormula:
        """Returns a LatexFormula representation of the formula."""
        return LatexFormula(
            return_symbol=r"l_{0}",
            result=f"{self:.2f}",
            equation=latex_max_curly_brackets(r"\alpha_1 \cdot \alpha_2 \cdot \alpha_3 \cdot \alpha_5 \cdot \alpha_6 \cdot l_{b,rqd}", r"l_{0,min}"),
            numeric_equation=latex_max_curly_brackets(
                rf"{self.alpha_1:.2f} \cdot {self.alpha_2:.2f} \cdot {self.alpha_3:.2f} \cdot "
                rf"{self.alpha_5:.2f} \cdot {self.alpha_6:.2f} \cdot {self.l_b_rqd:.2f}",
                f"{self.l_0_min:.2f}",
            ),
            comparison_operator_label="=",
        )


class SubForm8Dot10Alpha6(Formula):
    r"""Class representing the formula for the calculation of the coefficient [$α_{6}$]."""

    label = "8.8"
    source_document = NEN_EN_1992_1_1_C2_2011

    def __init__(self, rho_1: DIMENSIONLESS) -> None:
        r"""[$α_{6}$] Coefficient for the effect of reinforcement ratio [$-$].

        NEN-EN 1992-1-1+C2:2011 art.8.7.3(1) - Formula (8.8)

        Parameters
        ----------
        rho_1 : DIMENSIONLESS
            [$ρ_{1}$] Reinforcement percentage lapped within [$0,65 ⋅ l_{0}$] from the centre of the lap length
            considered (see figure 8.8) [$-$].
        """
        super().__init__()
        self.rho_1 = rho_1

    @staticmethod
    def _evaluate(rho_1: DIMENSIONLESS) -> DIMENSIONLESS:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(rho_l=rho_1)
        value_max_1_5 = min((rho_1 / 25) ** 0.5, 1.5)
        return max(value_max_1_5, 1)

    def latex(self) -> LatexFormula:
        """Returns a LatexFormula representation of the formula."""
        argument_1_formula = r"\left(\frac{\rho_1}{25}\right)^{0.5}"
        numerical_argument_1 = rf"\left(\frac{{{self.rho_1:.2f}}}{{25}}\right)^{{0.5}}"
        return LatexFormula(
            return_symbol=r"\alpha_6",
            result=f"{self:.2f}",
            equation=f"{latex_max_curly_brackets(latex_min_curly_brackets(argument_1_formula, '1.5'), '1')}",
            numeric_equation=f"{latex_max_curly_brackets(latex_min_curly_brackets(numerical_argument_1, '1.5'), '1')}",
            comparison_operator_label="=",
        )
