"""Tests for cross-section shapes."""

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
