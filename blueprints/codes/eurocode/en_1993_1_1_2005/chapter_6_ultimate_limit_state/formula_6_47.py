"""Formula 6.47 from EN 1993-1-1:2005: Chapter 6 - Ultimate Limit State."""

from blueprints.codes.eurocode.en_1993_1_1_2005 import EN_1993_1_1_2005
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import DIMENSIONLESS, MM2, MPA, N
from blueprints.validations import raise_if_less_or_equal_to_zero, raise_if_negative


class Form6Dot47DesignBucklingResistanceClass1And2And3(Formula):
    r"""Class representing formula 6.47 for the calculation of the design buckling resistance of a compression member
    with a Class 1, 2 or 3 cross-section.
    """

    label = "6.47"
    source_document = EN_1993_1_1_2005

    def __init__(
        self,
        chi: DIMENSIONLESS,
        a: MM2,
        f_y: MPA,
        gamma_m1: DIMENSIONLESS,
    ) -> None:
        r"""[$N_{b,Rd}$] Design buckling resistance of a compression member, for Class 1, 2 and 3 cross-sections [$N$].

        EN 1993-1-1:2005 art.6.3.1.1(3) - Formula (6.47)

        Parameters
        ----------
        chi : DIMENSIONLESS
            [$\chi$] Reduction factor for the relevant buckling mode [-].
        a : MM2
            [$A$] Area of the cross-section. Holes for fasteners at the column ends need not be taken into account,
            see art.6.3.1.1(4) [$mm^2$].
        f_y : MPA
            [$f_y$] Yield strength [$MPa$].
        gamma_m1 : DIMENSIONLESS
            [$\gamma_{M1}$] Partial factor for resistance of members to instability [-].
        """
        super().__init__()
        self.chi = chi
        self.a = a
        self.f_y = f_y
        self.gamma_m1 = gamma_m1

    @staticmethod
    def _evaluate(
        chi: DIMENSIONLESS,
        a: MM2,
        f_y: MPA,
        gamma_m1: DIMENSIONLESS,
    ) -> N:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(chi=chi, a=a, f_y=f_y)
        raise_if_less_or_equal_to_zero(gamma_m1=gamma_m1)

        return chi * a * f_y / gamma_m1

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 6.47."""
        _equation: str = r"\frac{\chi \cdot A \cdot f_y}{\gamma_{M1}}"
        _numeric_equation: str = latex_replace_symbols(
            _equation,
            {
                r"\chi": f"{self.chi:.{n}f}",
                r"A": f"{self.a:.{n}f}",
                r"f_y": f"{self.f_y:.{n}f}",
                r"\gamma_{M1}": f"{self.gamma_m1:.{n}f}",
            },
            False,
        )
        _numeric_equation_with_units: str = latex_replace_symbols(
            _equation,
            {
                r"\chi": f"{self.chi:.{n}f}",
                r"A": rf"{self.a:.{n}f} \ mm^2",
                r"f_y": rf"{self.f_y:.{n}f} \ MPa",
                r"\gamma_{M1}": f"{self.gamma_m1:.{n}f}",
            },
            False,
        )
        return LatexFormula(
            return_symbol=r"N_{b,Rd}",
            result=f"{self:.{n}f}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            numeric_equation_with_units=_numeric_equation_with_units,
            comparison_operator_label="=",
            unit="N",
        )
