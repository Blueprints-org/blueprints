"""Tests for triangular profile shapes."""

import pytest
from shapely.geometry import Polygon

from blueprints.structural_sections.geometric_profiles.triangle import RightAngledTriangularProfile


class TestRightAngledTriangularProfile:
    """Tests for the RightAngledTriangularProfile class."""

    def test_area(self, triangular_profile: RightAngledTriangularProfile) -> None:
        """Test the area property of the RightAngledTriangularProfile class."""
        assert triangular_profile.area == pytest.approx(expected=10000.0, rel=1e-6)

    def test_polygon(self, triangular_profile: RightAngledTriangularProfile) -> None:
        """Test the polygon property of the RightAngledTriangularProfile class."""
        assert isinstance(triangular_profile.polygon, Polygon)

    def test_section(self, triangular_profile: RightAngledTriangularProfile) -> None:
        """Test the section object of the RightAngledTriangularProfile class."""
        section = triangular_profile._section()  # noqa: SLF001
        assert section is not None

    def test_geometry(self, triangular_profile: RightAngledTriangularProfile) -> None:
        """Test the geometry property of the RightAngledTriangularProfile class."""
        geometry = triangular_profile._geometry()  # noqa: SLF001
        assert geometry is not None

    def test_mesh_settings(self, triangular_profile: RightAngledTriangularProfile) -> None:
        """Test the mesh_settings property of the RightAngledTriangularProfile class."""
        mesh_settings = triangular_profile.mesh_settings
        assert isinstance(mesh_settings, dict)
        assert "mesh_sizes" in mesh_settings

    def test_invalid_base(self) -> None:
        """Test initialization with an invalid base value."""
        with pytest.raises(ValueError, match="Base must be a positive value"):
            RightAngledTriangularProfile(name="InvalidBase", base=-10.0, height=200.0)

    def test_invalid_height(self) -> None:
        """Test initialization with an invalid height value."""
        with pytest.raises(ValueError, match="Height must be a positive value"):
            RightAngledTriangularProfile(name="InvalidHeight", base=100.0, height=-20.0)

    def test_mirrored_polygon(self) -> None:
        """Test the geometry property when the triangle is mirrored."""
        mirrored_triangle = RightAngledTriangularProfile(
            name="MirroredTriangle", base=100.0, height=200.0, mirrored_horizontally=True, mirrored_vertically=True
        )
        polygon = mirrored_triangle.polygon
        assert polygon.is_valid
        assert len(polygon.exterior.coords) == 4
        assert (polygon.exterior.coords[1][0], polygon.exterior.coords[1][1]) == (-100.0, 0)
        assert (polygon.exterior.coords[2][0], polygon.exterior.coords[2][1]) == (0, -200.0)

    def test_no_plotter_defined(self, triangular_profile: RightAngledTriangularProfile) -> None:
        """Test that accessing the plotter property raises an AttributeError if no plotter is defined."""
        with pytest.raises(AttributeError, match=r"No plotter is defined."):
            _ = triangular_profile.plotter

    def test_immutability(self, triangular_profile: RightAngledTriangularProfile) -> None:
        """Test that the RightAngledTriangularProfile dataclass is immutable."""
        with pytest.raises(AttributeError):
            triangular_profile.name = "New Name"  # type: ignore[misc]

    def test_transform(self, triangular_profile: RightAngledTriangularProfile) -> None:
        """Test the transform method of the RightAngledTriangularProfile class."""
        transformed_profile = triangular_profile.transform(horizontal_offset=10.0, vertical_offset=20.0, rotation=90.0)
        assert isinstance(transformed_profile, RightAngledTriangularProfile)
        assert pytest.approx(transformed_profile.centroid.x, rel=1e-6) == triangular_profile.centroid.x + 10.0
        assert pytest.approx(transformed_profile.centroid.y, rel=1e-6) == triangular_profile.centroid.y + 20.0
        assert pytest.approx(transformed_profile.profile_height, rel=1e-6) == triangular_profile.profile_width

    def test_max_thickness(self, triangular_profile: RightAngledTriangularProfile) -> None:
        """Test the max_thickness property of the RightAngledTriangularProfile class."""
        expected_max_thickness = min(triangular_profile.base, triangular_profile.height)
        assert triangular_profile.max_thickness == pytest.approx(expected=expected_max_thickness, rel=1e-6)
