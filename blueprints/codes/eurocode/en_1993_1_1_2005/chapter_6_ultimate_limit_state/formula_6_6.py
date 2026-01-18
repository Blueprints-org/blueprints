"""Formula 6.6 from EN 1993-1-1:2005: Chapter 6 - Ultimate Limit State."""

from blueprints.codes.eurocode.en_1993_1_1_2005 import EN_1993_1_1_2005
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import DIMENSIONLESS, MM2, MPA, N
from blueprints.validations import raise_if_less_or_equal_to_zero, raise_if_negative


class Form6Dot6DesignPlasticResistanceGrossCrossSection(Formula):
    r"""Class representing formula 6.6 for the calculation of [$N_{pl,Rd}$]."""

    label = "6.6"
    source_document = EN_1993_1_1_2005

    def __init__(
        self,
        a: MM2,
        f_y: MPA,
        gamma_m0: DIMENSIONLESS,
    ) -> None:
        r"""[$N_{pl,Rd}$] Calculation of the design plastic resistance of the gross cross-section [$N$].

        EN 1993-1-1:2005 art.6.2.3(2) - Formula (6.6)

        Parameters
        ----------
        a : MM2
            [$A$] Gross cross-sectional area [$mm^2$].
        f_y : MPA
            [$f_y$] Yield strength of the material [$MPa$].
        gamma_m0 : DIMENSIONLESS
            [$\gamma_{M0}$] Partial safety factor for resistance of cross-sections, irrespective of the class.
        """
        super().__init__()
        self.a = a
        self.f_y = f_y
        self.gamma_m0 = gamma_m0

    @staticmethod
    def _evaluate(
        a: MM2,
        f_y: MPA,
        gamma_m0: DIMENSIONLESS,
    ) -> N:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(a=a, f_y=f_y)
        raise_if_less_or_equal_to_zero(gamma_m0=gamma_m0)

        return (a * f_y) / gamma_m0

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 6.6."""
        _equation: str = r"\frac{A \cdot f_y}{\gamma_{M0}}"
        _numeric_equation: str = latex_replace_symbols(
            _equation,
            {
                r"A": f"{self.a:.{n}f}",
                r"f_y": f"{self.f_y:.{n}f}",
                r"\gamma_{M0}": f"{self.gamma_m0:.{n}f}",
            },
            False,
        )
        return LatexFormula(
            return_symbol=r"N_{pl,Rd}",
            result=f"{self:.{n}f}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            comparison_operator_label="=",
            unit="N",
        )
