"""Formula 8.6 from EN 1992-1-1:2004: Chapter 8: Detailing of reinforcement and prestressing tendons."""

from blueprints.codes.eurocode.en_1992_1_1_2004 import EN_1992_1_1_2004
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_max_curly_brackets, latex_replace_symbols
from blueprints.type_alias import MM
from blueprints.validations import raise_if_negative


class Form8Dot6MinimumTensionAnchorage(Formula):
    """Class representing formula 8.6 for the calculation of the minimum anchorage length if no other limitation is applied for anchorage in
    tension.
    """

    label = "8.6"
    source_document = EN_1992_1_1_2004

    def __init__(
        self,
        l_b_rqd: MM,
        diameter: MM,
    ) -> None:
        r"""[$l_{b,min}$] Minimum anchorage length if no other limitation is applied for anchorage in tension. [$mm$].

        EN 1992-1-1:2004 art.8.4.4(1) - Formula (8.6)

        Parameters
        ----------
        l_b_rqd: MM
            [$l_{b,rqd}$] Basic required anchorage length, for anchoring the force [$A_s \cdot \sigma_{sd}$] in a straight bar assuming constant
            bond stress (formula 8.3) [$mm$].
            Use your own implementation for this value or use the Form8Dot3RequiredAnchorageLength class.
        diameter: MM
            [$Ø$] Diameter of the bar [$mm$].
        """
        super().__init__()
        self.l_b_rqd = l_b_rqd
        self.diameter = diameter

    @staticmethod
    def _evaluate(l_b_rqd: MM, diameter: MM) -> MM:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(diameter=diameter, l_b_rqd=l_b_rqd)
        return max(0.3 * l_b_rqd, 10 * diameter, 100)

    def latex(self, n: int = 2) -> LatexFormula:
        """Returns a LatexFormula object for this formula."""
        _equation: str = latex_max_curly_brackets(r"0.3 \cdot l_{b,rqd}", r"10 \cdot Ø", r"100 \ \text{mm}")
        _equation_no_unit: str = latex_max_curly_brackets(r"0.3 \cdot l_{b,rqd}", r"10 \cdot Ø", r"100")
        _numeric_equation: str = latex_replace_symbols(
            _equation_no_unit,
            {
                r"l_{b,rqd}": f"{self.l_b_rqd:.{n}f}",
                r"Ø": f"{self.diameter:.{n}f}",
            },
            False,
        )
        _numeric_equation_with_units: str = latex_replace_symbols(
            _equation,
            {
                r"l_{b,rqd}": rf"{self.l_b_rqd:.{n}f} \ mm",
                r"Ø": rf"{self.diameter:.{n}f} \ mm",
            },
            False,
        )
        return LatexFormula(
            return_symbol=r"l_{b,min}",
            result=f"{self:.{n}f}",
            equation=_equation,
            numeric_equation=_numeric_equation,
            numeric_equation_with_units=_numeric_equation_with_units,
            comparison_operator_label="=",
            unit="mm",
        )