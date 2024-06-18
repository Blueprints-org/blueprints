"""Module for the concrete structural class
according to Table 4.3 from NEN-EN 1992-1-1+C2:2011: Chapter 4 - Durability and cover to reinforcement.
"""

from __future__ import annotations

from typing_extensions import Self

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011.chapter_4_durability_and_cover.table_4_1 import (
    Carbonation,
    Chloride,
    ChlorideSeawater,
    ExposureClasses,
)
from blueprints.materials.concrete import ConcreteMaterial, ConcreteStrengthClass

DEFAULT_STRUCTURAL_CLASS = 4
DESIGN_WORKING_LIFE_DEFAULT = 50
DESIGN_WORKING_LIFE_75 = 75
DESIGN_WORKING_LIFE_100 = 100


class ConcreteStructuralClassBase(int):
    """Structural class base of the concrete element.

    This Class can be used to keep track of the operations of the structural class of the concrete element.

    In accordance with:
    NEN-EN 1992-1-1:2005+A1:2015+NB:2016+A1:2020 Concrete - General
    """

    def __new__(
        cls,
        value: int,
        *args,  # noqa: ARG003
        **kwargs,  # noqa: ARG003
    ) -> Self:
        """Constructor of the StructuralClass class.

        Args:
            value (int): The value of the structural class

        Returns
        -------
            StructuralClass: The instance of the StructuralClass class
        """
        return super().__new__(cls, value)

    def __init__(
        self,
        value: int,  # noqa: ARG002
        explanation: str = "",
    ) -> None:
        """Initializer of the StructuralClass class.

        Args:
            value (int): The value of the structural class
            explanation (str): The explanation of the structural class calculation. Defaults "".
        """
        super().__init__()
        self.explanation = explanation

    def __str__(self) -> str:
        """Returns a string representation of the object.

        Overrides the default __str__ method to include the prefix 'S' before the string representation
        of the superclass.

        Returns
        -------
            str: The string representation of the object.
        """
        return f"S{super().__str__()}"


