"""Formula 8.92 from FprEN 1992-1-1:2023: Chapter 8 - Ultimate Limit State."""

from blueprints.codes.eurocode.fpr_en_1992_1_1_2023 import FPR_EN_1992_1_1_2023
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import DIMENSIONLESS, MM, MPA, N
from blueprints.validations import raise_if_less_or_equal_to_zero, raise_if_negative


class Form8Dot92DesignPunchingShearStress(Formula):
    r"""Class representing formula 8.92 for the calculation of the design punching shear stress at the control
    perimeter.

    This is the simplified route of 8.4.2(6), where the concentration of the shear forces along the control
    perimeter is covered by the coefficient [$\beta_e$] of Table 8.3. Formula (8.93) of 8.4.2(7) is the
    alternative route, in which that concentration follows from a detailed analysis of the shear stress
    distribution instead.
    """

    label = "8.92"
    source_document = FPR_EN_1992_1_1_2023

    def __init__(
        self,
        beta_e: DIMENSIONLESS,
        v_ed: N,
        b_0_5: MM,
        d_v: MM,
    ) -> None:
        r"""[$\tau_{Ed}$] Design punching shear stress at the control perimeter [$b_{0,5}$] [$MPa$].

        FprEN 1992-1-1:2023 (E) art. 8.4.2(6) - Formula (8.92)

        Parameters
        ----------
        beta_e : DIMENSIONLESS
            [$\beta_e$] Coefficient accounting for concentrations of the shear forces, which may be adopted from
            Table 8.3. The approximated values for internal, edge and corner columns may be used only if all the
            conditions listed in 8.4.2(6) are fulfilled, otherwise the refined values should be adopted [$-$].
        v_ed : N
            [$V_{Ed}$] Design shear force at the control perimeter [$b_{0,5}$]. All favourable loads acting on
            the tensile side of the planar member, soil reactions on foundations and ground slabs and the
            deviation forces in post-tensioned slabs inside the control perimeter may be deducted from the shear
            force at centre of supporting area to calculate it. In the case of foundations or ground slabs
            without shear reinforcement, the soil reaction may be deducted up to a distance of [$0,67 d_v$] from
            the face of the column. Note that Formula (8.93) uses [$v_{Ed}$], a shear force per unit width in
            N/mm, which is a different quantity [$N$].
        b_0_5 : MM
            [$b_{0,5}$] Length of the control perimeter, taken at a distance [$0,5 d_v$] from the face of the
            supporting area according to 8.4.2(2) to (5) [$mm$].
        d_v : MM
            [$d_v$] Shear-resisting effective depth of the slab according to Formula (8.91) [$mm$].
        """
        super().__init__()
        self.beta_e = beta_e
        self.v_ed = v_ed
        self.b_0_5 = b_0_5
        self.d_v = d_v

    @staticmethod
    def _evaluate(
        beta_e: DIMENSIONLESS,
        v_ed: N,
        b_0_5: MM,
        d_v: MM,
    ) -> MPA:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(beta_e=beta_e, v_ed=v_ed)
        raise_if_less_or_equal_to_zero(b_0_5=b_0_5, d_v=d_v)

        return beta_e * v_ed / (b_0_5 * d_v)

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 8.92."""
        _equation: str = r"\beta_e \cdot \frac{V_{Ed}}{b_{0,5} \cdot d_v}"
        _numeric_equation: str = latex_replace_symbols(
            template=_equation,
            replacements={
                r"\beta_e": f"{self.beta_e:.{n}f}",
                r"V_{Ed}": f"{self.v_ed:.{n}f}",
                r"b_{0,5}": f"{self.b_0_5:.{n}f}",
                r"d_v": f"{self.d_v:.{n}f}",
            },
            unique_symbol_check=True,
        )
        _numeric_equation_with_units: str = latex_replace_symbols(
            template=_equation,
            replacements={
                r"\beta_e": f"{self.beta_e:.{n}f}",
                r"V_{Ed}": rf"{self.v_ed:.{n}f} \ N",
                r"b_{0,5}": rf"{self.b_0_5:.{n}f} \ mm",
                r"d_v": rf"{self.d_v:.{n}f} \ mm",
            },
            unique_symbol_check=True,
        )
        return LatexFormula(
            return_symbol=r"\tau_{Ed}",
            result=f"{self:.{n}f}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            numeric_equation_with_units=_numeric_equation_with_units,
            comparison_operator_label="=",
            unit="MPa",
        )
