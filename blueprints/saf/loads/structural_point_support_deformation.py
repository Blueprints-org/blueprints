"""Structural point support deformation definitions following SAF specification.

Point support deformation represents imposed deformation of a point support where
displacement or rotation can be applied to a structural point support.
"""

from dataclasses import dataclass
from enum import Enum


class Direction(str, Enum):
    """Direction of point support deformation following SAF specification.

    Specifies deformation axis: X/Y/Z for translation, Rx/Ry/Rz for rotation.
    """

    X = "X"
    Y = "Y"
    Z = "Z"
    RX = "Rx"
    RY = "Ry"
    RZ = "Rz"


@dataclass(frozen=True)
class StructuralPointSupportDeformation:
    """Structural point support deformation following SAF specification.

    Definition following https://www.saf.guide/en/stable/loads/structuralpointsupportdeformation.html.

    This element represents imposed deformation of a point support where displacement
    or rotation can be applied to a structural point support.

    Attributes
    ----------
    name : str
        Human-readable unique identifier (e.g., "RS1").
    point_support : str
        Reference to StructuralPointSupport element name (e.g., "Sn6").
    direction : Direction
        Deformation axis: X, Y, Z (translation) or Rx, Ry, Rz (rotation).
    load_case : str
        Associated load case name (e.g., "LC5").
    translation_value : float | None, optional
        Imposed translation in millimeters. Required when direction = X, Y, or Z.
    rotation_value : float | None, optional
        Imposed rotation in milliradians. Required when direction = Rx, Ry, or Rz.
    id : str, optional
        Unique identifier (UUID format recommended).

    Raises
    ------
    ValueError
        If direction = X/Y/Z but translation_value is not specified.
        If direction = Rx/Ry/Rz but rotation_value is not specified.
        If direction = X/Y/Z but rotation_value is also specified.
        If direction = Rx/Ry/Rz but translation_value is also specified.

    Examples
    --------
    >>> from blueprints.saf import StructuralPointSupportDeformation, Direction
    >>> # Applied translation in X direction
    >>> deform = StructuralPointSupportDeformation(
    ...     name="RS1",
    ...     point_support="Sn6",
    ...     direction=Direction.X,
    ...     load_case="LC5",
    ...     translation_value=10.0,
    ... )

    >>> # Applied rotation about Y axis
    >>> rotate = StructuralPointSupportDeformation(
    ...     name="RS2",
    ...     point_support="Sn6",
    ...     direction=Direction.RY,
    ...     load_case="LC5",
    ...     rotation_value=5.0,
    ... )
    """

    name: str
    point_support: str
    direction: Direction
    load_case: str
    translation_value: float | None = None
    rotation_value: float | None = None
    id: str = ""

    def __post_init__(self) -> None:
        """Validate conditional requirements based on SAF specification.

        Raises
        ------
        ValueError
            If SAF specification constraints are violated.
        """
        self._validate_direction_value_format()

    def _validate_direction_value_format(self) -> None:
        """Validate that direction and value format are consistent."""
        translation_directions = {Direction.X, Direction.Y, Direction.Z}
        rotation_directions = {Direction.RX, Direction.RY, Direction.RZ}

        if self.direction in translation_directions:
            if self.translation_value is None:
                raise ValueError(f"translation_value must be specified when direction = {self.direction.value}")
            if self.rotation_value is not None:
                raise ValueError(f"rotation_value should not be specified when direction = {self.direction.value}")
        elif self.direction in rotation_directions:
            if self.rotation_value is None:
                raise ValueError(f"rotation_value must be specified when direction = {self.direction.value}")
            if self.translation_value is not None:
                raise ValueError(f"translation_value should not be specified when direction = {self.direction.value}")
