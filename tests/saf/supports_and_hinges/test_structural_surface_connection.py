"""Tests for StructuralSurfaceConnection class."""

import pytest

from blueprints.saf import StructuralSurfaceConnection


class TestStructuralSurfaceConnectionValidInitialization:
    """Test valid initialization of StructuralSurfaceConnection."""

    def test_basic_surface_connection(self) -> None:
        """Test basic surface connection with required parameters."""
        connection = StructuralSurfaceConnection(
            name="Sn6",
            two_d_member="S13",
            subsoil="Gravel",
            c1x=80.5,
            c1y=35.5,
            c1z=50.0,
            c2x=15.5,
            c2y=10.2,
        )
        assert connection.name == "Sn6"
        assert connection.two_d_member == "S13"
        assert connection.subsoil == "Gravel"
        assert connection.c1x == 80.5

    def test_surface_connection_with_all_optional_fields(self) -> None:
        """Test surface connection with all optional fields."""
        connection = StructuralSurfaceConnection(
            name="Sn6",
            two_d_member="S13",
            subsoil="Gravel",
            c1x=80.5,
            c1y=35.5,
            c1z=50.0,
            c2x=15.5,
            c2y=10.2,
            two_d_member_region="R1",
            description="Sandy gravel",
            c1z_spring="Linear",
            parent_id="parent-uuid",
            id="uuid-1234",
        )
        assert connection.two_d_member_region == "R1"
        assert connection.description == "Sandy gravel"
        assert connection.id == "uuid-1234"

    def test_surface_connection_loam_subsoil(self) -> None:
        """Test surface connection with loam subsoil."""
        connection = StructuralSurfaceConnection(
            name="Sn7",
            two_d_member="S14",
            subsoil="Loam",
            c1x=50.0,
            c1y=45.0,
            c1z=40.0,
            c2x=12.0,
            c2y=9.5,
        )
        assert connection.subsoil == "Loam"

    def test_surface_connection_sandy_subsoil(self) -> None:
        """Test surface connection with sandy subsoil."""
        connection = StructuralSurfaceConnection(
            name="Sn8",
            two_d_member="S15",
            subsoil="Sand",
            c1x=60.0,
            c1y=55.0,
            c1z=45.0,
            c2x=14.0,
            c2y=11.0,
        )
        assert connection.subsoil == "Sand"

    def test_surface_connection_clay_subsoil(self) -> None:
        """Test surface connection with clay subsoil."""
        connection = StructuralSurfaceConnection(
            name="Sn9",
            two_d_member="S16",
            subsoil="Clay",
            c1x=70.0,
            c1y=65.0,
            c1z=55.0,
            c2x=16.0,
            c2y=13.0,
        )
        assert connection.subsoil == "Clay"

    def test_surface_connection_with_region(self) -> None:
        """Test surface connection with member region."""
        connection = StructuralSurfaceConnection(
            name="Sn10",
            two_d_member="S13",
            two_d_member_region="R1",
            subsoil="Gravel",
            c1x=80.5,
            c1y=35.5,
            c1z=50.0,
            c2x=15.5,
            c2y=10.2,
        )
        assert connection.two_d_member_region == "R1"

    def test_surface_connection_with_description(self) -> None:
        """Test surface connection with description."""
        connection = StructuralSurfaceConnection(
            name="Sn11",
            two_d_member="S17",
            subsoil="Gravel",
            c1x=80.5,
            c1y=35.5,
            c1z=50.0,
            c2x=15.5,
            c2y=10.2,
            description="Medium dense sandy gravel",
        )
        assert connection.description == "Medium dense sandy gravel"

    def test_surface_connection_with_parent_id(self) -> None:
        """Test surface connection with parent ID."""
        connection = StructuralSurfaceConnection(
            name="Sn12",
            two_d_member="S18",
            subsoil="Gravel",
            c1x=80.5,
            c1y=35.5,
            c1z=50.0,
            c2x=15.5,
            c2y=10.2,
            parent_id="parent-abc123",
        )
        assert connection.parent_id == "parent-abc123"

    def test_surface_connection_zero_stiffness(self) -> None:
        """Test surface connection with zero stiffness values."""
        connection = StructuralSurfaceConnection(
            name="Sn13",
            two_d_member="S19",
            subsoil="Gravel",
            c1x=0.0,
            c1y=0.0,
            c1z=0.0,
            c2x=0.0,
            c2y=0.0,
        )
        assert connection.c1x == 0.0

    def test_surface_connection_large_stiffness(self) -> None:
        """Test surface connection with large stiffness values."""
        connection = StructuralSurfaceConnection(
            name="Sn14",
            two_d_member="S20",
            subsoil="Rock",
            c1x=1000.0,
            c1y=1000.0,
            c1z=1200.0,
            c2x=500.0,
            c2y=500.0,
        )
        assert connection.c1x == 1000.0

    def test_surface_connection_decimal_stiffness(self) -> None:
        """Test surface connection with decimal stiffness values."""
        connection = StructuralSurfaceConnection(
            name="Sn15",
            two_d_member="S21",
            subsoil="Gravel",
            c1x=80.123,
            c1y=35.456,
            c1z=50.789,
            c2x=15.234,
            c2y=10.567,
        )
        assert connection.c1x == 80.123

    def test_surface_connection_negative_stiffness(self) -> None:
        """Test surface connection with negative stiffness (edge case)."""
        connection = StructuralSurfaceConnection(
            name="Sn16",
            two_d_member="S22",
            subsoil="Gravel",
            c1x=-10.0,
            c1y=-5.0,
            c1z=-8.0,
            c2x=-2.0,
            c2y=-1.5,
        )
        assert connection.c1x == -10.0


