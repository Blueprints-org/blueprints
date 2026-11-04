"""Formula 8.1 from FprEN 1992-1-1:2023: Chapter 8: Ultimate limit states (ULS)."""

from blueprints.codes.eurocode.fpr_en_1992_1_1_2023 import FPR_EN_1992_1_1_2023
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import MM, NMM, N
from blueprints.validations import raise_if_less_or_equal_to_zero


class Form8Dot1MinimumDesignMoment(Formula):
    r"""Class representing formula 8.1 for the calculation of the minimum design moment to be considered
    together with an axial compression force.
    """

    label = "8.1"
    source_document = FPR_EN_1992_1_1_2023

    def __init__(
        self,
        n_ed: N,
        h: MM,
    ) -> None:
        r"""[$M_{Ed,min}$] Minimum design moment [$Nmm$].

        FprEN 1992-1-1:2023 (E) art. 8.1.1(5) - Formula (8.1)

        The standard prints this moment as [$\pm N_{Ed} \cdot e_{d,min}$]: the cross-section shall be designed
        for this minimum moment in both directions. This class returns the magnitude, and it is left to the
        caller to apply it with either sign.

        Parameters
        ----------
        n_ed : N
            [$N_{Ed}$] Design axial compression force [$N$].
        h : MM
            [$h$] Overall depth of the cross-section [$mm$].
        """
        super().__init__()
        self.n_ed = n_ed
        self.h = h

    @staticmethod
    def _evaluate(
        n_ed: N,
        h: MM,
    ) -> NMM:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_less_or_equal_to_zero(h=h)

        e_d_min = max(h / 30, 20)
        return abs(n_ed) * e_d_min

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 8.1."""
        _equation: str = r"\left|N_{Ed}\right| \cdot \max\left(\frac{h}{30}, 20\right)"
        _numeric_equation: str = latex_replace_symbols(
            template=_equation,
            replacements={
                r"N_{Ed}": f"{self.n_ed:.{n}f}",
                r"{h}": "{" + f"{self.h:.{n}f}" + "}",
            },
            unique_symbol_check=False,
        )
        _numeric_equation_with_units: str = latex_replace_symbols(
            template=_equation,
            replacements={
                r"N_{Ed}": rf"{self.n_ed:.{n}f} \ N",
                r"{h}": "{" + rf"{self.h:.{n}f} \ mm" + "}",
            },
            unique_symbol_check=False,
        )
        return LatexFormula(
            return_symbol=r"M_{Ed,min}",
            result=f"{self:.{n}f}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            numeric_equation_with_units=_numeric_equation_with_units,
            comparison_operator_label="=",
            unit="Nmm",
        )
