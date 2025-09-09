"""Module for building and editing cross-sections."""

from collections.abc import Sequence

from shapely.geometry import Polygon
from shapely.geometry.base import BaseGeometry
from shapely.geometry.polygon import orient

from blueprints.structural_sections._cross_section import CrossSection


def merge_polygons(elements: Sequence[CrossSection]) -> Polygon:
    """Return the polygon of the steel cross-section."""
    # check if there are any elements
    if not elements:
        raise ValueError("No elements have been added to the cross-section.")

    # return the polygon of the first element if there is only one
    if len(elements) == 1:
        return elements[0].polygon

    # Combine the polygons of all elements if there is multiple
    combined_polygon: BaseGeometry = elements[0].polygon
    for element in elements[1:]:
        combined_polygon = combined_polygon.union(element.polygon)

    # Ensure the result is a valid Polygon
    if not isinstance(combined_polygon, Polygon):
        raise TypeError("The combined geometry is not a valid Polygon.")

    # Ensure consistent orientation
    return orient(combined_polygon)
