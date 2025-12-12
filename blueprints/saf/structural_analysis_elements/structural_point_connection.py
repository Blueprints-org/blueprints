"""Point connection (node) definition for structural analysis following SAF specification.

A node defines the geometry of the analytical model and serves as a connection point.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class StructuralPointConnection:
    """Structural point connection (node) following SAF specification.

    Definition following https://www.saf.guide/en/stable/structural-analysis-elements/structuralpointconnection.html.

    A node (point connection) defines a point in 3D space within the Global Coordinate System
    and serves as a connection point for structural members and supports.

    Attributes
    ----------
    name : str
        Human-readable unique identifier (e.g., "N1", "N2").
    x : float
        Position along X-axis in the Global Coordinate System [m].
    y : float
        Position along Y-axis in the Global Coordinate System [m].
    z : float
        Position along Z-axis in the Global Coordinate System [m].
    id : str, optional
        Unique identifier (UUID format recommended).

    Raises
    ------
    ValueError
        If name is empty.

    Examples
    --------
    >>> from blueprints.saf import StructuralPointConnection
    >>> # Create a node at the origin
    >>> node1 = StructuralPointConnection(
    ...     name="N1",
    ...     x=0.0,
    ...     y=0.0,
    ...     z=0.0,
    ... )

    >>> # Create a node above the origin
    >>> node2 = StructuralPointConnection(
    ...     name="N2",
    ...     x=5.0,
    ...     y=0.0,
    ...     z=3.5,
    ... )

    >>> # Create a node with UUID
    >>> node3 = StructuralPointConnection(
    ...     name="N3",
    ...     x=10.0,
    ...     y=5.0,
    ...     z=0.0,
    ...     id="39f238a5-01d0-45cf-a2eb-958170fd4f39",
    ... )
    """

    name: str
    x: float
    y: float
    z: float
    id: str = ""

    def __post_init__(self) -> None:
        """Validate point connection properties.

        Raises
        ------
        ValueError
            If required fields are invalid.
        """
        if not self.name:
            raise ValueError("name cannot be empty")

    def distance_to(self, other: "StructuralPointConnection") -> float:
        """Calculate Euclidean distance to another node.

        Parameters
        ----------
        other : StructuralPointConnection
            The other node to calculate distance to.

        Returns
        -------
        float
            Distance in meters.

        Raises
        ------
        TypeError
            If other is not a StructuralPointConnection.
        """
        if not isinstance(other, StructuralPointConnection):
            raise TypeError("other must be a StructuralPointConnection")

        dx = self.x - other.x
        dy = self.y - other.y
        dz = self.z - other.z
        return (dx**2 + dy**2 + dz**2) ** 0.5
