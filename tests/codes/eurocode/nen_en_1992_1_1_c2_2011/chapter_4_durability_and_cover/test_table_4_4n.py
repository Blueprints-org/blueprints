"""Testing formula 4.4N of NEN-EN 1992-1-1+C2:2011."""

import pytest

from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011.chapter_4_durability_and_cover.table_4_1 import (
    Carbonation,
    Chemical,
    Chloride,
    ChlorideSeawater,
    FreezeThaw,
    Table4Dot1ExposureClasses,
)
from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011.chapter_4_durability_and_cover.table_4_3 import (
    ConcreteMaterial,
    ConcreteStrengthClass,
    Table4Dot3ConcreteStructuralClass,
)
from blueprints.codes.eurocode.nen_en_1992_1_1_c2_2011.chapter_4_durability_and_cover.table_4_4n import (
    Table4Dot4nMinimumCoverDurabilityReinforcementSteel,
)
from blueprints.type_alias import MM


class TestTable4Dot4nMinimumCoverDurabilityReinforcementSteel:
    """Validation for table 4.4 from NEN-EN 1992-1-1+C2:2011."""

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

    @pytest.mark.parametrize(
        ("representation", "expected_result"),
        [
            ("complete", r"c_{min,dur} = structural class S3 & exposure classes (XC2, XF4, XA1) = 20"),
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
