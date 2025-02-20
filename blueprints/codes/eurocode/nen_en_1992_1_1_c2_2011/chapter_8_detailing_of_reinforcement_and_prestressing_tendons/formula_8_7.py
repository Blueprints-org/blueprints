"""Formula 8.7 from NEN-EN 1992-1-1+C2:2011: Chapter 8: Detailing of reinforcement and prestressing tendons."""

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011 import NEN_EN_1992_1_1_C2_2011
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula, latex_max_curly_brackets
from blueprints.type_alias import MM
from blueprints.validations import raise_if_negative


class Form8Dot7MinimumCompressionAnchorage(Formula):
    """Class representing formula 8.7 for the calculation of the minimum anchorage length if no other limitation is applied for anchorage in
    compression.
    """

    label = "8.7"
    source_document = NEN_EN_1992_1_1_C2_2011

    def __init__(
        self,
        l_b_rqd: MM,
        diameter: MM,
    ) -> None:
        r"""[$l_{b,min}$] Minimum anchorage length if no other limitation is applied for anchorage in compression. [$mm$].

        NEN-EN 1992-1-1+C2:2011 art.8.4.4(1) - Formula (8.7)

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
        return max(0.6 * l_b_rqd, 10 * diameter, 100)

    def latex(self) -> LatexFormula:
        """Returns a LatexFormula object for this formula."""
        return LatexFormula(
            return_symbol=r"l_{b,min}",
            result=f"{self:.2f}",
            equation=latex_max_curly_brackets(r"0.6 \cdot l_{b,rqd}", r"10 \cdot Ø", r"100 \ \text{mm}"),
            numeric_equation=latex_max_curly_brackets(
                rf"0.6 \cdot {self.l_b_rqd:.2f}",
                rf"10 \cdot {self.diameter}",
                r"100",
            ),
            comparison_operator_label="=",
        )
