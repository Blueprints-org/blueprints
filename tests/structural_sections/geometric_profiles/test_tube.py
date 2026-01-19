"""Tests for circular tube profile shapes."""

import numpy as np
import pytest

from blueprints.structural_sections.geometric_profiles.tube import TubeProfile


class TestTubeProfile:
    """Tests for the TubeProfile class."""

    def test_area(self, tube_profile: TubeProfile) -> None:
        """Test the area property of the TubeProfile class."""
        expected_area = np.pi * (50.0**2 - 25.0**2)
        assert tube_profile.area == pytest.approx(expected=expected_area, rel=1e-3)

    def test_wall_thickness(self, tube_profile: TubeProfile) -> None:
        """Test the wall thickness property of the TubeProfile class."""
        expected_thickness = (100.0 - 50.0) / 2.0
        assert tube_profile.wall_thickness == pytest.approx(expected=expected_thickness, rel=1e-3)

    def test_polygon(self, tube_profile: TubeProfile) -> None:
        """Test the geometry property of the TubeProfile class."""
        polygon = tube_profile.polygon
        assert polygon.is_valid
        assert polygon.area == pytest.approx(expected=tube_profile.area, rel=1e-3)

    def test_invalid_outer_diameter(self) -> None:
        """Test initialization with an invalid outer diameter value."""
        with pytest.raises(ValueError, match="Outer diameter must be a positive value"):
            TubeProfile(name="InvalidOuter", outer_diameter=-10.0, inner_diameter=5.0, x=0.0, y=0.0)

    def test_invalid_inner_diameter(self) -> None:
        """Test initialization with an invalid inner diameter value."""
        with pytest.raises(ValueError, match="Inner diameter cannot be negative"):
            TubeProfile(name="InvalidInner", outer_diameter=10.0, inner_diameter=-5.0, x=0.0, y=0.0)

    def test_inner_diameter_greater_than_outer(self) -> None:
        """Test initialization with inner diameter greater than or equal to outer diameter."""
        with pytest.raises(ValueError, match="Inner diameter must be smaller than outer diameter"):
            TubeProfile(name="InvalidDiameters", outer_diameter=9.0, inner_diameter=10.0, x=0.0, y=0.0)

    def test_section(self, tube_profile: TubeProfile) -> None:
        """Test the section object of the TubeProfile class."""
        section = tube_profile._section()  # noqa: SLF001
        assert section is not None

    def test_geometry(self, tube_profile: TubeProfile) -> None:
        """Test the geometry property of the TubeProfile class."""
        geometry = tube_profile._geometry()  # noqa: SLF001
        assert geometry is not None

    def test_mesh_settings(self, tube_profile: TubeProfile) -> None:
        """Test the mesh_settings property of the TubeProfile class."""
        mesh_settings = tube_profile.mesh_settings
        assert isinstance(mesh_settings, dict)
        assert "mesh_sizes" in mesh_settings

    def test_no_plotter_defined(self, tube_profile: TubeProfile) -> None:
        """Test that accessing the plotter property raises an AttributeError if no plotter is defined."""
        with pytest.raises(AttributeError, match=r"No plotter is defined."):
            _ = tube_profile.plotter

    def test_immutability(self, tube_profile: TubeProfile) -> None:
        """Test that the TubeProfile dataclass is immutable."""
        with pytest.raises(AttributeError):
            tube_profile.name = "New Name"  # type: ignore[misc]

    def test_transform(self, tube_profile: TubeProfile) -> None:
        """Test the transform method of the TubeProfile class."""
        transformed_profile = tube_profile.transform(horizontal_offset=10.0, vertical_offset=20.0, rotation=90.0)
        assert isinstance(transformed_profile, TubeProfile)
        assert pytest.approx(transformed_profile.centroid.x, rel=1e-6) == tube_profile.centroid.x + 10.0
        assert pytest.approx(transformed_profile.centroid.y, rel=1e-6) == tube_profile.centroid.y + 20.0
        assert pytest.approx(transformed_profile.profile_height, rel=1e-6) == tube_profile.profile_width

    def test_max_thickness(self, tube_profile: TubeProfile) -> None:
        """Test the max_profile_thickness property of the TubeProfile class."""
        expected_max_thickness = (tube_profile.outer_diameter - tube_profile.inner_diameter) / 2.0
        assert tube_profile.max_profile_thickness == pytest.approx(expected=expected_max_thickness, rel=1e-6)
