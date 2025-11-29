"""Test the SteelCrossSection class."""

import pytest
from shapely.geometry import Point

from blueprints.structural_sections.steel.steel_cross_section import SteelCrossSection


class TestSteelCrossSection:
    """Test suite for the SteelCrossSection class."""

    def test_name(self, steel_cross_section: SteelCrossSection) -> None:
        """Test that the SteelCrossSection name works correctly."""
        assert steel_cross_section.cross_section.name == "IPE100"

    def test_area(self, steel_cross_section: SteelCrossSection) -> None:
        """Test that the SteelCrossSection area works correctly."""
        assert steel_cross_section.cross_section.area == pytest.approx(1032.6, 1e-3)

    def test_perimeter(self, steel_cross_section: SteelCrossSection) -> None:
        """Test that the SteelCrossSection perimeter works correctly."""
        assert steel_cross_section.cross_section.perimeter == pytest.approx(399.762, 1e-3)

    def test_centroid(self, steel_cross_section: SteelCrossSection) -> None:
        """Test that the SteelCrossSection centroid works correctly."""
        assert steel_cross_section.cross_section.centroid.equals_exact(Point(0.0, 0.0), 1e-3)

    def test_weight_per_meter(self, steel_cross_section: SteelCrossSection) -> None:
        """Test that the SteelCrossSection weight per meter is calculated correctly."""
        expected_weight: float = steel_cross_section.cross_section.area * steel_cross_section.material.density * 1e-6
        assert steel_cross_section.weight_per_meter == pytest.approx(expected_weight, 1e-3)

    def test_optional_parameters_default(
        self,
        steel_cross_section: SteelCrossSection,
    ) -> None:
        """Test that the optional parameters have correct default values."""
        assert steel_cross_section.horizontal_offset == 0.0
        assert steel_cross_section.vertical_offset == 0.0
        assert steel_cross_section.rotation_angle == 0.0

    @pytest.mark.parametrize(
        "kwargs",
        [
            {"horizontal_offset": 10.0},
            {"vertical_offset": 20.0},
            {"rotation_angle": 30.0},
            {"horizontal_offset": 10.0, "vertical_offset": 20.0},
            {"horizontal_offset": 10.0, "rotation_angle": 30.0},
            {"vertical_offset": 20.0, "rotation_angle": 30.0},
            {"horizontal_offset": 10.0, "vertical_offset": 20.0, "rotation_angle": 30.0},
        ],
    )
    def test_initialize_with_optional_parameters(
        self,
        steel_cross_section: SteelCrossSection,
        kwargs: dict,
    ) -> None:
        """Test that the SteelCrossSection can be initialized with optional parameters."""
        section = SteelCrossSection(
            cross_section=steel_cross_section.cross_section,
            material=steel_cross_section.material,
            **kwargs,
        )
        for key, value in kwargs.items():
            assert getattr(section, key) == value

    def test_transform(
        self,
        steel_cross_section: SteelCrossSection,
    ) -> None:
        """Test that the transform method works correctly."""
        original_cross_section = SteelCrossSection(
            cross_section=steel_cross_section.cross_section,
            material=steel_cross_section.material,
            horizontal_offset=10.0,
            vertical_offset=20.0,
            rotation_angle=30.0,
        )
        horizontal_offset = 15.0
        vertical_offset = 25.0
        rotation_angle = 45.0
        transformed_section = original_cross_section.transform(
            horizontal_offset=horizontal_offset,
            vertical_offset=vertical_offset,
            rotation_angle=rotation_angle,
        )
        assert transformed_section.horizontal_offset == 25.0
        assert transformed_section.vertical_offset == 45.0
        assert transformed_section.rotation_angle == 75.0
