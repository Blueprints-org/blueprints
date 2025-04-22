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

    def test_perimeter(self, triangular_cross_section: RightAngledTriangularCrossSection) -> None:
        """Test the perimeter property of the RightAngledTriangularCrossSection class."""
        expected_perimeter = 100.0 + 200.0 + (100.0**2 + 200.0**2) ** 0.5
        assert triangular_cross_section.perimeter == pytest.approx(expected=expected_perimeter, rel=1e-6)

    def test_centroid(self, triangular_cross_section: RightAngledTriangularCrossSection) -> None:
        """Test the centroid property of the RightAngledTriangularCrossSection class."""
        centroid = triangular_cross_section.centroid
        assert (centroid.x, centroid.y) == pytest.approx(expected=(100.0 / 3 + 100, 200.0 / 3 + 250), rel=1e-6)

    def test_moments_of_inertia(self, triangular_cross_section: RightAngledTriangularCrossSection) -> None:
        """Test the moments of inertia properties of the RightAngledTriangularCrossSection class."""
        expected_y = (100.0 * 200.0**3) / 36
        expected_z = (200.0 * 100.0**3) / 36
        assert triangular_cross_section.moment_of_inertia_about_y == pytest.approx(expected=expected_y, rel=1e-6)
        assert triangular_cross_section.moment_of_inertia_about_z == pytest.approx(expected=expected_z, rel=1e-6)

    def test_section_moduli(self, triangular_cross_section: RightAngledTriangularCrossSection) -> None:
        """Test the section moduli properties of the RightAngledTriangularCrossSection class."""
        expected_y_positive = (100.0 * 200.0**3) / (36 * (200.0 / 3 * 2))
        expected_z_positive = (200.0 * 100.0**3) / (36 * (100.0 / 3 * 2))
        expected_y_negative = (100.0 * 200.0**3) / (36 * (200.0 / 3))
        expected_z_negative = (200.0 * 100.0**3) / (36 * (100.0 / 3))
        assert triangular_cross_section.elastic_section_modulus_about_y_positive == pytest.approx(expected=expected_y_positive, rel=1e-6)
        assert triangular_cross_section.elastic_section_modulus_about_z_positive == pytest.approx(expected=expected_z_positive, rel=1e-6)
        assert triangular_cross_section.elastic_section_modulus_about_y_negative == pytest.approx(expected=expected_y_negative, rel=1e-6)
        assert triangular_cross_section.elastic_section_modulus_about_z_negative == pytest.approx(expected=expected_z_negative, rel=1e-6)

    def test_plastic_section_moduli(self, triangular_cross_section: RightAngledTriangularCrossSection) -> None:
        """Test the plastic section moduli properties of the RightAngledTriangularCrossSection class."""
        assert triangular_cross_section.plastic_section_modulus_about_y == pytest.approx(expected=390529.656, rel=1e-6)
        assert triangular_cross_section.plastic_section_modulus_about_z == pytest.approx(expected=195264.828, rel=1e-6)

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

    def test_section_properties(self, triangular_cross_section: RightAngledTriangularCrossSection) -> None:
        """Test the section properties of the RightAngledTriangularCrossSection class."""
        section_properties = triangular_cross_section.section_properties()
        assert section_properties.area == pytest.approx(expected=triangular_cross_section.area, rel=1e-2)
        assert section_properties.perimeter == pytest.approx(expected=triangular_cross_section.perimeter, rel=1e-2)
        assert section_properties.cx == pytest.approx(expected=triangular_cross_section.centroid.x, rel=1e-2)
        assert section_properties.cy == pytest.approx(expected=triangular_cross_section.centroid.y, rel=1e-2)
        assert section_properties.ixx_c == pytest.approx(expected=triangular_cross_section.moment_of_inertia_about_y, rel=1e-2)
        assert section_properties.iyy_c == pytest.approx(expected=triangular_cross_section.moment_of_inertia_about_z, rel=1e-2)
        assert section_properties.zxx_plus == pytest.approx(expected=triangular_cross_section.elastic_section_modulus_about_y_positive, rel=1e-2)
        assert section_properties.zyy_plus == pytest.approx(expected=triangular_cross_section.elastic_section_modulus_about_z_positive, rel=1e-2)
        assert section_properties.zxx_minus == pytest.approx(expected=triangular_cross_section.elastic_section_modulus_about_y_negative, rel=1e-2)
        assert section_properties.zyy_minus == pytest.approx(expected=triangular_cross_section.elastic_section_modulus_about_z_negative, rel=1e-2)
        assert section_properties.sxx == pytest.approx(expected=triangular_cross_section.plastic_section_modulus_about_y, rel=1e-2)
        assert section_properties.syy == pytest.approx(expected=triangular_cross_section.plastic_section_modulus_about_z, rel=1e-2)
