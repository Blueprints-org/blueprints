"""Formula 7.3 from EN 1995-1-1:2004."""

from blueprints.codes.eurocode.en_1995_1_1_2004 import EN_1995_1_1_2004
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
    source_document = EN_1995_1_1_2004

    def __init__(self, w: MM, f: KN, alpha: MM_KN) -> None:
        r"""
        [\frac{w/F}{\alpha}] Unity check of ratio between maximum instantaneous vertical deflection caused by a
        vertical static point load F and the applied force F.

        EN 1995-1-1:2004 art 7.3.3(2) - Formula (7.3)

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

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 7.3."""
        eq_for: str = r"\frac{w/F}{\alpha}"
        repl_symb = {
            "w": f"{self.w:.{n}f}",
            "F": f"{self.f:.{n}f}",
            r"\alpha": f"{self.alpha:.{n}f}",
        }
        return LatexFormula(
            return_symbol=r"UC",
            result=f"{self:.{n}f}",
            equation=eq_for,
            numeric_equation=latex_replace_symbols(eq_for, repl_symb),
        )
