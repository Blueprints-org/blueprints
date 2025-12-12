"""Composite shape definition for structural analysis following SAF specification.

Defines composite shape geometry for cross-sections when type is General.
"""

from dataclasses import dataclass
from typing import NamedTuple


class PolygonContour(NamedTuple):
    """Individual polygon contour coordinates.

    Attributes
    ----------
    coordinates : tuple[tuple[float, float], ...]
        Sequence of (y, z) coordinate pairs in mm defining the polygon.
    material_name : str, optional
        Reference to StructuralMaterial name (not required for openings).
    is_opening : bool
        True if this is an opening/hole (clockwise), False if solid (counter-clockwise).
    """

    coordinates: tuple[tuple[float, float], ...]
    material_name: str = ""
    is_opening: bool = False


@dataclass(frozen=True)
class CompositeShapeDef:
    """Composite shape definition following SAF specification.

    Definition following https://www.saf.guide/en/stable/structural-analysis-elements/compositeshapedef.html.

    Defines composite shape geometry for cross-sections. Used when cross-section type is General,
    and optionally for other types. Supports multiple polygons with openings.

    Attributes
    ----------
    name : str
        Profile name reference from StructuralCrossSection (e.g., "GEN_1").
    polygons : tuple[PolygonContour, ...]
        Sequence of polygon contours defining the shape.
        Each polygon contains coordinates and optional material reference.
        At least one solid polygon (non-opening) is required.
    id : str, optional
        Unique identifier (UUID format recommended).

    Raises
    ------
    ValueError
        If name is empty.
        If no polygons are defined.
        If no solid polygons exist (only openings).
        If more than 99 polygons are provided.
        If any polygon has fewer than 3 coordinates (not a valid polygon).
        If solid polygon has no material reference.
        If contour is not closed (first and last coordinates differ).

    Examples
    --------
    >>> from blueprints.saf import CompositeShapeDef, PolygonContour
    >>> # Simple rectangular cross-section
    >>> contour = PolygonContour(
    ...     coordinates=(
    ...         (-100.0, 0.0),
    ...         (-100.0, 200.0),
    ...         (100.0, 200.0),
    ...         (100.0, 0.0),
    ...     ),
    ...     material_name="S235",
    ...     is_opening=False,
    ... )
    >>> shape = CompositeShapeDef(
    ...     name="GEN_1",
    ...     polygons=(contour,),
    ... )

    >>> # Rectangular with circular opening
    >>> solid = PolygonContour(
    ...     coordinates=(
    ...         (-100.0, 0.0),
    ...         (-100.0, 200.0),
    ...         (100.0, 200.0),
    ...         (100.0, 0.0),
    ...     ),
    ...     material_name="S235",
    ...     is_opening=False,
    ... )
    >>> opening = PolygonContour(
    ...     coordinates=(
    ...         (-20.0, 100.0),
    ...         (-20.0, 120.0),
    ...         (20.0, 120.0),
    ...         (20.0, 100.0),
    ...     ),
    ...     is_opening=True,
    ... )
    >>> shape_with_opening = CompositeShapeDef(
    ...     name="GEN_2",
    ...     polygons=(solid, opening),
    ... )
    """

    name: str
    polygons: tuple[PolygonContour, ...]
    id: str = ""

    def __post_init__(self) -> None:
        """Validate composite shape definition.

        Raises
        ------
        ValueError
            If SAF specification constraints are violated.
        """
        if not self.name:
            raise ValueError("name cannot be empty")

        if not self.polygons:
            raise ValueError("polygons must contain at least one polygon")

        if len(self.polygons) > 99:
            raise ValueError("Maximum 99 polygons allowed per composite shape")

        # Track if at least one solid polygon exists
        has_solid_polygon = False

        for i, polygon in enumerate(self.polygons):
            self._validate_polygon(polygon, i)
            if not polygon.is_opening:
                has_solid_polygon = True

        if not has_solid_polygon:
            raise ValueError("At least one solid polygon (non-opening) is required per shape")

    def _validate_polygon(self, polygon: PolygonContour, index: int) -> None:
        """Validate individual polygon contour.

        Raises
        ------
        ValueError
            If polygon violates SAF specification constraints.
        """
        if len(polygon.coordinates) < 3:
            raise ValueError(f"Polygon {index} must have at least 3 coordinates (minimum valid polygon is a triangle)")

        # Validate that contour is closed
        if polygon.coordinates[0] != polygon.coordinates[-1]:
            raise ValueError(f"Polygon {index} must be closed (first and last coordinates must be identical)")

        # Validate solid polygons have material reference
        if not polygon.is_opening and not polygon.material_name:
            raise ValueError(f"Solid polygon {index} must have a material_name reference")

        # Validate coordinate format (each should be (y, z) tuple)
        for coord_idx, coord in enumerate(polygon.coordinates):
            if not isinstance(coord, tuple) or len(coord) != 2:
                raise ValueError(f"Polygon {index}, coordinate {coord_idx} must be a (y, z) tuple")
            y, z = coord
            # Validate that coordinates are numeric
            try:
                float(y)
                float(z)
            except (TypeError, ValueError):
                raise ValueError(f"Polygon {index}, coordinate {coord_idx} ({y}, {z}) must contain numeric values")

    def validate_contour_string(self, contour_string: str) -> tuple[tuple[float, float], ...]:
        """Validate and parse contour coordinate string.

        Expected format: "y1; z1|y2; z2|yi; zi"

        Parameters
        ----------
        contour_string : str
            Semicolon and pipe delimited coordinate string.

        Returns
        -------
        tuple[tuple[float, float], ...]
            Parsed (y, z) coordinate pairs.

        Raises
        ------
        ValueError
            If format is invalid.
        """
        if not contour_string:
            raise ValueError("contour_string cannot be empty")

        pairs = contour_string.split("|")
        coordinates = []

        for pair_idx, pair_raw in enumerate(pairs):
            pair = pair_raw.strip()
            if not pair:
                continue

            if ";" not in pair:
                raise ValueError(f'Invalid coordinate pair format "{pair}". Expected "y; z" format.')

            parts = pair.split(";")
            if len(parts) != 2:
                raise ValueError(f'Invalid coordinate pair format "{pair}". Should contain exactly one semicolon.')

            try:
                y = float(parts[0].strip())
                z = float(parts[1].strip())
                coordinates.append((y, z))
            except ValueError:
                raise ValueError(f"Coordinate pair {pair_idx} contains non-numeric values: {pair}")

        if len(coordinates) < 3:
            raise ValueError("At least 3 coordinate pairs required to form a valid polygon")

        return tuple(coordinates)
