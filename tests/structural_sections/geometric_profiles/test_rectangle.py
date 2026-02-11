"""Tests for rectangular shapes."""

import pytest
from sectionproperties.analysis import Section
from sectionproperties.post.post import SectionProperties

from blueprints.structural_sections.geometric_profiles.rectangle import RectangularProfile


class TestRectangularProfile:
    """Tests for the RectangularProfile class."""

    def test_area(self, rectangular_profile: RectangularProfile) -> None:
        """Test the area property of the RectangularProfile class."""
        assert rectangular_profile.area == pytest.approx(expected=20000.0, rel=1e-6)

    def test_invalid_width(self) -> None:
        """Test that an error is raised for invalid width."""
        with pytest.raises(ValueError, match="Width must be a positive value"):
            RectangularProfile(name="InvalidWidth", width=-10.0, height=200.0)

    def test_invalid_height(self) -> None:
        """Test that an error is raised for invalid height."""
        with pytest.raises(ValueError, match="Height must be a positive value"):
            RectangularProfile(name="InvalidHeight", width=100.0, height=-200.0)

    def test_polygon(self, rectangular_profile: RectangularProfile) -> None:
        """Test the geometry property of the RectangularProfile class."""
        polygon = rectangular_profile.polygon
        assert polygon.bounds == pytest.approx(expected=(50.0, 150.0, 150.0, 350.0), rel=1e-6)

    def test_section_properties_geometric(self, rectangular_profile_section_properties: SectionProperties) -> None:
        """Test the section properties of the RectangularProfile class."""
        assert rectangular_profile_section_properties.area == pytest.approx(expected=20000.0, rel=1e-6)
        assert rectangular_profile_section_properties.perimeter == pytest.approx(expected=600.0, rel=1e-6)
        assert rectangular_profile_section_properties.ixx_g == pytest.approx(expected=1316666666.6, rel=1e-6)

    def test_section_properties_plastic(self, rectangular_profile_section_properties: SectionProperties) -> None:
        """Test the section properties of the RectangularProfile class."""
        assert rectangular_profile_section_properties.syy == pytest.approx(expected=500000.0, rel=1e-6)
        assert rectangular_profile_section_properties.sxx == pytest.approx(expected=1000000.0, rel=1e-6)

    def test_section(self, rectangular_profile: RectangularProfile) -> None:
        """Test the geometry property of the RectangularProfile class."""
        section = rectangular_profile._section()  # noqa: SLF001
        assert isinstance(section, Section)

    def test_geometry(self, rectangular_profile: RectangularProfile) -> None:
        """Test the geometry property of the RectangularProfile class."""
        geometry = rectangular_profile._geometry()  # noqa: SLF001
        assert geometry is not None

    def test_mesh_settings(self, rectangular_profile: RectangularProfile) -> None:
        """Test the mesh_settings property of the RectangularProfile class."""
        mesh_settings = rectangular_profile.mesh_settings
        assert isinstance(mesh_settings, dict)
        assert "mesh_sizes" in mesh_settings

    def test_no_plotter_defined(self, rectangular_profile: RectangularProfile) -> None:
        """Test that accessing the plotter property raises an AttributeError if no plotter is defined."""
        with pytest.raises(AttributeError, match=r"No plotter is defined."):
            _ = rectangular_profile.plotter

    def test_immutability(self, rectangular_profile: RectangularProfile) -> None:
        """Test that the RectangularProfile dataclass is immutable."""
        with pytest.raises(AttributeError):
            rectangular_profile.name = "New Name"  # type: ignore[misc]

    def test_transform(self, rectangular_profile: RectangularProfile) -> None:
        """Test the transform method of the RectangularProfile class."""
        transformed_profile = rectangular_profile.transform(horizontal_offset=10.0, vertical_offset=20.0, rotation=90.0)
        assert isinstance(transformed_profile, RectangularProfile)
        assert pytest.approx(transformed_profile.centroid.x, rel=1e-6) == rectangular_profile.centroid.x + 10.0
        assert pytest.approx(transformed_profile.centroid.y, rel=1e-6) == rectangular_profile.centroid.y + 20.0
        assert pytest.approx(transformed_profile.profile_height, rel=1e-6) == rectangular_profile.profile_width

    def test_max_thickness(self, rectangular_profile: RectangularProfile) -> None:
        """Test the max_thickness property of the RectangularProfile class."""
        expected_max_thickness = min(rectangular_profile.width, rectangular_profile.height)
        assert rectangular_profile.max_thickness == pytest.approx(expected=expected_max_thickness, rel=1e-6)
