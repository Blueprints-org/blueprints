"""Table 4.2 from NEN-EN 1992-1-1+C2:2011: Chapter 4 - Durability and cover to reinforcement."""

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011 import NEN_EN_1992_1_1_C2_2011
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula
from blueprints.type_alias import MM
from blueprints.validations import raise_if_less_or_equal_to_zero


class Table4Dot2MinimumCoverWithRegardToBond(Formula):
    """Class representing the table 4.2 for the calculation of the minimum cover :math:`c_{min,b}` [:math:`mm`] requirements with regard to bond."""

    label = "4.2"
    source_document = NEN_EN_1992_1_1_C2_2011

    def __init__(
        self,
        diameter: MM,
        nominal_max_aggregate_size_greater_than_32_mm: bool,
    ) -> None:
        """[:math:`c_{min,b}`] Calculates the minimum concrete cover with regard to bond [:math:`mm`].

        NEN-EN 1992-1-1+C2:2011 art.4.4.1.2 (3) - Table (4.2)

        Parameters
        ----------
        diameter: MM
            Diameter of the reinforcement [:math:`mm`].
            In case of bundled bars, the equivalent diameter [:math:`Ø_{n}`] as defined in par. 8.9.1 should be used.
            Use your own implementation of this value or use the :class:`Form8Dot14EquivalentDiameterBundledBars` class.
        nominal_max_aggregate_size_greater_than_32_mm: bool
            Is the nominal maximum aggregate size greater than 32 [:math:`mm`]?
        """
        super().__init__()
        self.diameter = diameter
        self.nominal_max_aggregate_size_greater_than_32_mm = nominal_max_aggregate_size_greater_than_32_mm

    @staticmethod
    def _evaluate(
        diameter: MM,
        nominal_max_aggregate_size_greater_than_32_mm: bool,
    ) -> MM:
        """For more detailed documentation see the class docstring."""
        raise_if_less_or_equal_to_zero(diameter=diameter)
        if not isinstance(nominal_max_aggregate_size_greater_than_32_mm, bool):
            raise TypeError("The parameter 'nominal_max_aggregate_size_greater_than_32_mm' must be a boolean.")
        return diameter + 5 * nominal_max_aggregate_size_greater_than_32_mm

    def latex(self) -> LatexFormula:
        """Returns LatexFormula object for table 4.2."""
        suffix = " + 5" if self.nominal_max_aggregate_size_greater_than_32_mm else ""
        return LatexFormula(
            return_symbol=r"c_{min,b}",
            result=f"{self:.0f}",
            equation=r"(equivalent) rebar diameter" + suffix,
            numeric_equation=f"{self.diameter}" + suffix,
            comparison_operator_label="=",
        )
