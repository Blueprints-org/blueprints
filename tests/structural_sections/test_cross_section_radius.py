"""Tests for right-angled triangular cross-section shapes with a quarter circle."""

import math

import numpy as np
import pytest
from shapely.geometry import Point

from blueprints.structural_sections.cross_section_radius import RightAngleCurvedCrossSection


class TestRightAngleCurvedCrossSection:
    """Tests for the RightAngleCurvedCrossSection class."""

    @pytest.fixture
    def cross_section(self) -> RightAngleCurvedCrossSection:
        """Return a RightAngleCurvedCrossSection instance."""
        return RightAngleCurvedCrossSection(radius=50.0, x=100.0, y=250.0)

    def test_area(self, cross_section: RightAngleCurvedCrossSection) -> None:
        """Test the area property of the RightAngleCurvedCrossSection class."""
        expected_area = 50.0**2 - (np.pi * 50.0**2 / 4)
        assert cross_section.area == pytest.approx(expected=expected_area, rel=1e-6)

    def test_perimeter(self, cross_section: RightAngleCurvedCrossSection) -> None:
        """Test the perimeter property of the RightAngleCurvedCrossSection class."""
        expected_perimeter = 2 * 50.0 + (np.pi * 50.0 / 2)
        assert cross_section.perimeter == pytest.approx(expected=expected_perimeter, rel=1e-6)

    def test_plate_thickness(self, cross_section: RightAngleCurvedCrossSection) -> None:
        """Test the plate thickness property of the RightAngleCurvedCrossSection class."""
        expected_thickness = 50.0
        assert cross_section.plate_thickness == pytest.approx(expected=expected_thickness, rel=1e-6)

    def test_centroid(self, cross_section: RightAngleCurvedCrossSection) -> None:
        """Test the centroid property of the RightAngleCurvedCrossSection class."""
        centroid = cross_section.centroid
        assert isinstance(centroid, Point)

    def test_moments_of_inertia(self, cross_section: RightAngleCurvedCrossSection) -> None:
        """Test the moments of inertia properties of the RightAngleCurvedCrossSection class."""
        inertia_square = cross_section.radius**4 / 12
        area_square = cross_section.radius**2
        cog_square_to_reference_point = cross_section.radius / 2

        inertia_quarter_circle = math.pi * cross_section.radius**4 / 64
        area_quarter_circle = math.pi * cross_section.radius**2 / 4
        cog_quarter_circle_to_reference_point = cross_section.radius - 4 * cross_section.radius / 3 / np.pi

        inertia_reference_point_square = inertia_square + area_square * cog_square_to_reference_point**2
        inertia_about_reference_point_quarter_circle = inertia_quarter_circle + area_quarter_circle * cog_quarter_circle_to_reference_point**2
        expected_inertia_reference_point = inertia_reference_point_square - inertia_about_reference_point_quarter_circle

        expected_inertia = expected_inertia_reference_point - (area_square - area_quarter_circle) * (cross_section.centroid.y - cross_section.y) ** 2

        assert cross_section.moment_of_inertia_about_y == pytest.approx(expected=expected_inertia, rel=1e-6)
        assert cross_section.moment_of_inertia_about_z == pytest.approx(expected=expected_inertia, rel=1e-6)

    def test_section_moduli(self, cross_section: RightAngleCurvedCrossSection) -> None:
        """Test the section moduli properties of the RightAngleCurvedCrossSection class."""
        expected_modulus_positive = cross_section.moment_of_inertia_about_y / (cross_section.radius - cross_section.centroid.y + cross_section.y)
        expected_modulus_negative = cross_section.moment_of_inertia_about_y / (cross_section.centroid.y - cross_section.y)
        assert cross_section.elastic_section_modulus_about_y_positive == pytest.approx(expected=expected_modulus_positive, rel=1e-6)
        assert cross_section.elastic_section_modulus_about_y_negative == pytest.approx(expected=expected_modulus_negative, rel=1e-6)
        assert cross_section.elastic_section_modulus_about_z_positive == pytest.approx(expected=expected_modulus_positive, rel=1e-6)
        assert cross_section.elastic_section_modulus_about_z_negative == pytest.approx(expected=expected_modulus_negative, rel=1e-6)

    def test_plastic_section_moduli(self, cross_section: RightAngleCurvedCrossSection) -> None:
        """Test the plastic section moduli properties of the RightAngleCurvedCrossSection class."""
        expected_plastic_modulus = (50.0**3) / 30.73
        assert cross_section.plastic_section_modulus_about_y == pytest.approx(expected=expected_plastic_modulus, rel=1e-6)
        assert cross_section.plastic_section_modulus_about_z == pytest.approx(expected=expected_plastic_modulus, rel=1e-6)

    def test_geometry(self, cross_section: RightAngleCurvedCrossSection) -> None:
        """Test the geometry property of the RightAngleCurvedCrossSection class."""
        geometry = cross_section.geometry
        assert geometry.is_valid
        assert geometry.area == pytest.approx(expected=cross_section.area, rel=1e-3)

    def test_flipped_geometry(self) -> None:
        """Test the geometry property for flipped cross-sections."""
        # Test flipped horizontally
        cross_section = RightAngleCurvedCrossSection(radius=50.0, x=0.0, y=0.0)
        cross_section_flipped_horizontally = RightAngleCurvedCrossSection(radius=50.0, x=0.0, y=0.0, flipped_horizontally=True)
        assert cross_section_flipped_horizontally.geometry.centroid.x == pytest.approx(expected=-cross_section.geometry.centroid.x, rel=1e-3)
        assert cross_section_flipped_horizontally.area == pytest.approx(expected=cross_section.area, rel=1e-3)
        assert cross_section_flipped_horizontally.centroid.x == pytest.approx(expected=-cross_section.centroid.x, rel=1e-3)
        assert cross_section_flipped_horizontally.centroid.y == pytest.approx(expected=cross_section.centroid.y, rel=1e-3)

        # Test flipped vertically
        cross_section_flipped_vertically = RightAngleCurvedCrossSection(radius=50.0, x=0.0, y=0.0, flipped_vertically=True)
        assert cross_section_flipped_vertically.geometry.centroid.y == pytest.approx(expected=-cross_section.geometry.centroid.y, rel=1e-3)
        assert cross_section_flipped_vertically.area == pytest.approx(expected=cross_section.area, rel=1e-3)
        assert cross_section_flipped_vertically.centroid.x == pytest.approx(expected=cross_section.centroid.x, rel=1e-3)
        assert cross_section_flipped_vertically.centroid.y == pytest.approx(expected=-cross_section.centroid.y, rel=1e-3)

        # Test flipped both horizontally and vertically
        cross_section_flipped_both = RightAngleCurvedCrossSection(radius=50.0, x=0.0, y=0.0, flipped_horizontally=True, flipped_vertically=True)
        assert cross_section_flipped_both.geometry.centroid.x == pytest.approx(expected=-cross_section.geometry.centroid.x, rel=1e-3)
        assert cross_section_flipped_both.geometry.centroid.y == pytest.approx(expected=-cross_section.geometry.centroid.y, rel=1e-3)
        assert cross_section_flipped_both.area == pytest.approx(expected=cross_section.area, rel=1e-3)
        assert cross_section_flipped_both.centroid.x == pytest.approx(expected=-cross_section.centroid.x, rel=1e-3)
        assert cross_section_flipped_both.centroid.y == pytest.approx(expected=-cross_section.centroid.y, rel=1e-3)

    def test_radius_is_zero(self) -> None:
        """Test the behavior when radius is zero."""
        cross_section_zero_radius = RightAngleCurvedCrossSection(radius=0.0, x=0.0, y=0.0)
        assert cross_section_zero_radius.area == 0.0
        assert cross_section_zero_radius.perimeter == 0.0
        assert cross_section_zero_radius.moment_of_inertia_about_y == 0.0
        assert cross_section_zero_radius.moment_of_inertia_about_z == 0.0
        assert cross_section_zero_radius.elastic_section_modulus_about_y_positive == 0.0
