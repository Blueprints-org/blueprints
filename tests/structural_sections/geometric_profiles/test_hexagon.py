"""Tests for hexagonal profile shapes."""

import numpy as np
import pytest

from blueprints.structural_sections.geometric_profiles.hexagon import HexagonalProfile


class TestHexagonalProfile:
    """Tests for the HexagonalProfile class."""

    def test_area(self, hexagonal_profile: HexagonalProfile) -> None:
        """Test the area property of the HexagonalProfile class."""
        expected_area = (3 * np.sqrt(3) / 2) * 50.0**2
        assert hexagonal_profile.area == pytest.approx(expected=expected_area, rel=1e-6)

    def test_polygon(self, hexagonal_profile: HexagonalProfile) -> None:
        """Test the geometry property of the HexagonalProfile class."""
        polygon = hexagonal_profile.polygon
        assert polygon.is_valid
        assert polygon.area == pytest.approx(expected=hexagonal_profile.area, rel=1e-4)

    def test_invalid_side_length(self) -> None:
        """Test initialization with an invalid side length value."""
        with pytest.raises(ValueError, match="Side length must be a positive value"):
            HexagonalProfile(name="InvalidHexagon", side_length=-10.0, x=0.0, y=0.0)

    def test_section(self, hexagonal_profile: HexagonalProfile) -> None:
        """Test the section object of the HexagonalProfile class."""
        section = hexagonal_profile._section()  # noqa: SLF001
        assert section is not None

    def test_geometry(self, hexagonal_profile: HexagonalProfile) -> None:
        """Test the geometry property of the HexagonalProfile class."""
        geometry = hexagonal_profile._geometry()  # noqa: SLF001
        assert geometry is not None

    def test_mesh_settings(self, hexagonal_profile: HexagonalProfile) -> None:
        """Test the mesh_settings property of the HexagonalProfile class."""
        mesh_settings = hexagonal_profile.mesh_settings
        assert isinstance(mesh_settings, dict)
        assert "mesh_sizes" in mesh_settings

    def test_apothem(self, hexagonal_profile: HexagonalProfile) -> None:
        """Test the apothem property of the HexagonalProfile class."""
        expected_apothem = hexagonal_profile.side_length * np.sqrt(3) / 2
        assert hexagonal_profile.apothem == pytest.approx(expected=expected_apothem, rel=1e-6)

    def test_perimeter(self, hexagonal_profile: HexagonalProfile) -> None:
        """Test the perimeter property of the HexagonalProfile class."""
        expected_perimeter = 6 * hexagonal_profile.side_length
        assert hexagonal_profile.perimeter == pytest.approx(expected=expected_perimeter, rel=1e-6)

    def test_parameters_as_dict(self, hexagonal_profile: HexagonalProfile) -> None:
        """Test the parameters_as_dict method of the HexagonalProfile class."""
        params = hexagonal_profile.section_properties().asdict()
        assert params

    def test_no_plotter_defined(self, hexagonal_profile: HexagonalProfile) -> None:
        """Test that accessing the plotter property raises an AttributeError if no plotter is defined."""
        with pytest.raises(AttributeError, match=r"No plotter is defined."):
            _ = hexagonal_profile.plotter

    def test_immutability(self, hexagonal_profile: HexagonalProfile) -> None:
        """Test that the HexagonalProfile dataclass is immutable."""
        with pytest.raises(AttributeError):
            hexagonal_profile.name = "New Name"  # type: ignore[misc]

    def test_transform(self, hexagonal_profile: HexagonalProfile) -> None:
        """Test the transform method of the HexagonalProfile class."""
        transformed_profile = hexagonal_profile.transform(horizontal_offset=10.0, vertical_offset=20.0, rotation=90.0)
        assert isinstance(transformed_profile, HexagonalProfile)
        assert pytest.approx(transformed_profile.centroid.x, rel=1e-6) == hexagonal_profile.centroid.x + 10.0
        assert pytest.approx(transformed_profile.centroid.y, rel=1e-6) == hexagonal_profile.centroid.y + 20.0
        assert pytest.approx(transformed_profile.profile_height, rel=1e-6) == hexagonal_profile.profile_width

    def test_max_thickness(self, hexagonal_profile: HexagonalProfile) -> None:
        """Test the max_profile_thickness property of the HexagonalProfile class."""
        expected_max_thickness = hexagonal_profile.side_length * np.sqrt(3)
        assert hexagonal_profile.max_profile_thickness == pytest.approx(expected=expected_max_thickness, rel=1e-6)
