"""Tests for StructuralCurveActionFree dataclass.

Comprehensive test suite covering initialization, validation, and immutability
of the StructuralCurveActionFree class following SAF specification.
"""

import pytest

from blueprints.saf.loads.structural_curve_action_free import (
    CoordinateSystem,
    Direction,
    Distribution,
    Location,
    Segment,
    StructuralCurveActionFree,
)


class TestStructuralCurveActionFreeValidInitialization:
    """Tests for valid StructuralCurveActionFree initialization."""

    def test_uniform_line_load(self) -> None:
        """Test uniform line load along a simple line."""
        load = StructuralCurveActionFree(
            name="LF1",
            distribution=Distribution.UNIFORM,
            direction=Direction.Z,
            load_case="LC1",
            coordinate_x="0.0;5.0",
            coordinate_y="1.0;1.0",
            coordinate_z="0.0;0.0",
            segments="Line",
            coordinate_system=CoordinateSystem.GLOBAL,
            location=Location.LENGTH,
            value_1=-50.0,
        )
        assert load.name == "LF1"
        assert load.distribution == Distribution.UNIFORM
        assert load.direction == Direction.Z
        assert load.value_1 == -50.0

    def test_trapezoidal_line_load(self) -> None:
        """Test trapezoidal line load with varying magnitude."""
        load = StructuralCurveActionFree(
            name="LF2",
            distribution=Distribution.TRAPEZ,
            direction=Direction.Z,
            load_case="LC1",
            coordinate_x="0.0;5.0",
            coordinate_y="1.0;1.0",
            coordinate_z="0.0;0.0",
            segments="Line",
            coordinate_system=CoordinateSystem.GLOBAL,
            location=Location.LENGTH,
            value_1=-50.0,
            value_2=-75.0,
        )
        assert load.value_1 == -50.0
        assert load.value_2 == -75.0

    def test_load_with_curved_path(self) -> None:
        """Test load along a curved path."""
        load = StructuralCurveActionFree(
            name="LF3",
            distribution=Distribution.UNIFORM,
            direction=Direction.Z,
            load_case="LC1",
            coordinate_x="0.0;2.5;5.0",
            coordinate_y="0.0;1.0;0.0",
            coordinate_z="0.0;0.0;0.0",
            segments="Line;Circular arc",
            coordinate_system=CoordinateSystem.GLOBAL,
            location=Location.LENGTH,
            value_1=-60.0,
        )
        assert load.coordinate_x == "0.0;2.5;5.0"
        assert load.segments == "Line;Circular arc"

    def test_load_with_bezier_segment(self) -> None:
        """Test load with Bezier curve segment."""
        load = StructuralCurveActionFree(
            name="LF4",
            distribution=Distribution.UNIFORM,
            direction=Direction.Z,
            load_case="LC1",
            coordinate_x="0.0;1.0;2.0;3.0",
            coordinate_y="0.0;1.0;2.0;3.0",
            coordinate_z="0.0;0.0;0.0;0.0",
            segments="Bezier",
            coordinate_system=CoordinateSystem.GLOBAL,
            location=Location.LENGTH,
            value_1=-40.0,
        )
        assert load.segments == "Bezier"

    def test_load_with_spline_segment(self) -> None:
        """Test load with Spline curve segment."""
        load = StructuralCurveActionFree(
            name="LF5",
            distribution=Distribution.UNIFORM,
            direction=Direction.X,
            load_case="LC1",
            coordinate_x="0.0;1.0;2.0",
            coordinate_y="0.0;1.5;0.5",
            coordinate_z="0.0;0.5;1.0",
            segments="Spline",
            coordinate_system=CoordinateSystem.GLOBAL,
            location=Location.LENGTH,
            value_1=30.0,
        )
        assert load.direction == Direction.X
        assert load.value_1 == 30.0

    def test_vector_load_uniform(self) -> None:
        """Test vector load with uniform distribution."""
        load = StructuralCurveActionFree(
            name="LF6",
            distribution=Distribution.UNIFORM,
            direction=Direction.VECTOR,
            load_case="LC1",
            coordinate_x="0.0;5.0",
            coordinate_y="0.0;0.0",
            coordinate_z="0.0;0.0",
            segments="Line",
            coordinate_system=CoordinateSystem.GLOBAL,
            location=Location.LENGTH,
            vector_1="10;20;-50",
        )
        assert load.vector_1 == "10;20;-50"

    def test_vector_load_trapezoidal(self) -> None:
        """Test vector load with trapezoidal distribution."""
        load = StructuralCurveActionFree(
            name="LF7",
            distribution=Distribution.TRAPEZ,
            direction=Direction.VECTOR,
            load_case="LC1",
            coordinate_x="0.0;5.0",
            coordinate_y="0.0;0.0",
            coordinate_z="0.0;0.0",
            segments="Line",
            coordinate_system=CoordinateSystem.GLOBAL,
            location=Location.LENGTH,
            vector_1="10;20;-50",
            vector_2="15;25;-75",
        )
        assert load.vector_1 == "10;20;-50"
        assert load.vector_2 == "15;25;-75"

    def test_load_with_projection_location(self) -> None:
        """Test load with PROJECTION location."""
        load = StructuralCurveActionFree(
            name="LF8",
            distribution=Distribution.UNIFORM,
            direction=Direction.Z,
            load_case="LC1",
            coordinate_x="0.0;5.0",
            coordinate_y="0.0;0.0",
            coordinate_z="0.0;0.0",
            segments="Line",
            coordinate_system=CoordinateSystem.GLOBAL,
            location=Location.PROJECTION,
            value_1=-50.0,
        )
        assert load.location == Location.PROJECTION

    def test_load_with_local_coordinate_system(self) -> None:
        """Test load with local coordinate system."""
        load = StructuralCurveActionFree(
            name="LF9",
            distribution=Distribution.UNIFORM,
            direction=Direction.Z,
            load_case="LC1",
            coordinate_x="0.0;5.0",
            coordinate_y="0.0;0.0",
            coordinate_z="0.0;0.0",
            segments="Line",
            coordinate_system=CoordinateSystem.LOCAL,
            location=Location.LENGTH,
            value_1=-50.0,
        )
        assert load.coordinate_system == CoordinateSystem.LOCAL

    def test_load_with_action_type(self) -> None:
        """Test load with action type."""
        load = StructuralCurveActionFree(
            name="LF10",
            distribution=Distribution.UNIFORM,
            direction=Direction.Z,
            load_case="LC1",
            coordinate_x="0.0;5.0",
            coordinate_y="0.0;0.0",
            coordinate_z="0.0;0.0",
            segments="Line",
            coordinate_system=CoordinateSystem.GLOBAL,
            location=Location.LENGTH,
            value_1=-50.0,
            action_type="Wind",
        )
        assert load.action_type == "Wind"

    def test_load_in_y_direction(self) -> None:
        """Test load in Y direction."""
        load = StructuralCurveActionFree(
            name="LF11",
            distribution=Distribution.UNIFORM,
            direction=Direction.Y,
            load_case="LC1",
            coordinate_x="0.0;0.0",
            coordinate_y="0.0;5.0",
            coordinate_z="0.0;0.0",
            segments="Line",
            coordinate_system=CoordinateSystem.GLOBAL,
            location=Location.LENGTH,
            value_1=-40.0,
        )
        assert load.direction == Direction.Y

    def test_complex_multi_segment_path(self) -> None:
        """Test load with multiple segment types."""
        load = StructuralCurveActionFree(
            name="LF12",
            distribution=Distribution.UNIFORM,
            direction=Direction.Z,
            load_case="LC1",
            coordinate_x="0.0;2.5;5.0;7.5;10.0",
            coordinate_y="0.0;1.0;2.0;1.0;0.0",
            coordinate_z="0.0;0.0;0.0;0.0;0.0",
            segments="Line;Circular arc;Line;Parabolic arc",
            coordinate_system=CoordinateSystem.GLOBAL,
            location=Location.LENGTH,
            value_1=-35.0,
        )
        assert load.coordinate_x == "0.0;2.5;5.0;7.5;10.0"
        assert load.segments == "Line;Circular arc;Line;Parabolic arc"


