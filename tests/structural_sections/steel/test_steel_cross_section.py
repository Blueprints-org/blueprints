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
        assert steel_cross_section.x_offset == 0.0
        assert steel_cross_section.y_offset == 0.0
        assert steel_cross_section.rotation_angle == 0.0

    @pytest.mark.parametrize(
        "kwargs",
        [
            {"x_offset": 10.0},
            {"y_offset": 20.0},
            {"rotation_angle": 30.0},
            {"x_offset": 10.0, "y_offset": 20.0},
            {"x_offset": 10.0, "rotation_angle": 30.0},
            {"y_offset": 20.0, "rotation_angle": 30.0},
            {"x_offset": 10.0, "y_offset": 20.0, "rotation_angle": 30.0},
        ],
    )
    def test_optional_parameters_non_initializable(
        self,
        steel_cross_section: SteelCrossSection,
        kwargs: dict,
    ) -> None:
        """Test that the optional parameters can be set correctly."""
        with pytest.raises(TypeError):
            SteelCrossSection(
                cross_section=steel_cross_section.cross_section,
                material=steel_cross_section.material,
                **kwargs,
            )

    def test_transform(
        self,
        steel_cross_section: SteelCrossSection,
    ) -> None:
        """Test that the _transform method works correctly."""
        x_offset = 15.0
        y_offset = 25.0
        rotation_angle = 45.0
        transformed_section = steel_cross_section._transform(  # noqa: SLF001
            x_offset=x_offset,
            y_offset=y_offset,
            rotation_angle=rotation_angle,
        )
        assert transformed_section.x_offset == x_offset
        assert transformed_section.y_offset == y_offset
        assert transformed_section.rotation_angle == rotation_angle
