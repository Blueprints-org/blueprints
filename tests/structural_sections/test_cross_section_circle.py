"""Tests for cross-section shapes."""

import pytest
from sectionproperties.analysis import Section
from shapely import Polygon

from blueprints.structural_sections.cross_section_circle import CircularCrossSection


class TestCircularCrossSection:
    """Tests for the CircularCrossSection class."""

    def test_polygon(self, circular_cross_section: CircularCrossSection) -> None:
        """Test the polygon property of the CircularCrossSection class."""
        assert isinstance(circular_cross_section.polygon, Polygon)

    def test_wrong_input(self) -> None:
        """Test the wrong input for the CircularCrossSection class."""
        with pytest.raises(ValueError):
            CircularCrossSection(name="Circle", diameter=-200.0, x=0.0, y=0.0)

    def test_radius(self, circular_cross_section: CircularCrossSection) -> None:
        """Test the radius property of the CircularCrossSection class."""
        assert circular_cross_section.radius == pytest.approx(expected=100.0, rel=1e-6)

    def test_geometry_bounds(self, circular_cross_section: CircularCrossSection) -> None:
        """Test the bounds of the geometry property."""
        bounds = circular_cross_section.polygon.bounds
        assert bounds == pytest.approx(expected=(0.0, 150.0, 200.0, 350.0), rel=1e-6)

    def test_section(self, circular_cross_section: CircularCrossSection) -> None:
        """Test the section object of the CircularCrossSection class."""
        section = circular_cross_section.section()
        assert isinstance(section, Section)

    def test_geometry(self, circular_cross_section: CircularCrossSection) -> None:
        """Test the geometry property of the CircularCrossSection class."""
        geometry = circular_cross_section.geometry()
        assert geometry is not None
