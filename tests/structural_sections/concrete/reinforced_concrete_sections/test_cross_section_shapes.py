"""Tests for cross section shapes."""

import pytest

from blueprints.structural_sections.concrete.reinforced_concrete_sections.cross_section_shapes import CircularCrossSection, RectangularCrossSection


class TestCircularCrossSection:
    """Tests for the CircularCrossSection class."""

    @pytest.fixture
    def circular_cross_section(self) -> CircularCrossSection:
        """Return a CircularCrossSection instance."""
        return CircularCrossSection(diameter=200.0, x=0.0, y=0.0)

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
