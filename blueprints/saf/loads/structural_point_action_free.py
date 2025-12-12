"""Structural point action free (free point load) definitions following SAF specification.

Free point loads are applied to slabs at specific coordinates and may overlap
or affect multiple slabs.
"""

from dataclasses import dataclass
from enum import Enum
from typing import ClassVar


class Direction(str, Enum):
    """Direction of free point action following SAF specification.

    Specifies whether the action is applied in a single axis direction or as a vector.
    """

    X = "X"
    Y = "Y"
    Z = "Z"
    VECTOR = "Vector"


@dataclass(frozen=True)
class StructuralPointActionFree:
    """Structural point action free following SAF specification.

    Definition following https://www.saf.guide/en/stable/loads/structuralpointactionfree.html.

    A free point action represents a concentrated force applied at a specific global coordinate
    location on a slab. Unlike StructuralPointAction which references specific nodes or members,
    free point actions use absolute coordinates and may affect multiple slabs.

    Attributes
    ----------
    name : str
        Human-readable unique identifier (e.g., "FF1").
    direction : Direction
        Load direction: X, Y, Z, or Vector.
    load_case : str
        Reference to StructuralLoadCase name.
    coordinate_x : float
        Load point X-coordinate in meters.
    coordinate_y : float
        Load point Y-coordinate in meters.
    coordinate_z : float
        Load point Z-coordinate in meters.
    value : float | None, optional
        Load value in kN for single-axis directions (X/Y/Z).
        For Vector direction: use vector instead.
    vector : str | None, optional
        Load vector in "X;Y;Z" format in kN (e.g., "10;10;0").
        Required when direction = VECTOR.
    action_type : str, optional
        Load classification (e.g., "Standard", "Wind", "Snow", "Self weight").
    id : str, optional
        Unique identifier (UUID format recommended).

    Raises
    ------
    ValueError
        If direction = VECTOR but vector is not specified or not in "X;Y;Z" format.
        If direction = X/Y/Z but value is not specified.
        If direction = X/Y/Z but vector is in "X;Y;Z" format.

    Notes
    -----
    Only global coordinate system is supported for free point loads.

    Examples
    --------
    >>> from blueprints.saf import StructuralPointActionFree, Direction
    >>> # Point load in Z direction
    >>> load_z = StructuralPointActionFree(
    ...     name="FF1",
    ...     direction=Direction.Z,
    ...     load_case="LC1",
    ...     coordinate_x=0.0,
    ...     coordinate_y=1.0,
    ...     coordinate_z=3.25,
    ...     value=-50.0,
    ... )

    >>> # Vector load
    >>> load_vector = StructuralPointActionFree(
    ...     name="FF2",
    ...     direction=Direction.VECTOR,
    ...     load_case="LC1",
    ...     coordinate_x=2.5,
    ...     coordinate_y=3.0,
    ...     coordinate_z=2.0,
    ...     vector="10;10;-50",
    ... )
    """

    name: str
    direction: Direction
    load_case: str
    coordinate_x: float
    coordinate_y: float
    coordinate_z: float
    value: float | None = None
    vector: str | None = None
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

    def _validate_direction_value_format(self) -> None:
        """Validate that direction and value/vector format are consistent."""
        if self.direction == Direction.VECTOR:
            if self.vector is None:
                raise ValueError("vector must be specified when direction = Direction.VECTOR")
            if self._VECTOR_PATTERN not in self.vector:
                raise ValueError(f"vector must be in 'X;Y;Z' format for Vector direction, got '{self.vector}'")
        elif self.direction.value in self._SINGLE_AXIS_DIRECTIONS:
            if self.value is None:
                raise ValueError(f"value must be specified when direction = {self.direction.value}")
            if self._VECTOR_PATTERN in str(self.value):
                raise ValueError(f"value must be a single numeric value for {self.direction.value} direction, not vector format")