class TestStructuralCurveActionFreeValidation:
    """Tests for StructuralCurveActionFree validation."""

    def test_vector_direction_requires_vector_1(self) -> None:
        """Test that VECTOR direction requires vector_1."""
        with pytest.raises(ValueError, match="vector_1 must be specified"):
            StructuralCurveActionFree(
                name="LF1",
                distribution=Distribution.UNIFORM,
                direction=Direction.VECTOR,
                load_case="LC1",
                coordinate_x="0.0;5.0",
                coordinate_y="0.0;0.0",
                coordinate_z="0.0;0.0",
                segments="Line",
                coordinate_system=CoordinateSystem.GLOBAL,
                location=Location.LENGTH,
            )

    def test_vector_format_validation(self) -> None:
        """Test that vector format must contain semicolons."""
        with pytest.raises(ValueError, match="must be in 'X;Y;Z' format"):
            StructuralCurveActionFree(
                name="LF1",
                distribution=Distribution.UNIFORM,
                direction=Direction.VECTOR,
                load_case="LC1",
                coordinate_x="0.0;5.0",
                coordinate_y="0.0;0.0",
                coordinate_z="0.0;0.0",
                segments="Line",
                coordinate_system=CoordinateSystem.GLOBAL,
                location=Location.LENGTH,
                vector_1="10,20,30",  # Wrong format
            )

    def test_single_axis_direction_requires_value_1(self) -> None:
        """Test that single-axis directions require value_1."""
        with pytest.raises(ValueError, match="value_1 must be specified"):
            StructuralCurveActionFree(
                name="LF1",
                distribution=Distribution.UNIFORM,
                direction=Direction.Z,
                load_case="LC1",
                coordinate_x="0.0;5.0",
                coordinate_y="0.0;0.0",
                coordinate_z="0.0;0.0",
                segments="Line",
                coordinate_system=CoordinateSystem.GLOBAL,
                location=Location.LENGTH,
            )

    def test_trapez_requires_value_2_for_single_axis(self) -> None:
        """Test that TRAPEZ distribution requires value_2 for single-axis directions."""
        with pytest.raises(ValueError, match="value_2 must be specified"):
            StructuralCurveActionFree(
                name="LF1",
                distribution=Distribution.TRAPEZ,
                direction=Direction.Z,
                load_case="LC1",
                coordinate_x="0.0;5.0",
                coordinate_y="0.0;0.0",
                coordinate_z="0.0;0.0",
                segments="Line",
                coordinate_system=CoordinateSystem.GLOBAL,
                location=Location.LENGTH,
                value_1=-50.0,
            )

    def test_trapez_requires_vector_2_for_vector(self) -> None:
        """Test that TRAPEZ distribution requires vector_2 for vector direction."""
        with pytest.raises(ValueError, match="vector_2 must be specified"):
            StructuralCurveActionFree(
                name="LF1",
                distribution=Distribution.TRAPEZ,
                direction=Direction.VECTOR,
                load_case="LC1",
                coordinate_x="0.0;5.0",
                coordinate_y="0.0;0.0",
                coordinate_z="0.0;0.0",
                segments="Line",
                coordinate_system=CoordinateSystem.GLOBAL,
                location=Location.LENGTH,
                vector_1="10;20;-50",
            )


