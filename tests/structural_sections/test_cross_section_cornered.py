"""Tests for the circular cornered cross section."""

import pytest

from blueprints.structural_sections.cross_section_cornered import CircularCorneredCrossSection
from blueprints.validations import NegativeValueError


class TestCircularCorneredCrossSection:
    """Tests for the CircularCorneredCrossSection class."""

    def test_polygon(self, qcs_cross_section: CircularCorneredCrossSection) -> None:
        """Test the polygon property."""
        polygon = qcs_cross_section.polygon
        assert polygon.is_valid
        assert len(polygon.exterior.coords) > 0

    def test_section(self, qcs_cross_section: CircularCorneredCrossSection) -> None:
        """Test the section object."""
        section = qcs_cross_section._section()  # noqa: SLF001
        assert section is not None

    def test_geometry(self, qcs_cross_section: CircularCorneredCrossSection) -> None:
        """Test the geometry property."""
        geometry = qcs_cross_section._geometry()  # noqa: SLF001
        assert geometry is not None

    def test_mesh_settings(self, qcs_cross_section: CircularCorneredCrossSection) -> None:
        """Test the mesh_settings property."""
        mesh_settings = qcs_cross_section.mesh_settings
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
            CircularCorneredCrossSection(**kwargs)

    def test_invalid_outer_radius_greater_than_inner_plus_thickness(self) -> None:
        """Test initialization with an outer radius greater than inner radius plus thickness."""
        with pytest.raises(
            ValueError,
            match="Outer radius 20 must be smaller than or equal to inner radius 5 plus the thickness 10",
        ):
            CircularCorneredCrossSection(
                thickness_vertical=10,
                thickness_horizontal=10,
                inner_radius=5,
                outer_radius=20,
            )

    @pytest.mark.parametrize("corner_direction", [0, 1, 2, 3])
    def test_valid_corner_direction(self, corner_direction: int) -> None:
        """Test initialization with an invalid corner direction."""
        cross_section = CircularCorneredCrossSection(
            thickness_vertical=10,
            thickness_horizontal=10,
            inner_radius=5,
            outer_radius=10,
            corner_direction=corner_direction,
        )
        assert cross_section.polygon.is_valid

    def test_invalid_corner_direction(self) -> None:
        """Test initialization with an invalid corner direction."""
        with pytest.raises(ValueError, match="corner_direction must be one of 0, 1, 2, or 3, got 4"):
            CircularCorneredCrossSection(
                thickness_vertical=10,
                thickness_horizontal=10,
                inner_radius=5,
                outer_radius=10,
                corner_direction=4,
            )

    def test_no_plotter_defined(self, qcs_cross_section: CircularCorneredCrossSection) -> None:
        """Test that accessing the plotter property raises an AttributeError if no plotter is defined."""
        with pytest.raises(AttributeError, match="No plotter is defined."):
            _ = qcs_cross_section.plotter

    def test_immutability(self, qcs_cross_section: CircularCorneredCrossSection) -> None:
        """Test that the CircularCorneredCrossSection dataclass is immutable."""
        with pytest.raises(AttributeError):
            qcs_cross_section.name = "New Name"  # type: ignore[misc]
