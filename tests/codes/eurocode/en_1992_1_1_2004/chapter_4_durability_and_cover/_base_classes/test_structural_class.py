"""Test cases for the structural class definitions."""

from typing import Self

import pytest

from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_4_durability_and_cover._base_classes.structural_class import (
    AbstractConcreteStructuralClassCalculator,
    ConcreteStructuralClassBase,
)
from blueprints.materials.concrete import ConcreteMaterial
from tests.codes.eurocode.en_1992_1_1_2004.chapter_4_durability_and_cover._base_classes.test_exposure_classes import (
    DummyCarbonation,
    DummyChemical,
    DummyChloride,
    DummyChlorideSeawater,
    DummyExposureClasses,
    DummyFreezeThaw,
)


class MockConcreteStructuralClassCalculator(AbstractConcreteStructuralClassCalculator):
    """Mock class for the AbstractConcreteStructuralClassCalculator."""

    source_document = "Mock"
    DEFAULT_STRUCTURAL_CLASS = 1
    DEFAULT_EXPLANATION = "Default structural class (S1)"

    def __init__(
        self,
        exposure_classes: DummyExposureClasses,
        design_working_life: float,
        concrete_material: ConcreteMaterial,
        plate_geometry: bool,
        quality_control: bool,
    ) -> None:
        """Initializer of the MockConcreteStructuralClassCalculator class."""
        super().__init__(exposure_classes, design_working_life, concrete_material, plate_geometry, quality_control)

    def _structural_class_delta_concrete_grade(self) -> None:
        pass

    def _structural_class_delta_design_working_life(self) -> None:
        pass

    def _structural_class_delta_quality_control(self) -> None:
        if self.quality_control:
            self.update_structural_class(1, "Quality control")

    def _structural_class_delta_plate_geometry(self) -> None:
        pass


class MockConcreteStructuralClass(ConcreteStructuralClassBase):
    """Mock class for the ConcreteStructuralClassBase."""

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
        return super().__new__(cls, MockConcreteStructuralClassCalculator, *args, **kwargs)


@pytest.fixture
def structural_class() -> MockConcreteStructuralClass:
    """Fixture that returns an instance of the structural class for testing."""
    exposure_classes = DummyExposureClasses(
        dummy_carbonation=DummyCarbonation.XC1,
        dummy_chloride=DummyChloride.NA,
        dummy_chloride_seawater=DummyChlorideSeawater.NA,
        dummy_freeze_thaw=DummyFreezeThaw.NA,
        dummy_chemical=DummyChemical.XA1,
    )
    design_working_life = 50.0
    concrete_material = ConcreteMaterial()
    plate_geometry = True
    quality_control = True
    return MockConcreteStructuralClass(
        exposure_classes=exposure_classes,
        design_working_life=design_working_life,
        concrete_material=concrete_material,
        plate_geometry=plate_geometry,
        quality_control=quality_control,
    )


@pytest.fixture
def calculator() -> MockConcreteStructuralClassCalculator:
    """Fixture that returns an instance of the calculator for testing."""
    exposure_classes = DummyExposureClasses(
        dummy_carbonation=DummyCarbonation.XC1,
        dummy_chloride=DummyChloride.NA,
        dummy_chloride_seawater=DummyChlorideSeawater.NA,
        dummy_freeze_thaw=DummyFreezeThaw.NA,
        dummy_chemical=DummyChemical.XA1,
    )
    design_working_life = 50.0
    concrete_material = ConcreteMaterial()
    plate_geometry = True
    quality_control = True
    return MockConcreteStructuralClassCalculator(
        exposure_classes=exposure_classes,
        design_working_life=design_working_life,
        concrete_material=concrete_material,
        plate_geometry=plate_geometry,
        quality_control=quality_control,
    )


