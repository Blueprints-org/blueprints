"""Storey definition for structural analysis following SAF specification.

Represents floor levels or storeys in a structural model.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class StructuralStorey:
    """Structural storey (floor level) following SAF specification.

    Definition following https://www.saf.guide/en/stable/structural-analysis-elements/structuralstorey.html.

    A storey represents a floor level or horizontal plane in a structural model,
    defined by a height elevation.

    Attributes
    ----------
    name : str
        Human-readable unique identifier (e.g., "Ground Floor", "Level 1").
    height_level : float
        Elevation measurement in meters where zero refers to the global coordinate
        system origin (typically the XY plane). Can be negative for below-origin storeys.
    id : str, optional
        Unique identifier (UUID format recommended).

    Raises
    ------
    ValueError
        If name is empty.

    Examples
    --------
    >>> from blueprints.saf import StructuralStorey
    >>> # Ground floor at origin
    >>> ground_floor = StructuralStorey(
    ...     name="Ground Floor",
    ...     height_level=0.0,
    ... )

    >>> # First floor 3.5 meters above ground
    >>> level_1 = StructuralStorey(
    ...     name="Level 1",
    ...     height_level=3.5,
    ... )

    >>> # Basement 2 meters below ground
    >>> basement = StructuralStorey(
    ...     name="Basement",
    ...     height_level=-2.0,
    ... )

    >>> # With UUID identifier
    >>> level_2 = StructuralStorey(
    ...     name="Level 2",
    ...     height_level=7.0,
    ...     id="39f238a5-01d0-45cf-a2eb-958170fd4f39",
    ... )
    """

    name: str
    height_level: float
    id: str = ""

    def __post_init__(self) -> None:
        """Validate storey properties.

        Raises
        ------
        ValueError
            If SAF specification constraints are violated.
        """
        if not self.name:
            raise ValueError("name cannot be empty")
