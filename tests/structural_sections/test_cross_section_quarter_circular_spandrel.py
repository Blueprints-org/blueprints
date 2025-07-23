"""Tests for right-angled triangular cross-section shapes with a quarter circle."""

import pytest

from blueprints.structural_sections.cross_section_quarter_circular_spandrel import QuarterCircularSpandrelCrossSection


class TestQuarterCircularSpandrelCrossSection:
    """Tests for the QuarterCircularSpandrelCrossSection class."""

    def test_polygon(self, qcs_cross_section: QuarterCircularSpandrelCrossSection) -> None:
        """Test the polygon property."""
        polygon = qcs_cross_section.polygon
        assert polygon.is_valid
        assert len(polygon.exterior.coords) > 0

    def test_geometry(self, qcs_cross_section: QuarterCircularSpandrelCrossSection) -> None:
        """Test the geometry property."""
        geometry = qcs_cross_section.geometry()
        assert geometry is not None

    def test_invalid_thickness_vertical(self) -> None:
        """Test initialization with an invalid vertical thickness."""
        with pytest.raises(ValueError, match="Thickness vertical must be positive"):
            QuarterCircularSpandrelCrossSection(
                thickness_vertical=0,
                thickness_horizontal=10,
                inner_radius=5,
                outer_radius=10,
            )

    def test_invalid_thickness_horizontal(self) -> None:
        """Test initialization with an invalid horizontal thickness."""
        with pytest.raises(ValueError, match="Thickness horizontal must be positive"):
            QuarterCircularSpandrelCrossSection(
                thickness_vertical=10,
                thickness_horizontal=0,
                inner_radius=5,
                outer_radius=10,
            )

    def test_invalid_inner_radius(self) -> None:
        """Test initialization with an invalid inner radius."""
        with pytest.raises(ValueError, match="Inner radius must be non-negative"):
            QuarterCircularSpandrelCrossSection(
                thickness_vertical=10,
                thickness_horizontal=10,
                inner_radius=-1,
                outer_radius=10,
            )

    def test_invalid_outer_radius(self) -> None:
        """Test initialization with an invalid outer radius."""
        with pytest.raises(ValueError, match="Outer radius must be non-negative"):
            QuarterCircularSpandrelCrossSection(
                thickness_vertical=10,
                thickness_horizontal=10,
                inner_radius=5,
                outer_radius=-1,
            )

    def test_invalid_outer_radius_greater_than_inner_plus_thickness(self) -> None:
        """Test initialization with an outer radius greater than inner radius plus thickness."""
        with pytest.raises(
            ValueError,
            match="Outer radius 20 must be smaller than or equal to inner radius 5 plus the thickness 10",
        ):
            QuarterCircularSpandrelCrossSection(
                thickness_vertical=10,
                thickness_horizontal=10,
                inner_radius=5,
                outer_radius=20,
            )
