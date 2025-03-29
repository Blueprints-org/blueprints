"""Tests for hexagonal cross-section shapes."""

import numpy as np
import pytest
from shapely.geometry import Point

from blueprints.structural_sections.cross_section_hexagon import HexagonalCrossSection


class TestHexagonalCrossSection:
    """Tests for the HexagonalCrossSection class."""

    @pytest.fixture
    def hexagonal_cross_section(self) -> HexagonalCrossSection:
        """Return a HexagonalCrossSection instance."""
        return HexagonalCrossSection(name="Hexagon", side_length=50.0, x=0.0, y=0.0)

    def test_area(self, hexagonal_cross_section: HexagonalCrossSection) -> None:
        """Test the area property of the HexagonalCrossSection class."""
        expected_area = (3 * np.sqrt(3) / 2) * 50.0**2
        assert hexagonal_cross_section.area == pytest.approx(expected=expected_area, rel=1e-6)

    def test_perimeter(self, hexagonal_cross_section: HexagonalCrossSection) -> None:
        """Test the perimeter property of the HexagonalCrossSection class."""
        expected_perimeter = 6 * 50.0
        assert hexagonal_cross_section.perimeter == pytest.approx(expected=expected_perimeter, rel=1e-6)

    def test_plate_thickness(self, hexagonal_cross_section: HexagonalCrossSection) -> None:
        """Test the plate thickness property of the HexagonalCrossSection class."""
        expected_thickness = 50.0 * np.sqrt(3)
        assert hexagonal_cross_section.plate_thickness == pytest.approx(expected=expected_thickness, rel=1e-6)

    def test_centroid(self, hexagonal_cross_section: HexagonalCrossSection) -> None:
        """Test the centroid property of the HexagonalCrossSection class."""
        centroid = hexagonal_cross_section.centroid
        assert (centroid.x, centroid.y) == pytest.approx(expected=(0.0, 0.0), rel=1e-6)

    def test_moments_of_inertia(self, hexagonal_cross_section: HexagonalCrossSection) -> None:
        """Test the moments of inertia properties of the HexagonalCrossSection class."""
        expected_inertia = (5 / 16) * np.sqrt(3) * 50.0**4
        assert hexagonal_cross_section.moment_of_inertia_about_y == pytest.approx(expected=expected_inertia, rel=1e-6)
        assert hexagonal_cross_section.moment_of_inertia_about_z == pytest.approx(expected=expected_inertia, rel=1e-6)

    def test_polar_moment_of_inertia(self, hexagonal_cross_section: HexagonalCrossSection) -> None:
        """Test the polar moment of inertia property of the HexagonalCrossSection class."""
        expected_polar = (5 / 8) * np.sqrt(3) * 50.0**4
        assert hexagonal_cross_section.polar_moment_of_inertia == pytest.approx(expected=expected_polar, rel=1e-6)

    def test_section_moduli(self, hexagonal_cross_section: HexagonalCrossSection) -> None:
        """Test the section moduli properties of the HexagonalCrossSection class."""
        expected_modulus_y = ((5 / 16) * np.sqrt(3) * 50.0**4) / (50.0 * np.sqrt(3) / 2)
        expected_modulus_z = ((5 / 16) * np.sqrt(3) * 50.0**4) / 50.0
        assert hexagonal_cross_section.elastic_section_modulus_about_y_positive == pytest.approx(expected=expected_modulus_y, rel=1e-6)
        assert hexagonal_cross_section.elastic_section_modulus_about_z_positive == pytest.approx(expected=expected_modulus_z, rel=1e-6)
        assert hexagonal_cross_section.elastic_section_modulus_about_y_negative == pytest.approx(expected=expected_modulus_y, rel=1e-6)
        assert hexagonal_cross_section.elastic_section_modulus_about_z_negative == pytest.approx(expected=expected_modulus_z, rel=1e-6)

    def test_plastic_section_moduli(self, hexagonal_cross_section: HexagonalCrossSection) -> None:
        """Test the plastic section moduli properties of the HexagonalCrossSection class."""
        expected_plastic_modulus = (50.0**3) * np.sqrt(3) / 4
        assert hexagonal_cross_section.plastic_section_modulus_about_y == pytest.approx(expected=expected_plastic_modulus, rel=1e-6)
        assert hexagonal_cross_section.plastic_section_modulus_about_z == pytest.approx(expected=expected_plastic_modulus, rel=1e-6)

    def test_geometry(self, hexagonal_cross_section: HexagonalCrossSection) -> None:
        """Test the geometry property of the HexagonalCrossSection class."""
        geometry = hexagonal_cross_section.geometry
        assert geometry.is_valid
        assert geometry.area == pytest.approx(expected=hexagonal_cross_section.area, rel=1e-4)

    def test_vertices(self, hexagonal_cross_section: HexagonalCrossSection) -> None:
        """Test the vertices property of the HexagonalCrossSection class."""
        vertices = hexagonal_cross_section.vertices
        assert len(vertices) == 7  # 6 vertices + 1 repeated for closure
        for vertex in vertices:
            assert isinstance(vertex, Point)

    def test_dotted_mesh(self, hexagonal_cross_section: HexagonalCrossSection) -> None:
        """Test the dotted mesh property of the HexagonalCrossSection class."""
        dotted_mesh = hexagonal_cross_section.dotted_mesh()
        assert len(dotted_mesh) > 0
        for point in dotted_mesh:
            assert hexagonal_cross_section.geometry.contains(point)

    def test_invalid_side_length(self) -> None:
        """Test initialization with an invalid side length value."""
        with pytest.raises(ValueError, match="Side length must be a positive value"):
            HexagonalCrossSection(name="InvalidHexagon", side_length=-10.0, x=0.0, y=0.0)

    def test_custom_mesh_size(self, hexagonal_cross_section: HexagonalCrossSection) -> None:
        """Test the dotted mesh property with a custom mesh size."""
        dotted_mesh = hexagonal_cross_section.dotted_mesh(max_mesh_size=10.0)
        assert len(dotted_mesh) > 0
        for point in dotted_mesh:
            assert hexagonal_cross_section.geometry.contains(point)
