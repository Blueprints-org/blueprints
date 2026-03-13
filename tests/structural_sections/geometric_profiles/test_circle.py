"""Tests for circular shapes."""

import pytest
from sectionproperties.analysis import Section
from shapely import Polygon

from blueprints.structural_sections.geometric_profiles.circle import CircularProfile


class TestCircularProfile:
    """Tests for the CircularProfile class."""

    def test_polygon(self, circular_profile: CircularProfile) -> None:
        """Test the polygon property of the CircularProfile class."""
        assert isinstance(circular_profile.polygon, Polygon)

    def test_wrong_input(self) -> None:
        """Test the wrong input for the CircularProfile class."""
        with pytest.raises(ValueError):
            CircularProfile(name="Circle", diameter=-200.0, x=0.0, y=0.0)

    def test_radius(self, circular_profile: CircularProfile) -> None:
        """Test the radius property of the CircularProfile class."""
        assert circular_profile.radius == pytest.approx(expected=100.0, rel=1e-6)

    def test_geometry_bounds(self, circular_profile: CircularProfile) -> None:
        """Test the bounds of the geometry property."""
        bounds = circular_profile.polygon.bounds
        assert bounds == pytest.approx(expected=(0.0, 150.0, 200.0, 350.0), rel=1e-6)

    def test_section(self, circular_profile: CircularProfile) -> None:
        """Test the section object of the CircularProfile class."""
        section = circular_profile._section()  # noqa: SLF001
        assert isinstance(section, Section)

    def test_geometry(self, circular_profile: CircularProfile) -> None:
        """Test the geometry property of the CircularProfile class."""
        geometry = circular_profile._geometry()  # noqa: SLF001
        assert geometry is not None

    def test_mesh_settings(self, circular_profile: CircularProfile) -> None:
        """Test the mesh_settings property of the CircularProfile class."""
        mesh_settings = circular_profile.mesh_settings
        assert isinstance(mesh_settings, dict)
        assert "mesh_sizes" in mesh_settings

    def test_no_plotter_defined(self, circular_profile: CircularProfile) -> None:
        """Test that accessing the plotter property raises an AttributeError if no plotter is defined."""
        with pytest.raises(AttributeError, match=r"No plotter is defined."):
            _ = circular_profile.plotter

    def test_immutability(self, circular_profile: CircularProfile) -> None:
        """Test that the CircularProfile dataclass is immutable."""
        with pytest.raises(AttributeError):
            circular_profile.name = "New Name"  # type: ignore[misc]

    def test_transform(self, circular_profile: CircularProfile) -> None:
        """Test the transform method of the CircularProfile class."""
        transformed_profile = circular_profile.transform(horizontal_offset=10.0, vertical_offset=20.0, rotation=90.0)
        assert isinstance(transformed_profile, CircularProfile)
        assert pytest.approx(transformed_profile.centroid.x, rel=1e-6) == circular_profile.centroid.x + 10.0
        assert pytest.approx(transformed_profile.centroid.y, rel=1e-6) == circular_profile.centroid.y + 20.0
        assert pytest.approx(transformed_profile.profile_height, rel=1e-6) == circular_profile.profile_width

    def test_max_thickness(self, circular_profile: CircularProfile) -> None:
        """Test the max_thickness property of the CircularProfile class."""
        expected_max_thickness = 200.0
        assert circular_profile.max_thickness == pytest.approx(expected=expected_max_thickness, rel=1e-6)