class TestConcreteStructuralClassBase:
    """Test class for the ConcreteStructuralClassBase."""

    def test_concrete_structural_class_base_creation(self, structural_class: MockConcreteStructuralClass) -> None:
        """Test case to check the creation of ConcreteStructuralClassBase instance."""
        assert isinstance(structural_class, ConcreteStructuralClassBase)
        assert isinstance(structural_class, int)

    def test_concrete_structural_class_base_invalid_calculator(self) -> None:
        """Test case to check the creation of ConcreteStructuralClassBase instance with invalid calculator."""
        with pytest.raises(TypeError):
            ConcreteStructuralClassBase(MockConcreteStructuralClass, 1)  # type: ignore[arg-type]

    def test_concrete_structural_class_base_explanation(self, structural_class: MockConcreteStructuralClass) -> None:
        """Test case to check the explanation property of ConcreteStructuralClassBase."""
        assert hasattr(structural_class, "explanation")
        assert isinstance(structural_class.explanation, str)

    def test_concrete_structural_class_base_explanation_setter(self, structural_class: MockConcreteStructuralClass) -> None:
        """Test case to check the explanation setter of ConcreteStructuralClassBase."""
        with pytest.raises(AttributeError):
            structural_class.explanation = "Test explanation"

    def test_concrete_structural_class_base_string_representation(self, structural_class: MockConcreteStructuralClass) -> None:
        """Test case to check the string representation of ConcreteStructuralClassBase."""
        assert isinstance(str(structural_class), str)


class TestAbstractConcreteStructuralClassCalculator:
    """Test class for the AbstractConcreteStructuralClassCalculator."""

    @pytest.mark.parametrize(
        ("attribute", "calculated"),
        [
            ("exposure_classes", False),
            ("design_working_life", False),
            ("concrete_material", False),
            ("plate_geometry", False),
            ("quality_control", False),
            ("non_affecting_attribute", True),
        ],
    )
    def test_setattr_attribute_affecting_calculation(
        self, attribute: str, calculated: bool, calculator: MockConcreteStructuralClassCalculator
    ) -> None:
        """Test case to check if the right attributes affecting calculation trigger recalculation
        and those not affecting do not trigger recalculation.
        """
        calculator.calculate_structural_class()
        assert calculator._calculated  # noqa: SLF001

        setattr(calculator, attribute, 0)
        assert calculator._calculated == calculated  # noqa: SLF001

    def test_source_document(self, calculator: MockConcreteStructuralClassCalculator) -> None:
        """Test case to check the source document."""
        assert calculator.source_document == "Mock"

    def test_structural_class(self, calculator: MockConcreteStructuralClassCalculator) -> None:
        """Test case to check the structural class if calculate_structural_class() is not yet called."""
        with pytest.raises(ValueError):
            calculator.structural_class

    def test_explanation(self, calculator: MockConcreteStructuralClassCalculator) -> None:
        """Test case to check the explanation."""
        with pytest.raises(ValueError):
            calculator.explanation

    def test_update_structural_class(self, calculator: MockConcreteStructuralClassCalculator) -> None:
        """Test case to update the structural class and explanation."""
        calculator.update_structural_class(2, "Test explanation")
        assert calculator._structural_class == 3  # noqa: SLF001
        assert calculator._explanation == "Default structural class (S1) + 2 classes (Test explanation)"  # noqa: SLF001

    def test_update_structural_class_delta_not_int(self, calculator: MockConcreteStructuralClassCalculator) -> None:
        """Test case to check if update structural class raises error if delta is not an int."""
        with pytest.raises(TypeError):
            calculator.update_structural_class(2.2, "Test explanation")  # type: ignore[arg-type]

    def test_calculate_structural_class(self, calculator: MockConcreteStructuralClassCalculator) -> None:
        """Test case to calculate the structural class."""
        calculator.calculate_structural_class()
        assert calculator.structural_class == 2
        assert calculator.explanation == "Default structural class (S1) + 1 class (Quality control)"
