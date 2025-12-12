"""Structural curve action free (free line load) definitions following SAF specification.

Free line loads are applied to slabs along a specific border defined by coordinates
and can affect multiple slabs.
"""

from dataclasses import dataclass
from enum import Enum
from typing import ClassVar


class Distribution(str, Enum):
    """Distribution type of free curve action following SAF specification.

    Specifies how the load varies along the line.
    """

    UNIFORM = "Uniform"
    TRAPEZ = "Trapez"


class Direction(str, Enum):
    """Direction of free curve action following SAF specification.

    Specifies whether the action is a single-axis load or a vector.
    """

    X = "X"
    Y = "Y"
    Z = "Z"
    VECTOR = "Vector"


class CoordinateSystem(str, Enum):
    """Coordinate system for free curve action following SAF specification.

    Global or local coordinate system reference.
    """

    GLOBAL = "Global"
    LOCAL = "Local"


class Location(str, Enum):
    """Location type for free curve action application following SAF specification.

    Specifies whether load is applied based on length or projection.
    """

    LENGTH = "Length"
    PROJECTION = "Projection"


class Segment(str, Enum):
    """Shape type of line segments following SAF specification.

    Defines how the load path is shaped.
    """

    LINE = "Line"
    CIRCULAR_ARC = "Circular arc"
    BEZIER = "Bezier"
    PARABOLIC_ARC = "Parabolic arc"
    SPLINE = "Spline"


@dataclass(frozen=True)
class StructuralCurveActionFree:
    """Structural curve action free following SAF specification.

    Definition following https://www.saf.guide/en/stable/loads/structuralcurveactionfree.html.

    A free curve action represents a distributed line load applied along a specific border or
    load path on a slab. Unlike StructuralCurveAction which applies to specific 1D members or edges,
    free curve actions use global coordinates and can affect multiple slabs.

    Attributes
    ----------
    name : str
        Human-readable unique identifier (e.g., "LF5").
    distribution : Distribution
        Load distribution: Uniform or Trapez (linearly varying).
    direction : Direction
        Load direction: X, Y, Z, or Vector.
    load_case : str
        Reference to StructuralLoadCase name.
    coordinate_x : str
        X-coordinates defining the line in meters, semicolon-separated (e.g., "0.0;5.0").
    coordinate_y : str
        Y-coordinates defining the line in meters, semicolon-separated (e.g., "1.0;1.0").
    coordinate_z : str
        Z-coordinates defining the line in meters, semicolon-separated (e.g., "0.0;0.0").
    segments : str
        Shape types of line segments, semicolon-separated (e.g., "Line;Circular arc").
    coordinate_system : CoordinateSystem
        Global or Local coordinate system.
    location : Location
        Load application method: Length or Projection.
    value_1 : float | None, optional
        Load magnitude for single-axis directions (X/Y/Z) in kN/m.
        For Vector direction: use vector_1 instead.
        Closer to origin for trapezoidal distribution.
    value_2 : float | None, optional
        Second load magnitude for trapezoidal distribution (X/Y/Z) in kN/m.
        Further from origin. Required when distribution = TRAPEZ and direction != VECTOR.
    vector_1 : str | None, optional
        Load vector for Vector direction in "X;Y;Z" format (kN/m).
        Closer to origin for trapezoidal distribution.
    vector_2 : str | None, optional
        Second load vector for trapezoidal distribution in "X;Y;Z" format (kN/m).
        Further from origin. Required when distribution = TRAPEZ and direction = VECTOR.
    action_type : str, optional
        Load classification (e.g., "Standard", "Wind", "Snow").
    id : str, optional
        Unique identifier (UUID format recommended).

    Raises
    ------
    ValueError
        If direction = VECTOR but vector_1 is not specified or not in "X;Y;Z" format.
        If direction = X/Y/Z but value_1 is not specified.
        If distribution = TRAPEZ but value_2/vector_2 is not specified.

    Examples
    --------
    >>> from blueprints.saf import StructuralCurveActionFree, Direction, Distribution, CoordinateSystem, Location, Segment
    >>> # Uniform line load along a line
    >>> load = StructuralCurveActionFree(
    ...     name="LF1",
    ...     distribution=Distribution.UNIFORM,
    ...     direction=Direction.Z,
    ...     load_case="LC1",
    ...     coordinate_x="0.0;5.0",
    ...     coordinate_y="1.0;1.0",
    ...     coordinate_z="0.0;0.0",
    ...     segments="Line",
    ...     coordinate_system=CoordinateSystem.GLOBAL,
    ...     location=Location.LENGTH,
    ...     value_1=-50.0,
    ... )

    >>> # Trapezoidal load with curved path
    >>> trapezoidal = StructuralCurveActionFree(
    ...     name="LF2",
    ...     distribution=Distribution.TRAPEZ,
    ...     direction=Direction.Z,
    ...     load_case="LC1",
    ...     coordinate_x="0.0;2.5;5.0",
    ...     coordinate_y="0.0;1.0;0.0",
    ...     coordinate_z="0.0;0.0;0.0",
    ...     segments="Line;Circular arc",
    ...     coordinate_system=CoordinateSystem.GLOBAL,
    ...     location=Location.LENGTH,
    ...     value_1=-50.0,
    ...     value_2=-75.0,
    ... )
    """

    name: str
    distribution: Distribution
    direction: Direction
    load_case: str
    coordinate_x: str
    coordinate_y: str
    coordinate_z: str
    segments: str
    coordinate_system: CoordinateSystem
    location: Location
    value_1: float | None = None
    value_2: float | None = None
    vector_1: str | None = None
    vector_2: str | None = None
    action_type: str = ""
    id: str = ""

    _SINGLE_AXIS_DIRECTIONS: ClassVar[set[str]] = {"X", "Y", "Z"}
    _VECTOR_PATTERN: ClassVar[str] = ";"

    def __post_init__(self) -> None:
        """Validate conditional requirements based on SAF specification.

        Raises
        ------
        ValueError
            If SAF specification constraints are violated.
        """
        self._validate_direction_value_format()
        self._validate_distribution_requirements()

    def _validate_direction_value_format(self) -> None:
        """Validate that direction and value/vector format are consistent."""
        if self.direction == Direction.VECTOR:
            if self.vector_1 is None:
                raise ValueError("vector_1 must be specified when direction = Direction.VECTOR")
            if self._VECTOR_PATTERN not in self.vector_1:
                raise ValueError(f"vector_1 must be in 'X;Y;Z' format for Vector direction, got '{self.vector_1}'")
        elif self.direction.value in self._SINGLE_AXIS_DIRECTIONS:
            if self.value_1 is None:
                raise ValueError(f"value_1 must be specified when direction = {self.direction.value}")

    def _validate_distribution_requirements(self) -> None:
        """Validate requirements based on distribution type."""
        if self.distribution == Distribution.TRAPEZ:
            if self.direction == Direction.VECTOR:
                if self.vector_2 is None:
                    raise ValueError("vector_2 must be specified when distribution = TRAPEZ and direction = VECTOR")
            elif self.value_2 is None:
                raise ValueError("value_2 must be specified when distribution = TRAPEZ and direction != VECTOR")
