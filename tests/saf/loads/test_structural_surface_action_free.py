"""Tests for StructuralSurfaceActionFree class."""

import pytest

from blueprints.saf import StructuralSurfaceActionFree
from blueprints.saf.loads.structural_surface_action_free import (
    CoordinateSystem,
    Direction,
    Distribution,
    Edge,
    Location,
)


class TestStructuralSurfaceActionFreeValidInitialization:
    """Test valid initialization of StructuralSurfaceActionFree."""

    def test_uniform_load_basic(self) -> None:
        """Test basic uniform surface load with minimum attributes."""
        load = StructuralSurfaceActionFree(
            name="FF1",
            direction=Direction.Z,
            distribution=Distribution.UNIFORM,
            load_case="LC1",
            coordinate_x="0.0;5.0;5.0;0.0",
            coordinate_y="0.0;0.0;3.0;3.0",
            coordinate_z="0.0;0.0;0.0;0.0",
            edges="Line;Line;Line;Line",
            coordinate_system=CoordinateSystem.GLOBAL,
            location=Location.LENGTH,
            q="-10",
        )
        assert load.name == "FF1"
        assert load.direction == Direction.Z
        assert load.distribution == Distribution.UNIFORM
        assert load.load_case == "LC1"
        assert load.q == "-10"

    def test_uniform_load_with_optional_fields(self) -> None:
        """Test uniform load with all optional fields specified."""
        load = StructuralSurfaceActionFree(
            name="FF1",
            direction=Direction.Z,
            distribution=Distribution.UNIFORM,
            load_case="LC1",
            coordinate_x="0.0;5.0;5.0;0.0",
            coordinate_y="0.0;0.0;3.0;3.0",
            coordinate_z="0.0;0.0;0.0;0.0",
            edges="Line;Line;Line;Line",
            coordinate_system=CoordinateSystem.GLOBAL,
            location=Location.LENGTH,
            q="-10",
            action_type="Wind",
            id="uuid-1234",
        )
        assert load.action_type == "Wind"
        assert load.id == "uuid-1234"

    def test_direction_x_load(self) -> None:
        """Test DirectionX load with two corner values."""
        load = StructuralSurfaceActionFree(
            name="FF2",
            direction=Direction.X,
            distribution=Distribution.DIRECTION_X,
            load_case="LC1",
            coordinate_x="0.0;5.0;5.0;0.0",
            coordinate_y="0.0;0.0;3.0;3.0",
            coordinate_z="0.0;0.0;0.0;0.0",
            edges="Line;Line;Line;Line",
            coordinate_system=CoordinateSystem.GLOBAL,
            location=Location.LENGTH,
            q="C1:-5;C2:-7",
        )
        assert load.direction == Direction.X
        assert load.distribution == Distribution.DIRECTION_X
        assert load.q == "C1:-5;C2:-7"

    def test_direction_y_load(self) -> None:
        """Test DirectionY load with two corner values."""
        load = StructuralSurfaceActionFree(
            name="FF3",
            direction=Direction.Y,
            distribution=Distribution.DIRECTION_Y,
            load_case="LC1",
            coordinate_x="0.0;5.0;5.0;0.0",
            coordinate_y="0.0;0.0;3.0;3.0",
            coordinate_z="0.0;0.0;0.0;0.0",
            edges="Line;Line;Line;Line",
            coordinate_system=CoordinateSystem.GLOBAL,
            location=Location.LENGTH,
            q="C1:-2;C2:-4",
        )
        assert load.direction == Direction.Y
        assert load.distribution == Distribution.DIRECTION_Y

    def test_direction_xy_load(self) -> None:
        """Test DirectionXY load with three corner values."""
        load = StructuralSurfaceActionFree(
            name="FF4",
            direction=Direction.Z,
            distribution=Distribution.DIRECTION_XY,
            load_case="LC1",
            coordinate_x="0.0;5.0;5.0;0.0",
            coordinate_y="0.0;0.0;3.0;3.0",
            coordinate_z="0.0;0.0;0.0;0.0",
            edges="Line;Line;Line;Line",
            coordinate_system=CoordinateSystem.GLOBAL,
            location=Location.LENGTH,
            q="C1:-3;C2:-2;C3:-1",
        )
        assert load.distribution == Distribution.DIRECTION_XY
        assert load.q == "C1:-3;C2:-2;C3:-1"

    def test_local_coordinate_system(self) -> None:
        """Test load with local coordinate system."""
        load = StructuralSurfaceActionFree(
            name="FF5",
            direction=Direction.Z,
            distribution=Distribution.UNIFORM,
            load_case="LC1",
            coordinate_x="0.0;5.0;5.0;0.0",
            coordinate_y="0.0;0.0;3.0;3.0",
            coordinate_z="0.0;0.0;0.0;0.0",
            edges="Line;Line;Line;Line",
            coordinate_system=CoordinateSystem.LOCAL,
            location=Location.LENGTH,
            q="-10",
        )
        assert load.coordinate_system == CoordinateSystem.LOCAL

    def test_projection_location(self) -> None:
        """Test load with projection location."""
        load = StructuralSurfaceActionFree(
            name="FF6",
            direction=Direction.Z,
            distribution=Distribution.UNIFORM,
            load_case="LC1",
            coordinate_x="0.0;5.0;5.0;0.0",
            coordinate_y="0.0;0.0;3.0;3.0",
            coordinate_z="0.0;0.0;0.0;0.0",
            edges="Line;Line;Line;Line",
            coordinate_system=CoordinateSystem.GLOBAL,
            location=Location.PROJECTION,
            q="-10",
        )
        assert load.location == Location.PROJECTION

    def test_bezier_edge(self) -> None:
        """Test load with Bezier curve edges."""
        load = StructuralSurfaceActionFree(
            name="FF7",
            direction=Direction.Z,
            distribution=Distribution.UNIFORM,
            load_case="LC1",
            coordinate_x="0.0;5.0;5.0;0.0",
            coordinate_y="0.0;1.0;3.0;2.0",
            coordinate_z="0.0;0.0;0.0;0.0",
            edges="Line;Bezier;Line;Bezier",
            coordinate_system=CoordinateSystem.GLOBAL,
            location=Location.LENGTH,
            q="-10",
        )
        assert load.edges == "Line;Bezier;Line;Bezier"

    def test_circle_arc_edge(self) -> None:
        """Test load with circular arc edges."""
        load = StructuralSurfaceActionFree(
            name="FF8",
            direction=Direction.Z,
            distribution=Distribution.UNIFORM,
            load_case="LC1",
            coordinate_x="0.0;5.0;5.0;0.0",
            coordinate_y="0.0;1.0;3.0;2.0",
            coordinate_z="0.0;0.0;0.0;0.0",
            edges="Circle arc;Line;Circle arc;Line",
            coordinate_system=CoordinateSystem.GLOBAL,
            location=Location.LENGTH,
            q="-10",
        )
        assert load.edges == "Circle arc;Line;Circle arc;Line"

    def test_parabolic_arc_edge(self) -> None:
        """Test load with parabolic arc edges."""
        load = StructuralSurfaceActionFree(
            name="FF9",
            direction=Direction.Z,
            distribution=Distribution.UNIFORM,
            load_case="LC1",
            coordinate_x="0.0;5.0;5.0;0.0",
            coordinate_y="0.0;1.0;3.0;2.0",
            coordinate_z="0.0;0.0;0.0;0.0",
            edges="Line;Parabolic arc;Line;Parabolic arc",
            coordinate_system=CoordinateSystem.GLOBAL,
            location=Location.LENGTH,
            q="-10",
        )
        assert "Parabolic arc" in load.edges

    def test_spline_edge(self) -> None:
        """Test load with spline edges."""
        load = StructuralSurfaceActionFree(
            name="FF10",
            direction=Direction.Z,
            distribution=Distribution.UNIFORM,
            load_case="LC1",
            coordinate_x="0.0;2.5;5.0;5.0;0.0",
            coordinate_y="0.0;1.0;1.0;3.0;3.0",
            coordinate_z="0.0;0.0;0.0;0.0;0.0",
            edges="Line;Spline;Spline;Line;Line",
            coordinate_system=CoordinateSystem.GLOBAL,
            location=Location.LENGTH,
            q="-10",
        )
        assert "Spline" in load.edges

    def test_positive_load_value(self) -> None:
        """Test load with positive magnitude."""
        load = StructuralSurfaceActionFree(
            name="FF11",
            direction=Direction.Z,
            distribution=Distribution.UNIFORM,
            load_case="LC1",
            coordinate_x="0.0;5.0;5.0;0.0",
            coordinate_y="0.0;0.0;3.0;3.0",
            coordinate_z="0.0;0.0;0.0;0.0",
            edges="Line;Line;Line;Line",
            coordinate_system=CoordinateSystem.GLOBAL,
            location=Location.LENGTH,
            q="15",
        )
        assert load.q == "15"

    def test_zero_load_value(self) -> None:
        """Test load with zero magnitude."""
        load = StructuralSurfaceActionFree(
            name="FF12",
            direction=Direction.Z,
            distribution=Distribution.UNIFORM,
            load_case="LC1",
            coordinate_x="0.0;5.0;5.0;0.0",
            coordinate_y="0.0;0.0;3.0;3.0",
            coordinate_z="0.0;0.0;0.0;0.0",
            edges="Line;Line;Line;Line",
            coordinate_system=CoordinateSystem.GLOBAL,
            location=Location.LENGTH,
            q="0",
        )
        assert load.q == "0"


