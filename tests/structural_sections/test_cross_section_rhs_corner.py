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

    def test_section_properties(self, rhscf_corner_cross_section: RHSCFCornerCrossSection) -> None:
        """Test the section properties of the RHSCFCornerCrossSection class."""
        section_properties = rhscf_corner_cross_section.section_properties()
        assert section_properties.area == pytest.approx(expected=rhscf_corner_cross_section.area, rel=1e-2)
        assert section_properties.perimeter == pytest.approx(expected=rhscf_corner_cross_section.perimeter, rel=1e-2)
        assert section_properties.cx == pytest.approx(expected=rhscf_corner_cross_section.centroid.x, rel=1e-2)
        assert section_properties.cy == pytest.approx(expected=rhscf_corner_cross_section.centroid.y, rel=1e-2)
        assert section_properties.ixx_c == pytest.approx(expected=rhscf_corner_cross_section.moment_of_inertia_about_y, rel=1e-2)
        assert section_properties.iyy_c == pytest.approx(expected=rhscf_corner_cross_section.moment_of_inertia_about_z, rel=1e-2)
        assert section_properties.zxx_plus == pytest.approx(expected=rhscf_corner_cross_section.elastic_section_modulus_about_y_positive, rel=1e-2)
        assert section_properties.zyy_plus == pytest.approx(expected=rhscf_corner_cross_section.elastic_section_modulus_about_z_positive, rel=1e-2)
        assert section_properties.zxx_minus == pytest.approx(expected=rhscf_corner_cross_section.elastic_section_modulus_about_y_negative, rel=1e-2)
        assert section_properties.zyy_minus == pytest.approx(expected=rhscf_corner_cross_section.elastic_section_modulus_about_z_negative, rel=1e-2)
        assert section_properties.sxx == pytest.approx(expected=rhscf_corner_cross_section.plastic_section_modulus_about_y, rel=1e-2)
        assert section_properties.syy == pytest.approx(expected=rhscf_corner_cross_section.plastic_section_modulus_about_z, rel=1e-2)
