"""Test for the concrete structural class
according to Table 4.3 from NEN-EN 1992-1-1:2005+A1:2015+NB:2016+A1:2020: Chapter 4 - Durability and cover to reinforcement.
"""

import pytest

from blueprints.codes.eurocode.nen_en_1992_1_1_a1_2020.chapter_4_durability_and_cover.table_4_1 import (
    Carbonation,
    Chemical,
    Chloride,
    ChlorideSeawater,
    FreezeThaw,
    Table4Dot1ExposureClasses,
)
from blueprints.codes.eurocode.nen_en_1992_1_1_a1_2020.chapter_4_durability_and_cover.table_4_3 import (
    ConcreteMaterial,
    ConcreteStrengthClass,
    ConcreteStructuralClassBase,
    ConcreteStructuralClassCalculator,
    Table4Dot3ConcreteStructuralClass,
)
from blueprints.type_alias import YEARS

DUMMY_EXPOSURE_CLASSES_NA = Table4Dot1ExposureClasses()

DUMMY_EXPOSURE_CLASSES = Table4Dot1ExposureClasses(
    carbonation=Carbonation.XC2,
    chloride=Chloride.XD1,
    chloride_seawater=ChlorideSeawater.XS1,
    freeze_thaw=FreezeThaw.NA,
    chemical=Chemical.XA2,
)


class TestConcreteStructuralClassCalculator:
    """Unit tests for the ConcreteStructuralClassCalculator class."""

    @pytest.mark.parametrize(
        ("design_working_life", "expected_structural_class", "expected_explanation"),
        [
            (40, 4, " + 0 class (40 < 50 => 50 years)"),
            (50, 4, " + 0 class (50 years)"),
            (60, 5, " + 1 class (50 < 60 < 75 => 75 years)"),
            (75, 5, " + 1 class (75 years)"),
            (90, 6, " + 2 classes (90 > 75 => 100 years)"),
            (100, 6, " + 2 classes (100 years)"),
        ],
    )
    def test_structural_class_delta_design_working_life(
        self, design_working_life: YEARS, expected_structural_class: int, expected_explanation: str
    ) -> None:
        """Test the _structural_class_delta_design_working_life method of the ConcreteStructuralClassCalculator class."""
        # Using the default values for the other parameters so that they do not influence the test
        calculator = ConcreteStructuralClassCalculator(
            DUMMY_EXPOSURE_CLASSES_NA,
            design_working_life,
            ConcreteMaterial(ConcreteStrengthClass("C20/25")),
            False,
            False,
        )

        calculator.calculate_structural_class()

        assert calculator.structural_class == expected_structural_class
        assert expected_explanation in calculator.explanation

    @pytest.mark.parametrize(
        ("plate_geometry", "expected_structural_class", "expected_explanation"),
        [(True, 3, " - 1 class (plate geometry)"), (False, 4, " + 0 class (no plate geometry)")],
    )
    def test_structural_class_delta_plate_geometry(self, plate_geometry: bool, expected_structural_class: int, expected_explanation: str) -> None:
        """Test the _structural_class_delta_plate_geometry method of the ConcreteStructuralClassCalculator class."""
        # Using the default values for the other parameters so that they do not influence the test
        calculator = ConcreteStructuralClassCalculator(
            DUMMY_EXPOSURE_CLASSES_NA,
            50,
            ConcreteMaterial(ConcreteStrengthClass("C20/25")),
            plate_geometry,
            False,
        )

        calculator.calculate_structural_class()

        assert calculator.structural_class == expected_structural_class
        assert expected_explanation in calculator.explanation

    @pytest.mark.parametrize(
        ("quality_control", "expected_structural_class", "expected_explanation"),
        [(True, 3, " - 1 class (quality control)"), (False, 4, " + 0 class (no quality control)")],
    )
    def test_structural_class_delta_quality_control(self, quality_control: bool, expected_structural_class: int, expected_explanation: str) -> None:
        """Test the _structural_class_delta_quality_control method of the ConcreteStructuralClassCalculator class."""
        # Using the default values for the other parameters so that they do not influence the test
        calculator = ConcreteStructuralClassCalculator(
            DUMMY_EXPOSURE_CLASSES_NA,
            50,
            ConcreteMaterial(ConcreteStrengthClass("C20/25")),
            False,
            quality_control,
        )

        calculator.calculate_structural_class()

        assert calculator.structural_class == expected_structural_class
        assert expected_explanation in calculator.explanation

    @pytest.mark.parametrize(
        ("concrete_grade", "exposure_classes", "expected_structural_class", "expected_explanation"),
        [
            (
                ConcreteMaterial(ConcreteStrengthClass("C20/25")),
                Table4Dot1ExposureClasses(Carbonation.NA, Chloride.NA, ChlorideSeawater.NA, FreezeThaw.NA, Chemical.NA),
                4,
                " + 0 class (no reduction with respect to concrete grade)",
            ),
            (
                ConcreteMaterial(ConcreteStrengthClass("C30/37")),
                Table4Dot1ExposureClasses(Carbonation.XC1, Chloride.NA, ChlorideSeawater.NA, FreezeThaw.NA, Chemical.NA),
                3,
                " - 1 class (concrete grade >= C30/37)",
            ),
            (
                ConcreteMaterial(ConcreteStrengthClass("C35/45")),
                Table4Dot1ExposureClasses(Carbonation.XC2, Chloride.NA, ChlorideSeawater.NA, FreezeThaw.NA, Chemical.NA),
                3,
                " - 1 class (concrete grade >= C35/45)",
            ),
            (
                ConcreteMaterial(ConcreteStrengthClass("C40/50")),
                Table4Dot1ExposureClasses(Carbonation.NA, Chloride.NA, ChlorideSeawater.XS1, FreezeThaw.NA, Chemical.NA),
                3,
                " - 1 class (concrete grade >= C40/50)",
            ),
            (
                ConcreteMaterial(ConcreteStrengthClass("C45/55")),
                Table4Dot1ExposureClasses(Carbonation.NA, Chloride.XD3, ChlorideSeawater.NA, FreezeThaw.NA, Chemical.NA),
                3,
                " - 1 class (concrete grade >= C45/55)",
            ),
        ],
    )
    def test_structural_class_delta_concrete_grade(
        self, concrete_grade: ConcreteMaterial, exposure_classes: Table4Dot1ExposureClasses, expected_structural_class: int, expected_explanation: str
    ) -> None:
        """Test the _structural_class_delta_concrete_grade method of the ConcreteStructuralClassCalculator class."""
        # Using the default values for the other parameters so that they do not influence the test
        calculator = ConcreteStructuralClassCalculator(
            exposure_classes=exposure_classes,
            concrete_material=concrete_grade,
            design_working_life=50,
            plate_geometry=False,
            quality_control=False,
        )

        calculator.calculate_structural_class()

        assert calculator.structural_class == expected_structural_class
        assert expected_explanation in calculator.explanation


