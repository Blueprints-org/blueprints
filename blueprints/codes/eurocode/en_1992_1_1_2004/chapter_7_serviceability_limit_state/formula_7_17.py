"""Formula 7.17 from EN 1992-1-1:2004: Chapter 7 - Serviceability limit state (SLS)."""

from blueprints.codes.eurocode.en_1992_1_1_2004 import EN_1992_1_1_2004
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import DIMENSIONLESS, MM2, N
from blueprints.validations import raise_if_less_or_equal_to_zero


class Form7Dot1MultiplicationFactorLimitSlenderness(Formula):
    r"""Class representing formula 7.17 for the calculation of the stress multiplication factor for the limit span to depth ratio."""

    label = "7.17"
    source_document = EN_1992_1_1_2004

    def __init__(
        self,
        f_yk: N,
        a_s_req: MM2,
        a_s_prov: MM2,
    ) -> None:
        r"""[$\frac{310}{\sigma_s}$] Calculation of the multiplication factor [$-$].

        EN 1992-1-1:2004 art.7.4.2(2) - Formula (7.17)

        Parameters
        ----------
        f_yk : MPa
            [$f_{yk}$] Characteristic yield strength of the steel [$MPa$].
        a_s_req : MM2
            [$A_{s,req}$] Area of steel required at this section for ultimate limit state [$mm^2$].
        a_s_prov : MM2
            [$A_{s,prov}$] Area of steel provided at this section [$mm^2$].
        """
        super().__init__()
        self.f_yk = f_yk
        self.a_s_req = a_s_req
        self.a_s_prov = a_s_prov

    @staticmethod
    def _evaluate(
        f_yk: N,
        a_s_req: MM2,
        a_s_prov: MM2,
    ) -> DIMENSIONLESS:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_less_or_equal_to_zero(f_yk=f_yk, a_s_req=a_s_req, a_s_prov=a_s_prov)

        return 500 / (f_yk * a_s_req / a_s_prov)

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 7.17."""
        _equation: str = r"\frac{500}{f_{yk} \cdot \frac{A_{s,req}}{A_{s,prov}}}"
        _numeric_equation: str = latex_replace_symbols(
            _equation,
            {
                r"f_{yk}": f"{self.f_yk:.{n}f}",
                r"A_{s,req}": f"{self.a_s_req:.{n}f}",
                r"A_{s,prov}": f"{self.a_s_prov:.{n}f}",
            },
            False,
        )
        return LatexFormula(
            return_symbol=r"\frac{310}{\sigma_s}",
            result=f"{self:.{n}f}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            comparison_operator_label="=",
            unit="-",
        )
