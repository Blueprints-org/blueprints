"""Tests for cross-section shapes."""

import pytest
from sectionproperties.analysis import Section
from sectionproperties.post.post import SectionProperties

from blueprints.structural_sections.cross_section_rectangle import RectangularCrossSection


class TestRectangularCrossSection:
    """Tests for the RectangularCrossSection class."""

    def test_area(self, rectangular_cross_section: RectangularCrossSection) -> None:
        """Test the area property of the RectangularCrossSection class."""
        assert rectangular_cross_section.area == pytest.approx(expected=20000.0, rel=1e-6)

    def test_invalid_width(self) -> None:
        """Test that an error is raised for invalid width."""
        with pytest.raises(ValueError, match="Width must be a positive value"):
            RectangularCrossSection(name="InvalidWidth", width=-10.0, height=200.0)

    def test_invalid_height(self) -> None:
        """Test that an error is raised for invalid height."""
        with pytest.raises(ValueError, match="Height must be a positive value"):
            RectangularCrossSection(name="InvalidHeight", width=100.0, height=-200.0)

    def test_polygon(self, rectangular_cross_section: RectangularCrossSection) -> None:
        """Test the geometry property of the RectangularCrossSection class."""
        polygon = rectangular_cross_section.polygon
        assert polygon.bounds == pytest.approx(expected=(50.0, 150.0, 150.0, 350.0), rel=1e-6)

    def test_section(self, rectangular_cross_section: RectangularCrossSection) -> None:
        """Test the geometry property of the RectangularCrossSection class."""
        section = rectangular_cross_section.section()
        assert isinstance(section, Section)

    def test_section_properties_geometric(self, rectangular_cross_section_section_properties: SectionProperties) -> None:
        """Test the section properties of the RectangularCrossSection class."""
        assert rectangular_cross_section_section_properties.area == pytest.approx(expected=20000.0, rel=1e-6)
        assert rectangular_cross_section_section_properties.perimeter == pytest.approx(expected=600.0, rel=1e-6)
        assert rectangular_cross_section_section_properties.ixx_g == pytest.approx(expected=1316666666.6, rel=1e-6)

    def test_section_properties_plastic(self, rectangular_cross_section_section_properties: SectionProperties) -> None:
        """Test the section properties of the RectangularCrossSection class."""
        assert rectangular_cross_section_section_properties.syy == pytest.approx(expected=500000.0, rel=1e-6)
        assert rectangular_cross_section_section_properties.sxx == pytest.approx(expected=1000000.0, rel=1e-6)

    def test_geometry(self, rectangular_cross_section: RectangularCrossSection) -> None:
        """Test the geometry property of the RectangularCrossSection class."""
        geometry = rectangular_cross_section.geometry()
        assert geometry is not None
