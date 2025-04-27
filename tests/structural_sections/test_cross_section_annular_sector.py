"""Tests for cross-section shapes."""

import math

import numpy as np
import pytest
from sectionproperties.analysis import Section

from blueprints.structural_sections.cross_section_annular_sector import AnnularSectorCrossSection


class TestAnnularSectorCrossSection:
    """Tests for the AnnularSectorCrossSection class."""

    def test_area(self, annular_sector_cross_section: AnnularSectorCrossSection) -> None:
        """Test the area property of the AnnularSectorCrossSection class."""
        expected_area = (annular_sector_cross_section.outer_radius**2 - annular_sector_cross_section.inner_radius**2) * np.pi / 4
        assert annular_sector_cross_section.area == pytest.approx(expected=expected_area, rel=1e-6)

    def test_width(self, annular_sector_cross_section: AnnularSectorCrossSection) -> None:
        """Test the width property of the AnnularSectorCrossSection class."""
        expected_width = 110.0
        assert annular_sector_cross_section.width == pytest.approx(expected=expected_width, rel=1e-6)

    def test_height(self, annular_sector_cross_section: AnnularSectorCrossSection) -> None:
        """Test the height property of the AnnularSectorCrossSection class."""
        expected_height = 110.0
        assert annular_sector_cross_section.height == pytest.approx(expected=expected_height, rel=1e-6)

    def test_perimeter(self, annular_sector_cross_section: AnnularSectorCrossSection) -> None:
        """Test the perimeter property of the AnnularSectorCrossSection class."""
        angle_radians = 90.0 * (np.pi / 180)
        expected_perimeter = angle_radians * (110.0 + 90.0) + 2 * 20.0
        assert annular_sector_cross_section.perimeter == pytest.approx(expected=expected_perimeter, rel=1e-6)

    def test_centroid(self, annular_sector_cross_section: AnnularSectorCrossSection) -> None:
        """Test the centroid property of the AnnularSectorCrossSection class."""
        centroid = annular_sector_cross_section.centroid
        halve_angle_radians = np.radians(annular_sector_cross_section.end_angle - annular_sector_cross_section.start_angle) / 2
        centroid_radius = (2 * np.sin(halve_angle_radians) / (3 * halve_angle_radians)) * (
            (annular_sector_cross_section.outer_radius**3 - annular_sector_cross_section.inner_radius**3)
            / (annular_sector_cross_section.outer_radius**2 - annular_sector_cross_section.inner_radius**2)
        )
        centroid_angle = np.radians((annular_sector_cross_section.start_angle + annular_sector_cross_section.end_angle) / 2)
        centroid_x = annular_sector_cross_section.x + centroid_radius * np.cos(np.radians(90) - centroid_angle)
        centroid_y = annular_sector_cross_section.y + centroid_radius * np.sin(np.radians(90) - centroid_angle)
        assert centroid.x == pytest.approx(expected=centroid_x, rel=1e-6)
        assert centroid.y == pytest.approx(expected=centroid_y, rel=1e-6)

    def test_moments_of_inertia(self, annular_sector_cross_section: AnnularSectorCrossSection) -> None:
        """Test the moments of inertia properties of the AnnularSectorCrossSection class."""
        assert annular_sector_cross_section.moment_of_inertia_about_y == annular_sector_cross_section.moment_of_inertia_about_z

    def test_section_moduli(self, annular_sector_cross_section: AnnularSectorCrossSection) -> None:
        """Test the section moduli properties of the AnnularSectorCrossSection class."""
        assert annular_sector_cross_section.elastic_section_modulus_about_y_positive == pytest.approx(
            expected=annular_sector_cross_section.elastic_section_modulus_about_z_positive, rel=1e-6
        )
        assert annular_sector_cross_section.elastic_section_modulus_about_y_negative == pytest.approx(
            expected=annular_sector_cross_section.elastic_section_modulus_about_z_negative, rel=1e-6
        )

    def test_plastic_section_moduli(self, annular_sector_cross_section: AnnularSectorCrossSection) -> None:
        """Test the plastic section moduli properties of the AnnularSectorCrossSection class."""
        assert annular_sector_cross_section.plastic_section_modulus_about_y is None
        assert annular_sector_cross_section.plastic_section_modulus_about_z is None

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
        assert annular_sector.area == pytest.approx(expected=expected_area, rel=1e-6)

    def test_moments_of_inertia_approximation_with_rectangle(self) -> None:
        """Test the moments of inertia by approximating the annular sector with a rectangle."""
        annular_sector = AnnularSectorCrossSection(
            inner_radius=1000,  # mm
            thickness=0.1,  # mm
            start_angle=-2,  # degrees
            end_angle=2,  # degrees
            x=0,  # mm
            y=0,  # mm
        )
        # Approximate the moments of inertia using a rectangle
        angle_radians = math.radians(annular_sector.end_angle - annular_sector.start_angle)
        approximate_width = angle_radians * annular_sector.radius_centerline
        approximate_height = annular_sector.thickness

        # Moment of inertia about the z-axis
        approximate_moi_z = (approximate_height * approximate_width**3) / 12
        assert annular_sector.moment_of_inertia_about_z == pytest.approx(expected=approximate_moi_z, rel=1e-3)

        annular_sector = AnnularSectorCrossSection(
            inner_radius=1000,  # mm
            thickness=0.1,  # mm
            start_angle=88,  # degrees
            end_angle=92,  # degrees
            x=0,  # mm
            y=0,  # mm
        )
        # Approximate the moments of inertia using a rectangle
        angle_radians = math.radians(annular_sector.end_angle - annular_sector.start_angle)
        approximate_width = annular_sector.thickness
        approximate_height = angle_radians * annular_sector.radius_centerline

        # Moment of inertia about the z-axis
        approximate_moi_y = (approximate_height**3 * approximate_width) / 12
        assert annular_sector.moment_of_inertia_about_y == pytest.approx(expected=approximate_moi_y, rel=1e-3)

    def test_section_properties(self, annular_sector_cross_section: AnnularSectorCrossSection) -> None:
        """Test the section properties of the HexagonalCrossSection class."""
        section_properties = annular_sector_cross_section.section_properties()
        assert section_properties.area == pytest.approx(expected=annular_sector_cross_section.area, rel=1e-2)
        assert section_properties.perimeter == pytest.approx(expected=annular_sector_cross_section.perimeter, rel=1e-2)
        assert section_properties.cx == pytest.approx(expected=annular_sector_cross_section.centroid.x, rel=1e-2)
        assert section_properties.cy == pytest.approx(expected=annular_sector_cross_section.centroid.y, rel=1e-2)
        assert section_properties.ixx_c == pytest.approx(expected=annular_sector_cross_section.moment_of_inertia_about_y, rel=1e-2)
        assert section_properties.iyy_c == pytest.approx(expected=annular_sector_cross_section.moment_of_inertia_about_z, rel=1e-2)
        assert section_properties.zxx_plus == pytest.approx(expected=annular_sector_cross_section.elastic_section_modulus_about_y_positive, rel=1e-2)
        assert section_properties.zyy_plus == pytest.approx(expected=annular_sector_cross_section.elastic_section_modulus_about_z_positive, rel=1e-2)
        assert section_properties.zxx_minus == pytest.approx(expected=annular_sector_cross_section.elastic_section_modulus_about_y_negative, rel=1e-2)
        assert section_properties.zyy_minus == pytest.approx(expected=annular_sector_cross_section.elastic_section_modulus_about_z_negative, rel=1e-2)

    def test_section_properties_359_degrees(self, annular_sector_cross_section_359_degrees: AnnularSectorCrossSection) -> None:
        """Test the section properties of the HexagonalCrossSection class with 359 degrees."""
        section_properties = annular_sector_cross_section_359_degrees.section_properties()
        assert section_properties.area == pytest.approx(expected=annular_sector_cross_section_359_degrees.area, rel=1e-2)
        assert section_properties.perimeter == pytest.approx(expected=annular_sector_cross_section_359_degrees.perimeter, rel=1e-2)
        assert section_properties.cx == pytest.approx(expected=annular_sector_cross_section_359_degrees.centroid.x, rel=1e-2)
        assert section_properties.cy == pytest.approx(expected=annular_sector_cross_section_359_degrees.centroid.y, rel=1e-2)
        assert section_properties.ixx_c == pytest.approx(expected=annular_sector_cross_section_359_degrees.moment_of_inertia_about_y, rel=1e-2)
        assert section_properties.iyy_c == pytest.approx(expected=annular_sector_cross_section_359_degrees.moment_of_inertia_about_z, rel=1e-2)
        assert section_properties.zxx_plus == pytest.approx(
            expected=annular_sector_cross_section_359_degrees.elastic_section_modulus_about_y_positive, rel=1e-2
        )
        assert section_properties.zyy_plus == pytest.approx(
            expected=annular_sector_cross_section_359_degrees.elastic_section_modulus_about_z_positive, rel=1e-2
        )
        assert section_properties.zxx_minus == pytest.approx(
            expected=annular_sector_cross_section_359_degrees.elastic_section_modulus_about_y_negative, rel=1e-2
        )
        assert section_properties.zyy_minus == pytest.approx(
            expected=annular_sector_cross_section_359_degrees.elastic_section_modulus_about_z_negative, rel=1e-2
        )
