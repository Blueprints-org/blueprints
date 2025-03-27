"""Tests for cross-section shapes."""

import math

import pytest
from shapely import Polygon

from blueprints.structural_sections.cross_section_circle import CircularCrossSection


class TestCircularCrossSection:
    """Tests for the CircularCrossSection class."""

    @pytest.fixture
    def circular_cross_section(self) -> CircularCrossSection:
        """Return a CircularCrossSection instance."""
        return CircularCrossSection(diameter=200.0, x=0.0, y=0.0)

    def test_geometry(self, circular_cross_section: CircularCrossSection) -> None:
        """Test the geometry property of the CircularCrossSection class."""
        assert isinstance(circular_cross_section.geometry, Polygon)

    def test_area(self, circular_cross_section: CircularCrossSection) -> None:
        """Test the area property of the CircularCrossSection class."""
        assert circular_cross_section.area == pytest.approx(expected=31415.92653, rel=1e-6)

    def test_perimeter(self, circular_cross_section: CircularCrossSection) -> None:
        """Test the perimeter property of the CircularCrossSection class."""
        assert circular_cross_section.perimeter == pytest.approx(expected=628.31853, rel=1e-6)

    def test_centroid(self, circular_cross_section: CircularCrossSection) -> None:
        """Test the centroid property of the CircularCrossSection class."""
        centroid = circular_cross_section.centroid
        assert (centroid.x, centroid.y) == pytest.approx(expected=(0.0, 0.0), rel=1e-6)

    def test_vertices(self, circular_cross_section: CircularCrossSection) -> None:
        """Test the vertices property of the CircularCrossSection class."""
        vertices = circular_cross_section.vertices
        first_vertex = vertices[0]
        last_vertex = vertices[-1]
        assert len(vertices) == 65
        assert (first_vertex.x, first_vertex.y) == pytest.approx(expected=(100.0, 0.0), rel=1e-6)
        assert (last_vertex.x, last_vertex.y) == pytest.approx(expected=(100.0, 0.0), rel=1e-6)

    def test_wrong_input(self) -> None:
        """Test the wrong input for the CircularCrossSection class."""
        with pytest.raises(ValueError):
            CircularCrossSection(diameter=-200.0, x=0.0, y=0.0)

    def test_moments_of_inertia(self, circular_cross_section: CircularCrossSection) -> None:
        """Test the moments of inertia properties of the CircularCrossSection class."""
        expected_moi = (1 / 64) * math.pi * 200**4
        assert circular_cross_section.moment_of_inertia_about_y == pytest.approx(expected=expected_moi, rel=1e-6)
        assert circular_cross_section.moment_of_inertia_about_z == pytest.approx(expected=expected_moi, rel=1e-6)

    def test_section_moduli(self, circular_cross_section: CircularCrossSection) -> None:
        """Test the section moduli properties of the CircularCrossSection class."""
        expected_section_modulus = (1 / 32) * math.pi * 200**3
        assert circular_cross_section.elastic_section_modulus_about_y_positive == pytest.approx(expected=expected_section_modulus, rel=1e-6)
        assert circular_cross_section.elastic_section_modulus_about_z_positive == pytest.approx(expected=expected_section_modulus, rel=1e-6)

    def test_polar_moment_of_inertia(self, circular_cross_section: CircularCrossSection) -> None:
        """Test the polar moment of inertia property of the CircularCrossSection class."""
        expected_polar_moi = (1 / 32) * math.pi * 200**4
        assert circular_cross_section.polar_moment_of_inertia == pytest.approx(expected=expected_polar_moi, rel=1e-6)

    def test_plastic_section_moduli(self, circular_cross_section: CircularCrossSection) -> None:
        """Test the plastic section moduli properties of the CircularCrossSection class."""
        expected_plastic_modulus = (1 / 6) * 200**3
        assert circular_cross_section.plastic_section_modulus_about_y == pytest.approx(expected=expected_plastic_modulus, rel=1e-6)
        assert circular_cross_section.plastic_section_modulus_about_z == pytest.approx(expected=expected_plastic_modulus, rel=1e-6)
