"""Module containing the class definition for a combined steel cross-section,
enabling cross-sections composed of multiple steel components with potentially different materials and geometries.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from blueprints.structural_sections.steel.steel_cross_section import SteelCrossSection
from blueprints.type_alias import KG_M, MPA


@dataclass(frozen=True)
class CombinedSteelCrossSection:
    """Representation of a combined steel cross-section made up of multiple steel cross-sections.

    Each steel cross-section can have its own geometry and material properties, including offsets and rotations.

    Parameters
    ----------
    steel_cross_sections : tuple[SteelCrossSection, ...]
        A tuple of SteelCrossSection instances.

    Usage example:
    >>> from blueprints.structural_sections.steel.combined_steel_cross_section import CombinedSteelCrossSection
    >>> from blueprints.structural_sections.steel.steel_cross_section import SteelCrossSection
    >>>
    >>> main_steel_cross_section = SteelCrossSection(profile=..., material=...)
    >>> stiffener = SteelCrossSection(profile=..., material=...)
    >>> # Create a combined steel cross-section with the main section and a stiffener.
    >>> combined_section = CombinedSteelCrossSection(steel_cross_sections=(main_steel_cross_section, stiffener))
    >>> # Alternatively, you can add sections one by one.
    >>> # This is useful for dynamically building complex cross-sections.
    >>> complex_combined_section = CombinedSteelCrossSection()
    >>> complex_combined_section = complex_combined_section.add_steel_cross_sections(steel_cross_section=main_steel_cross_section)
    >>> complex_combined_section = complex_combined_section.add_steel_cross_sections(steel_cross_section=stiffener)
    """

    steel_cross_sections: tuple[SteelCrossSection, ...] = field(default_factory=tuple)
    """Collection of steel cross-sections."""

    def __post_init__(self) -> None:
        """
        Validate the steel cross-sections after initialization.

        Raises
        ------
        TypeError
            If any item in steel_cross_sections is not an instance of SteelCrossSection.
        """
        if any(not isinstance(section, SteelCrossSection) for section in self.steel_cross_sections):
            raise TypeError("All items in steel_cross_sections must be instances of SteelCrossSection.")

    def add_steel_cross_sections(
        self,
        *steel_cross_sections: SteelCrossSection,
    ) -> CombinedSteelCrossSection:
        """
        Add steel cross-sections to the combined cross-section.

        Parameters
        ----------
        steel_cross_sections : SteelCrossSection
            The steel cross-sections to add.

        Returns
        -------
        CombinedSteelCrossSection
            A new instance of CombinedSteelCrossSection with the added steel cross-sections.
        """
        return CombinedSteelCrossSection(steel_cross_sections=(*self.steel_cross_sections, *steel_cross_sections))

    @property
    def yield_strength(self) -> MPA:
        """
        Calculate the total yield strength of the combined steel cross-section.

        Returns
        -------
        MPA
            The total yield strength of the combined steel cross-section.
        """
        strengths = [section.yield_strength for section in self.steel_cross_sections if section.yield_strength]
        return min(strengths)

    @property
    def ultimate_strength(self) -> MPA:
        """
        Calculate the total ultimate strength of the combined steel cross-section.

        Returns
        -------
        MPA
            The total ultimate strength of the combined steel cross-section.
        """
        strengths = [section.ultimate_strength for section in self.steel_cross_sections if section.ultimate_strength]
        return min(strengths)

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
