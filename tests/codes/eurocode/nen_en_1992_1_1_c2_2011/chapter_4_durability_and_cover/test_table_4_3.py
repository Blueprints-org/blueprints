"""Test for the concrete structural class
according to Table 4.3 from NEN-EN 1992-1-1+C2:2011: Chapter 4 - Durability and cover to reinforcement.
"""

import pytest

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011.chapter_4_durability_and_cover.table_4_1 import (
    Carbonation,
    Chemical,
    Chloride,
    ChlorideSeawater,
    ExposureClasses,
    FreezeThaw,
)
from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011.chapter_4_durability_and_cover.table_4_3 import (
    ConcreteMaterial,
    ConcreteStrengthClass,
    ConcreteStructuralClass,
    ConcreteStructuralClassBase,
    ConcreteStructuralClassCalculator,
)
from blueprints.type_alias import YEARS

DUMMY_EXPOSURE_CLASSES = ExposureClasses(
    carbonation=Carbonation.XC2,
    chloride=Chloride.XD1,
    chloride_seawater=ChlorideSeawater.XS1,
    freeze=FreezeThaw.NA,
    chemical=Chemical.XA2,
)


class TestConcreteStructuralClassCalculator:
    """Unit tests for the ConcreteStructuralClassCalculator class."""

    @pytest.mark.parametrize(
        ("design_working_life", "expected_structural_class", "expected_explanation"),
        [(50, 4, "(50 years)"), (75, 5, "(75 years)"), (100, 6, "(100 years)")],
    )
    def test_structural_class_delta_design_working_life(
        self, design_working_life: YEARS, expected_structural_class: int, expected_explanation: str
    ) -> None:
        """Test the _structural_class_delta_design_working_life method of the ConcreteStructuralClassCalculator class."""
        calculator = ConcreteStructuralClassCalculator(
            DUMMY_EXPOSURE_CLASSES,
            design_working_life,
            ConcreteMaterial(ConcreteStrengthClass("C20/25")),
            False,
            False,
        )

        calculator._structural_class_delta_design_working_life()  # noqa: SLF001
        calculator._calculated = True  # noqa: SLF001

        assert calculator.structural_class == expected_structural_class
        assert calculator.explanation.endswith(expected_explanation)

    @pytest.mark.parametrize(
        ("plate_geometry", "expected_structural_class", "expected_explanation"),
        [(True, 3, "(plate geometry)"), (False, 4, "(no plate geometry)")],
    )
    def test_structural_class_delta_plate_geometry(self, plate_geometry: bool, expected_structural_class: int, expected_explanation: str) -> None:
        """Test the _structural_class_delta_plate_geometry method of the ConcreteStructuralClassCalculator class."""
        calculator = ConcreteStructuralClassCalculator(
            DUMMY_EXPOSURE_CLASSES,
            50,
            ConcreteMaterial(ConcreteStrengthClass("C20/25")),
            plate_geometry,
            False,
        )

        calculator._structural_class_delta_plate_geometry()  # noqa: SLF001
        calculator._calculated = True  # noqa: SLF001

        assert calculator.structural_class == expected_structural_class
        assert calculator.explanation.endswith(expected_explanation)

    @pytest.mark.parametrize(
        ("quality_control", "expected_structural_class", "expected_explanation"),
        [(True, 3, "(quality control)"), (False, 4, "(no quality control)")],
    )
    def test_structural_class_delta_quality_control(self, quality_control: bool, expected_structural_class: int, expected_explanation: str) -> None:
        """Test the _structural_class_delta_quality_control method of the ConcreteStructuralClassCalculator class."""
        calculator = ConcreteStructuralClassCalculator(
            DUMMY_EXPOSURE_CLASSES,
            50,
            ConcreteMaterial(ConcreteStrengthClass("C20/25")),
            False,
            quality_control,
        )

        calculator._structural_class_delta_quality_control()  # noqa: SLF001
        calculator._calculated = True  # noqa: SLF001

        assert calculator.structural_class == expected_structural_class
        assert calculator.explanation.endswith(expected_explanation)

    @pytest.mark.parametrize(
        ("concrete_grade", "exposure_classes", "expected_structural_class", "expected_explanation"),
        [
            (
                ConcreteMaterial(ConcreteStrengthClass("C20/25")),
                ExposureClasses(Carbonation.NA, Chloride.NA, ChlorideSeawater.NA, FreezeThaw.NA, Chemical.NA),
                4,
                "(no reduction with respect to concrete grade)",
            ),
            (
                ConcreteMaterial(ConcreteStrengthClass("C30/37")),
                ExposureClasses(Carbonation.XC1, Chloride.NA, ChlorideSeawater.NA, FreezeThaw.NA, Chemical.NA),
                3,
                "(concrete grade >= C30/37)",
            ),
            (
                ConcreteMaterial(ConcreteStrengthClass("C35/45")),
                ExposureClasses(Carbonation.XC2, Chloride.NA, ChlorideSeawater.NA, FreezeThaw.NA, Chemical.NA),
                3,
                "(concrete grade >= C35/45)",
            ),
            (
                ConcreteMaterial(ConcreteStrengthClass("C40/50")),
                ExposureClasses(Carbonation.NA, Chloride.NA, ChlorideSeawater.XS1, FreezeThaw.NA, Chemical.NA),
                3,
                "(concrete grade >= C40/50)",
            ),
            (
                ConcreteMaterial(ConcreteStrengthClass("C45/55")),
                ExposureClasses(Carbonation.NA, Chloride.XD3, ChlorideSeawater.NA, FreezeThaw.NA, Chemical.NA),
                3,
                "(concrete grade >= C45/55)",
            ),
        ],
    )
    def test_structural_class_delta_concrete_grade(
        self, concrete_grade: ConcreteMaterial, exposure_classes: ExposureClasses, expected_structural_class: int, expected_explanation: str
    ) -> None:
        """Test the _structural_class_delta_concrete_grade method of the ConcreteStructuralClassCalculator class."""
        calculator = ConcreteStructuralClassCalculator(
            exposure_classes=exposure_classes,
            concrete_material=concrete_grade,
            design_working_life=50,
            plate_geometry=False,
            quality_control=False,
        )

        calculator._structural_class_delta_concrete_grade()  # noqa: SLF001
        calculator._calculated = True  # noqa: SLF001

        assert calculator.structural_class == expected_structural_class
        assert calculator.explanation.endswith(expected_explanation)


class TestConcreteStructuralClass:
    """Unit tests for the ConcreteStructuralClass class."""

    def test_new_instance(self) -> None:
        """Test if a new instance can be instantiated."""
        new_instance = ConcreteStructuralClass(
            exposure_classes=DUMMY_EXPOSURE_CLASSES,
            design_working_life=50,
            concrete_material=ConcreteMaterial(ConcreteStrengthClass("C20/25")),
            plate_geometry=False,
            quality_control=False,
        )

        assert isinstance(new_instance, ConcreteStructuralClass)
        assert isinstance(new_instance, ConcreteStructuralClassBase)
        assert isinstance(new_instance, int)

    def test_new_instance_attributes(self) -> None:
        """Test if the new instance has the 'explanation' attribute."""
        new_instance = ConcreteStructuralClass(
            exposure_classes=DUMMY_EXPOSURE_CLASSES,
            design_working_life=50,
            concrete_material=ConcreteMaterial(ConcreteStrengthClass("C20/25")),
            plate_geometry=False,
            quality_control=False,
        )

        assert hasattr(new_instance, "explanation")
