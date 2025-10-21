"""Tests for the MeshCreator class and cross-section base functionality."""

from sectionproperties.pre import Geometry
from shapely import Polygon

from blueprints.structural_sections._cross_section import MeshCreator


class TestMeshCreator:
    """Tests for the MeshCreator class."""

    def test_init_required_parameter_only(self) -> None:
        """Test MeshCreator initialization with only required parameter."""
        mesh_creator = MeshCreator(mesh_sizes=2.0)

        assert mesh_creator.mesh_settings == {"mesh_sizes": 2.0}

    def test_init_with_optional_parameters(self) -> None:
        """Test MeshCreator initialization with optional parameters."""
        mesh_creator = MeshCreator(mesh_sizes=1.5, min_angle=30.0, coarse=True)

        expected_settings = {"mesh_sizes": 1.5, "min_angle": 30.0, "coarse": True}
        assert mesh_creator.mesh_settings == expected_settings

    def test_init_with_none_values_excluded(self) -> None:
        """Test that None values are excluded from mesh_settings."""
        mesh_creator = MeshCreator(mesh_sizes=2.5, min_angle=None, coarse=False)

        expected_settings = {"mesh_sizes": 2.5, "coarse": False}
        assert mesh_creator.mesh_settings == expected_settings

    def test_init_with_kwargs(self) -> None:
        """Test MeshCreator initialization with additional kwargs."""
        mesh_creator = MeshCreator(mesh_sizes=3.0, min_angle=25.0, custom_param="test_value", another_param=42)

        expected_settings = {"mesh_sizes": 3.0, "min_angle": 25.0, "custom_param": "test_value", "another_param": 42}
        assert mesh_creator.mesh_settings == expected_settings

    def test_mesh_settings_property(self) -> None:
        """Test the mesh_settings property returns correct dictionary."""
        mesh_creator = MeshCreator(mesh_sizes=1.0, min_angle=20.0)

        settings = mesh_creator.mesh_settings
        assert isinstance(settings, dict)
        assert settings["mesh_sizes"] == 1.0
        assert settings["min_angle"] == 20.0

    def test_call_with_geometry(self) -> None:
        """Test calling MeshCreator on a geometry object."""
        # Create a simple square polygon for testing
        square = Polygon([(0, 0), (10, 0), (10, 10), (0, 10)])
        geometry = Geometry(geom=square)

        mesh_creator = MeshCreator(mesh_sizes=2.0)
        result = mesh_creator(geometry)

        assert isinstance(result, Geometry)
        # The result should be a meshed geometry
        assert result is not None

    def test_call_with_geometry_custom_settings(self) -> None:
        """Test calling MeshCreator with custom mesh settings."""
        # Create a simple triangle for testing
        triangle = Polygon([(0, 0), (5, 0), (2.5, 5)])
        geometry = Geometry(geom=triangle)

        mesh_creator = MeshCreator(mesh_sizes=1.5, min_angle=30.0, coarse=False)
        result = mesh_creator(geometry)

        assert isinstance(result, Geometry)
        assert result is not None

    def test_mesh_creator_modifiable_settings(self) -> None:
        """Test that mesh_settings returns the internal dictionary which can not be modified."""
        mesh_creator = MeshCreator(mesh_sizes=2.0, min_angle=30.0)
        original_count = len(mesh_creator.mesh_settings)

        # Modifying the returned dict should not affect internal state
        returned_settings = mesh_creator.mesh_settings
        returned_settings["new_key"] = "new_value"

        # Internal state should not be modified
        assert len(mesh_creator.mesh_settings) == original_count
        assert "new_key" not in mesh_creator.mesh_settings

    def test_none_kwargs_filtered_out(self) -> None:
        """Test that kwargs with None values are filtered out."""
        mesh_creator = MeshCreator(mesh_sizes=1.0, min_angle=25.0, coarse=None, extra_param=None, valid_param="test")

        expected_settings = {"mesh_sizes": 1.0, "min_angle": 25.0, "valid_param": "test"}
        assert mesh_creator.mesh_settings == expected_settings