class TestStructuralSurfaceActionFreeValidation:
    """Test validation of StructuralSurfaceActionFree."""

    def test_uniform_with_corner_notation_raises_error(self) -> None:
        """Test that Uniform distribution with corner notation raises ValueError."""
        with pytest.raises(
            ValueError,
            match="q must be a single numeric value for Uniform distribution",
        ):
            StructuralSurfaceActionFree(
                name="FF1",
                direction=Direction.Z,
                distribution=Distribution.UNIFORM,
                load_case="LC1",
                coordinate_x="0.0;5.0;5.0;0.0",
                coordinate_y="0.0;0.0;3.0;3.0",
                coordinate_z="0.0;0.0;0.0;0.0",
                edges="Line;Line;Line;Line",
                coordinate_system=CoordinateSystem.GLOBAL,
                location=Location.LENGTH,
                q="C1:-10",
            )

    def test_direction_x_with_one_corner_raises_error(self) -> None:
        """Test that DirectionX with only one corner value raises ValueError."""
        with pytest.raises(
            ValueError,
            match="q must contain exactly 2 corner values",
        ):
            StructuralSurfaceActionFree(
                name="FF2",
                direction=Direction.X,
                distribution=Distribution.DIRECTION_X,
                load_case="LC1",
                coordinate_x="0.0;5.0;5.0;0.0",
                coordinate_y="0.0;0.0;3.0;3.0",
                coordinate_z="0.0;0.0;0.0;0.0",
                edges="Line;Line;Line;Line",
                coordinate_system=CoordinateSystem.GLOBAL,
                location=Location.LENGTH,
                q="C1:-5",
            )

    def test_direction_x_with_three_corners_raises_error(self) -> None:
        """Test that DirectionX with three corner values raises ValueError."""
        with pytest.raises(
            ValueError,
            match="q must contain exactly 2 corner values",
        ):
            StructuralSurfaceActionFree(
                name="FF2",
                direction=Direction.X,
                distribution=Distribution.DIRECTION_X,
                load_case="LC1",
                coordinate_x="0.0;5.0;5.0;0.0",
                coordinate_y="0.0;0.0;3.0;3.0",
                coordinate_z="0.0;0.0;0.0;0.0",
                edges="Line;Line;Line;Line",
                coordinate_system=CoordinateSystem.GLOBAL,
                location=Location.LENGTH,
                q="C1:-5;C2:-7;C3:-3",
            )

    def test_direction_y_with_one_corner_raises_error(self) -> None:
        """Test that DirectionY with only one corner value raises ValueError."""
        with pytest.raises(
            ValueError,
            match="q must contain exactly 2 corner values",
        ):
            StructuralSurfaceActionFree(
                name="FF3",
                direction=Direction.Y,
                distribution=Distribution.DIRECTION_Y,
                load_case="LC1",
                coordinate_x="0.0;5.0;5.0;0.0",
                coordinate_y="0.0;0.0;3.0;3.0",
                coordinate_z="0.0;0.0;0.0;0.0",
                edges="Line;Line;Line;Line",
                coordinate_system=CoordinateSystem.GLOBAL,
                location=Location.LENGTH,
                q="C1:-2",
            )

    def test_direction_xy_with_two_corners_raises_error(self) -> None:
        """Test that DirectionXY with only two corner values raises ValueError."""
        with pytest.raises(
            ValueError,
            match="q must contain exactly 3 corner values",
        ):
            StructuralSurfaceActionFree(
                name="FF4",
                direction=Direction.Z,
                distribution=Distribution.DIRECTION_XY,
                load_case="LC1",
                coordinate_x="0.0;5.0;5.0;0.0",
                coordinate_y="0.0;0.0;3.0;3.0",
                coordinate_z="0.0;0.0;0.0;0.0",
                edges="Line;Line;Line;Line",
                coordinate_system=CoordinateSystem.GLOBAL,
                location=Location.LENGTH,
                q="C1:-3;C2:-2",
            )

    def test_direction_xy_with_four_corners_raises_error(self) -> None:
        """Test that DirectionXY with four corner values raises ValueError."""
        with pytest.raises(
            ValueError,
            match="q must contain exactly 3 corner values",
        ):
            StructuralSurfaceActionFree(
                name="FF4",
                direction=Direction.Z,
                distribution=Distribution.DIRECTION_XY,
                load_case="LC1",
                coordinate_x="0.0;5.0;5.0;0.0",
                coordinate_y="0.0;0.0;3.0;3.0",
                coordinate_z="0.0;0.0;0.0;0.0",
                edges="Line;Line;Line;Line",
                coordinate_system=CoordinateSystem.GLOBAL,
                location=Location.LENGTH,
                q="C1:-3;C2:-2;C3:-1;C4:-5",
            )


