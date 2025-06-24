"""Tests for cross-section shapes."""

import pytest
from shapely.geometry import Polygon

from blueprints.structural_sections.cross_section_triangle import RightAngledTriangularCrossSection


class TestRightAngledTriangularCrossSection:
    """Tests for the RightAngledTriangularCrossSection class."""

    def test_area(self, triangular_cross_section: RightAngledTriangularCrossSection) -> None:
        """Test the area property of the RightAngledTriangularCrossSection class."""
        assert triangular_cross_section.area == pytest.approx(expected=10000.0, rel=1e-6)

    def test_polygon(self, triangular_cross_section: RightAngledTriangularCrossSection) -> None:
        """Test the polygon property of the RightAngledTriangularCrossSection class."""
        assert isinstance(triangular_cross_section.polygon, Polygon)

    def test_geometry(self, triangular_cross_section: RightAngledTriangularCrossSection) -> None:
        """Test the geometry property of the RightAngledTriangularCrossSection class."""
        geometry = triangular_cross_section.geometry()
        assert geometry is not None

    def test_invalid_base(self) -> None:
        """Test initialization with an invalid base value."""
        with pytest.raises(ValueError, match="Base must be a positive value"):
            RightAngledTriangularCrossSection(name="InvalidBase", base=-10.0, height=200.0)

    def test_invalid_height(self) -> None:
        """Test initialization with an invalid height value."""
        with pytest.raises(ValueError, match="Height must be a positive value"):
            RightAngledTriangularCrossSection(name="InvalidHeight", base=100.0, height=-20.0)

    def test_mirrored_polygon(self) -> None:
        """Test the geometry property when the triangle is mirrored."""
        mirrored_triangle = RightAngledTriangularCrossSection(
            name="MirroredTriangle", base=100.0, height=200.0, mirrored_horizontally=True, mirrored_vertically=True
        )
        polygon = mirrored_triangle.polygon
        assert polygon.is_valid
        assert len(polygon.exterior.coords) == 4
        assert (polygon.exterior.coords[1][0], polygon.exterior.coords[1][1]) == (-100.0, 0)
        assert (polygon.exterior.coords[2][0], polygon.exterior.coords[2][1]) == (0, -200.0)
