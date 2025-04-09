"""Tests for circular tube cross-section shapes."""

import numpy as np
import pytest

from blueprints.structural_sections.cross_section_tube import TubeCrossSection


class TestTubeCrossSection:
    """Tests for the TubeCrossSection class."""

    @pytest.fixture
    def tube_cross_section(self) -> TubeCrossSection:
        """Return a TubeCrossSection instance."""
        return TubeCrossSection(name="Tube", outer_diameter=100.0, inner_diameter=50.0, x=100.0, y=250.0)

    def test_area(self, tube_cross_section: TubeCrossSection) -> None:
        """Test the area property of the TubeCrossSection class."""
        expected_area = np.pi * (50.0**2 - 25.0**2)
        assert tube_cross_section.area == pytest.approx(expected=expected_area, rel=1e-6)

    def test_perimeter(self, tube_cross_section: TubeCrossSection) -> None:
        """Test the perimeter property of the TubeCrossSection class."""
        expected_perimeter = 2 * np.pi * (50.0 + 25.0)
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

    def test_geometry(self, tube_cross_section: TubeCrossSection) -> None:
        """Test the geometry property of the TubeCrossSection class."""
        geometry = tube_cross_section.geometry
        assert geometry.is_valid
        assert geometry.area == pytest.approx(expected=tube_cross_section.area, rel=1e-4)

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
            TubeCrossSection(name="InvalidDiameters", outer_diameter=10.0, inner_diameter=10.0, x=0.0, y=0.0)