class TestStructuralSurfaceActionFreeEnums:
    """Test enum values and functionality."""

    def test_direction_enum_values(self) -> None:
        """Test all Direction enum values."""
        assert Direction.X.value == "X"
        assert Direction.Y.value == "Y"
        assert Direction.Z.value == "Z"

    def test_distribution_enum_values(self) -> None:
        """Test all Distribution enum values."""
        assert Distribution.UNIFORM.value == "Uniform"
        assert Distribution.DIRECTION_X.value == "DirectionX"
        assert Distribution.DIRECTION_Y.value == "DirectionY"
        assert Distribution.DIRECTION_XY.value == "DirectionXY"

    def test_coordinate_system_enum_values(self) -> None:
        """Test all CoordinateSystem enum values."""
        assert CoordinateSystem.GLOBAL.value == "Global"
        assert CoordinateSystem.LOCAL.value == "Local"

    def test_location_enum_values(self) -> None:
        """Test all Location enum values."""
        assert Location.LENGTH.value == "Length"
        assert Location.PROJECTION.value == "Projection"

    def test_edge_enum_values(self) -> None:
        """Test all Edge enum values."""
        assert Edge.LINE.value == "Line"
        assert Edge.BEZIER.value == "Bezier"
        assert Edge.CIRCLE_ARC.value == "Circle arc"
        assert Edge.PARABOLIC_ARC.value == "Parabolic arc"
        assert Edge.SPLINE.value == "Spline"


