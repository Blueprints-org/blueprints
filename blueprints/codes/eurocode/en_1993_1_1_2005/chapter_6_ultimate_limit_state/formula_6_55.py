"""Formula 6.55 from EN 1993-1-1:2005: Chapter 6 - Ultimate Limit State."""

from blueprints.codes.eurocode.en_1993_1_1_2005 import EN_1993_1_1_2005
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import (
    LatexFormula,
    latex_replace_symbols,
)
from blueprints.type_alias import DIMENSIONLESS, MM3, MPA, NMM
from blueprints.validations import (
    raise_if_less_or_equal_to_zero,
    raise_if_negative,
)


class Form6Dot55DesignBucklingResistanceMoment(Formula):
    r"""Class representing formula 6.55 for the calculation of [$M_{b,Rd}$]."""

    label = "6.55"
    source_document = EN_1993_1_1_2005

    def __init__(
        self,
        chi_lt: DIMENSIONLESS,
        w_y: MM3,
        f_y: MPA,
        gamma_m1: DIMENSIONLESS,
    ) -> None:
        r"""[$M_{b,Rd}$] Design buckling resistance moment [$Nmm$].

        EN 1993-1-1:2005 art.6.3.2.1(3) - Formula (6.55)

        Parameters
        ----------
        chi_lt : DIMENSIONLESS
            [$\chi_{LT}$] Reduction factor for lateral-torsional buckling [-].
        w_y : MM3
            [$W_y$] Appropriate section modulus [$mm^3$].
        f_y : MPA
            [$f_y$] Yield strength of the material [$MPa$].
        gamma_m1 : DIMENSIONLESS
            [$\gamma_{M1}$] Partial factor for resistance of members to
            instability [-].
        """
        super().__init__()
        self.chi_lt = chi_lt
        self.w_y = w_y
        self.f_y = f_y
        self.gamma_m1 = gamma_m1

    @staticmethod
    def _evaluate(
        chi_lt: DIMENSIONLESS,
        w_y: MM3,
        f_y: MPA,
        gamma_m1: DIMENSIONLESS,
    ) -> NMM:
        """Evaluates the formula, see the __init__ method."""
        raise_if_negative(chi_lt=chi_lt, w_y=w_y, f_y=f_y)
        raise_if_less_or_equal_to_zero(gamma_m1=gamma_m1)

        return chi_lt * w_y * f_y / gamma_m1

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 6.55."""
        _equation: str = r"\chi_{LT} \cdot W_y \cdot \frac{f_y}{\gamma_{M1}}"
        _numeric_equation: str = latex_replace_symbols(
            _equation,
            {
                r"\chi_{LT}": f"{self.chi_lt:.{n}f}",
                r"W_y": f"{self.w_y:.{n}f}",
                r"f_y": f"{self.f_y:.{n}f}",
                r"\gamma_{M1}": f"{self.gamma_m1:.{n}f}",
            },
            False,
        )
        _numeric_equation_with_units: str = latex_replace_symbols(
            _equation,
            {
                r"\chi_{LT}": f"{self.chi_lt:.3f}",
                r"W_y": rf"{self.w_y:.3f} \ mm^3",
                r"f_y": rf"{self.f_y:.3f} \ MPa",
                r"\gamma_{M1}": f"{self.gamma_m1:.3f}",
            },
            True,
        )
        return LatexFormula(
            return_symbol=r"M_{b,Rd}",
            result=f"{self:.{n}f}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            numeric_equation_with_units=_numeric_equation_with_units,
            comparison_operator_label="=",
            unit="Nmm",
        )
