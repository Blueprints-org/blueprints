"""Tests for cross-section shapes."""

import pytest
from sectionproperties.analysis import Section
from shapely import Polygon

from blueprints.structural_sections.geometric_cross_sections.cross_section_circle import CircularCrossSection


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
        section = circular_cross_section._section()  # noqa: SLF001
        assert isinstance(section, Section)

    def test_geometry(self, circular_cross_section: CircularCrossSection) -> None:
        """Test the geometry property of the CircularCrossSection class."""
        geometry = circular_cross_section._geometry()  # noqa: SLF001
        assert geometry is not None

    def test_mesh_settings(self, circular_cross_section: CircularCrossSection) -> None:
        """Test the mesh_settings property of the CircularCrossSection class."""
        mesh_settings = circular_cross_section.mesh_settings
        assert isinstance(mesh_settings, dict)
        assert "mesh_sizes" in mesh_settings

    def test_no_plotter_defined(self, circular_cross_section: CircularCrossSection) -> None:
        """Test that accessing the plotter property raises an AttributeError if no plotter is defined."""
        with pytest.raises(AttributeError, match="No plotter is defined."):
            _ = circular_cross_section.plotter

    def test_immutability(self, circular_cross_section: CircularCrossSection) -> None:
        """Test that the CircularCrossSection dataclass is immutable."""
        with pytest.raises(AttributeError):
            circular_cross_section.name = "New Name"  # type: ignore[misc]
