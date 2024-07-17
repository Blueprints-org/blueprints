"""Test Line class."""

from typing import Literal

import pytest
from shapely import Point

from blueprints.geometry.line import Line


class TestLine:
    """Test Line."""

    @pytest.fixture(autouse=True)
    def line(self) -> Line:
        """Fixture."""
        start_point = Point(0, 0, 0)
        end_point = Point(3, 4, 5)
        return Line(start_point=start_point, end_point=end_point)

    def test_error_same_points(self) -> None:
        """Test the error when the same points are given."""
        with pytest.raises(ValueError):
            Line(Point(0, 0, 0), Point(0, 0, 0))

    def test_initiate_with_no_z_value(self) -> None:
        """Test the initiation with no z value."""
        line = Line(Point(0, 0), Point(3, 4))
        assert line.start_point.has_z
        assert line.end_point.has_z

    def test_midpoint(self, line: Line) -> None:
        """Test the midpoint."""
        midpoint = line.midpoint
        assert midpoint == Point(1.5, 2.0, 2.5)

    def test_delta_x(self, line: Line) -> None:
        """Test the delta x."""
        assert line.delta_x == 3.0

    def test_delta_y(self, line: Line) -> None:
        """Test the delta y."""
        assert line.delta_y == 4.0

    def test_delta_z(self, line: Line) -> None:
        """Test the delta z."""
        assert line.delta_z == 5.0

    def test_length(self, line: Line) -> None:
        """Test the length."""
        assert line.length == pytest.approx(expected=7.07106, rel=1e-5)

    def test_angle(self, line: Line) -> None:
        """Test the angle."""
        angle = line.angle()
        assert angle == pytest.approx(expected=53.130, rel=1e-5)

    @pytest.mark.parametrize(
        ("distance", "reference", "x", "y", "z"),
        [
            (0.33, "start", 0.14, 0.18667, 0.2333),
            (0.33, "end", 2.86, 3.81333, 4.7667),
        ],
    )
    def test_get_internal_point(self, line: Line, distance: float, reference: Literal["start", "end"], x: float, y: float, z: float) -> None:
        """Test the internal points."""
        point = line.get_internal_point(distance=distance, reference=reference)
        assert (point.x, point.y, point.z) == pytest.approx(expected=(x, y, z), rel=1e-3)

    def test_get_internal_point_error(self, line: Line) -> None:
        """Test the internal point error."""
        with pytest.raises(ValueError):
            line.get_internal_point(distance=1.5, reference="middle")  # type: ignore[arg-type]
        with pytest.raises(ValueError):
            line.get_internal_point(distance=-1.5)
        with pytest.raises(ValueError):
            line.get_internal_point(distance=100_000)

    @pytest.mark.parametrize(
        ("distance", "direction", "expected_line"),
        [
            (-3.5355, "start", Line(Point(1.5, 2.0, 2.5), Point(3, 4, 5))),
            (-3.5355, "end", Line(Point(0, 0, 0), Point(1.5, 2.0, 2.5))),
            (1.0, "start", Line(Point(-0.42426, -0.565685, -0.707106), Point(3, 4, 5))),
            (1.0, "end", Line(Point(0, 0, 0), Point(3.424264, 4.565685, 5.707106))),
        ],
    )
    def test_adjust_length(self, line: Line, distance: float, direction: Literal["start", "end"], expected_line: Line) -> None:
        """Test the adjustment of the length."""
        adjusted_line = line.adjust_length(distance=distance, direction=direction)
        assert adjusted_line == expected_line

    def test_adjust_length_error(self, line: Line) -> None:
        """Test the adjustment of the length error."""
        with pytest.raises(ValueError):
            line.adjust_length(distance=1.5, direction="middle")  # type: ignore[arg-type]
        with pytest.raises(ValueError):
            line.adjust_length(distance=-100)

    def test_evenly_spaced_points(self, line: Line) -> None:
        """Test the evenly spaced points."""
        points = line.get_evenly_spaced_points(n=5)
        assert len(points) == 5
        assert points[0] == Point(0, 0, 0)
        assert points[-1] == Point(3, 4, 5)

    def test_evenly_spaced_points_error(self, line: Line) -> None:
        """Test the evenly spaced points error."""
        with pytest.raises(ValueError):
            line.get_evenly_spaced_points(n=1)
        with pytest.raises(TypeError):
            line.get_evenly_spaced_points(n=1.5)  # type: ignore[arg-type]

    def test_divide_into_n_lines(self, line: Line) -> None:
        """Test the division into n lines."""
        lines = line.divide_into_n_lines(n=5)
        assert len(lines) == 5
        assert lines[0].start_point == Point(0, 0, 0)
        assert lines[-1].end_point == Point(3, 4, 5)

    def test_divide_into_n_lines_error(self, line: Line) -> None:
        """Test the division into n lines error."""
        with pytest.raises(ValueError):
            line.divide_into_n_lines(n=1)
        with pytest.raises(TypeError):
            line.divide_into_n_lines(n=1.5)  # type: ignore[arg-type]

    def test_eq_true(self, line: Line) -> None:
        """Test the equality."""
        assert line == Line(Point(0, 0, 0), Point(3, 4, 5))

    def test_eq_false(self, line: Line) -> None:
        """Test the equality."""
        assert line != Line(Point(0, 0, 0), Point(3, 4, 6))

    def test_eq_not_line(self, line: Line) -> None:
        """Test the equality."""
        with pytest.raises(NotImplementedError):
            line == "Line"

    def test_repr(self, line: Line) -> None:
        """Test the representation."""
        assert repr(line) == "Line(POINT Z (0 0 0), POINT Z (3 4 5))"