class ConcreteStructuralClassBuilder:
    """Structural class delta of the concrete element.

    In accordance with:
    NEN-EN 1992-1-1:2005+A1:2015+NB:2016+A1:2020 Concrete - General
    """

    def __init__(
        self,
        exposure_classes: ExposureClasses,
        design_working_life: float = DESIGN_WORKING_LIFE_DEFAULT,
        concrete_material: ConcreteMaterial = ConcreteMaterial(),
        plate_geometry: bool = False,
        quality_control: bool = False,
    ) -> None:
        """Initializer of the ConcreteStructuralClassDelta class.

        This class should be used to calculate the structural class. This has to be used with the
        StructuralClassBase class. The StructuralClassBase is able to keep track of the explanation of all operations.

        Parameters
        ----------
            value (int): The value of the structural class
            explanation (str): The explanation of the structural class
        """
        self.exposure_classes = exposure_classes
        self.design_working_life = design_working_life
        self.concrete_material = concrete_material
        self.plate_geometry = plate_geometry
        self.quality_control = quality_control
        self._structural_class = DEFAULT_STRUCTURAL_CLASS
        self._explanation: str = "Default structural class (S4)"
        self._calculated = False

    @property
    def structural_class(self) -> ConcreteStructuralClassBase:
        """Property which returns the structural class."""
        if not self._calculated:
            raise ValueError("The structural class has not been calculated yet.")
        return ConcreteStructuralClassBase(self._structural_class, self._explanation)

    def update_structural_class(self, delta: int, explanation: str) -> None:
        """Update the structural class with the given delta and explanation.

        Parameters
        ----------
            delta (int): The delta to be added to the structural class.
            explanation (str): The explanation of the structural class calculation.
        """
        if not isinstance(delta, int):
            raise TypeError(f"unsupported delta type(s) for the update operation: '{type(delta)}'")
        unit_suffix = "classes" if abs(delta) > 1 else "class"
        operator_symbol = "+" if delta >= 0 else "-"
        self._structural_class += delta
        self._explanation = f"{self._explanation} {operator_symbol} {abs(delta)} {unit_suffix} ({explanation})"

    def calculate_structural_class(
        self,
    ) -> None:
        """Property which calculates the structural class.

        Based on the actual exposure classes according to Table 4.3N of
        EN-EN 1992-1-1:2005+A1:2015+NB:2016+A1:2020 Concrete - General

        Returns
        -------
            ConcreteStructuralClass: the calculated structural class
        """
        if not self._calculated:
            self._structural_class_delta_design_working_life()
            self._structural_class_delta_concrete_grade()
            self._structural_class_delta_plate_geometry()
            self._structural_class_delta_quality_control()
            self._calculated = True

    def _structural_class_delta_design_working_life(self) -> None:
        """Calculates the addition to the structural class based on the design working life.

        In accordance with:
        NEN-EN 1992-1-1:2005+A1:2015+NB:2016+A1:2020 Concrete - General
        """
        if DESIGN_WORKING_LIFE_75 <= self.design_working_life < DESIGN_WORKING_LIFE_100:
            self.update_structural_class(1, f"{DESIGN_WORKING_LIFE_75} jr.")
        elif self.design_working_life >= DESIGN_WORKING_LIFE_100:
            self.update_structural_class(2, f"{DESIGN_WORKING_LIFE_100} jr.")
        else:
            self.update_structural_class(0, f"{DESIGN_WORKING_LIFE_DEFAULT} jr.")

    def _structural_class_delta_quality_control(self) -> None:
        """Calculates the addition to the structural class based on the quality control.

        In accordance with:
        NEN-EN 1992-1-1:2005+A1:2015+NB:2016+A1:2020 Concrete - General
        """
        if quality_control:
            self.update_structural_class(-1, "quality control")
        else:
            self.update_structural_class(0, "no quality control")

    def _structural_class_delta_plate_geometry(self) -> None:
        """Calculates the addition to the structural class based on the plate geometry.

        In accordance with:
        NEN-EN 1992-1-1:2005+A1:2015+NB:2016+A1:2020 Concrete - General
        """
        if plate_geometry:
            self.update_structural_class(-1, "plate geometry")
        else:
            self.update_structural_class(0, "no plate geometry")

    def _structural_class_delta_concrete_grade(self) -> None:
        """Calculates the addition to the structural class based on the concrete grade.

        In accordance with:
        NEN-EN 1992-1-1:2005+A1:2015+NB:2016+A1:2020 Concrete - General
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
                    if concrete_material.f_ck < ConcreteMaterial(concrete_grade).f_ck
                    else self.update_structural_class(-1, f"concrete grade >= {concrete_grade.value}")
                )
        return (
            self.update_structural_class(0, "no reduction with respect to concrete grade")
            if concrete_material.f_ck < ConcreteMaterial(ConcreteStrengthClass("C30/37")).f_ck
            else self.update_structural_class(-1, "concrete grade >= C30/37")
        )


class ConcreteStructuralClass(ConcreteStructuralClassBase):
    """Structural class of the concrete element.

    This Class keeps track of the operations of the structural class of the concrete element.

    In accordance with:
    NEN-EN 1992-1-1:2005+A1:2015+NB:2016+A1:2020 Concrete - General
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
        builder = ConcreteStructuralClassBuilder(*args, **kwargs)
        builder.calculate_structural_class()
        structural_class = builder.structural_class
        new_instance = super().__new__(cls, structural_class)
        new_instance.explanation = structural_class.explanation
        return new_instance

    def __init__(
        self,
        exposure_classes: ExposureClasses,
        design_working_life: float = DESIGN_WORKING_LIFE_DEFAULT,
        concrete_material: ConcreteMaterial = ConcreteMaterial(),
        plate_geometry: bool = False,
        quality_control: bool = False,
    ) -> None:
        """Initializer of the StructuralClass class.

        Parameters
        ----------
            value (int): The value of the structural class
            explanation (str): The explanation of the structural class calculation. Defaults "".
        """


if __name__ == "__main__":
    # Example of the usage of the ConcreteStructuralClass class
    exposure_classes = ExposureClasses(Carbonation.XC2, Chloride.XD1)
    design_working_life = 75
    concrete_material = ConcreteMaterial(ConcreteStrengthClass("C40/50"))
    plate_geometry = False
    quality_control = False

    structural_class = ConcreteStructuralClass(
        exposure_classes,
        design_working_life,
        concrete_material,
        plate_geometry,
        quality_control,
    )
    print(structural_class)  # noqa: T201
    print(type(structural_class))  # noqa: T201
    print(structural_class.explanation)  # noqa: T201
