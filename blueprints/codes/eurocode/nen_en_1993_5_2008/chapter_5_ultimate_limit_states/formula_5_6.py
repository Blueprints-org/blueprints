"""Formula 5.6 from NEN-EN 1993-5:2008 Chapter 5 - Ultimate limit state."""

from blueprints.codes.eurocode.nen_en_1993_5_2008.chapter_5_ultimate_limit_states import NEN_EN_1993_5_2008
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula
from blueprints.type_alias import MM, MM2
from blueprints.validations import raise_if_less_or_equal_to_zero


class Form5Dot6ProjectedShearArea(Formula):
    """Class representing formula 5.6 for the projected shear area for each web of a U-profile or Z-profile."""

    label = "5.6"
    source_document = NEN_EN_1993_5_2008

    def __init__(
        self,
        h: MM,  # Overall height
        t_f: MM,  # Flange thickness
        t_w: MM,  # Web thickness
    ) -> None:
        """[Av] Calculate the projected shear area based on formula 5.6 from NEN-EN 1993-5:2007(E) art. 5.2.2(5).

        Parameters
        ----------
        h : MM
            [h] Overall height in [mm].
        t_f : MM
            [tf] Flange thickness in [mm].
        tw : MM
            [tw] Web thickness in [mm].
        """
        super().__init__()
        self.h: float = h
        self.tf: float = tf
        self.tw: float = tw

    @staticmethod
    def _evaluate(
        h: MM,
        tf: MM,
        tw: MM,
    ) -> MM2:
        """Evaluates the formula for projected shear area."""
        raise_if_less_or_equal_to_zero(h=h, tf=tf, tw=tw)
        return tw * (h - tf)

    def latex(self) -> LatexFormula:
        """Returns LatexFormula object for formula 5.6."""
        return LatexFormula(
            return_symbol=r"A_v",
            result=str(self),
            equation=r"t_w \left(h - t_f \right)",
            numeric_equation=rf"{self.tw} \cdot \left({self.h} - {self.tf} \right)",
            comparison_operator_label="=",
        )
