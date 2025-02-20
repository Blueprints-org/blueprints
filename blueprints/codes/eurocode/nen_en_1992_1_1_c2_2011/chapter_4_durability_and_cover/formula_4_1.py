"""Formula 4.1 from NEN-EN 1992-1-1+C2:2011: Chapter 4 - Durability and cover to reinforcement."""

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011 import NEN_EN_1992_1_1_C2_2011
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula
from blueprints.type_alias import MM
from blueprints.validations import raise_if_negative


class Form4Dot1NominalConcreteCover(Formula):
    r"""Class representing the formula 4.1 for the calculation of the nominal concrete cover [$c_{nom}$] [$mm$]."""

    label = "4.1"
    source_document = NEN_EN_1992_1_1_C2_2011

    def __init__(
        self,
        c_min: MM,
        delta_c_dev: MM,
    ) -> None:
        r"""[$c_{nom}$] Calculates the nominal concrete cover [$mm$].

        Please be advised that this formula does not take various considerations in art.4.4.1.2 and 4.4.1.3 into account.
        For a more detailed calculation, please refer to the NominalConcreteCover class.

        NEN-EN 1992-1-1+C2:2011 art.4.4.1.1 (2) - Formula (4.1)

        Parameters
        ----------
        c_min: MM
            [$c_{min}$] Minimum concrete cover based on art. 4.4.1.2 [$mm$].
        delta_c_dev: MM
            [$\Delta c_{dev}$] Construction tolerance based on art. 4.4.1.3 [$mm$].
        """
        super().__init__()
        self.c_min = c_min
        self.delta_c_dev = delta_c_dev

    @staticmethod
    def _evaluate(
        c_min: MM,
        delta_c_dev: MM,
    ) -> MM:
        """For more detailed documentation see the class docstring."""
        raise_if_negative(c_min=c_min, delta_c_dev=delta_c_dev)
        return c_min + delta_c_dev

    def latex(self) -> LatexFormula:
        """Returns LatexFormula object for formula 4.1."""
        return LatexFormula(
            return_symbol=r"c_{nom}",
            result=str(self),
            equation=r"c_{min}+\Delta c_{dev}",
            numeric_equation=f"{self.c_min}+{self.delta_c_dev}",
            comparison_operator_label="=",
        )
