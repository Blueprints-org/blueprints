"""Tests for RHSCF Corner cross-section."""

import pytest

from blueprints.structural_sections.cross_section_rhs_corner import RHSCFCornerCrossSection


class TestRHSCFCornerCrossSection:
    """Tests for the RHSCFCornerCrossSection class."""

    def test_polygon(self, rhscf_corner_cross_section: RHSCFCornerCrossSection) -> None:
        """Test the polygon property."""
        polygon = rhscf_corner_cross_section.polygon
        assert polygon.is_valid
        assert len(polygon.exterior.coords) > 0

    def test_geometry(self, rhscf_corner_cross_section: RHSCFCornerCrossSection) -> None:
        """Test the geometry property."""
        geometry = rhscf_corner_cross_section.geometry()
        assert geometry is not None

    def test_invalid_thickness_vertical(self) -> None:
        """Test initialization with an invalid vertical thickness."""
        with pytest.raises(ValueError, match="Thickness vertical must be positive"):
            RHSCFCornerCrossSection(
                thickness_vertical=0,
                thickness_horizontal=10,
                inner_radius=5,
                outer_radius=10,
            )

    def test_invalid_thickness_horizontal(self) -> None:
        """Test initialization with an invalid horizontal thickness."""
        with pytest.raises(ValueError, match="Thickness horizontal must be positive"):
            RHSCFCornerCrossSection(
                thickness_vertical=10,
                thickness_horizontal=0,
                inner_radius=5,
                outer_radius=10,
            )

    def test_invalid_inner_radius(self) -> None:
        """Test initialization with an invalid inner radius."""
        with pytest.raises(ValueError, match="Inner radius must be positive"):
            RHSCFCornerCrossSection(
                thickness_vertical=10,
                thickness_horizontal=10,
                inner_radius=-1,
                outer_radius=10,
            )

    def test_invalid_outer_radius(self) -> None:
        """Test initialization with an invalid outer radius."""
        with pytest.raises(ValueError, match="Outer radius must be positive"):
            RHSCFCornerCrossSection(
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
            RHSCFCornerCrossSection(
                thickness_vertical=10,
                thickness_horizontal=10,
                inner_radius=5,
                outer_radius=20,
            )
