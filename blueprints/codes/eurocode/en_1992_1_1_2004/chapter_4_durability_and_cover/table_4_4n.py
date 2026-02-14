"""Table 4.4N from EN 1992-1-1:2004: Chapter 4 - Durability and cover to reinforcement."""

from blueprints.codes.eurocode.en_1992_1_1_2004 import EN_1992_1_1_2004
from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_4_durability_and_cover._base_classes.structural_class import ConcreteStructuralClassBase
from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_4_durability_and_cover.table_4_1 import Table4Dot1ExposureClasses
from blueprints.codes.formula import Formula
from blueprints.codes.latex_formula import LatexFormula
from blueprints.type_alias import MM


class Table4Dot4nMinimumCoverDurabilityReinforcementSteel(Formula):
    r"""Class representing the table 4.4N
    for the calculation of the minimum cover [$c_{min,dur}$] [$mm$] requirements with regard to durability
    for reinforcement steel.
    """

    label = "4.4N"
    source_document = EN_1992_1_1_2004

    def __init__(
        self,
        exposure_classes: Table4Dot1ExposureClasses,
        structural_class: ConcreteStructuralClassBase,
    ) -> None:
        r"""[$c_{min,dur}$] Calculates the minimum concrete cover with regard to durability [$mm$] for reinforcement steel.

        EN 1992-1-1:2004 art.4.4.1.2 (5) - Table (4.4N)

        Parameters
        ----------
        exposure_classes: Table4Dot1ExposureClasses
            The exposure classes of the concrete. Use the [$Table4Dot1ExposureClasses$] class. [$-$]
        structural_class: ConcreteStructuralClassBase
            The structural class of the concrete. Use the [$Table4Dot3ConcreteStructuralClass$] class. [$-$]
        """
        super().__init__()
        self.exposure_classes: Table4Dot1ExposureClasses = exposure_classes
        self.structural_class: ConcreteStructuralClassBase = structural_class

    @staticmethod
    def _evaluate(
        exposure_classes: Table4Dot1ExposureClasses,
        structural_class: ConcreteStructuralClassBase,
    ) -> MM:
        """For more detailed documentation see the class docstring."""
        if not isinstance(structural_class, int):
            raise TypeError(f"Structural class must be (a subclass of) an integer, not {type(structural_class)}.")

        if structural_class < 1 or structural_class > 6:
            raise ValueError("Structural class must be between 1 and 6.")

        if exposure_classes.chloride.value in [
            "XD3",
            "XD2",
        ] or exposure_classes.chloride_seawater.value in ["XS2", "XS3"]:
            calculated_cover = 20 + structural_class * 5
        elif exposure_classes.chloride.value == "XD1" or exposure_classes.chloride_seawater.value == "XS1":
            calculated_cover = 15 + structural_class * 5
        elif exposure_classes.carbonation.value == "XC4":
            calculated_cover = 10 + structural_class * 5
        elif exposure_classes.carbonation.value in ["XC2", "XC3"]:
            calculated_cover = 5 + structural_class * 5
        elif exposure_classes.carbonation.value == "XC1":
            calculated_cover = max(10, ((structural_class - 1) * 5))
        else:
            calculated_cover = max(10, ((structural_class - 2) * 5))

        return calculated_cover

    def latex(self, n: int = 0) -> LatexFormula:
        """Returns LatexFormula object for table 4.4N."""
        return LatexFormula(
            return_symbol=r"c_{min,dur}",
            result=f"{self:.{n}f}",
            equation=r"\text{" + rf"structural class {self.structural_class} and exposure classes ({self.exposure_classes})" + "}",
            comparison_operator_label="=",
        )
