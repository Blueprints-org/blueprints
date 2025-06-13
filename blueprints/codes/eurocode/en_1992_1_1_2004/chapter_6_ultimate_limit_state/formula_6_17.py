"""Formula 6.17 from EN 1992-1-1:2004: Chapter 6 - Ultimate limit state."""

from blueprints.codes.eurocode.en_1992_1_1_2004 import EN_1992_1_1_2004
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula
from blueprints.type_alias import MM
from blueprints.validations import raise_if_negative


class Form6Dot17NominalWebWidth(Formula):
    r"""Class representing formula 6.17 for the calculation of the nominal web width (for non-grouted ducts, grouted plastic ducts
    and unbonded tendons), [$b_{w,nom}$].
    """

    label = "6.17"
    source_document = EN_1992_1_1_2004

    def __init__(
        self,
        b_w: MM,
        diameters: list[MM],
    ) -> None:
        r"""[$b_{w,nom}$] Nominal web width [$mm$].

        EN 1992-1-1:2004 art.6.2.3(6) - Formula (6.17)

        Parameters
        ----------
        b_w : MM
            [$b_{w}$] Web width [$mm$].
        diameters : list[MM]
            [$⌀$] Diameters of the reinforcement bars for the most unfavourable level [$mm$].
        """
        super().__init__()
        self.b_w = b_w
        self.diameters = diameters

    @staticmethod
    def _evaluate(
        b_w: MM,
        diameters: list[MM],
    ) -> MM:
        """Evaluates the formula, for more information see the __init__ method."""
        raise_if_negative(b_w=b_w)
        for diameter in diameters:
            raise_if_negative(diameter=diameter)

        return b_w - 1.2 * sum(diameters)

    def latex(self, n: int = 3) -> LatexFormula:
        """Returns LatexFormula object for formula 6.17."""
        return LatexFormula(
            return_symbol=r"b_{w,nom}",
            result=f"{self:.{n}f}",
            equation=r"b_{w} - 1.2 \cdot \sum(⌀)",
            numeric_equation=rf"{self.b_w:.{n}f} - 1.2 \cdot \left({' + '.join([f'{d:.{n}f}' for d in self.diameters])} \right)",
            comparison_operator_label="=",
            unit="mm",
        )