class TestStructuralSurfaceActionFreeImmutability:
    """Test immutability of StructuralSurfaceActionFree."""

    def test_frozen_dataclass(self) -> None:
        """Test that instances are frozen and immutable."""
        load = StructuralSurfaceActionFree(
            name="FF1",
            direction=Direction.Z,
            distribution=Distribution.UNIFORM,
            load_case="LC1",
            coordinate_x="0.0;5.0;5.0;0.0",
            coordinate_y="0.0;0.0;3.0;3.0",
            coordinate_z="0.0;0.0;0.0;0.0",
            edges="Line;Line;Line;Line",
            coordinate_system=CoordinateSystem.GLOBAL,
            location=Location.LENGTH,
            q="-10",
        )
        with pytest.raises(AttributeError):
            load.name = "FF2"  # type: ignore[misc]

    def test_hash_support(self) -> None:
        """Test that frozen instances are hashable."""
        load1 = StructuralSurfaceActionFree(
            name="FF1",
            direction=Direction.Z,
            distribution=Distribution.UNIFORM,
            load_case="LC1",
            coordinate_x="0.0;5.0;5.0;0.0",
            coordinate_y="0.0;0.0;3.0;3.0",
            coordinate_z="0.0;0.0;0.0;0.0",
            edges="Line;Line;Line;Line",
            coordinate_system=CoordinateSystem.GLOBAL,
            location=Location.LENGTH,
            q="-10",
        )
        load_dict = {load1: "first"}
        assert load_dict[load1] == "first"


