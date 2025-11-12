"""Formula 5.6 from EN 1993-5:2007 Chapter 5 - Ultimate limit state."""

from blueprints.codes.eurocode.en_1993_5_2007 import EN_1993_5_2007
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula
from blueprints.type_alias import MM, MM2
from blueprints.validations import raise_if_less_or_equal_to_zero


class Form5Dot6ProjectedShearArea(Formula):
    """Class representing formula 5.6 for the projected shear area for each web of a U-profile or Z-profile."""

    label = "5.6"
    source_document = EN_1993_5_2007

    def __init__(
        self,
        h: MM,
        t_f: MM,
        t_w: MM,
    ) -> None:
        r"""[$A_{v}$] Calculate the projected shear area for each web of a U-profile or Z-profile in [$mm^2$].

        EN 1993-5:2007(E) art.5.2.2(5) - Formula (5.6)

        Parameters
        ----------
        h : MM
            [$h$] Overall height in [$mm$].
        t_f : MM
            [$t_{f}$] Flange thickness in [$mm$].
        t_w : MM
            [$t_{w}$] Web thickness in [$mm$].
        """
        super().__init__()
        self.h: MM = h
        self.t_f: MM = t_f
        self.t_w: MM = t_w

    @staticmethod
    def _evaluate(
        h: MM,
        t_f: MM,
        t_w: MM,
    ) -> MM2:
        """Evaluates the formula for projected shear area."""
        raise_if_less_or_equal_to_zero(h=h, t_f=t_f, t_w=t_w)
        return t_w * (h - t_f)

    def latex(self, n: int = 2) -> LatexFormula:
        """Returns LatexFormula object for formula 5.6."""
        return LatexFormula(
            return_symbol=r"A_v",
            result=f"{self:.{n}f}",
            equation=r"t_w \left(h - t_f \right)",
            numeric_equation=rf"{self.t_w} \cdot \left({self.h} - {self.t_f} \right)",
            comparison_operator_label="=",
        )
