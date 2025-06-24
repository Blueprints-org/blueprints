"""Tests for hexagonal cross-section shapes."""

import numpy as np
import pytest

from blueprints.structural_sections.cross_section_hexagon import HexagonalCrossSection


class TestHexagonalCrossSection:
    """Tests for the HexagonalCrossSection class."""

    def test_area(self, hexagonal_cross_section: HexagonalCrossSection) -> None:
        """Test the area property of the HexagonalCrossSection class."""
        expected_area = (3 * np.sqrt(3) / 2) * 50.0**2
        assert hexagonal_cross_section.area == pytest.approx(expected=expected_area, rel=1e-6)

    def test_polygon(self, hexagonal_cross_section: HexagonalCrossSection) -> None:
        """Test the geometry property of the HexagonalCrossSection class."""
        polygon = hexagonal_cross_section.polygon
        assert polygon.is_valid
        assert polygon.area == pytest.approx(expected=hexagonal_cross_section.area, rel=1e-4)

    def test_invalid_side_length(self) -> None:
        """Test initialization with an invalid side length value."""
        with pytest.raises(ValueError, match="Side length must be a positive value"):
            HexagonalCrossSection(name="InvalidHexagon", side_length=-10.0, x=0.0, y=0.0)

    def test_geometry(self, hexagonal_cross_section: HexagonalCrossSection) -> None:
        """Test the geometry property of the HexagonalCrossSection class."""
        geometry = hexagonal_cross_section.geometry()
        assert geometry is not None
