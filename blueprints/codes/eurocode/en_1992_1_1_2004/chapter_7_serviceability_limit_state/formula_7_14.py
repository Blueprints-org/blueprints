"""Formula 7.14 from EN 1992-1-1:2004: Chapter 7 - Serviceability limit state (SLS)."""

from blueprints.codes.eurocode.en_1992_1_1_2004 import EN_1992_1_1_2004
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_replace_symbols
from blueprints.type_alias import MM
from blueprints.validations import raise_if_negative


class Form7Dot14MaximumCrackSpacing(Formula):
    r"""Class representing formula 7.14 for the calculation of crack spacing [$s_{r,max}$]."""

    label = "7.14"
    source_document = EN_1992_1_1_2004

    def __init__(
        self,
        h: MM,
        x: MM,
    ) -> None:
        r"""[$s_{r,max}$] Where the spacing of the bonded reinforcement exceeds 5(c+⌀/2) (see Figure 7.2) or where
        there is no bonded reinforcement within the tension zone, an upper bound to the crack width
        may be found by assuming a maximum crack spacing with this formula [$mm$].

        EN 1992-1-1:2004 art.7.3.4(3) - Formula (7.14)

        Parameters
        ----------
        h : MM
            [$h$] Depth of the neutral axis [$mm$].
        x : MM
            [$x$] Depth of the concrete tension surface [$mm$].
        """
        super().__init__()
        self.h = h
        self.x = x

    @staticmethod
    def _evaluate(
        h: MM,
        x: MM,
    ) -> MM:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(h=h, x=x)

        return 1.3 * (h - x)

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 7.14."""
        _equation: str = r"1.3 \cdot (h - x)"
        _numeric_equation: str = latex_replace_symbols(
            _equation,
            {
                r"h": f"{self.h:.{n}f}",
                r"x": f"{self.x:.{n}f}",
            },
            False,
        )
        return LatexFormula(
            return_symbol=r"s_{r,max}",
            result=f"{self:.{n}f}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            comparison_operator_label="=",
            unit="mm",
        )
