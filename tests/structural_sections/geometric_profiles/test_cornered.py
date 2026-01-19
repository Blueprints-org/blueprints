"""Tests for the circular cornered profile."""

import pytest

from blueprints.structural_sections.geometric_profiles.cornered import CircularCorneredProfile
from blueprints.validations import NegativeValueError


class TestCircularCorneredProfile:
    """Tests for the CircularCorneredProfile class."""

    def test_polygon(self, qcs_profile: CircularCorneredProfile) -> None:
        """Test the polygon property."""
        polygon = qcs_profile.polygon
        assert polygon.is_valid
        assert len(polygon.exterior.coords) > 0

    def test_section(self, qcs_profile: CircularCorneredProfile) -> None:
        """Test the section object."""
        section = qcs_profile._section()  # noqa: SLF001
        assert section is not None

    def test_geometry(self, qcs_profile: CircularCorneredProfile) -> None:
        """Test the geometry property."""
        geometry = qcs_profile._geometry()  # noqa: SLF001
        assert geometry is not None

    def test_mesh_settings(self, qcs_profile: CircularCorneredProfile) -> None:
        """Test the mesh_settings property."""
        mesh_settings = qcs_profile.mesh_settings
        assert isinstance(mesh_settings, dict)
        assert "mesh_sizes" in mesh_settings

    @pytest.mark.parametrize(
        "kwargs",
        [
            {"thickness_vertical": -1, "thickness_horizontal": 10, "inner_radius": 5, "outer_radius": 10},
            {"thickness_vertical": 10, "thickness_horizontal": -1, "inner_radius": 5, "outer_radius": 10},
            {"thickness_vertical": 10, "thickness_horizontal": 10, "inner_radius": -1, "outer_radius": 10},
            {"thickness_vertical": 10, "thickness_horizontal": 10, "inner_radius": 5, "outer_radius": -1},
        ],
    )
    def test_raise_error_when_negative_values_are_given(self, kwargs: dict) -> None:
        """Test NegativeValueError is raised for negative values."""
        with pytest.raises(NegativeValueError):
            CircularCorneredProfile(**kwargs)

    def test_invalid_outer_radius_greater_than_inner_plus_thickness(self) -> None:
        """Test initialization with an outer radius greater than inner radius plus thickness."""
        with pytest.raises(
            ValueError,
            match="Outer radius 20 must be smaller than or equal to inner radius 5 plus the thickness 10",
        ):
            CircularCorneredProfile(
                thickness_vertical=10,
                thickness_horizontal=10,
                inner_radius=5,
                outer_radius=20,
            )

    @pytest.mark.parametrize("corner_direction", [0, 1, 2, 3])
    def test_valid_corner_direction(self, corner_direction: int) -> None:
        """Test initialization with an invalid corner direction."""
        profile = CircularCorneredProfile(
            thickness_vertical=10,
            thickness_horizontal=10,
            inner_radius=5,
            outer_radius=10,
            corner_direction=corner_direction,
        )
        assert profile.polygon.is_valid

    def test_invalid_corner_direction(self) -> None:
        """Test initialization with an invalid corner direction."""
        with pytest.raises(ValueError, match="corner_direction must be one of 0, 1, 2, or 3, got 4"):
            CircularCorneredProfile(
                thickness_vertical=10,
                thickness_horizontal=10,
                inner_radius=5,
                outer_radius=10,
                corner_direction=4,
            )

    def test_no_plotter_defined(self, qcs_profile: CircularCorneredProfile) -> None:
        """Test that accessing the plotter property raises an AttributeError if no plotter is defined."""
        with pytest.raises(AttributeError, match=r"No plotter is defined."):
            _ = qcs_profile.plotter

    def test_immutability(self, qcs_profile: CircularCorneredProfile) -> None:
        """Test that the CircularCorneredProfile dataclass is immutable."""
        with pytest.raises(AttributeError):
            qcs_profile.name = "New Name"  # type: ignore[misc]

    def test_transform(self, qcs_profile: CircularCorneredProfile) -> None:
        """Test the transform method of the CircularCorneredProfile class."""
        transformed_profile = qcs_profile.transform(horizontal_offset=15.0, vertical_offset=25.0, rotation=90.0)
        assert isinstance(transformed_profile, CircularCorneredProfile)
        assert pytest.approx(transformed_profile.centroid.x, rel=1e-6) == qcs_profile.centroid.x + 15.0
        assert pytest.approx(transformed_profile.centroid.y, rel=1e-6) == qcs_profile.centroid.y + 25.0
        assert pytest.approx(transformed_profile.profile_height, rel=1e-6) == qcs_profile.profile_width

    def test_max_thickness(self, qcs_profile: CircularCorneredProfile) -> None:
        """Test the max_profile_thickness property of the CircularCorneredProfile class."""
        expected_max_thickness = min(qcs_profile.thickness_vertical, qcs_profile.thickness_horizontal)
        assert qcs_profile.max_profile_thickness == pytest.approx(expected=expected_max_thickness, rel=1e-6)
