"""Tests for cross-section shapes."""

import numpy as np
import pytest
from shapely.geometry import Point

from blueprints.structural_sections.cross_section_annular_sector import AnnularSectorCrossSection


class TestAnnularSectorCrossSection:
    """Tests for the AnnularSectorCrossSection class."""

    @pytest.fixture
    def annular_sector_cross_section(self) -> AnnularSectorCrossSection:
        """Return an AnnularSectorCrossSection instance."""
        return AnnularSectorCrossSection(
            name="AnnularSector",
            inner_radius=90.0,
            thickness=20.0,
            start_angle=0.0,
            end_angle=90.0,
            x=0.0,
            y=0.0,
        )

    def test_area(self, annular_sector_cross_section: AnnularSectorCrossSection) -> None:
        """Test the area property of the AnnularSectorCrossSection class."""
        expected_area = 0.5 * (90.0 * (np.pi / 180)) * ((110.0**2) - (90.0**2))
        assert annular_sector_cross_section.area == pytest.approx(expected=expected_area, rel=1e-6)

    def test_perimeter(self, annular_sector_cross_section: AnnularSectorCrossSection) -> None:
        """Test the perimeter property of the AnnularSectorCrossSection class."""
        angle_radians = 90.0 * (np.pi / 180)
        expected_perimeter = angle_radians * (110.0 + 90.0) + 2 * 20.0
        assert annular_sector_cross_section.perimeter == pytest.approx(expected=expected_perimeter, rel=1e-6)

    def test_centroid(self, annular_sector_cross_section: AnnularSectorCrossSection) -> None:
        """Test the centroid property of the AnnularSectorCrossSection class."""
        centroid = annular_sector_cross_section.centroid
        assert isinstance(centroid, Point)

    def test_moments_of_inertia(self, annular_sector_cross_section: AnnularSectorCrossSection) -> None:
        """Test the moments of inertia properties of the AnnularSectorCrossSection class."""
        assert annular_sector_cross_section.moment_of_inertia_about_y > 0
        assert annular_sector_cross_section.moment_of_inertia_about_z > 0

    def test_section_moduli(self, annular_sector_cross_section: AnnularSectorCrossSection) -> None:
        """Test the section moduli properties of the AnnularSectorCrossSection class."""
        assert annular_sector_cross_section.elastic_section_modulus_about_y_positive > 0
        assert annular_sector_cross_section.elastic_section_modulus_about_z_positive > 0
        assert annular_sector_cross_section.elastic_section_modulus_about_y_negative > 0
        assert annular_sector_cross_section.elastic_section_modulus_about_z_negative > 0

    def test_polar_moment_of_inertia(self, annular_sector_cross_section: AnnularSectorCrossSection) -> None:
        """Test the polar moment of inertia property of the AnnularSectorCrossSection class."""
        assert annular_sector_cross_section.polar_moment_of_inertia > 0

    def test_plastic_section_moduli(self, annular_sector_cross_section: AnnularSectorCrossSection) -> None:
        """Test the plastic section moduli properties of the AnnularSectorCrossSection class."""
        assert annular_sector_cross_section.plastic_section_modulus_about_y > 0
        assert annular_sector_cross_section.plastic_section_modulus_about_z > 0

    def test_dotted_mesh(self, annular_sector_cross_section: AnnularSectorCrossSection) -> None:
        """Test the dotted mesh property of the AnnularSectorCrossSection class."""
        dotted_mesh = annular_sector_cross_section.dotted_mesh()
        assert len(dotted_mesh) > 0

    def test_geometry(self, annular_sector_cross_section: AnnularSectorCrossSection) -> None:
        """Test the geometry property of the AnnularSectorCrossSection class."""
        geometry = annular_sector_cross_section.geometry
        assert geometry.is_valid
        assert len(geometry.exterior.coords) > 0

    def test_plate_thickness(self, annular_sector_cross_section: AnnularSectorCrossSection) -> None:
        """Test the plate thickness property of the AnnularSectorCrossSection class."""
        assert annular_sector_cross_section.plate_thickness == pytest.approx(expected=20.0, rel=1e-6)

    def test_vertices(self, annular_sector_cross_section: AnnularSectorCrossSection) -> None:
        """Test the vertices property of the AnnularSectorCrossSection class."""
        vertices = annular_sector_cross_section.vertices
        assert len(vertices) > 0

    def test_dotted_mesh_with_custom_mesh_size(self, annular_sector_cross_section: AnnularSectorCrossSection) -> None:
        """Test the dotted mesh property with a custom mesh size."""
        dotted_mesh = annular_sector_cross_section.dotted_mesh(max_mesh_size=10.0)
        assert len(dotted_mesh) > 0
        for point in dotted_mesh:
            assert annular_sector_cross_section.geometry.contains(point)

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

    """Test initialization with an invalid start angle value."""
    with pytest.raises(ValueError, match="Start angle must be between -360 and 360 degrees"):
        AnnularSectorCrossSection(
            name="InvalidStartAngle",
            inner_radius=100.0,
            thickness=20.0,
            start_angle=400.0,
            end_angle=450.0,
            x=0.0,
            y=0.0,
        )

    def test_invalid_end_angle(self) -> None:
        """Test initialization with an invalid end angle value."""
        with pytest.raises(ValueError, match="End angle must be larger than start angle and not more than 360 degrees more"):
            AnnularSectorCrossSection(
                name="InvalidEndAngle",
                inner_radius=100.0,
                thickness=20.0,
                start_angle=0.0,
                end_angle=400.0,
                x=0.0,
                y=0.0,
            )