class TestStructuralCurveActionFreeEquality:
    """Tests for StructuralCurveActionFree equality."""

    def test_equal_loads_with_same_attributes(self) -> None:
        """Test that loads with same attributes are equal."""
        load1 = StructuralCurveActionFree(
            name="LF1",
            distribution=Distribution.UNIFORM,
            direction=Direction.Z,
            load_case="LC1",
            coordinate_x="0.0;5.0",
            coordinate_y="0.0;0.0",
            coordinate_z="0.0;0.0",
            segments="Line",
            coordinate_system=CoordinateSystem.GLOBAL,
            location=Location.LENGTH,
            value_1=-50.0,
        )
        load2 = StructuralCurveActionFree(
            name="LF1",
            distribution=Distribution.UNIFORM,
            direction=Direction.Z,
            load_case="LC1",
            coordinate_x="0.0;5.0",
            coordinate_y="0.0;0.0",
            coordinate_z="0.0;0.0",
            segments="Line",
            coordinate_system=CoordinateSystem.GLOBAL,
            location=Location.LENGTH,
            value_1=-50.0,
        )
        assert load1 == load2

    def test_unequal_loads_different_values(self) -> None:
        """Test that loads with different values are not equal."""
        load1 = StructuralCurveActionFree(
            name="LF1",
            distribution=Distribution.UNIFORM,
            direction=Direction.Z,
            load_case="LC1",
            coordinate_x="0.0;5.0",
            coordinate_y="0.0;0.0",
            coordinate_z="0.0;0.0",
            segments="Line",
            coordinate_system=CoordinateSystem.GLOBAL,
            location=Location.LENGTH,
            value_1=-50.0,
        )
        load2 = StructuralCurveActionFree(
            name="LF1",
            distribution=Distribution.UNIFORM,
            direction=Direction.Z,
            load_case="LC1",
            coordinate_x="0.0;5.0",
            coordinate_y="0.0;0.0",
            coordinate_z="0.0;0.0",
            segments="Line",
            coordinate_system=CoordinateSystem.GLOBAL,
            location=Location.LENGTH,
            value_1=-75.0,
        )
        assert load1 != load2

    def test_frozen_immutability(self) -> None:
        """Test that load instances are frozen (immutable)."""
        load = StructuralCurveActionFree(
            name="LF1",
            distribution=Distribution.UNIFORM,
            direction=Direction.Z,
            load_case="LC1",
            coordinate_x="0.0;5.0",
            coordinate_y="0.0;0.0",
            coordinate_z="0.0;0.0",
            segments="Line",
            coordinate_system=CoordinateSystem.GLOBAL,
            location=Location.LENGTH,
            value_1=-50.0,
        )
        with pytest.raises(AttributeError):
            load.value_1 = -75.0  # type: ignore[misc]


