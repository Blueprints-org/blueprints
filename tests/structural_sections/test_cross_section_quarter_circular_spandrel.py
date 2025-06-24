"""Tests for right-angled triangular cross-section shapes with a quarter circle."""

import numpy as np
import pytest

from blueprints.structural_sections.cross_section_quarter_circular_spandrel import QuarterCircularSpandrelCrossSection


class TestQuarterCircularSpandrelCrossSection:
    """Tests for the QuarterCircularSpandrelCrossSection class."""

    def test_area(self, qcs_cross_section: QuarterCircularSpandrelCrossSection) -> None:
        """Test the area property of the QuarterCircularSpandrelCrossSection class."""
        expected_area = 50.0**2 - (np.pi * 50.0**2 / 4)
        assert qcs_cross_section.area == pytest.approx(expected=expected_area, rel=1e-3)

    def test_polygon(self, qcs_cross_section: QuarterCircularSpandrelCrossSection) -> None:
        """Test the geometry property of the QuarterCircularSpandrelCrossSection class."""
        polygon = qcs_cross_section.polygon
        assert polygon.is_valid
        assert polygon.area == pytest.approx(expected=qcs_cross_section.area, rel=1e-3)

    def test_mirrored_geometry(self) -> None:
        """Test the geometry property for flipped cross-sections."""
        # Test flipped horizontally
        qcs_cross_section = QuarterCircularSpandrelCrossSection(radius=50.0, x=0.0, y=0.0)
        qcs_cross_section_mirrored_horizontally = QuarterCircularSpandrelCrossSection(radius=50.0, x=0.0, y=0.0, mirrored_horizontally=True)
        assert qcs_cross_section_mirrored_horizontally.polygon.centroid.x == pytest.approx(expected=-qcs_cross_section.polygon.centroid.x, rel=1e-3)
        assert qcs_cross_section_mirrored_horizontally.area == pytest.approx(expected=qcs_cross_section.area, rel=1e-3)

        # Test flipped vertically
        qcs_cross_section_mirrored_vertically = QuarterCircularSpandrelCrossSection(radius=50.0, x=0.0, y=0.0, mirrored_vertically=True)
        assert qcs_cross_section_mirrored_vertically.polygon.centroid.y == pytest.approx(expected=-qcs_cross_section.polygon.centroid.y, rel=1e-3)
        assert qcs_cross_section_mirrored_vertically.area == pytest.approx(expected=qcs_cross_section.area, rel=1e-3)

        # Test flipped both horizontally and vertically
        qcs_cross_section_mirrored_both = QuarterCircularSpandrelCrossSection(
            radius=50.0, x=0.0, y=0.0, mirrored_horizontally=True, mirrored_vertically=True
        )
        assert qcs_cross_section_mirrored_both.polygon.centroid.x == pytest.approx(expected=-qcs_cross_section.polygon.centroid.x, rel=1e-3)
        assert qcs_cross_section_mirrored_both.polygon.centroid.y == pytest.approx(expected=-qcs_cross_section.polygon.centroid.y, rel=1e-3)
        assert qcs_cross_section_mirrored_both.area == pytest.approx(expected=qcs_cross_section.area, rel=1e-3)

    def test_radius_is_zero(self) -> None:
        """Test the behavior when radius is zero."""
        qcs_cross_section_zero_radius = QuarterCircularSpandrelCrossSection(radius=0.0, x=0.0, y=0.0)
        assert qcs_cross_section_zero_radius.area == 0.0
