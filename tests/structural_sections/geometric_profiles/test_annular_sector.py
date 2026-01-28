"""Tests for annular sector shapes."""

import pytest
from sectionproperties.analysis import Section

from blueprints.structural_sections.geometric_profiles.annular_sector import AnnularSectorProfile


class TestAnnularSectorProfile:
    """Tests for the AnnularSectorProfile class."""

    def test_width(self, annular_sector_profile: AnnularSectorProfile) -> None:
        """Test the width property of the AnnularSectorProfile class."""
        expected_width = 110.0
        assert annular_sector_profile.profile_width == pytest.approx(expected=expected_width, rel=1e-6)

    def test_height(self, annular_sector_profile: AnnularSectorProfile) -> None:
        """Test the height property of the AnnularSectorProfile class."""
        expected_height = 110.0
        assert annular_sector_profile.profile_height == pytest.approx(expected=expected_height, rel=1e-6)

    def test_polygon(self, annular_sector_profile: AnnularSectorProfile) -> None:
        """Test the polygon property of the AnnularSectorProfile class."""
        assert annular_sector_profile.polygon.is_valid
        assert len(annular_sector_profile.polygon.exterior.coords) > 0

    def test_section(self, annular_sector_profile: AnnularSectorProfile) -> None:
        """Test the section object of the AnnularSectorProfile class."""
        section = annular_sector_profile._section()  # noqa: SLF001
        assert isinstance(section, Section)

    def test_geometry(self, annular_sector_profile: AnnularSectorProfile) -> None:
        """Test the geometry property of the AnnularSectorProfile class."""
        geometry = annular_sector_profile._geometry()  # noqa: SLF001
        assert geometry is not None

    def test_mesh_settings(self, annular_sector_profile: AnnularSectorProfile) -> None:
        """Test the mesh_settings property of the AnnularSectorProfile class."""
        mesh_settings = annular_sector_profile.mesh_settings
        assert isinstance(mesh_settings, dict)
        assert "mesh_sizes" in mesh_settings

    def test_invalid_radius(self) -> None:
        """Test initialization with an invalid radius value."""
        with pytest.raises(ValueError, match="Radius must be zero or positive"):
            AnnularSectorProfile(
                name="InvalidRadius",
                inner_radius=-10.0,
                thickness=20.0,
                start_angle=0.0,
                end_angle=90.0,
                x=0.0,
                y=0.0,
            )

    def test_invalid_thickness(self) -> None:
        """Test initialization with an invalid thickness value."""
        with pytest.raises(ValueError, match="Thickness must be a positive value"):
            AnnularSectorProfile(
                name="InvalidThickness",
                inner_radius=100.0,
                thickness=-20.0,
                start_angle=0.0,
                end_angle=90.0,
                x=0.0,
                y=0.0,
            )

    def test_invalid_end_angle_smaller_than_start_angle(self) -> None:
        """Test initialization with an invalid end angle value."""
        with pytest.raises(ValueError):
            AnnularSectorProfile(
                name="InvalidEndAngle",
                inner_radius=100.0,
                thickness=20.0,
                start_angle=90.0,
                end_angle=0.0,
                x=0.0,
                y=0.0,
            )

    @pytest.mark.parametrize(
        ("start_angle", "end_angle"),
        [
            (0, 360),
            (0, 720),
            (-50, 360),
            (0, 400),
        ],
    )
    def test_total_angle_greater_or_equal_than_360(self, start_angle: float, end_angle: float) -> None:
        """Test initialization with an invalid end angle value."""
        with pytest.raises(ValueError):
            AnnularSectorProfile(
                name="Invalid total angle, greater than 360 degrees",
                inner_radius=100.0,
                thickness=20.0,
                start_angle=start_angle,
                end_angle=end_angle,
                x=0.0,
                y=0.0,
            )

    def test_invalid_start_angle(self) -> None:
        """Test initialization with an invalid end angle value."""
        with pytest.raises(ValueError):
            AnnularSectorProfile(
                name="InvalidEndAngle",
                inner_radius=100.0,
                thickness=20.0,
                start_angle=-683,
                end_angle=270,
                x=0.0,
                y=0.0,
            )

    @pytest.mark.parametrize(
        ("start_angle", "end_angle", "expected_area"),
        [
            (0, 90, 3141.5926),
            (0, 180, 3141.5926 * 2),
            (0, 270, 3141.5926 * 3),
            (0, 359.9999999, 3141.5926 * 4),
            (90, 180, 3141.5926),
            (90, 270, 3141.5926 * 2),
            (90, 360, 3141.5926 * 3),
            (-90, 269.999999, 3141.5926 * 4),
            (-180, 90, 3141.5926 * 3),
            (-360, -270, 3141.5926),
        ],
    )
    def test_area_at_different_angles(self, start_angle: float, end_angle: float, expected_area: float) -> None:
        """Test the area property of the AnnularSectorProfile class at different angles.
        A full donut (0 to 360 degrees) should have an area of 0.
        a quarter donut (0 to 90 degrees) should have an area of pi * (outer_radius^2 - inner_radius^2) / 4.
        """
        annular_sector = AnnularSectorProfile(
            inner_radius=90.0,
            thickness=20.0,
            start_angle=start_angle,
            end_angle=end_angle,
            x=100.0,
            y=250.0,
        )
        assert annular_sector.area == pytest.approx(expected=expected_area, rel=1e-3)

    def test_no_plotter_defined(self, annular_sector_profile: AnnularSectorProfile) -> None:
        """Test that accessing the plotter property raises an AttributeError if no plotter is defined."""
        with pytest.raises(AttributeError, match=r"No plotter is defined."):
            _ = annular_sector_profile.plotter

    def test_immutability(self, annular_sector_profile: AnnularSectorProfile) -> None:
        """Test that the AnnularSectorProfile dataclass is immutable."""
        with pytest.raises(AttributeError):
            annular_sector_profile.name = "New Name"  # type: ignore[misc]

    def test_transform(self, annular_sector_profile: AnnularSectorProfile) -> None:
        """Test the transform method of the AnnularSectorProfile profile."""
        transformed_profile = annular_sector_profile.transform(horizontal_offset=1000, vertical_offset=500, rotation=90)
        assert transformed_profile is not None
        assert isinstance(transformed_profile, AnnularSectorProfile)
        assert pytest.approx(transformed_profile.centroid.x, rel=1e-6) == annular_sector_profile.centroid.x + 1000
        assert pytest.approx(transformed_profile.centroid.y, rel=1e-6) == annular_sector_profile.centroid.y + 500
        assert pytest.approx(transformed_profile.profile_height, rel=1e-6) == annular_sector_profile.profile_width

    def test_max_thickness(self, annular_sector_profile: AnnularSectorProfile) -> None:
        """Test the max_profile_thickness property of the AnnularSectorProfile class."""
        expected_max_thickness = 20.0
        assert annular_sector_profile.max_profile_thickness == pytest.approx(expected=expected_max_thickness, rel=1e-6)
