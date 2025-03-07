"""Formula 3.12 from NEN-EN 1992-1-1+C2:2011: Chapter 3 - Materials."""

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011 import NEN_EN_1992_1_1_C2_2011
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula
from blueprints.type_alias import DIMENSIONLESS, MPA


class Form3Dot12AutogeneShrinkageInfinity(Formula):
    """Class representing formula 3.12, which calculates the autogeneous shrinkage strain at t=infinity."""

    source_document = NEN_EN_1992_1_1_C2_2011
    label = "3.12"

    def __init__(
        self,
        f_ck: MPA,
    ) -> None:
        r"""[$\epsilon_{ca}(\infty)$] Autogeneous shrinkage strain at t=infinity [$-$].

        NEN-EN 1992-1-1+C2:2011 art.3.1.4(6) - Formula (3.12)

        Parameters
        ----------
        f_ck : MPA
            [$f_{ck}$] Compressive strength concrete [$MPa$].

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
        """Evaluates the formula, for more information see the __init__ method."""
        if f_ck < 0:
            raise ValueError(f"Invalid f_ck: {f_ck}. f_ck cannot be negative")
        return 2.5 * (f_ck - 10) * 10**-6

    def latex(self) -> LatexFormula:
        """Returns LatexFormula object for formula 3.12."""
        return LatexFormula(
            return_symbol=r"\epsilon_{ca}(\infty)",
            result=f"{self:.6f}",
            equation=r"2.5 \cdot (f_{ck} - 10) \cdot 10^{-6}",
            numeric_equation=rf"2.5 \cdot ({self.f_ck:.3f} - 10) \cdot 10^{{-6}}",
            comparison_operator_label="=",
        )
