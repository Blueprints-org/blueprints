"""Tests for circular tube cross-section shapes."""

import numpy as np
import pytest

from blueprints.structural_sections.cross_section_tube import TubeCrossSection


class TestTubeCrossSection:
    """Tests for the TubeCrossSection class."""

    def test_area(self, tube_cross_section: TubeCrossSection) -> None:
        """Test the area property of the TubeCrossSection class."""
        expected_area = np.pi * (50.0**2 - 25.0**2)
        assert tube_cross_section.area == pytest.approx(expected=expected_area, rel=1e-3)

    def test_wall_thickness(self, tube_cross_section: TubeCrossSection) -> None:
        """Test the wall thickness property of the TubeCrossSection class."""
        expected_thickness = (100.0 - 50.0) / 2.0
        assert tube_cross_section.wall_thickness == pytest.approx(expected=expected_thickness, rel=1e-3)

    def test_polygon(self, tube_cross_section: TubeCrossSection) -> None:
        """Test the geometry property of the TubeCrossSection class."""
        polygon = tube_cross_section.polygon
        assert polygon.is_valid
        assert polygon.area == pytest.approx(expected=tube_cross_section.area, rel=1e-3)

    def test_invalid_outer_diameter(self) -> None:
        """Test initialization with an invalid outer diameter value."""
        with pytest.raises(ValueError, match="Outer diameter must be a positive value"):
            TubeCrossSection(name="InvalidOuter", outer_diameter=-10.0, inner_diameter=5.0, x=0.0, y=0.0)

    def test_invalid_inner_diameter(self) -> None:
        """Test initialization with an invalid inner diameter value."""
        with pytest.raises(ValueError, match="Inner diameter cannot be negative"):
            TubeCrossSection(name="InvalidInner", outer_diameter=10.0, inner_diameter=-5.0, x=0.0, y=0.0)

    def test_inner_diameter_greater_than_outer(self) -> None:
        """Test initialization with inner diameter greater than or equal to outer diameter."""
        with pytest.raises(ValueError, match="Inner diameter must be smaller than outer diameter"):
            TubeCrossSection(name="InvalidDiameters", outer_diameter=9.0, inner_diameter=10.0, x=0.0, y=0.0)

    def test_geometry(self, tube_cross_section: TubeCrossSection) -> None:
        """Test the geometry property of the TubeCrossSection class."""
        geometry = tube_cross_section.geometry()
        assert geometry is not None
