"""Tests for cross-section shapes."""

import pytest

from blueprints.structural_sections.cross_section_rectangle import RectangularCrossSection


class TestRectangularCrossSection:
    """Tests for the RectangularCrossSection class."""

    @pytest.fixture
    def rectangular_cross_section(self) -> RectangularCrossSection:
        """Return a RectangularCrossSection instance."""
        return RectangularCrossSection(width=100.0, height=200.0)

    def test_area(self, rectangular_cross_section: RectangularCrossSection) -> None:
        """Test the area property of the RectangularCrossSection class."""
        assert rectangular_cross_section.area == pytest.approx(expected=20000.0, rel=1e-6)

    def test_perimeter(self, rectangular_cross_section: RectangularCrossSection) -> None:
        """Test the perimeter property of the RectangularCrossSection class."""
        assert rectangular_cross_section.perimeter == pytest.approx(expected=600.0, rel=1e-6)

    def test_centroid(self, rectangular_cross_section: RectangularCrossSection) -> None:
        """Test the centroid property of the RectangularCrossSection class."""
        centroid = rectangular_cross_section.centroid
        assert (centroid.x, centroid.y) == pytest.approx(expected=(0.0, 0.0), rel=1e-6)

    def test_vertices(self, rectangular_cross_section: RectangularCrossSection) -> None:
        """Test the vertices property of the RectangularCrossSection class."""
        vertices = rectangular_cross_section.vertices
        first_vertex = vertices[0]
        last_vertex = vertices[-1]
        assert len(vertices) == 5
        assert (first_vertex.x, first_vertex.y) == pytest.approx(expected=(-50.0, -100.00), rel=1e-6)
        assert (last_vertex.x, last_vertex.y) == pytest.approx(expected=(-50.0, -100.00), rel=1e-6)

    def test_moments_of_inertia(self, rectangular_cross_section: RectangularCrossSection) -> None:
        """Test the moments of inertia properties of the RectangularCrossSection class."""
        assert rectangular_cross_section.moment_of_inertia_about_y == pytest.approx(expected=1 / 12 * 100 * 200**3, rel=1e-6)
        assert rectangular_cross_section.moment_of_inertia_about_z == pytest.approx(expected=1 / 12 * 200 * 100**3, rel=1e-6)

    def test_section_moduli(self, rectangular_cross_section: RectangularCrossSection) -> None:
        """Test the section moduli properties of the RectangularCrossSection class."""
        assert rectangular_cross_section.elastic_section_modulus_about_y_positive == pytest.approx(expected=1 / 6 * 100 * 200**2, rel=1e-6)
        assert rectangular_cross_section.elastic_section_modulus_about_z_positive == pytest.approx(expected=1 / 6 * 200 * 100**2, rel=1e-6)

    def test_polar_moment_of_inertia(self, rectangular_cross_section: RectangularCrossSection) -> None:
        """Test the polar moment of inertia property of the RectangularCrossSection class."""
        assert rectangular_cross_section.polar_moment_of_inertia == pytest.approx(expected=1 / 12 * 100 * 200**3 + 1 / 12 * 200 * 100**3, rel=1e-6)

    def test_plastic_section_moduli(self, rectangular_cross_section: RectangularCrossSection) -> None:
        """Test the plastic section moduli properties of the RectangularCrossSection class."""
        assert rectangular_cross_section.plastic_section_modulus_about_y == pytest.approx(expected=1 / 4 * 100 * 200**2, rel=1e-6)
        assert rectangular_cross_section.plastic_section_modulus_about_z == pytest.approx(expected=1 / 4 * 200 * 100**2, rel=1e-6)
