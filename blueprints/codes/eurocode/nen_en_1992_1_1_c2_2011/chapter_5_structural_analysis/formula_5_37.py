"""Formula 5.37 from NEN-EN 1992-1-1+C2:2011: Chapter 5 - Structural Analysis."""

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011 import NEN_EN_1992_1_1_C2_2011
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula
from blueprints.type_alias import DIMENSIONLESS, MPA
from blueprints.validations import raise_if_negative


class Form5Dot37CreepFactor(Formula):
    r"""Class representing formula 5.37 for the calculation of the creep factor, [$K_{\phi}$]."""

    label = "5.37"
    source_document = NEN_EN_1992_1_1_C2_2011

    def __init__(
        self,
        f_ck: MPA,
        lambda_: DIMENSIONLESS,
        phi_ef: DIMENSIONLESS,
    ) -> None:
        r"""[$K_{\phi}$] Creep factor [$-$].

        NEN-EN 1992-1-1+C2:2011 art.5.8.8.3(4) - Formula (5.37)

        Parameters
        ----------
        f_ck : MPA
            [$f_{ck}$] Characteristic compressive strength of concrete [$MPa$].
        lambda_ : DIMENSIONLESS
            [$\lambda$] Slenderness ratio, see 5.8.3.1 [-].
        phi_ef : DIMENSIONLESS
            [$\phi_{ef}$] Effective creep ratio, see 5.8.4 [-].
        """
        super().__init__()
        self.f_ck = f_ck
        self.lambda_ = lambda_
        self.phi_ef = phi_ef

    @staticmethod
    def _evaluate(
        f_ck: MPA,
        lambda_: float,
        phi_ef: float,
    ) -> float:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(
            f_ck=f_ck,
            lambda_=lambda_,
            phi_ef=phi_ef,
        )

        return max(1 + (0.35 + f_ck / 200 - lambda_ / 150) * phi_ef, 1)

    def latex(self) -> LatexFormula:
        """Returns LatexFormula object for formula 5.37."""
        return LatexFormula(
            return_symbol=r"K_{\phi}",
            result=f"{self:.3f}",
            equation=r"\max\left(1 + \left(0.35 + \frac{f_{ck}}{200} - \frac{\lambda}{150}\right) \cdot \phi_{ef}; 1\right)",
            numeric_equation=rf"\max\left(1 + \left(0.35 + \frac{{{self.f_ck:.3f}}}{{200}} - \frac{{{self.lambda_:.3f}}}{{150}}\right) "
            rf"\cdot {self.phi_ef:.3f}; 1\right)",
            comparison_operator_label="=",
            unit="-",
        )
