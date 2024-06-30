"""Fixtures for geometry tests."""

import pytest
from shapely.geometry import Point

from blueprints.geometry.line import Line


@pytest.fixture()
def fixture_line_horizontal() -> Line:
    """Fixture for a horizontal line."""
    return Line(Point(0, 0, 0), Point(1, 0, 0))


@pytest.fixture()
def fixture_line_vertical() -> Line:
    """Fixture for a vertical line."""
    return Line(Point(0, 0, 0), Point(0, 1, 0))


@pytest.fixture()
def fixture_line_diagonal() -> Line:
    """Fixture for a diagonal line."""
    return Line(Point(0, 0, 0), Point(1, 1, 1))