class TestTable4Dot3ConcreteStructuralClass:
    """Unit tests for the Table4Dot3ConcreteStructuralClass class."""

    def test_new_instance(self) -> None:
        """Test if a new instance can be instantiated."""
        new_instance = Table4Dot3ConcreteStructuralClass(
            exposure_classes=DUMMY_EXPOSURE_CLASSES,
            design_working_life=50,
            concrete_material=ConcreteMaterial(ConcreteStrengthClass("C20/25")),
            plate_geometry=False,
            quality_control=False,
        )

        assert isinstance(new_instance, Table4Dot3ConcreteStructuralClass)
        assert isinstance(new_instance, ConcreteStructuralClassBase)
        assert isinstance(new_instance, int)

    def test_new_instance_list_of_exposure_classes(self) -> None:
        """Test if a new instance can be instantiated with a list of exposure classes."""
        new_instance = Table4Dot3ConcreteStructuralClass(
            exposure_classes=["XC2", "XD1", "XS1", "XA2"],
            design_working_life=50,
            concrete_material=ConcreteMaterial(ConcreteStrengthClass("C20/25")),
            plate_geometry=False,
            quality_control=False,
        )

        assert isinstance(new_instance, Table4Dot3ConcreteStructuralClass)
        assert isinstance(new_instance, ConcreteStructuralClassBase)
        assert isinstance(new_instance, int)

    def test_new_instance_attributes(self) -> None:
        """Test if the new instance has the 'explanation' attribute."""
        new_instance = Table4Dot3ConcreteStructuralClass(
            exposure_classes=DUMMY_EXPOSURE_CLASSES,
            design_working_life=50,
            concrete_material=ConcreteMaterial(ConcreteStrengthClass("C20/25")),
            plate_geometry=False,
            quality_control=False,
        )

        assert hasattr(new_instance, "explanation")