class TestEnums:
    """Tests for enums used in StructuralCurveActionFree."""

    def test_all_distribution_values(self) -> None:
        """Test all distribution values."""
        distributions = list(Distribution)
        assert len(distributions) == 2
        assert Distribution.UNIFORM in distributions
        assert Distribution.TRAPEZ in distributions

    def test_all_direction_values(self) -> None:
        """Test all direction values."""
        directions = list(Direction)
        assert len(directions) == 4

    def test_all_segment_values(self) -> None:
        """Test all segment values."""
        segments = list(Segment)
        assert len(segments) == 5
        assert Segment.LINE in segments
        assert Segment.CIRCULAR_ARC in segments
        assert Segment.BEZIER in segments
        assert Segment.PARABOLIC_ARC in segments
        assert Segment.SPLINE in segments


class TestStructuralCurveActionFreeEdgeCases:
    """Tests for StructuralCurveActionFree edge cases."""

    def test_very_large_load_value(self) -> None:
        """Test load with very large value."""
        load = StructuralCurveActionFree(
            name="LF1",
            distribution=Distribution.UNIFORM,
            direction=Direction.Z,
            load_case="LC1",
            coordinate_x="0.0;5.0",
            coordinate_y="0.0;0.0",
            coordinate_z="0.0;0.0",
            segments="Line",
            coordinate_system=CoordinateSystem.GLOBAL,
            location=Location.LENGTH,
            value_1=-1e10,
        )
        assert load.value_1 == -1e10

    def test_complex_coordinate_path(self) -> None:
        """Test load with complex coordinate path."""
        load = StructuralCurveActionFree(
            name="LF1",
            distribution=Distribution.UNIFORM,
            direction=Direction.Z,
            load_case="LC1",
            coordinate_x="0.5;1.5;2.75;3.25;4.0;5.25",
            coordinate_y="0.0;0.5;1.0;1.5;1.0;0.5",
            coordinate_z="0.0;0.0;0.5;1.0;0.75;0.0",
            segments="Line;Circular arc;Line;Bezier;Spline",
            coordinate_system=CoordinateSystem.GLOBAL,
            location=Location.LENGTH,
            value_1=-45.0,
        )
        assert load.coordinate_z == "0.0;0.0;0.5;1.0;0.75;0.0"

    def test_negative_coordinates(self) -> None:
        """Test load with negative coordinates."""
        load = StructuralCurveActionFree(
            name="LF1",
            distribution=Distribution.UNIFORM,
            direction=Direction.Z,
            load_case="LC1",
            coordinate_x="-5.0;0.0;5.0",
            coordinate_y="-2.0;0.0;2.0",
            coordinate_z="-1.0;0.0;1.0",
            segments="Line;Line",
            coordinate_system=CoordinateSystem.GLOBAL,
            location=Location.LENGTH,
            value_1=-30.0,
        )
        assert load.coordinate_x == "-5.0;0.0;5.0"
