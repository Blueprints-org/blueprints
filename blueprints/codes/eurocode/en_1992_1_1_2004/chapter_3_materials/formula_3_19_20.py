"""Formula 3.19 and 3.20 from EN 1992-1-1:2004: Chapter 3 - Materials."""

from blueprints.codes.eurocode.en_1992_1_1_2004 import EN_1992_1_1_2004
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula
from blueprints.type_alias import DIMENSIONLESS, MPA


class Form3Dot19And20EffectivePressureZoneHeight(Formula):
    """Class representing formula 3.19 and 3.20 for the calculation of the λ factor for the effective pressure zone height."""

    label = "3.19 - 3.20"
    source_document = EN_1992_1_1_2004

    def __init__(
        self,
        f_ck: MPA,
    ) -> None:
        r"""[$\lambda$] Factor effective pressure zone height [$-$].

        EN 1992-1-1:2004 art.3.1.7(3) - Formula (3.19) and (3.20)

        Parameters
        ----------
        f_ck : MPA
            [$f_{ck}$] Characteristic compressive strength concrete [$MPa$].
            Valid range: [$f_{ck} \leq 90$].

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
            return 0.8
        if f_ck <= 90:
            return 0.8 - (f_ck - 50) / 400
        raise ValueError(f"Invalid f_ck: {f_ck}. Maximum of f_ck is 90 MPa")

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 3.19 and 3.20."""
        return LatexFormula(
            return_symbol=r"\lambda",
            result=f"{self:.{n}f}",
            equation=r"0.8" if self.f_ck <= 50 else r"0.8 - (f_{ck} - 50) / 400",
            numeric_equation=r"0.8" if self.f_ck <= 50 else rf"0.8 - ({self.f_ck:.{n}f} - 50) / 400",
            comparison_operator_label="=",
        )
