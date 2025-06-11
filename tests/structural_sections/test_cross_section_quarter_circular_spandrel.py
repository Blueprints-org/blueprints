"""Tests for right-angled triangular cross-section shapes with a quarter circle."""

import numpy as np
import pytest
from shapely.geometry import Point

from blueprints.structural_sections.cross_section_quarter_circular_spandrel import QuarterCircularSpandrelCrossSection


class TestQuarterCircularSpandrelCrossSection:
    """Tests for the QuarterCircularSpandrelCrossSection class."""

    def test_area(self, qcs_cross_section: QuarterCircularSpandrelCrossSection) -> None:
        """Test the area property of the QuarterCircularSpandrelCrossSection class."""
        expected_area = 50.0**2 - (np.pi * 50.0**2 / 4)
        assert qcs_cross_section.area == pytest.approx(expected=expected_area, rel=1e-6)

    def test_perimeter(self, qcs_cross_section: QuarterCircularSpandrelCrossSection) -> None:
        """Test the perimeter property of the QuarterCircularSpandrelCrossSection class."""
        expected_perimeter = 2 * 50.0 + (np.pi * 50.0 / 2)
        assert qcs_cross_section.perimeter == pytest.approx(expected=expected_perimeter, rel=1e-6)

    def test_centroid(self, qcs_cross_section: QuarterCircularSpandrelCrossSection) -> None:
        """Test the centroid property of the QuarterCircularSpandrelCrossSection class."""
        expected_centroid = Point(111.1683969472876, 261.1683969472876)
        assert qcs_cross_section.centroid == pytest.approx(expected=expected_centroid, rel=1e-6)

    def test_moments_of_inertia(self, qcs_cross_section: QuarterCircularSpandrelCrossSection) -> None:
        """Test the moments of inertia properties of the QuarterCircularSpandrelCrossSection class."""
        expected_inertia = (9 * np.pi**2 - 84 * np.pi + 176) / (144 * (4 - np.pi)) * 50**4

        assert qcs_cross_section.moment_of_inertia_about_y == pytest.approx(expected=expected_inertia, rel=1e-6)
        assert qcs_cross_section.moment_of_inertia_about_z == pytest.approx(expected=expected_inertia, rel=1e-6)

    def test_section_moduli(self, qcs_cross_section: QuarterCircularSpandrelCrossSection) -> None:
        """Test the section moduli properties of the QuarterCircularSpandrelCrossSection class."""
        expected_modulus_positive = qcs_cross_section.moment_of_inertia_about_y / (
            qcs_cross_section.radius - qcs_cross_section.centroid.y + qcs_cross_section.y
        )
        expected_modulus_negative = qcs_cross_section.moment_of_inertia_about_y / (qcs_cross_section.centroid.y - qcs_cross_section.y)
        assert qcs_cross_section.elastic_section_modulus_about_y_positive == pytest.approx(expected=expected_modulus_positive, rel=1e-6)
        assert qcs_cross_section.elastic_section_modulus_about_y_negative == pytest.approx(expected=expected_modulus_negative, rel=1e-6)
        assert qcs_cross_section.elastic_section_modulus_about_z_positive == pytest.approx(expected=expected_modulus_positive, rel=1e-6)
        assert qcs_cross_section.elastic_section_modulus_about_z_negative == pytest.approx(expected=expected_modulus_negative, rel=1e-6)

    def test_plastic_section_moduli(self, qcs_cross_section: QuarterCircularSpandrelCrossSection) -> None:
        """Test the plastic section moduli properties of the QuarterCircularSpandrelCrossSection class."""
        expected_plastic_modulus = (50.0**3) / 31.6851045070407
        assert qcs_cross_section.plastic_section_modulus_about_y == pytest.approx(expected=expected_plastic_modulus, rel=1e-6)
        assert qcs_cross_section.plastic_section_modulus_about_z == pytest.approx(expected=expected_plastic_modulus, rel=1e-6)

    def test_polygon(self, qcs_cross_section: QuarterCircularSpandrelCrossSection) -> None:
        """Test the geometry property of the QuarterCircularSpandrelCrossSection class."""
        polygon = qcs_cross_section.polygon
        assert polygon.is_valid
        assert polygon.area == pytest.approx(expected=qcs_cross_section.area, rel=1e-2)

    def test_mirrored_geometry(self) -> None:
        """Test the geometry property for flipped cross-sections."""
        # Test flipped horizontally
        qcs_cross_section = QuarterCircularSpandrelCrossSection(radius=50.0, x=0.0, y=0.0)
        qcs_cross_section_mirrored_horizontally = QuarterCircularSpandrelCrossSection(radius=50.0, x=0.0, y=0.0, mirrored_horizontally=True)
        assert qcs_cross_section_mirrored_horizontally.polygon.centroid.x == pytest.approx(expected=-qcs_cross_section.polygon.centroid.x, rel=1e-3)
        assert qcs_cross_section_mirrored_horizontally.area == pytest.approx(expected=qcs_cross_section.area, rel=1e-3)
        assert qcs_cross_section_mirrored_horizontally.centroid.x == pytest.approx(expected=-qcs_cross_section.centroid.x, rel=1e-3)
        assert qcs_cross_section_mirrored_horizontally.centroid.y == pytest.approx(expected=qcs_cross_section.centroid.y, rel=1e-3)

        # Test flipped vertically
        qcs_cross_section_mirrored_vertically = QuarterCircularSpandrelCrossSection(radius=50.0, x=0.0, y=0.0, mirrored_vertically=True)
        assert qcs_cross_section_mirrored_vertically.polygon.centroid.y == pytest.approx(expected=-qcs_cross_section.polygon.centroid.y, rel=1e-3)
        assert qcs_cross_section_mirrored_vertically.area == pytest.approx(expected=qcs_cross_section.area, rel=1e-3)
        assert qcs_cross_section_mirrored_vertically.centroid.x == pytest.approx(expected=qcs_cross_section.centroid.x, rel=1e-3)
        assert qcs_cross_section_mirrored_vertically.centroid.y == pytest.approx(expected=-qcs_cross_section.centroid.y, rel=1e-3)

        # Test flipped both horizontally and vertically
        qcs_cross_section_mirrored_both = QuarterCircularSpandrelCrossSection(
            radius=50.0, x=0.0, y=0.0, mirrored_horizontally=True, mirrored_vertically=True
        )
        assert qcs_cross_section_mirrored_both.polygon.centroid.x == pytest.approx(expected=-qcs_cross_section.polygon.centroid.x, rel=1e-3)
        assert qcs_cross_section_mirrored_both.polygon.centroid.y == pytest.approx(expected=-qcs_cross_section.polygon.centroid.y, rel=1e-3)
        assert qcs_cross_section_mirrored_both.area == pytest.approx(expected=qcs_cross_section.area, rel=1e-3)
        assert qcs_cross_section_mirrored_both.centroid.x == pytest.approx(expected=-qcs_cross_section.centroid.x, rel=1e-3)
        assert qcs_cross_section_mirrored_both.centroid.y == pytest.approx(expected=-qcs_cross_section.centroid.y, rel=1e-3)

    def test_radius_is_zero(self) -> None:
        """Test the behavior when radius is zero."""
        qcs_cross_section_zero_radius = QuarterCircularSpandrelCrossSection(radius=0.0, x=0.0, y=0.0)
        assert qcs_cross_section_zero_radius.area == 0.0
        assert qcs_cross_section_zero_radius.perimeter == 0.0
        assert qcs_cross_section_zero_radius.moment_of_inertia_about_y == 0.0
        assert qcs_cross_section_zero_radius.moment_of_inertia_about_z == 0.0
        assert qcs_cross_section_zero_radius.elastic_section_modulus_about_y_positive == 0.0

    def test_section_properties(self, qcs_cross_section: QuarterCircularSpandrelCrossSection) -> None:
        """Test the section properties of the RectangularCrossSection class."""
        section_properties = qcs_cross_section.section_properties()
        assert section_properties.area == pytest.approx(expected=qcs_cross_section.area, rel=1e-2)
        assert section_properties.perimeter == pytest.approx(expected=qcs_cross_section.perimeter, rel=1e-2)
        assert section_properties.cx == pytest.approx(expected=qcs_cross_section.centroid.x, rel=1e-2)
        assert section_properties.cy == pytest.approx(expected=qcs_cross_section.centroid.y, rel=1e-2)
        assert section_properties.ixx_c == pytest.approx(expected=qcs_cross_section.moment_of_inertia_about_y, rel=1e-2)
        assert section_properties.iyy_c == pytest.approx(expected=qcs_cross_section.moment_of_inertia_about_z, rel=1e-2)
        assert section_properties.zxx_plus == pytest.approx(expected=qcs_cross_section.elastic_section_modulus_about_y_positive, rel=1e-2)
        assert section_properties.zyy_plus == pytest.approx(expected=qcs_cross_section.elastic_section_modulus_about_z_positive, rel=1e-2)
        assert section_properties.zxx_minus == pytest.approx(expected=qcs_cross_section.elastic_section_modulus_about_y_negative, rel=1e-2)
        assert section_properties.zyy_minus == pytest.approx(expected=qcs_cross_section.elastic_section_modulus_about_z_negative, rel=1e-2)
        assert section_properties.sxx == pytest.approx(expected=qcs_cross_section.plastic_section_modulus_about_y, rel=1e-2)
        assert section_properties.syy == pytest.approx(expected=qcs_cross_section.plastic_section_modulus_about_z, rel=1e-2)
