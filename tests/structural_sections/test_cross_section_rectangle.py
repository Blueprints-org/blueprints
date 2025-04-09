"""Tests for cross-section shapes."""

import pytest

from blueprints.structural_sections.cross_section_rectangle import RectangularCrossSection


class TestRectangularCrossSection:
    """Tests for the RectangularCrossSection class."""

    @pytest.fixture
    def rectangular_cross_section(self) -> RectangularCrossSection:
        """Return a RectangularCrossSection instance."""
        return RectangularCrossSection(name="Rectangle", width=100.0, height=200.0, x=100.0, y=250.0)

    def test_area(self, rectangular_cross_section: RectangularCrossSection) -> None:
        """Test the area property of the RectangularCrossSection class."""
        assert rectangular_cross_section.area == pytest.approx(expected=20000.0, rel=1e-6)

    def test_perimeter(self, rectangular_cross_section: RectangularCrossSection) -> None:
        """Test the perimeter property of the RectangularCrossSection class."""
        assert rectangular_cross_section.perimeter == pytest.approx(expected=600.0, rel=1e-6)

    def test_centroid(self, rectangular_cross_section: RectangularCrossSection) -> None:
        """Test the centroid property of the RectangularCrossSection class."""
        centroid = rectangular_cross_section.centroid
        assert (centroid.x, centroid.y) == pytest.approx(expected=(100.0, 250.0), rel=1e-6)

    def test_moments_of_inertia(self, rectangular_cross_section: RectangularCrossSection) -> None:
        """Test the moments of inertia properties of the RectangularCrossSection class."""
        expected_y = 1 / 12 * 100 * 200**3
        expected_z = 1 / 12 * 200 * 100**3
        assert rectangular_cross_section.moment_of_inertia_about_y == pytest.approx(expected=expected_y, rel=1e-6)
        assert rectangular_cross_section.moment_of_inertia_about_z == pytest.approx(expected=expected_z, rel=1e-6)

    def test_section_moduli(self, rectangular_cross_section: RectangularCrossSection) -> None:
        """Test the section moduli properties of the RectangularCrossSection class."""
        expected_y_positive = 1 / 6 * 100 * 200**2
        expected_z_positive = 1 / 6 * 200 * 100**2
        expected_y_negative = 1 / 6 * 100 * 200**2
        expected_z_negative = 1 / 6 * 200 * 100**2
        assert rectangular_cross_section.elastic_section_modulus_about_y_positive == pytest.approx(expected=expected_y_positive, rel=1e-6)
        assert rectangular_cross_section.elastic_section_modulus_about_z_positive == pytest.approx(expected=expected_z_positive, rel=1e-6)
        assert rectangular_cross_section.elastic_section_modulus_about_y_negative == pytest.approx(expected=expected_y_negative, rel=1e-6)
        assert rectangular_cross_section.elastic_section_modulus_about_z_negative == pytest.approx(expected=expected_z_negative, rel=1e-6)

    def test_plastic_section_moduli(self, rectangular_cross_section: RectangularCrossSection) -> None:
        """Test the plastic section moduli properties of the RectangularCrossSection class."""
        expected_y = 1 / 4 * 100 * 200**2
        expected_z = 1 / 4 * 200 * 100**2
        assert rectangular_cross_section.plastic_section_modulus_about_y == pytest.approx(expected=expected_y, rel=1e-6)
        assert rectangular_cross_section.plastic_section_modulus_about_z == pytest.approx(expected=expected_z, rel=1e-6)

    def test_invalid_width(self) -> None:
        """Test that an error is raised for invalid width."""
        with pytest.raises(ValueError, match="Width must be a positive value"):
            RectangularCrossSection(name="InvalidWidth", width=-10.0, height=200.0)

    def test_invalid_height(self) -> None:
        """Test that an error is raised for invalid height."""
        with pytest.raises(ValueError, match="Height must be a positive value"):
            RectangularCrossSection(name="InvalidHeight", width=100.0, height=-200.0)

    def test_geometry(self, rectangular_cross_section: RectangularCrossSection) -> None:
        """Test the geometry property of the RectangularCrossSection class."""
        geometry = rectangular_cross_section.geometry
        assert geometry.bounds == pytest.approx(expected=(50.0, 150.0, 150.0, 350.0), rel=1e-6)

    def test_plate_thickness(self, rectangular_cross_section: RectangularCrossSection) -> None:
        """Test the plate_thickness property of the RectangularCrossSection class."""
        assert rectangular_cross_section.plate_thickness == pytest.approx(expected=100.0, rel=1e-6)
