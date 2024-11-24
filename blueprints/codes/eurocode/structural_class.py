"""Generic module for the concrete structural class according to NEN-EN 1992-1-1 Concrete - General."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Self

from blueprints.codes.eurocode.exposure_classes import ExposureClassesBase as ExposureClasses
from blueprints.materials.concrete import ConcreteMaterial
from blueprints.type_alias import YEARS


class ConcreteStructuralClassBase(int):
    """Base class for the Structural class of the concrete element.

    This Class can be used to keep track of the operations of the structural class of the concrete element.

    In accordance with:
    NEN-EN 1992-1-1 Concrete - General
    """

    def __new__(
        cls,
        concrete_structural_class_calculator: type[AbstractConcreteStructuralClassCalculator],
        *args,
        **kwargs,
    ) -> Self:
        """Constructor of the ConcreteStructuralClassBase class.

        Parameters
        ----------
        concrete_structural_class_calculator: type[AbstractConcreteStructuralClassCalculator]
            The calculator class for the structural class of the concrete element
        *args
            Arguments for initiating the calculator instance
        **kwargs
            Keyword arguments for initiating the calculator instance

        Raises
        ------
        TypeError
            If concrete_structural_class_calculator is not a subclass of AbstractConcreteStructuralClassCalculator

        Returns
        -------
        StructuralClass
            The instance of the ConcreteStructuralClassBase class
        """
        if not issubclass(concrete_structural_class_calculator, AbstractConcreteStructuralClassCalculator):
            raise TypeError(f"unsupported calculator type(s) for the ConcreteStructuralClassBase class: '{concrete_structural_class_calculator}'")
        calculator_instance = concrete_structural_class_calculator(*args, **kwargs)
        calculator_instance.calculate_structural_class()
        structural_class = calculator_instance.structural_class
        new_instance = super().__new__(cls, structural_class)
        new_instance.explanation = calculator_instance.explanation
        return new_instance

    @property
    def explanation(self) -> str:
        """Property which returns the structural class explanation.

        Returns
        -------
        str
            The explanation of the structural class
        """
        return self._explanation

    @explanation.setter
    def explanation(self, explanation: str) -> None:
        """Setter for the explanation of the structural class.

        Parameters
        ----------
        explanation: str
            The explanation of the structural class

        Raises
        ------
        AttributeError
            If the explanation is already set
        """
        if not hasattr(self, "_explanation"):
            self._explanation = explanation
        else:
            raise AttributeError(f"Attribute 'explanation' of {self.__class__} object is read-only and cannot be modified after initialization.")

    def __str__(self) -> str:
        """Returns a string representation of the object.

        Overrides the default __str__ method to include the prefix 'S' before the string representation
        of the superclass.

        Returns
        -------
        str
            The string representation of the object.
        """
        return f"S{super().__str__()}"


class AbstractConcreteStructuralClassCalculator(ABC):
    """(Abstract class for) Structural class calculator of the concrete element.

    This abstract class is in accordance with:
    NEN-EN 1992-1-1 Concrete - General

    This abstract class should be implemented in for each specific release of the Eurocode.
    """

    DEFAULT_STRUCTURAL_CLASS = 0
    DEFAULT_EXPLANATION = ""

    def __init__(
        self,
        exposure_classes: ExposureClasses,
        design_working_life: YEARS,
        concrete_material: ConcreteMaterial,
        plate_geometry: bool,
        quality_control: bool,
    ) -> None:
        """Initializer of the AbstractConcreteStructuralClassCalculator class.

        The concrete implementation of this class will be used to calculate the structural class.

        Parameters
        ----------
        exposure_classes : ExposureClasses
            The exposure classes of the concrete element
        design_working_life : YEARS
            The design working life of the concrete element
        concrete_material : ConcreteMaterial
            The concrete material of the concrete element
        plate_geometry : bool
            True if the concrete element has a plate geometry, False otherwise
        quality_control : bool
            True if the quality control of the concrete element is ensured, False otherwise
        """
        self.exposure_classes = exposure_classes
        self.design_working_life = design_working_life
        self.concrete_material = concrete_material
        self.plate_geometry = plate_geometry
        self.quality_control = quality_control
        self._calculated = False
        self._structural_class = self.DEFAULT_STRUCTURAL_CLASS
        self._explanation = self.DEFAULT_EXPLANATION

    def __setattr__(self, name: str, value: Any) -> None:  # noqa: ANN401
        """Setter for the attributes of the class.

        This method is used to set the attributes of the class and check if the structural class needs to be recalculated.

        Parameters
        ----------
        name: str
            The name of the attribute
        value: Any
            The value of the attribute
        """
        attributes_affecting_calculation = {"exposure_classes", "design_working_life", "concrete_material", "plate_geometry", "quality_control"}
        if name in attributes_affecting_calculation and getattr(self, name, None) != value:
            self._calculated = False
        super().__setattr__(name, value)

    @property
    @abstractmethod
    def source_document(self) -> str:
        """Property for the source document.

        For example, "NEN-EN 1992-1-1+C2:2011"
        Try to use the official and complete name of the document including publishing year, if possible.

        Returns
        -------
        str
            The reference to the document where the structural class calculation method originates.
            This is an abstract method and must be implemented in all subclasses.
        """

    @property
    def structural_class(self) -> int:
        """Property which returns the structural class.

        Returns
        -------
        int
            the structural class
        """
        if not self._calculated:
            raise ValueError("The structural class has not been calculated yet.")
        return self._structural_class

    @property
    def explanation(self) -> str:
        """Property which returns the structural class explanation."""
        if not self._calculated:
            raise ValueError("The structural class has not been calculated yet.")
        return self._explanation

    def update_structural_class(self, delta: int, explanation: str) -> None:
        """Method to update the structural class with the given delta and explanation.

        Parameters
        ----------
        delta: int
            The delta to be added to the structural class
        explanation: str
            The explanation of the structural class calculation

        Raises
        ------
        TypeError
            If the delta is not an integer
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
        """Method to execute the calculation of the structural class."""
        if not self._calculated:
            self._structural_class_delta_design_working_life()
            self._structural_class_delta_concrete_grade()
            self._structural_class_delta_plate_geometry()
            self._structural_class_delta_quality_control()
            self._calculated = True

    @abstractmethod
    def _structural_class_delta_design_working_life(self) -> None:
        """Calculates the addition to the structural class based on the design working life."""

    @abstractmethod
    def _structural_class_delta_quality_control(self) -> None:
        """Calculates the addition to the structural class based on the quality control."""

    @abstractmethod
    def _structural_class_delta_plate_geometry(self) -> None:
        """Calculates the addition to the structural class based on the plate geometry."""

    @abstractmethod
    def _structural_class_delta_concrete_grade(self) -> None:
        """Calculates the addition to the structural class based on the concrete grade."""
