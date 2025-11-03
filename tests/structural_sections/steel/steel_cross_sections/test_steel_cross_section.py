"""Test suite for CombinedSteelCrossSection."""

import matplotlib as mpl

mpl.use("Agg")

import pytest

from blueprints.codes.eurocode.en_1993_1_1_2005.chapter_3_materials.table_3_1 import SteelStrengthClass
from blueprints.materials.steel import SteelMaterial
from blueprints.structural_sections.cross_section_rectangle import RectangularCrossSection
from blueprints.structural_sections.steel.steel_cross_sections._steel_cross_section import CombinedSteelCrossSection
from blueprints.structural_sections.steel.steel_element import SteelElement


class TestCombinedSteelCrossSection:
    """Test suite for CombinedSteelCrossSection."""

    def test_empty_combined_steel_cross_section(self, empty_combined_steel_cross_section: CombinedSteelCrossSection) -> None:
        """Test the code of the combined steel cross-section."""
        with pytest.raises(ValueError):
            _ = empty_combined_steel_cross_section.polygon

    def test_invalid_combined_elements(self, empty_combined_steel_cross_section: CombinedSteelCrossSection) -> None:
        """Test the code of the combined steel cross-section."""
        steel_material = SteelMaterial(steel_class=SteelStrengthClass.S355)
        empty_combined_steel_cross_section.elements = [
            SteelElement(
                cross_section=RectangularCrossSection(width=500, height=500, x=0, y=0),
                material=steel_material,
                nominal_thickness=500,
            ),
            SteelElement(
                cross_section=RectangularCrossSection(width=250, height=250, x=1000, y=0),
                material=steel_material,
                nominal_thickness=250,
            ),
        ]

        with pytest.raises(TypeError):
            _ = empty_combined_steel_cross_section.polygon
