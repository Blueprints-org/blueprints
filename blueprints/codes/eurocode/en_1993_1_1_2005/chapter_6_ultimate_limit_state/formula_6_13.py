"""Formula 6.13 from EN 1993-1-1:2005: Chapter 6 - Ultimate Limit State."""

from blueprints.codes.eurocode.en_1993_1_1_2005 import EN_1993_1_1_2005
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import DIMENSIONLESS, MM3, MPA, NMM
from blueprints.validations import raise_if_less_or_equal_to_zero, raise_if_negative


class Form6Dot13MCRdClass1And2(Formula):
    r"""Class representing formula 6.13 for the calculation of [$M_{c,Rd}$]."""

    label = "6.13"
    source_document = EN_1993_1_1_2005

    def __init__(
        self,
        w_pl: MM3,
        f_y: MPA,
        gamma_m0: DIMENSIONLESS,
    ) -> None:
        r"""[$M_{c,Rd}$] Calculation of the design resistance of the cross-section for bending about one principal axis [$Nmm$].
        This equation is only valid for cross-sections with class 1, or 2.

        EN 1993-1-1:2005 art.6.2.5(2) - Formula (6.13)

        Parameters
        ----------
        w_pl : MM3
            [$W_{pl}$] Plastic section modulus of the cross-section [$mm^3$].
        f_y : MPA
            [$f_y$] Yield strength of the material [$MPa$].
        gamma_m0 : DIMENSIONLESS
            [$\gamma_{M0}$] Partial safety factor for resistance of cross-sections.
        """
        super().__init__()
        self.w_pl = w_pl
        self.f_y = f_y
        self.gamma_m0 = gamma_m0

    @staticmethod
    def _evaluate(
        w_pl: MM3,
        f_y: MPA,
        gamma_m0: DIMENSIONLESS,
    ) -> NMM:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(w_pl=w_pl, f_y=f_y)
        raise_if_less_or_equal_to_zero(gamma_m0=gamma_m0)

        return (w_pl * f_y) / gamma_m0

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 6.13."""
        _equation: str = r"\frac{W_{pl} \cdot f_y}{\gamma_{M0}}"
        _numeric_equation: str = latex_replace_symbols(
            _equation,
            {
                r"W_{pl}": f"{self.w_pl:.{n}f}",
                r"f_y": f"{self.f_y:.{n}f}",
                r"\gamma_{M0}": f"{self.gamma_m0:.{n}f}",
            },
            False,
        )
        return LatexFormula(
            return_symbol=r"M_{c,Rd}",
            result=f"{self:.{n}f}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            comparison_operator_label="=",
            unit="Nmm",
        )
