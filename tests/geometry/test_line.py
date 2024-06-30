"""Line tests."""

import pytest
from shapely.geometry import Point

from blueprints.geometry.line import Line, Reference


class TestLine:
    """Tests for the Line class."""

    def test_length(self, fixture_line_diagonal: Line) -> None:
        """Test the length property of the Line class."""
        assert fixture_line_diagonal.length == pytest.approx(1.73205080757)

    def test_delta_x(self, fixture_line_horizontal: Line) -> None:
        """Test the delta_x property of the Line class."""
        assert fixture_line_horizontal.delta_x == 1

    def test_delta_y(self, fixture_line_vertical: Line) -> None:
        """Test the delta_y property of the Line class."""
        assert fixture_line_vertical.delta_y == 1

    def test_delta_z(self, fixture_line_diagonal: Line) -> None:
        """Test the delta_z property of the Line class."""
        assert fixture_line_diagonal.delta_z == 1

    def test_midpoint(self, fixture_line_diagonal: Line) -> None:
        """Test the midpoint property of the Line class."""
        assert fixture_line_diagonal.midpoint == Point(0.5, 0.5, 0.5)

    def test_angle(self, fixture_line_diagonal: Line) -> None:
        """Test the angle method of the Line class."""
        assert fixture_line_diagonal.angle() == pytest.approx(45)

    def test_get_internal_point_from_start(self, fixture_line_diagonal: Line) -> None:
        """Test the get_internal_point method of the Line class."""
        result = fixture_line_diagonal.get_internal_point(distance=1, reference_point=Reference.START)
        expected = Point(0.577, 0.577, 0.577)
        assert (result.x, result.y, result.z) == pytest.approx(expected=(expected.x, expected.y, expected.z), abs=1e-3)

    def test_get_internal_point_from_end(self, fixture_line_diagonal: Line) -> None:
        """Test the get_internal_point method of the Line class."""
        result = fixture_line_diagonal.get_internal_point(distance=1, reference_point=Reference.END)
        expected = Point(0.423, 0.423, 0.423)
        assert (result.x, result.y, result.z) == pytest.approx(expected=(expected.x, expected.y, expected.z), abs=1e-3)

    def test_extend_from_end(self, fixture_line_diagonal: Line) -> None:
        """Test the extend method of the Line class."""
        fixture_line_diagonal.extend(1)
        result = fixture_line_diagonal.end_point
        expected = Point(1.577, 1.577, 1.577)
        assert (result.x, result.y, result.z) == pytest.approx(expected=(expected.x, expected.y, expected.z), abs=1e-3)

    def test_extend_from_start(self, fixture_line_diagonal: Line) -> None:
        """Test the extend method of the Line class."""
        fixture_line_diagonal.extend(1, Reference.START)
        result = fixture_line_diagonal.start_point
        expected = Point(-0.577, -0.577, -0.577)
        assert (result.x, result.y, result.z) == pytest.approx(expected=(expected.x, expected.y, expected.z), abs=1e-3)

    def test_get_evenly_spaced_points(self, fixture_line_diagonal: Line) -> None:
        """Test the get_evenly_spaced_points method of the Line class."""
        points = fixture_line_diagonal.get_evenly_spaced_points(3)
        assert points == [Point(0, 0, 0), Point(0.5, 0.5, 0.5), Point(1, 1, 1)]

    def test_divide_into_n_lines(self, fixture_line_diagonal: Line) -> None:
        """Test the divide_into_n_lines method of the Line class."""
        lines = fixture_line_diagonal.divide_into_n_lines(2)
        assert lines[0].start_point == Point(0, 0, 0)
        assert lines[0].end_point == Point(0.5, 0.5, 0.5)
        assert lines[1].start_point == Point(0.5, 0.5, 0.5)
        assert lines[1].end_point == Point(1, 1, 1)

    def test_raise_error_same_start_end_point(self) -> None:
        """Test that an error is raised when the start and end points are the same."""
        with pytest.raises(ValueError):
            Line(Point(0, 0, 0), Point(0, 0, 0))

    @pytest.mark.parametrize("distance", [100, -1])
    def test_raise_error_get_internal_point_invalid_distance(self, fixture_line_diagonal: Line, distance: float) -> None:
        """Test that an error is raised when the distance is invalid."""
        with pytest.raises(ValueError):
            fixture_line_diagonal.get_internal_point(distance=distance)

    def test_raise_error_get_internal_point_invalid_reference_point(self, fixture_line_diagonal: Line) -> None:
        """Test that an error is raised when the reference point is invalid."""
        with pytest.raises(ValueError):
            fixture_line_diagonal.get_internal_point(distance=1, reference_point="invalid")  # type: ignore[arg-type]

    def test_raise_error_extend_invalid_direction(self, fixture_line_diagonal: Line) -> None:
        """Test that an error is raised when the direction is invalid."""
        with pytest.raises(ValueError):
            fixture_line_diagonal.extend(extra_length=1, direction="invalid")  # type: ignore[arg-type]

    @pytest.mark.parametrize("n", [1, 1.5])
    def test_raise_error_get_evenly_spaced_points_invalid_n(self, fixture_line_diagonal: Line, n: float) -> None:
        """Test that an error is raised when n is invalid."""
        with pytest.raises(ValueError):
            fixture_line_diagonal.get_evenly_spaced_points(n=n)  # type: ignore[arg-type]

    @pytest.mark.parametrize("n", [1, 1.5])
    def test_raise_error_divide_into_n_lines_invalid_n(self, fixture_line_diagonal: Line, n: float) -> None:
        """Test that an error is raised when n is invalid."""
        with pytest.raises(ValueError):
            fixture_line_diagonal.divide_into_n_lines(n=n)  # type: ignore[arg-type]

    def test_eq(self) -> None:
        """Test the __eq__ method of the Line class."""
        line1 = Line(Point(0, 0, 0), Point(1, 1, 1))
        line2 = Line(Point(0, 0, 0), Point(1, 1, 1))
        assert line1 == line2

    def test_raise_error_wrong_eq_input(self) -> None:
        """Test that an error is raised when the input is invalid."""
        with pytest.raises(NotImplementedError):
            Line(Point(0, 0, 0), Point(1, 1, 1)) == "invalid"  # type: ignore[arg-type]
