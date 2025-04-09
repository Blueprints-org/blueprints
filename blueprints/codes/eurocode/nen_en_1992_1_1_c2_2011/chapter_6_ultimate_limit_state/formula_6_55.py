"""Formula 6.55 from NEN-EN 1992-1-1+C2:2011: Chapter 6 - Ultimate Limit State."""

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011 import NEN_EN_1992_1_1_C2_2011
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import MPA
from blueprints.validations import raise_if_negative


class Form6Dot55DesignStrengthConcreteStruts(Formula):
    r"""Class representing formula 6.55 for the calculation of [$\sigma_{Rd,max}$]."""

    label = "6.55"
    source_document = NEN_EN_1992_1_1_C2_2011

    def __init__(
        self,
        f_cd: MPA,
    ) -> None:
        r"""[$\sigma_{Rd,max}$] Calculation of the design strength of concrete struts.

        NEN-EN 1992-1-1+C2:2011 art.6.5.2(1) - Formula (6.55)

        Parameters
        ----------
        f_cd : MPA
            [$f_{cd}$] Design compressive strength of concrete [$MPa$].
        """
        super().__init__()
        self.f_cd = f_cd

    @staticmethod
    def _evaluate(
        f_cd: MPA,
    ) -> MPA:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(f_cd=f_cd)

        return f_cd

    def latex(self) -> LatexFormula:
        """Returns LatexFormula object for formula 6.55."""
        _equation: str = r"f_{cd}"
        _numeric_equation: str = latex_replace_symbols(
            _equation,
            {
                r"f_{cd}": f"{self.f_cd:.3f}",
            },
            False,
        )
        return LatexFormula(
            return_symbol=r"\sigma_{Rd,max}",
            result=f"{self:.3f}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            comparison_operator_label="=",
            unit="MPa",
        )
