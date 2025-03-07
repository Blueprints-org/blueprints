"""Formula 6.10a/bN from NEN-EN 1992-1-1+C2:2011: Chapter 6 - Ultimate limit state."""

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011 import NEN_EN_1992_1_1_C2_2011
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula
from blueprints.type_alias import DIMENSIONLESS, MPA
from blueprints.validations import raise_if_negative


class Form6Dot10abNStrengthReductionFactor(Formula):
    r"""Class representing formula 6.10a/bN for the calculation of the strength reduction factor for concrete cracked in shear."""

    label = "6.10a/bN"
    source_document = NEN_EN_1992_1_1_C2_2011

    def __init__(
        self,
        f_ck: MPA,
    ) -> None:
        r"""[$\nu_{1}$] Strength reduction factor for concrete cracked in shear [$-$].

        NEN-EN 1992-1-1+C2:2011 art.6.2.3(3) - Formula (6.10.aN and 6.10.bN)

        Parameters
        ----------
        f_ck : MPA
            [$f_{ck}$] Characteristic compressive strength of concrete [$MPa$].
        """
        super().__init__()
        self.f_ck = f_ck

    @staticmethod
    def _evaluate(
        f_ck: MPA,
    ) -> DIMENSIONLESS:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(f_ck=f_ck)

        if f_ck <= 60:
            return 0.6
        return max(0.9 - f_ck / 200, 0.5)

    def latex(self) -> LatexFormula:
        """Returns LatexFormula object for formula 6.10a/bN."""
        return LatexFormula(
            return_symbol=r"\nu_{1}",
            result=f"{self:.3f}",
            equation=r"\begin{cases} 0.600 & \text{if } f_{ck} \leq 60 MPa \\ \max\left(0.9 - \frac{f_{ck}}{200}, 0.5\right) "
            r"& \text{if } f_{ck} /ge 60 MPa \end{cases}",
            numeric_equation=rf"\begin{{cases}} 0.600 & \text{{if }} {self.f_ck} \leq 60 MPa \\ "
            rf"\max\left(0.9 - \frac{{{self.f_ck}}}{{200}}, 0.5\right) & \text{{if }} {self.f_ck} /ge 60 MPa \end{{cases}}",
            comparison_operator_label="=",
            unit="-",
        )
