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

    def test_section(self, hexagonal_cross_section: HexagonalCrossSection) -> None:
        """Test the section object of the HexagonalCrossSection class."""
        section = hexagonal_cross_section._section()  # noqa: SLF001
        assert section is not None

    def test_geometry(self, hexagonal_cross_section: HexagonalCrossSection) -> None:
        """Test the geometry property of the HexagonalCrossSection class."""
        geometry = hexagonal_cross_section._geometry()  # noqa: SLF001
        assert geometry is not None

    def test_mesh_settings(self, hexagonal_cross_section: HexagonalCrossSection) -> None:
        """Test the mesh_settings property of the HexagonalCrossSection class."""
        mesh_settings = hexagonal_cross_section.mesh_settings
        assert isinstance(mesh_settings, dict)
        assert "mesh_sizes" in mesh_settings

    def test_apothem(self, hexagonal_cross_section: HexagonalCrossSection) -> None:
        """Test the apothem property of the HexagonalCrossSection class."""
        expected_apothem = hexagonal_cross_section.side_length * np.sqrt(3) / 2
        assert hexagonal_cross_section.apothem == pytest.approx(expected=expected_apothem, rel=1e-6)

    def test_perimter(self, hexagonal_cross_section: HexagonalCrossSection) -> None:
        """Test the perimeter property of the HexagonalCrossSection class."""
        expected_perimeter = 6 * hexagonal_cross_section.side_length
        assert hexagonal_cross_section.perimeter == pytest.approx(expected=expected_perimeter, rel=1e-6)

    def test_parameters_as_dict(self, hexagonal_cross_section: HexagonalCrossSection) -> None:
        """Test the parameters_as_dict method of the HexagonalCrossSection class."""
        params = hexagonal_cross_section.section_properties().asdict()
        assert params

    def test_no_plotter_defined(self, hexagonal_cross_section: HexagonalCrossSection) -> None:
        """Test that accessing the plotter property raises an AttributeError if no plotter is defined."""
        with pytest.raises(AttributeError, match="No plotter is defined."):
            _ = hexagonal_cross_section.plotter
