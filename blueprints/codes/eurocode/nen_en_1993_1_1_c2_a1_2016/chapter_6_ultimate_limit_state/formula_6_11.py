"""Formula 6.11 from NEN-EN 1993-1-1+C2+A1:2016: Chapter 6 - Ultimate Limit State."""

from blueprints.codes.eurocode.nen_en_1993_1_1_c2_a1_2016 import NEN_EN_1993_1_1_C2_A1_2016
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import DIMENSIONLESS, MM2, MPA, N
from blueprints.validations import raise_if_less_or_equal_to_zero, raise_if_negative


class Form6Dot11NcRdClass4(Formula):
    r"""Class representing formula 6.11 for the calculation of [$N_{c,Rd}$]."""

    label = "6.11"
    source_document = NEN_EN_1993_1_1_C2_A1_2016

    def __init__(
        self,
        a_eff: MM2,
        f_y: MPA,
        gamma_m0: DIMENSIONLESS,
    ) -> None:
        r"""[$N_{c,Rd}$] Calculation of the design resistance of the cross-section for uniform compression [$N$].
        This equation is only valid for cross-sections with class 4.

        NEN-EN 1993-1-1+C2+A1:2016 art.6.2.4(2) - Formula (6.11)

        Parameters
        ----------
        a_eff : MM2
            [$A_{eff}$] Effective area of the cross-section [$mm^2$].
        f_y : MPA
            [$f_y$] Yield strength of the material [$MPa$].
        gamma_m0 : DIMENSIONLESS
            [$\gamma_{M0}$] Partial safety factor for resistance of cross-sections.
        """
        super().__init__()
        self.a_eff = a_eff
        self.f_y = f_y
        self.gamma_m0 = gamma_m0

    @staticmethod
    def _evaluate(
        a_eff: MM2,
        f_y: MPA,
        gamma_m0: DIMENSIONLESS,
    ) -> N:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(a_eff=a_eff, f_y=f_y)
        raise_if_less_or_equal_to_zero(gamma_m0=gamma_m0)

        return a_eff * f_y / gamma_m0

    def latex(self) -> LatexFormula:
        """Returns LatexFormula object for formula 6.11."""
        _equation: str = r"\frac{A_{eff} \cdot f_y}{\gamma_{M0}}"
        _numeric_equation: str = latex_replace_symbols(
            _equation,
            {
                r"A_{eff}": f"{self.a_eff:.3f}",
                r"f_y": f"{self.f_y:.3f}",
                r"\gamma_{M0}": f"{self.gamma_m0:.3f}",
            },
            False,
        )
        return LatexFormula(
            return_symbol=r"N_{c,Rd}",
            result=f"{self:.3f}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            comparison_operator_label="=",
            unit="N",
        )
