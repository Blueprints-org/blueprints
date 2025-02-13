"""Module for the concrete structural class
according to Table 4.3 from NEN-EN 1992-1-1+C2:2011: Chapter 4 - Durability and cover to reinforcement.
"""

from collections.abc import Sequence
from typing import Self

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011 import NEN_EN_1992_1_1_C2_2011
from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011.chapter_4_durability_and_cover.table_4_1 import (
    Carbonation,
    Chloride,
    ChlorideSeawater,
    Table4Dot1ExposureClasses,
)
from blueprints.codes.eurocode.structural_class import AbstractConcreteStructuralClassCalculator, ConcreteStructuralClassBase
from blueprints.materials.concrete import ConcreteMaterial, ConcreteStrengthClass
from blueprints.type_alias import YEARS

"""Design working life in years as defined in table 4.3 of NEN-EN 1992-1-1+C2:2011."""
DESIGN_WORKING_LIFE_DEFAULT = 50
DESIGN_WORKING_LIFE_100 = 100


class ConcreteStructuralClassCalculator(AbstractConcreteStructuralClassCalculator):
    """Implementation of the structural class calculator of the concrete element.

    In accordance with:
    NEN-EN 1992-1-1+C2:2011 Concrete - General
    """

    source_document = NEN_EN_1992_1_1_C2_2011
    DEFAULT_STRUCTURAL_CLASS = 4
    DEFAULT_EXPLANATION = "Default structural class (S4)"

    def __init__(
        self,
        exposure_classes: Table4Dot1ExposureClasses | Sequence[str],
        design_working_life: YEARS,
        concrete_material: ConcreteMaterial,
        plate_geometry: bool,
        quality_control: bool,
    ) -> None:
        """Initializer of the ConcreteStructuralClassCalculator class.

        Parameters
        ----------
        exposure_classes : ExposureClasses | Sequence[str]
            The exposure classes of the concrete element. This can be a sequence of strings or an instance of the ExposureClasses class.
        design_working_life : YEARS, optional
            The design working life of the concrete element
        concrete_material : ConcreteMaterial, optional
            The concrete material of the concrete element
        plate_geometry : bool, optional
            True if the concrete element has a plate geometry, False otherwise
        quality_control : bool, optional
            True if the quality control of the concrete element is ensured, False otherwise
        """
        if not isinstance(exposure_classes, Table4Dot1ExposureClasses):
            exposure_classes = Table4Dot1ExposureClasses.from_exposure_list(exposure_classes)
        super().__init__(exposure_classes, design_working_life, concrete_material, plate_geometry, quality_control)

    def _structural_class_delta_design_working_life(self) -> None:
        """Calculates the addition to the structural class based on the design working life.

        In accordance with:
        NNEN-EN 1992-1-1+C2:2011 Concrete - General
        """
        if self.design_working_life > DESIGN_WORKING_LIFE_DEFAULT:
            explanation = (
                f"{DESIGN_WORKING_LIFE_100} years"
                if self.design_working_life == DESIGN_WORKING_LIFE_100
                else f"{self.design_working_life} > {DESIGN_WORKING_LIFE_DEFAULT} => {DESIGN_WORKING_LIFE_100} years"
            )
            self.update_structural_class(2, explanation)
        else:
            self.update_structural_class(0, f"{DESIGN_WORKING_LIFE_DEFAULT} years")

    def _structural_class_delta_quality_control(self) -> None:
        """Calculates the addition to the structural class based on the quality control.

        In accordance with:
        NNEN-EN 1992-1-1+C2:2011 Concrete - General
        """
        if self.quality_control:
            self.update_structural_class(-1, "quality control")
        else:
            self.update_structural_class(0, "no quality control")

    def _structural_class_delta_plate_geometry(self) -> None:
        """Calculates the addition to the structural class based on the plate geometry.

        In accordance with:
        NNEN-EN 1992-1-1+C2:2011 Concrete - General
        """
        if self.plate_geometry:
            self.update_structural_class(-1, "plate geometry")
        else:
            self.update_structural_class(0, "no plate geometry")

    def _structural_class_delta_concrete_grade(self) -> None:
        """Calculates the addition to the structural class based on the concrete grade.

        In accordance with:
        NNEN-EN 1992-1-1+C2:2011 Concrete - General
        """
        decisive_exposure_classes = {
            ConcreteStrengthClass("C45/55"): {Chloride.XD3.value, ChlorideSeawater.XS2.value, ChlorideSeawater.XS3.value},
            ConcreteStrengthClass("C40/50"): {Carbonation.XC4.value, Chloride.XD1.value, Chloride.XD2.value, ChlorideSeawater.XS1.value},
            ConcreteStrengthClass("C35/45"): {Carbonation.XC2.value, Carbonation.XC3.value},
            ConcreteStrengthClass("C30/37"): {Carbonation.XC1.value},
        }
        exposure_classes = {exposure_class.value for exposure_class in self.exposure_classes}

        for concrete_grade, decisive_exposure_class in decisive_exposure_classes.items():
            if decisive_exposure_class.intersection(exposure_classes):
                return (
                    self.update_structural_class(0, "no reduction with respect to concrete grade")
                    if self.concrete_material.f_ck < ConcreteMaterial(concrete_grade).f_ck
                    else self.update_structural_class(-1, f"concrete grade >= {concrete_grade.value}")
                )
        return (
            self.update_structural_class(0, "no reduction with respect to concrete grade")
            if self.concrete_material.f_ck < ConcreteMaterial(ConcreteStrengthClass("C30/37")).f_ck
            else self.update_structural_class(-1, "concrete grade >= C30/37")
        )


class Table4Dot3ConcreteStructuralClass(ConcreteStructuralClassBase):
    """Implementation of table 4.3 from NEN-EN 1992-1-1+C2:2011 Concrete - General.

    Structural class of the concrete element.
    """

    def __new__(
        cls,
        *args,
        **kwargs,
    ) -> Self:
        """Constructor of the StructuralClass class.

        Parameters
        ----------
            value (int): The value of the structural class

        Returns
        -------
            Self (ConcreteStructuralClass): The instance of the ConcreteStructuralClass class
        """
        return super().__new__(cls, ConcreteStructuralClassCalculator, *args, **kwargs)

    def __init__(
        self,
        exposure_classes: Table4Dot1ExposureClasses | Sequence[str],
        design_working_life: YEARS,
        concrete_material: ConcreteMaterial,
        plate_geometry: bool,
        quality_control: bool,
    ) -> None:
        """Initializer of the ConcreteStructuralClass class.

        Parameters
        ----------
        exposure_classes : Table4Dot1ExposureClasses | Sequence[str]
            The exposure classes of the concrete element. This can be a sequence of strings or an instance of the ExposureClasses class.
        design_working_life : YEARS
            The design working life of the concrete element
        concrete_material : ConcreteMaterial
            The concrete material of the concrete element
        plate_geometry : bool
            True if the concrete element has a plate geometry, False otherwise
        quality_control : bool
            True if the quality control of the concrete element is ensured, False otherwise
        """