class TestStructuralSurfaceActionFreeEquality:
    """Test equality comparison of StructuralSurfaceActionFree."""

    def test_equal_instances(self) -> None:
        """Test that identical instances are equal."""
        load1 = StructuralSurfaceActionFree(
            name="FF1",
            direction=Direction.Z,
            distribution=Distribution.UNIFORM,
            load_case="LC1",
            coordinate_x="0.0;5.0;5.0;0.0",
            coordinate_y="0.0;0.0;3.0;3.0",
            coordinate_z="0.0;0.0;0.0;0.0",
            edges="Line;Line;Line;Line",
            coordinate_system=CoordinateSystem.GLOBAL,
            location=Location.LENGTH,
            q="-10",
        )
        load2 = StructuralSurfaceActionFree(
            name="FF1",
            direction=Direction.Z,
            distribution=Distribution.UNIFORM,
            load_case="LC1",
            coordinate_x="0.0;5.0;5.0;0.0",
            coordinate_y="0.0;0.0;3.0;3.0",
            coordinate_z="0.0;0.0;0.0;0.0",
            edges="Line;Line;Line;Line",
            coordinate_system=CoordinateSystem.GLOBAL,
            location=Location.LENGTH,
            q="-10",
        )
        assert load1 == load2

    def test_unequal_instances_different_name(self) -> None:
        """Test that instances with different names are not equal."""
        load1 = StructuralSurfaceActionFree(
            name="FF1",
            direction=Direction.Z,
            distribution=Distribution.UNIFORM,
            load_case="LC1",
            coordinate_x="0.0;5.0;5.0;0.0",
            coordinate_y="0.0;0.0;3.0;3.0",
            coordinate_z="0.0;0.0;0.0;0.0",
            edges="Line;Line;Line;Line",
            coordinate_system=CoordinateSystem.GLOBAL,
            location=Location.LENGTH,
            q="-10",
        )
        load2 = StructuralSurfaceActionFree(
            name="FF2",
            direction=Direction.Z,
            distribution=Distribution.UNIFORM,
            load_case="LC1",
            coordinate_x="0.0;5.0;5.0;0.0",
            coordinate_y="0.0;0.0;3.0;3.0",
            coordinate_z="0.0;0.0;0.0;0.0",
            edges="Line;Line;Line;Line",
            coordinate_system=CoordinateSystem.GLOBAL,
            location=Location.LENGTH,
            q="-10",
        )
        assert load1 != load2

    def test_unequal_instances_different_q(self) -> None:
        """Test that instances with different q values are not equal."""
        load1 = StructuralSurfaceActionFree(
            name="FF1",
            direction=Direction.Z,
            distribution=Distribution.UNIFORM,
            load_case="LC1",
            coordinate_x="0.0;5.0;5.0;0.0",
            coordinate_y="0.0;0.0;3.0;3.0",
            coordinate_z="0.0;0.0;0.0;0.0",
            edges="Line;Line;Line;Line",
            coordinate_system=CoordinateSystem.GLOBAL,
            location=Location.LENGTH,
            q="-10",
        )
        load2 = StructuralSurfaceActionFree(
            name="FF1",
            direction=Direction.Z,
            distribution=Distribution.UNIFORM,
            load_case="LC1",
            coordinate_x="0.0;5.0;5.0;0.0",
            coordinate_y="0.0;0.0;3.0;3.0",
            coordinate_z="0.0;0.0;0.0;0.0",
            edges="Line;Line;Line;Line",
            coordinate_system=CoordinateSystem.GLOBAL,
            location=Location.LENGTH,
            q="-20",
        )
        assert load1 != load2


