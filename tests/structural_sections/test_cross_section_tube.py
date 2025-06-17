"""Tests for circular tube cross-section shapes."""

import numpy as np
import pytest

from blueprints.structural_sections.cross_section_tube import TubeCrossSection


class TestTubeCrossSection:
    """Tests for the TubeCrossSection class."""

    def test_area(self, tube_cross_section: TubeCrossSection) -> None:
        """Test the area property of the TubeCrossSection class."""
        expected_area = np.pi * (50.0**2 - 25.0**2)
        assert tube_cross_section.area == pytest.approx(expected=expected_area, rel=1e-6)

    def test_perimeter(self, tube_cross_section: TubeCrossSection) -> None:
        """Test the perimeter property of the TubeCrossSection class."""
        expected_perimeter = 2 * np.pi * 50.0
        assert tube_cross_section.perimeter == pytest.approx(expected=expected_perimeter, rel=1e-6)

    def test_wall_thickness(self, tube_cross_section: TubeCrossSection) -> None:
        """Test the wall thickness property of the TubeCrossSection class."""
        expected_thickness = (100.0 - 50.0) / 2.0
        assert tube_cross_section.wall_thickness == pytest.approx(expected=expected_thickness, rel=1e-6)

    def test_centroid(self, tube_cross_section: TubeCrossSection) -> None:
        """Test the centroid property of the TubeCrossSection class."""
        centroid = tube_cross_section.centroid
        assert (centroid.x, centroid.y) == pytest.approx(expected=(100.0, 250.0), rel=1e-6)

    def test_moments_of_inertia(self, tube_cross_section: TubeCrossSection) -> None:
        """Test the moments of inertia properties of the TubeCrossSection class."""
        expected_inertia = (np.pi / 64) * (100.0**4 - 50.0**4)
        assert tube_cross_section.moment_of_inertia_about_y == pytest.approx(expected=expected_inertia, rel=1e-6)
        assert tube_cross_section.moment_of_inertia_about_z == pytest.approx(expected=expected_inertia, rel=1e-6)

    def test_section_moduli(self, tube_cross_section: TubeCrossSection) -> None:
        """Test the section moduli properties of the TubeCrossSection class."""
        expected_modulus = (np.pi / 64) * (100.0**4 - 50.0**4) / 50.0
        assert tube_cross_section.elastic_section_modulus_about_y_positive == pytest.approx(expected=expected_modulus, rel=1e-6)
        assert tube_cross_section.elastic_section_modulus_about_z_positive == pytest.approx(expected=expected_modulus, rel=1e-6)
        assert tube_cross_section.elastic_section_modulus_about_y_negative == pytest.approx(expected=expected_modulus, rel=1e-6)
        assert tube_cross_section.elastic_section_modulus_about_z_negative == pytest.approx(expected=expected_modulus, rel=1e-6)

    def test_plastic_section_moduli(self, tube_cross_section: TubeCrossSection) -> None:
        """Test the plastic section moduli properties of the TubeCrossSection class."""
        expected_plastic_modulus = (100.0**3 - 50.0**3) / 6
        assert tube_cross_section.plastic_section_modulus_about_y == pytest.approx(expected=expected_plastic_modulus, rel=1e-6)
        assert tube_cross_section.plastic_section_modulus_about_z == pytest.approx(expected=expected_plastic_modulus, rel=1e-6)

    def test_polygon(self, tube_cross_section: TubeCrossSection) -> None:
        """Test the geometry property of the TubeCrossSection class."""
        polygon = tube_cross_section.polygon
        assert polygon.is_valid
        assert polygon.area == pytest.approx(expected=tube_cross_section.area, rel=1e-3)

    def test_invalid_outer_diameter(self) -> None:
        """Test initialization with an invalid outer diameter value."""
        with pytest.raises(ValueError, match="Outer diameter must be a positive value"):
            TubeCrossSection(name="InvalidOuter", outer_diameter=-10.0, inner_diameter=5.0, x=0.0, y=0.0)

    def test_invalid_inner_diameter(self) -> None:
        """Test initialization with an invalid inner diameter value."""
        with pytest.raises(ValueError, match="Inner diameter cannot be negative"):
            TubeCrossSection(name="InvalidInner", outer_diameter=10.0, inner_diameter=-5.0, x=0.0, y=0.0)

    def test_inner_diameter_greater_than_outer(self) -> None:
        """Test initialization with inner diameter greater than or equal to outer diameter."""
        with pytest.raises(ValueError, match="Inner diameter must be smaller than outer diameter"):
            TubeCrossSection(name="InvalidDiameters", outer_diameter=9.0, inner_diameter=10.0, x=0.0, y=0.0)

    def test_geometry(self, tube_cross_section: TubeCrossSection) -> None:
        """Test the geometry property of the TubeCrossSection class."""
        geometry = tube_cross_section.geometry()
        assert geometry is not None

    def test_section_properties(self, tube_cross_section: TubeCrossSection) -> None:
        """Test the section properties of the TubeCrossSection class."""
        section_properties = tube_cross_section.section_properties()
        assert section_properties.area == pytest.approx(expected=tube_cross_section.area, rel=1e-2)
        assert section_properties.perimeter == pytest.approx(expected=tube_cross_section.perimeter, rel=1e-2)
        assert section_properties.cx == pytest.approx(expected=tube_cross_section.centroid.x, rel=1e-2)
        assert section_properties.cy == pytest.approx(expected=tube_cross_section.centroid.y, rel=1e-2)
        assert section_properties.ixx_c == pytest.approx(expected=tube_cross_section.moment_of_inertia_about_y, rel=1e-2)
        assert section_properties.iyy_c == pytest.approx(expected=tube_cross_section.moment_of_inertia_about_z, rel=1e-2)
        assert section_properties.zxx_plus == pytest.approx(expected=tube_cross_section.elastic_section_modulus_about_y_positive, rel=1e-2)
        assert section_properties.zyy_plus == pytest.approx(expected=tube_cross_section.elastic_section_modulus_about_z_positive, rel=1e-2)
        assert section_properties.zxx_minus == pytest.approx(expected=tube_cross_section.elastic_section_modulus_about_y_negative, rel=1e-2)
        assert section_properties.zyy_minus == pytest.approx(expected=tube_cross_section.elastic_section_modulus_about_z_negative, rel=1e-2)
        assert section_properties.sxx == pytest.approx(expected=tube_cross_section.plastic_section_modulus_about_y, rel=1e-2)
        assert section_properties.syy == pytest.approx(expected=tube_cross_section.plastic_section_modulus_about_z, rel=1e-2)
