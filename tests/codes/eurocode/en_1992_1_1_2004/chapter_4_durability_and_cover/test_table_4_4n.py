"""Testing formula 4.4N of EN 1992-1-1:2004."""

import pytest

from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_4_durability_and_cover.table_4_1 import (
    Carbonation,
    Chemical,
    Chloride,
    ChlorideSeawater,
    FreezeThaw,
    Table4Dot1ExposureClasses,
)
from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_4_durability_and_cover.table_4_3 import (
    ConcreteMaterial,
    ConcreteStrengthClass,
    Table4Dot3ConcreteStructuralClass,
)
from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_4_durability_and_cover.table_4_4n import (
    Table4Dot4nMinimumCoverDurabilityReinforcementSteel,
)
from blueprints.type_alias import MM


class TestTable4Dot4nMinimumCoverDurabilityReinforcementSteel:
    """Validation for table 4.4 from EN 1992-1-1:2004."""

    @pytest.mark.parametrize(
        ("exposure_classes", "structural_class", "expected_result"),
        [
            (
                Table4Dot1ExposureClasses(Carbonation.XC2, Chloride.XD1, ChlorideSeawater.XS3, FreezeThaw.XF4, Chemical.XA1),
                6,
                50,
            ),
            (
                Table4Dot1ExposureClasses(Carbonation.XC2, Chloride.XD3, ChlorideSeawater.XS2, FreezeThaw.XF4, Chemical.XA1),
                5,
                45,
            ),
            (
                Table4Dot1ExposureClasses(Carbonation.XC2, Chloride.XD1, ChlorideSeawater.XS2, FreezeThaw.XF4, Chemical.XA1),
                5,
                45,
            ),
            (
                Table4Dot1ExposureClasses(Carbonation.NA, Chloride.NA, ChlorideSeawater.NA, FreezeThaw.NA, Chemical.NA),
                4,
                10,
            ),
            (
                Table4Dot1ExposureClasses(Carbonation.XC2, Chloride.NA, ChlorideSeawater.NA, FreezeThaw.XF4, Chemical.XA1),
                3,
                20,
            ),
            (
                Table4Dot1ExposureClasses(Carbonation.XC2, Chloride.XD1, ChlorideSeawater.NA, FreezeThaw.XF4, Chemical.XA1),
                2,
                25,
            ),
            (
                Table4Dot1ExposureClasses(Carbonation.XC4, Chloride.NA, ChlorideSeawater.NA, FreezeThaw.XF4, Chemical.XA1),
                1,
                15,
            ),
            (
                Table4Dot1ExposureClasses(Carbonation.XC1, Chloride.NA, ChlorideSeawater.NA, FreezeThaw.XF2, Chemical.XA1),
                5,
                20,
            ),
        ],
    )
    def test_evaluation(
        self, exposure_classes: Table4Dot1ExposureClasses, structural_class: Table4Dot3ConcreteStructuralClass, expected_result: MM
    ) -> None:
        """Test the evaluation of the result."""
        table_4_4 = Table4Dot4nMinimumCoverDurabilityReinforcementSteel(
            exposure_classes=exposure_classes,
            structural_class=structural_class,
        )

        assert table_4_4 == pytest.approx(expected=expected_result, rel=1e-4)

    def test_evaluation_valid_structural_class_type(self) -> None:
        """Test if the evaluation raises TypeError when the structural class is not an integer."""
        exposure_classes = Table4Dot1ExposureClasses(Carbonation.XC2, Chloride.XD1, ChlorideSeawater.XS3, FreezeThaw.XF4, Chemical.XA1)
        structural_class = Table4Dot3ConcreteStructuralClass(exposure_classes, 50, ConcreteMaterial(ConcreteStrengthClass("C20/25")), True, False)

        assert Table4Dot4nMinimumCoverDurabilityReinforcementSteel(exposure_classes, structural_class) == 35

    def test_evaluation_invalid_structural_class_type(self) -> None:
        """Test if the evaluation raises TypeError when the structural class is not an integer."""
        exposure_classes = Table4Dot1ExposureClasses(Carbonation.XC2, Chloride.XD1, ChlorideSeawater.XS3, FreezeThaw.XF4, Chemical.XA1)
        structural_class = "S4"

        with pytest.raises(TypeError):
            Table4Dot4nMinimumCoverDurabilityReinforcementSteel(exposure_classes, structural_class)  # type: ignore[arg-type]

    def test_evaluation_invalid_structural_class_value(self) -> None:
        """Test if the evaluation raises ValueError when the structural class is not between 1 and 6."""
        exposure_classes = Table4Dot1ExposureClasses(Carbonation.XC2, Chloride.XD1, ChlorideSeawater.XS3, FreezeThaw.XF4, Chemical.XA1)
        structural_class = 7

        with pytest.raises(ValueError):
            Table4Dot4nMinimumCoverDurabilityReinforcementSteel(exposure_classes, structural_class)  # type: ignore[arg-type]

    @pytest.mark.parametrize(
        ("representation", "expected_result"),
        [
            ("complete", r"c_{min,dur} = \text{structural class S3 and exposure classes (XC2, XF4, XA1)} = 20"),
            ("short", "c_{min,dur} = 20"),
        ],
    )
    def test_latex(self, representation: str, expected_result: str) -> None:
        """Test the latex implementation."""
        # Test data
        exposure_classes = Table4Dot1ExposureClasses(Carbonation.XC2, Chloride.NA, ChlorideSeawater.NA, FreezeThaw.XF4, Chemical.XA1)
        structural_class = Table4Dot3ConcreteStructuralClass(exposure_classes, 50, ConcreteMaterial(ConcreteStrengthClass("C20/25")), True, False)

        c_min_dur = Table4Dot4nMinimumCoverDurabilityReinforcementSteel(
            exposure_classes=exposure_classes,
            structural_class=structural_class,
        ).latex()

        actual = {
            "complete": c_min_dur.complete,
            "short": c_min_dur.short,
            "string": str(c_min_dur),
        }

        assert actual[representation] == expected_result, f"{representation} representation failed."
