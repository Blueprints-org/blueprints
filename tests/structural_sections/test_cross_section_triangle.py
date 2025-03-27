"""Tests for cross-section shapes."""

import pytest

from blueprints.structural_sections.cross_section_triangle import RightAngledTriangularCrossSection


class TestRightAngledTriangularCrossSection:
    """Tests for the RightAngledTriangularCrossSection class."""

    @pytest.fixture
    def triangular_cross_section(self) -> RightAngledTriangularCrossSection:
        """Return a RightAngledTriangularCrossSection instance."""
        return RightAngledTriangularCrossSection(name="Triangle", base=100.0, height=200.0)

    def test_area(self, triangular_cross_section: RightAngledTriangularCrossSection) -> None:
        """Test the area property of the RightAngledTriangularCrossSection class."""
        assert triangular_cross_section.area == pytest.approx(expected=10000.0, rel=1e-6)

    def test_perimeter(self, triangular_cross_section: RightAngledTriangularCrossSection) -> None:
        """Test the perimeter property of the RightAngledTriangularCrossSection class."""
        expected_perimeter = 100.0 + 200.0 + (100.0**2 + 200.0**2) ** 0.5
        assert triangular_cross_section.perimeter == pytest.approx(expected=expected_perimeter, rel=1e-6)

    def test_centroid(self, triangular_cross_section: RightAngledTriangularCrossSection) -> None:
        """Test the centroid property of the RightAngledTriangularCrossSection class."""
        centroid = triangular_cross_section.centroid
        assert (centroid.x, centroid.y) == pytest.approx(expected=(100.0 / 3, 200.0 / 3), rel=1e-6)

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
        assert triangular_cross_section.elastic_section_modulus_about_y_positive == pytest.approx(expected=expected_y_positive, rel=1e-6)
        assert triangular_cross_section.elastic_section_modulus_about_z_positive == pytest.approx(expected=expected_z_positive, rel=1e-6)

    def test_polar_moment_of_inertia(self, triangular_cross_section: RightAngledTriangularCrossSection) -> None:
        """Test the polar moment of inertia property of the RightAngledTriangularCrossSection class."""
        expected_polar = (100.0 * 200.0**3) / 36 + (200.0 * 100.0**3) / 36
        assert triangular_cross_section.polar_moment_of_inertia == pytest.approx(expected=expected_polar, rel=1e-6)

    def test_plastic_section_moduli(self, triangular_cross_section: RightAngledTriangularCrossSection) -> None:
        """Test the plastic section moduli properties of the RightAngledTriangularCrossSection class."""
        expected_y = (100.0 * 200.0**2) / 4
        expected_z = (200.0 * 100.0**2) / 4
        assert triangular_cross_section.plastic_section_modulus_about_y == pytest.approx(expected=expected_y, rel=1e-6)
        assert triangular_cross_section.plastic_section_modulus_about_z == pytest.approx(expected=expected_z, rel=1e-6)
