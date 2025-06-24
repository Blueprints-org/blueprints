"""Tests for cross-section shapes."""

import pytest
from sectionproperties.analysis import Section

from blueprints.structural_sections.cross_section_annular_sector import AnnularSectorCrossSection


class TestAnnularSectorCrossSection:
    """Tests for the AnnularSectorCrossSection class."""

    def test_width(self, annular_sector_cross_section: AnnularSectorCrossSection) -> None:
        """Test the width property of the AnnularSectorCrossSection class."""
        expected_width = 110.0
        assert annular_sector_cross_section.width == pytest.approx(expected=expected_width, rel=1e-6)

    def test_height(self, annular_sector_cross_section: AnnularSectorCrossSection) -> None:
        """Test the height property of the AnnularSectorCrossSection class."""
        expected_height = 110.0
        assert annular_sector_cross_section.height == pytest.approx(expected=expected_height, rel=1e-6)

    def test_polygon(self, annular_sector_cross_section: AnnularSectorCrossSection) -> None:
        """Test the polygon property of the AnnularSectorCrossSection class."""
        assert annular_sector_cross_section.polygon.is_valid
        assert len(annular_sector_cross_section.polygon.exterior.coords) > 0

    def test_section(self, annular_sector_cross_section: AnnularSectorCrossSection) -> None:
        """Test the section object of the AnnularSectorCrossSection class."""
        section = annular_sector_cross_section.section()
        assert isinstance(section, Section)

    def test_geometry(self, annular_sector_cross_section: AnnularSectorCrossSection) -> None:
        """Test the geometry property of the AnnularSectorCrossSection class."""
        geometry = annular_sector_cross_section.geometry()
        assert geometry is not None

    def test_invalid_radius(self) -> None:
        """Test initialization with an invalid radius value."""
        with pytest.raises(ValueError, match="Radius must be zero or positive"):
            AnnularSectorCrossSection(
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
            AnnularSectorCrossSection(
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
            AnnularSectorCrossSection(
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
            AnnularSectorCrossSection(
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
            AnnularSectorCrossSection(
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
        """Test the area property of the AnnularSectorCrossSection class at different angles.
        A full donut (0 to 360 degrees) should have an area of 0.
        a quarter donut (0 to 90 degrees) should have an area of pi * (outer_radius^2 - inner_radius^2) / 4.
        """
        annular_sector = AnnularSectorCrossSection(
            inner_radius=90.0,
            thickness=20.0,
            start_angle=start_angle,
            end_angle=end_angle,
            x=100.0,
            y=250.0,
        )
        assert annular_sector.area == pytest.approx(expected=expected_area, rel=1e-3)
