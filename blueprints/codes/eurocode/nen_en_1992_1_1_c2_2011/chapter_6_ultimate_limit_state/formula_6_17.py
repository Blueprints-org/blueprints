"""Formula 6.17 from NEN-EN 1992-1-1+C2:2011: Chapter 6 - Ultimate limit state."""

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011 import NEN_EN_1992_1_1_C2_2011
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula
from blueprints.type_alias import MM
from blueprints.validations import raise_if_negative


class Form6Dot17NominalWebWidth(Formula):
    r"""Class representing formula 6.17 for the calculation of the nominal web width, :math:`b_{w,nom}`."""

    label = "6.17"
    source_document = NEN_EN_1992_1_1_C2_2011

    def __init__(
        self,
        b_w: MM,
        diameters: list[MM],
    ) -> None:
        r"""[:math:`b_{w,nom}`] Nominal web width [:math:`mm`].

        NEN-EN 1992-1-1+C2:2011 art.6.2.3(6) - Formula (6.17)

        Parameters
        ----------
        b_w : MM
            [:math:`b_{w}`] Web width [:math:`mm`].
        diameters : list[MM]
            [:math:`⌀`] Diameters of the reinforcement bars for the most unfavourable level [:math:`mm`].
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

    def latex(self) -> LatexFormula:
        """Returns LatexFormula object for formula 6.17."""
        return LatexFormula(
            return_symbol=r"b_{w,nom}",
            result=f"{self:.3f}",
            equation=r"b_{w} - 1.2 \cdot \sum(⌀)",
            numeric_equation=rf"{self.b_w:.3f} - 1.2 \cdot \left({' + '.join([f'{d:.3f}' for d in self.diameters])} \right)",
            comparison_operator_label="=",
            unit="mm",
        )