class TestStructuralSurfaceConnectionImmutability:
    """Test immutability of StructuralSurfaceConnection."""

    def test_frozen_dataclass(self) -> None:
        """Test that instances are frozen and immutable."""
        connection = StructuralSurfaceConnection(
            name="Sn6",
            two_d_member="S13",
            subsoil="Gravel",
            c1x=80.5,
            c1y=35.5,
            c1z=50.0,
            c2x=15.5,
            c2y=10.2,
        )
        with pytest.raises(AttributeError):
            connection.name = "Sn7"  # type: ignore[misc]

    def test_hash_support(self) -> None:
        """Test that frozen instances are hashable."""
        connection1 = StructuralSurfaceConnection(
            name="Sn6",
            two_d_member="S13",
            subsoil="Gravel",
            c1x=80.5,
            c1y=35.5,
            c1z=50.0,
            c2x=15.5,
            c2y=10.2,
        )
        connection_dict = {connection1: "first"}
        assert connection_dict[connection1] == "first"


class TestStructuralSurfaceConnectionEquality:
    """Test equality of StructuralSurfaceConnection."""

    def test_equal_instances(self) -> None:
        """Test that identical instances are equal."""
        conn1 = StructuralSurfaceConnection(
            name="Sn6",
            two_d_member="S13",
            subsoil="Gravel",
            c1x=80.5,
            c1y=35.5,
            c1z=50.0,
            c2x=15.5,
            c2y=10.2,
        )
        conn2 = StructuralSurfaceConnection(
            name="Sn6",
            two_d_member="S13",
            subsoil="Gravel",
            c1x=80.5,
            c1y=35.5,
            c1z=50.0,
            c2x=15.5,
            c2y=10.2,
        )
        assert conn1 == conn2

    def test_unequal_instances_different_name(self) -> None:
        """Test that instances with different names are not equal."""
        conn1 = StructuralSurfaceConnection(
            name="Sn6",
            two_d_member="S13",
            subsoil="Gravel",
            c1x=80.5,
            c1y=35.5,
            c1z=50.0,
            c2x=15.5,
            c2y=10.2,
        )
        conn2 = StructuralSurfaceConnection(
            name="Sn7",
            two_d_member="S13",
            subsoil="Gravel",
            c1x=80.5,
            c1y=35.5,
            c1z=50.0,
            c2x=15.5,
            c2y=10.2,
        )
        assert conn1 != conn2

    def test_unequal_instances_different_stiffness(self) -> None:
        """Test that instances with different stiffness are not equal."""
        conn1 = StructuralSurfaceConnection(
            name="Sn6",
            two_d_member="S13",
            subsoil="Gravel",
            c1x=80.5,
            c1y=35.5,
            c1z=50.0,
            c2x=15.5,
            c2y=10.2,
        )
        conn2 = StructuralSurfaceConnection(
            name="Sn6",
            two_d_member="S13",
            subsoil="Gravel",
            c1x=90.0,
            c1y=35.5,
            c1z=50.0,
            c2x=15.5,
            c2y=10.2,
        )
        assert conn1 != conn2


class TestStructuralSurfaceConnectionEdgeCases:
    """Test edge cases and special scenarios."""

    def test_empty_optional_description(self) -> None:
        """Test that empty description is default."""
        connection = StructuralSurfaceConnection(
            name="Sn6",
            two_d_member="S13",
            subsoil="Gravel",
            c1x=80.5,
            c1y=35.5,
            c1z=50.0,
            c2x=15.5,
            c2y=10.2,
        )
        assert connection.description == ""

    def test_empty_optional_id(self) -> None:
        """Test that empty id is default."""
        connection = StructuralSurfaceConnection(
            name="Sn6",
            two_d_member="S13",
            subsoil="Gravel",
            c1x=80.5,
            c1y=35.5,
            c1z=50.0,
            c2x=15.5,
            c2y=10.2,
        )
        assert connection.id == ""

    def test_very_small_stiffness(self) -> None:
        """Test with very small stiffness values."""
        connection = StructuralSurfaceConnection(
            name="Sn6",
            two_d_member="S13",
            subsoil="Soft clay",
            c1x=0.001,
            c1y=0.001,
            c1z=0.005,
            c2x=0.0001,
            c2y=0.0001,
        )
        assert connection.c1x == 0.001

    def test_mixed_stiffness_values(self) -> None:
        """Test with mixed stiffness values (high and low)."""
        connection = StructuralSurfaceConnection(
            name="Sn6",
            two_d_member="S13",
            subsoil="Gravel",
            c1x=800.5,
            c1y=3.5,
            c1z=50.0,
            c2x=150.5,
            c2y=1.2,
        )
        assert connection.c1x == 800.5
        assert connection.c1y == 3.5

    def test_different_members(self) -> None:
        """Test surface connections with different members."""
        conn1 = StructuralSurfaceConnection(
            name="Sn1",
            two_d_member="S1",
            subsoil="Gravel",
            c1x=80.5,
            c1y=35.5,
            c1z=50.0,
            c2x=15.5,
            c2y=10.2,
        )
        conn2 = StructuralSurfaceConnection(
            name="Sn2",
            two_d_member="S2",
            subsoil="Gravel",
            c1x=80.5,
            c1y=35.5,
            c1z=50.0,
            c2x=15.5,
            c2y=10.2,
        )
        assert conn1.two_d_member != conn2.two_d_member

    def test_scientific_notation_stiffness(self) -> None:
        """Test with stiffness values in scientific notation."""
        connection = StructuralSurfaceConnection(
            name="Sn6",
            two_d_member="S13",
            subsoil="Gravel",
            c1x=1e2,
            c1y=3.5e1,
            c1z=5e1,
            c2x=1.55e1,
            c2y=1.02e1,
        )
        assert connection.c1x == 100.0
        assert connection.c2y == 10.2
