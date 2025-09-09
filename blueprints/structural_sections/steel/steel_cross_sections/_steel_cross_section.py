"""Base class of all steel cross-sections."""

from abc import ABC
from collections.abc import Sequence
from dataclasses import dataclass, field

from shapely.geometry import Polygon
from shapely.geometry.base import BaseGeometry
from shapely.geometry.polygon import orient

from blueprints.structural_sections._cross_section import CrossSection
from blueprints.structural_sections.steel.steel_element import SteelElement
from blueprints.type_alias import KG_M, MPA


@dataclass(kw_only=True)
class CombinedSteelCrossSection(CrossSection, ABC):
    """Base class of all steel cross-sections.

    Parameters
    ----------
    elements : Sequence[SteelElement], optional
        A sequence of steel elements that make up the cross-section.
        Default is an empty list.
    name : str, optional
        The name of the cross-section. Default is "Combined Steel Cross Section".
    """

    elements: Sequence[SteelElement] = field(default_factory=list)
    name: str = "Combined Steel Cross Section"

    @property
    def polygon(self) -> Polygon:
        """Return the polygon of the steel cross-section."""
        # check if there are any elements
        if not self.elements:
            raise ValueError("No elements have been added to the cross-section.")

        # return the polygon of the first element if there is only one
        if len(self.elements) == 1:
            return self.elements[0].cross_section.polygon

        # Combine the polygons of all elements if there is multiple
        combined_polygon: BaseGeometry = self.elements[0].cross_section.polygon
        for element in self.elements[1:]:
            combined_polygon = combined_polygon.union(element.cross_section.polygon)

        # Ensure the result is a valid Polygon
        if not isinstance(combined_polygon, Polygon):
            raise TypeError("The combined geometry is not a valid Polygon.")

        # Ensure consistent orientation
        return orient(combined_polygon)

    @property
    def weight_per_meter(self) -> KG_M:
        """
        Calculate the weight per meter of the steel element.

        Returns
        -------
        KG_M
            The weight per meter of the steel element.
        """
        return sum(element.weight_per_meter for element in self.elements)

    @property
    def yield_strength(self) -> MPA:
        """
        Calculate the yield strength of the steel element.

        This is the minimum yield strength of all elements in the cross-section.

        Returns
        -------
        MPa
            The yield strength of the steel element.
        """
        return min(element.yield_strength for element in self.elements)

    @property
    def ultimate_strength(self) -> MPA:
        """
        Calculate the ultimate strength of the steel element.

        This is the minimum ultimate strength of all elements in the cross-section.

        Returns
        -------
        MPa
            The ultimate strength of the steel element.
        """
        return min(element.ultimate_strength for element in self.elements)
