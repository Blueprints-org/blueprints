"""Formula 7.3 from NEN-EN 1995-1-1+C1+A1:2011/C1:2012."""

from blueprints.codes.eurocode.nen_en_1995_1_1_2011 import NEN_EN_1995_1_1_2011_2012
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import DIMENSIONLESS, KN, MM, MM_KN
from blueprints.validations import raise_if_less_or_equal_to_zero


class Form7Dot3RatioDeflectionPointLoadUC(Formula):
    r"""
    Class representing formula 7.3 for the calculation of ratio between maximum instantaneous
    vertical deflection due to vertical static point load F and the applied force F.
    """

    label = "7.3"
    source_document = NEN_EN_1995_1_1_2011_2012

    def __init__(self, w: MM, f: KN, alpha: MM_KN) -> None:
        r"""
        [\frac{w/F}{\alpha}] Unity check of ratio between maximum instantaneous vertical deflection caused by a
        vertical static point load F and the applied force F.

        NEN-EN 1995-1-1 art 7.3.3(2) - Formula (7.3)

        Parameters
        ----------
        w : MM
            [$w$] is the maximum instantaneous vertical deflection caused by a vertical static point load F [$mm$].
        f : KN
            [$F$] Vertical static point load F that can engage in any point of the floor [$kN$].
        alpha : MM_KN
            [$\alpha$] Limit of ratio between instantaneous deflection and point load (equal to 1 according to Dutch National Annex) [$mm/kN$].

        Returns
        -------
        None
        """
        super().__init__()
        self.w = w
        self.f = f
        self.alpha = alpha

    @staticmethod
    def _evaluate(w: MM, f: KN, alpha: MM_KN) -> DIMENSIONLESS:
        """Evaluate the formula, for more information see the __init__ method."""
        raise_if_less_or_equal_to_zero(w=w, f=f, alpha=alpha)
        ratio = w / f
        return ratio / alpha

    def latex(self) -> LatexFormula:
        """Returns LatexFormula object for formula 7.3."""
        eq_for: str = r"\frac{w/F}{\alpha}"
        repl_symb = {
            "w": f"{self.w:.3f}",
            "F": f"{self.f:.2f}",
            r"\alpha": f"{self.alpha:.2f}",
        }
        return LatexFormula(
            return_symbol=r"UC",
            result=f"{self:.2f}",
            equation=eq_for,
            numeric_equation=latex_replace_symbols(eq_for, repl_symb),
        )
