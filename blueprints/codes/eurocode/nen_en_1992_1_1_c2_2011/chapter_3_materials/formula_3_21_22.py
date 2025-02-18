"""Formula 3.21 and 3.22 from NEN-EN 1992-1-1+C2:2011: Chapter 3 - Materials."""

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011 import NEN_EN_1992_1_1_C2_2011
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula
from blueprints.type_alias import DIMENSIONLESS, MPA


class Form3Dot21And22EffectiveStrength(Formula):
    r"""[$\eta$] Class representing formula 3.21 and 3.22 for the calculation of the factor for the effective strength [$-$]."""

    label = "3.21 - 3.22"
    source_document = NEN_EN_1992_1_1_C2_2011

    def __init__(
        self,
        f_ck: MPA,
    ) -> None:
        r"""[$\eta$] Factor effective strength [$-$].

        NEN-EN 1992-1-1+C2:2011 art.3.1.7(3) - Formula (3.21) and (3.22)

        Parameters
        ----------
        f_ck : MPA
            [$f_{ck}$] Characteristic compressive strength concrete [$MPa$].
            Valid range: [$f_{ck} \leq 90 MPa$].

        Returns
        -------
        None
        """
        super().__init__()
        self.f_ck = f_ck

    @staticmethod
    def _evaluate(
        f_ck: MPA,
    ) -> DIMENSIONLESS:
        r"""Evaluates the formula, for more information see the __init__ method."""
        if f_ck <= 50:
            return 1.0
        if f_ck <= 90:
            return 1.0 - (f_ck - 50) / 200
        raise ValueError(f"Invalid f_ck: {f_ck}. Maximum of f_ck is 90 MPa")

    def latex(self) -> LatexFormula:
        r"""Returns LatexFormula object for formula 3.21 and 3.22."""
        return LatexFormula(
            return_symbol=r"\eta",
            result=f"{self:.3f}",
            equation=r"1.0" if self.f_ck <= 50 else r"1.0 - (f_{ck} - 50) / 200",
            numeric_equation=r"1.0" if self.f_ck <= 50 else rf"1.0 - ({self.f_ck:.3f} - 50) / 200",
            comparison_operator_label="=",
        )
