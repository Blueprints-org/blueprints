"""Table 4.5N from NEN-EN 1992-1-1:2005+A1:2015+NB:2016+A1:2020: Chapter 4 - Durability and cover to reinforcement."""

from blueprints.codes.eurocode.exposure_classes import ExposureClassesBase
from blueprints.codes.eurocode.nen_en_1992_1_1_a1_2020 import NEN_EN_1992_1_1_A1_2020
from blueprints.codes.eurocode.structural_class import ConcreteStructuralClassBase
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula
from blueprints.type_alias import MM


class Table4Dot5nMinimumCoverDurabilityPrestressingSteel(Formula):
    r"""Class representing the table 4.5N
    for the calculation of the minimum cover [$c_{min,dur}$] [$mm$] requirements with regard to durability
    for prestressing steel.
    """

    label = "4.5N"
    source_document = NEN_EN_1992_1_1_A1_2020

    def __init__(
        self,
        exposure_classes: ExposureClassesBase,
        structural_class: ConcreteStructuralClassBase,
    ) -> None:
        r"""[$c_{min,dur}$] Calculates the minimum concrete cover with regard to durability [$mm$] for prestressing steel.

        NEN-EN 1992-1-1:2005+A1:2015+NB:2016+A1:2020 art.4.4.1.2 (5) - Table (4.5N)

        Parameters
        ----------
        exposure_classes: ExposureClassesBase
            The exposure classes of the concrete. Use the [$Table4Dot1ExposureClasses$] class. [$-$]
        structural_class: ConcreteStructuralClassBase
            The structural class of the concrete. Use the [$Table4Dot3ConcreteStructuralClass$] class. [$-$]
        """
        super().__init__()
        self.exposure_classes = exposure_classes
        self.structural_class = structural_class

    @staticmethod
    def _evaluate(
        exposure_classes: ExposureClassesBase,
        structural_class: ConcreteStructuralClassBase,
    ) -> MM:
        """For more detailed documentation see the class docstring."""
        if not isinstance(structural_class, int):
            raise TypeError(f"Structural class must be (a subclass of) an integer, not {type(structural_class)}.")

        if exposure_classes.chloride.value in [
            "XD3",
            "XD2",
        ] or exposure_classes.chloride_seawater.value in ["XS2", "XS3"]:
            calculated_cover = 25 + structural_class * 5
        elif exposure_classes.chloride.value == "XD1" or exposure_classes.chloride_seawater.value == "XS1":
            calculated_cover = 20 + structural_class * 5
        elif exposure_classes.carbonation.value == "XC4":
            calculated_cover = 15 + structural_class * 5
        elif exposure_classes.carbonation.value in ["XC2", "XC3"]:
            calculated_cover = 10 + structural_class * 5
        elif exposure_classes.carbonation.value == "XC1":
            calculated_cover = max(15, (structural_class * 5))
        else:
            calculated_cover = max(10, ((structural_class - 2) * 5))

        return calculated_cover

    def latex(self) -> LatexFormula:
        """Returns LatexFormula object for table 4.5N."""
        return LatexFormula(
            return_symbol=r"c_{min,dur}",
            result=f"{self:.0f}",
            equation=rf"structural class {self.structural_class} & exposure classes ({self.exposure_classes})",
            comparison_operator_label="=",
        )
