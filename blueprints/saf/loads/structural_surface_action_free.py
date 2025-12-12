"""Structural surface action free (free surface load) definitions following SAF specification.

Free surface loads are applied to slabs along a defined boundary and can affect multiple slabs.
"""

from dataclasses import dataclass
from enum import Enum
from typing import ClassVar


class Direction(str, Enum):
    """Direction of free surface action following SAF specification.

    Specifies the load direction axis.
    """

    X = "X"
    Y = "Y"
    Z = "Z"


class Distribution(str, Enum):
    """Distribution type of free surface action following SAF specification.

    Specifies how the load varies across the surface.
    """

    UNIFORM = "Uniform"
    DIRECTION_X = "DirectionX"
    DIRECTION_Y = "DirectionY"
    DIRECTION_XY = "DirectionXY"


class CoordinateSystem(str, Enum):
    """Coordinate system for free surface action following SAF specification.

    Global or local coordinate system reference.
    """

    GLOBAL = "Global"
    LOCAL = "Local"


class Location(str, Enum):
    """Location type for free surface action application following SAF specification.

    Specifies whether load is applied directly or as plan projection.
    """

    LENGTH = "Length"
    PROJECTION = "Projection"


class Edge(str, Enum):
    """Edge type for polygon segments following SAF specification.

    Specifies how polygon vertices are connected.
    """

    LINE = "Line"
    BEZIER = "Bezier"
    CIRCLE_ARC = "Circle arc"
    PARABOLIC_ARC = "Parabolic arc"
    SPLINE = "Spline"


@dataclass(frozen=True)
class StructuralSurfaceActionFree:
    """Structural surface action free following SAF specification.

    Definition following https://www.saf.guide/en/stable/loads/structuralsurfaceactionfree.html.

    A free surface action represents a distributed load applied to a slab along a specific
    boundary polygon. Unlike StructuralSurfaceAction which applies to the entire slab, free
    surface actions use polygon boundaries and can affect multiple slabs.

    Attributes
    ----------
    name : str
        Human-readable unique identifier (e.g., "FF1").
    direction : Direction
        Load direction: X, Y, or Z.
    distribution : Distribution
        Load variation pattern: Uniform, DirectionX, DirectionY, or DirectionXY.
    load_case : str
        Reference to StructuralLoadCase name.
    coordinate_x : str
        X-coordinates of polygon vertices in meters, semicolon-separated (e.g., "0.0;5.0;5.0;0.0").
    coordinate_y : str
        Y-coordinates of polygon vertices in meters, semicolon-separated (e.g., "0.0;0.0;3.0;3.0").
    coordinate_z : str
        Z-coordinates of polygon vertices in meters, semicolon-separated (e.g., "0.0;0.0;0.0;0.0").
    edges : str
        Connection types between vertices, semicolon-separated (e.g., "Line;Line;Line;Line").
    coordinate_system : CoordinateSystem
        Global or Local coordinate system.
    location : Location
        Load application method: Length or Projection.
    q : str
        Load magnitude in kN/m². Format depends on distribution:
        - Uniform: single value (e.g., "-10")
        - DirectionX/Y: two corner values (e.g., "C1:-5;C2:-7")
        - DirectionXY: three corner values (e.g., "C1:-3;C2:-2;C3:-1")
    action_type : str, optional
        Load classification (e.g., "Standard", "Wind", "Snow").
    id : str, optional
        Unique identifier (UUID format recommended).

    Raises
    ------
    ValueError
        If distribution = DirectionX/DirectionY but q does not contain exactly 2 corner values.
        If distribution = DirectionXY but q does not contain exactly 3 corner values.
        If distribution = Uniform but q contains corner value notation.

    Examples
    --------
    >>> from blueprints.saf import StructuralSurfaceActionFree, Direction, Distribution, CoordinateSystem, Location
    >>> # Uniform surface load on polygon
    >>> load = StructuralSurfaceActionFree(
    ...     name="FF1",
    ...     direction=Direction.Z,
    ...     distribution=Distribution.UNIFORM,
    ...     load_case="LC1",
    ...     coordinate_x="0.0;5.0;5.0;0.0",
    ...     coordinate_y="0.0;0.0;3.0;3.0",
    ...     coordinate_z="0.0;0.0;0.0;0.0",
    ...     edges="Line;Line;Line;Line",
    ...     coordinate_system=CoordinateSystem.GLOBAL,
    ...     location=Location.LENGTH,
    ...     q="-10",
    ... )

    >>> # DirectionX load with varying magnitude
    >>> directional_load = StructuralSurfaceActionFree(
    ...     name="FF2",
    ...     direction=Direction.Z,
    ...     distribution=Distribution.DIRECTION_X,
    ...     load_case="LC1",
    ...     coordinate_x="0.0;5.0;5.0;0.0",
    ...     coordinate_y="0.0;0.0;3.0;3.0",
    ...     coordinate_z="0.0;0.0;0.0;0.0",
    ...     edges="Line;Line;Line;Line",
    ...     coordinate_system=CoordinateSystem.GLOBAL,
    ...     location=Location.LENGTH,
    ...     q="C1:-5;C2:-7",
    ... )
    """

    name: str
    direction: Direction
    distribution: Distribution
    load_case: str
    coordinate_x: str
    coordinate_y: str
    coordinate_z: str
    edges: str
    coordinate_system: CoordinateSystem
    location: Location
    q: str
    action_type: str = ""
    id: str = ""

    _CORNER_PATTERN: ClassVar[str] = "C"
    _SEPARATOR: ClassVar[str] = ";"

    def __post_init__(self) -> None:
        """Validate conditional requirements based on SAF specification.

        Raises
        ------
        ValueError
            If SAF specification constraints are violated.
        """
        self._validate_distribution_q_format()

    def _validate_distribution_q_format(self) -> None:
        """Validate that distribution and q format are consistent."""
        has_corner_notation = self._CORNER_PATTERN in self.q

        if self.distribution == Distribution.UNIFORM and has_corner_notation:
            raise ValueError(f"q must be a single numeric value for Uniform distribution, not corner notation: '{self.q}'")
        if self.distribution == Distribution.DIRECTION_X:
            corner_count = self.q.count(self._CORNER_PATTERN)
            if corner_count != 2:
                raise ValueError(f"q must contain exactly 2 corner values (C1 and C2) for DirectionX distribution, got {corner_count}: '{self.q}'")
        if self.distribution == Distribution.DIRECTION_Y:
            corner_count = self.q.count(self._CORNER_PATTERN)
            if corner_count != 2:
                raise ValueError(f"q must contain exactly 2 corner values (C1 and C2) for DirectionY distribution, got {corner_count}: '{self.q}'")
        if self.distribution == Distribution.DIRECTION_XY:
            corner_count = self.q.count(self._CORNER_PATTERN)
            if corner_count != 3:
                raise ValueError(
                    f"q must contain exactly 3 corner values (C1, C2, and C3) for DirectionXY distribution, got {corner_count}: '{self.q}'"
                )