class TestStructuralSurfaceActionFreeEdgeCases:
    """Test edge cases and special scenarios."""

    def test_large_polygon(self) -> None:
        """Test load with many polygon vertices."""
        load = StructuralSurfaceActionFree(
            name="FF1",
            direction=Direction.Z,
            distribution=Distribution.UNIFORM,
            load_case="LC1",
            coordinate_x="0.0;1.0;2.0;3.0;4.0;5.0;5.0;4.0;3.0;2.0;1.0;0.0",
            coordinate_y="0.0;0.0;0.0;0.0;0.0;0.0;3.0;3.0;3.0;3.0;3.0;3.0",
            coordinate_z="0.0;0.0;0.0;0.0;0.0;0.0;0.0;0.0;0.0;0.0;0.0;0.0",
            edges="Line;Line;Line;Line;Line;Line;Line;Line;Line;Line;Line;Line",
            coordinate_system=CoordinateSystem.GLOBAL,
            location=Location.LENGTH,
            q="-10",
        )
        assert load.name == "FF1"

    def test_decimal_q_values(self) -> None:
        """Test load with decimal load values."""
        load = StructuralSurfaceActionFree(
            name="FF1",
            direction=Direction.Z,
            distribution=Distribution.UNIFORM,
            load_case="LC1",
            coordinate_x="0.0;5.0;5.0;0.0",
            coordinate_y="0.0;0.0;3.0;3.0",
            coordinate_z="0.0;0.0;0.0;0.0",
            edges="Line;Line;Line;Line",
            coordinate_system=CoordinateSystem.GLOBAL,
            location=Location.LENGTH,
            q="-10.5",
        )
        assert load.q == "-10.5"

    def test_direction_x_load_with_decimal_corners(self) -> None:
        """Test DirectionX load with decimal corner values."""
        load = StructuralSurfaceActionFree(
            name="FF2",
            direction=Direction.X,
            distribution=Distribution.DIRECTION_X,
            load_case="LC1",
            coordinate_x="0.0;5.0;5.0;0.0",
            coordinate_y="0.0;0.0;3.0;3.0",
            coordinate_z="0.0;0.0;0.0;0.0",
            edges="Line;Line;Line;Line",
            coordinate_system=CoordinateSystem.GLOBAL,
            location=Location.LENGTH,
            q="C1:-5.5;C2:-7.25",
        )
        assert load.q == "C1:-5.5;C2:-7.25"

    def test_direction_xy_load_with_all_positive_corners(self) -> None:
        """Test DirectionXY load with all positive corner values."""
        load = StructuralSurfaceActionFree(
            name="FF4",
            direction=Direction.Z,
            distribution=Distribution.DIRECTION_XY,
            load_case="LC1",
            coordinate_x="0.0;5.0;5.0;0.0",
            coordinate_y="0.0;0.0;3.0;3.0",
            coordinate_z="0.0;0.0;0.0;0.0",
            edges="Line;Line;Line;Line",
            coordinate_system=CoordinateSystem.GLOBAL,
            location=Location.LENGTH,
            q="C1:3;C2:2;C3:1",
        )
        assert load.q == "C1:3;C2:2;C3:1"

    def test_empty_action_type(self) -> None:
        """Test that empty action_type is default."""
        load = StructuralSurfaceActionFree(
            name="FF1",
            direction=Direction.Z,
            distribution=Distribution.UNIFORM,
            load_case="LC1",
            coordinate_x="0.0;5.0;5.0;0.0",
            coordinate_y="0.0;0.0;3.0;3.0",
            coordinate_z="0.0;0.0;0.0;0.0",
            edges="Line;Line;Line;Line",
            coordinate_system=CoordinateSystem.GLOBAL,
            location=Location.LENGTH,
            q="-10",
        )
        assert load.action_type == ""

    def test_empty_id(self) -> None:
        """Test that empty id is default."""
        load = StructuralSurfaceActionFree(
            name="FF1",
            direction=Direction.Z,
            distribution=Distribution.UNIFORM,
            load_case="LC1",
            coordinate_x="0.0;5.0;5.0;0.0",
            coordinate_y="0.0;0.0;3.0;3.0",
            coordinate_z="0.0;0.0;0.0;0.0",
            edges="Line;Line;Line;Line",
            coordinate_system=CoordinateSystem.GLOBAL,
            location=Location.LENGTH,
            q="-10",
        )
        assert load.id == ""
