"""Formula 7.3 from NEN-EN 1992-1-1+C2:2011: Chapter 7 - Serviceability limit state (SLS)."""

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011 import NEN_EN_1992_1_1_C2_2011
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula
from blueprints.type_alias import DIMENSIONLESS, KN, MM2, MPA
from blueprints.unit_conversion import KN_TO_N


class Form7Dot3CoefficientKc(Formula):
    """Class representing the formula 7.3 for the coefficient kc for flanges of tubular cross-sections and T-sections."""

    label = "7.3"
    source_document = NEN_EN_1992_1_1_C2_2011

    def __init__(
        self,
        f_cr: KN,
        a_ct: MM2,
        f_ct_eff: MPA,
    ) -> None:
        r"""[$kc$] Calculates kc for flanges of tubular cross-sections and T-sections [$-$].

        NEN-EN 1992-1-1:2011 art.7.3.2(2) - Formula (7.3)

        Parameters
        ----------
        f_cr : KN
            [$F_{cr}$] Absolute value of the tensile force within the flange immediately before cracking due to the cracking moment calculated with
            [$f_{ct,eff}$] [$kN$].
        a_ct : MM2
            [$A_{ct}$] Area of the concrete within the tension zone. The tension zone is that part of the cross-section that,
            according to the calculation, is under tension just before the first crack occurs [$mm^2$].
        f_ct_eff : MPA
            [$f_{ct,eff}$] Average value of the tensile strength of the concrete at the time when the first cracks can be expected [$MPa$].
        """
        super().__init__()
        self.f_cr = f_cr
        self.a_ct = a_ct
        self.f_ct_eff = f_ct_eff

    @staticmethod
    def _evaluate(
        f_cr: KN,
        a_ct: MM2,
        f_ct_eff: MPA,
    ) -> DIMENSIONLESS:
        """Evaluates the formula, for more information see the __init__ method."""
        if a_ct <= 0:
            raise ValueError("The value of a_ct must be greater than zero.")
        if f_ct_eff <= 0:
            raise ValueError("The value of f_ct_eff must be greater than zero.")
        return max(0.9 * (abs(f_cr) * KN_TO_N / (a_ct * f_ct_eff)), 0.5)

    def latex(self) -> LatexFormula:
        """Returns LatexFormula object for formula 7.3."""
        return LatexFormula(
            return_symbol=r"k_c",
            result=f"{self:.3f}",
            equation=r"\max\left(0.9 \cdot \frac{F_{cr}}{A_{ct} \cdot f_{ct,eff}}, 0.5\right)",
            numeric_equation=rf"\max\left(0.9 \cdot \frac{{{self.f_cr:.3f}}}{{{self.a_ct:.3f} \cdot {self.f_ct_eff:.3f}}}, 0.5\right)",
            comparison_operator_label="=",
        )
