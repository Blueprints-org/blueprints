"""Module containing the class definition for a combined steel cross-section,
enabling cross-sections composed of multiple steel components with potentially different materials and geometries.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from blueprints.structural_sections.steel.steel_cross_section import SteelCrossSection, SteelCrossSectionProtocol
from blueprints.type_alias import DEG, KG_M, MM


@dataclass(frozen=True, kw_only=True)
class CombinedSteelCrossSection(SteelCrossSectionProtocol):
    """Representation of a combined steel cross-section made up of multiple steel cross-sections.

    Usage example:
    >>> # Assuming main_steel_cross_section and stiffener are predefined SteelCrossSection instances
        combined_section = (
            CombinedSteelCrossSection()
            .add_steel_cross_section(
                steel_cross_section=main_steel_cross_section,
                x_offset=0,
                y_offset=0,
                rotation_angle=0,
            )
            .add_steel_cross_section(
                steel_cross_section=stiffener,
                x_offset=0,
                y_offset=main_steel_cross_section.cross_section.cross_section_height / 2 + stiffener.cross_section.cross_section_height / 2,
                rotation_angle=0,
            )
        )
    """

    _steel_cross_sections: tuple[SteelCrossSection, ...] = field(init=False, default_factory=tuple)
    """Collection of transformed steel cross-sections."""

    @property
    def steel_cross_sections(self) -> tuple[SteelCrossSection, ...]:
        """
        Get the transformed steel cross-sections that make up the combined cross-section.

        Returns
        -------
        tuple[SteelCrossSection, ...]
            The tuple of transformed steel cross-sections.
        """
        return self._steel_cross_sections

    @classmethod
    def _from_steel_cross_sections(
        cls,
        steel_cross_sections: tuple[SteelCrossSection, ...],
    ) -> CombinedSteelCrossSection:
        """
        Create a CombinedSteelCrossSection from a tuple of SteelCrossSection instances.

        Parameters
        ----------
        steel_cross_sections : tuple[SteelCrossSection, ...]
            A tuple of SteelCrossSection instances.

        Returns
        -------
        CombinedSteelCrossSection
            A new instance of CombinedSteelCrossSection.

        Raises
        ------
        ValueError
            If no SteelCrossSection instances are provided.
        TypeError
            If any item in steel_cross_sections is not an instance of SteelCrossSection.
        """
        combined_section = cls()
        if not steel_cross_sections:
            raise ValueError("At least one SteelCrossSection must be provided.")
        if any(not isinstance(section, SteelCrossSection) for section in steel_cross_sections):
            raise TypeError("All items in steel_cross_sections must be instances of SteelCrossSection.")
        object.__setattr__(combined_section, "_steel_cross_sections", steel_cross_sections)
        return combined_section

    def add_steel_cross_section(
        self,
        steel_cross_section: SteelCrossSection,
        x_offset: MM = 0.0,
        y_offset: MM = 0.0,
        rotation_angle: DEG = 0.0,
    ) -> CombinedSteelCrossSection:
        """
        Add a steel cross-section to the combined cross-section.

        Parameters
        ----------
        steel_cross_section : SteelCrossSection
            The steel cross-section to add.
        x_offset : MM
            The x-coordinate offset of the cross-section's centroid [mm].
        y_offset : MM
            The y-coordinate offset of the cross-section's centroid [mm].
        rotation_angle : DEG
            The rotation angle of the cross-section in degrees (counter-clockwise).

        Returns
        -------
        CombinedSteelCrossSection
            A new instance of CombinedSteelCrossSection with the added steel cross-section.
        """
        new_positioned_section = steel_cross_section._transform(  # noqa: SLF001
            x_offset=x_offset,
            y_offset=y_offset,
            rotation_angle=rotation_angle,
        )
        new_sections = (*self.steel_cross_sections, new_positioned_section)
        return CombinedSteelCrossSection._from_steel_cross_sections(new_sections)

    @property
    def weight_per_meter(self) -> KG_M:
        """
        Calculate the total weight per meter of the combined steel cross-section.

        Returns
        -------
        KG_M
            The total weight per meter of the combined steel cross-section.
        """
        return sum(section.weight_per_meter for section in self.steel_cross_sections)
