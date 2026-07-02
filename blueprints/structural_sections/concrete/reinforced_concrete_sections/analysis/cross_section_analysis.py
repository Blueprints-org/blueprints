"""Analyzer for reinforced-concrete cross-sections.

Owns a lazily built, cached backend section per analysis level so that ``ReinforcedCrossSection`` stays a
pure data object. Only the SLS uncracked analysis is available in this phase; cracked and ULS analyses
slot into the same cache without an API change.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from blueprints.structural_sections.concrete.reinforced_concrete_sections.analysis._adapter import (
    AnalysisLevel,
    analyse_cracked,
    analyse_uncracked,
    build_concrete_section,
    flexural_tensile_strength,
)
from blueprints.structural_sections.concrete.reinforced_concrete_sections.analysis._adapter import (
    cracked_properties as _cracked_properties_backend,
)
from blueprints.structural_sections.concrete.reinforced_concrete_sections.analysis.results import CrackedProperties, StressStrainResult
from blueprints.structural_sections.concrete.reinforced_concrete_sections.base import ReinforcedCrossSection
from blueprints.structural_sections.section_forces import SectionForces

if TYPE_CHECKING:
    from concreteproperties import ConcreteSection


class CrossSectionAnalysis:
    """Compute strains and stresses of a reinforced cross-section from section forces."""

    def __init__(self, cross_section: ReinforcedCrossSection) -> None:
        """Initialize the analyzer.

        Parameters
        ----------
        cross_section : ReinforcedCrossSection
            The reinforced cross-section to analyze (geometry + materials + longitudinal rebars).
        """
        self._cross_section = cross_section
        self._sections: dict[AnalysisLevel, ConcreteSection] = {}

    def _backend_section(self, level: AnalysisLevel = AnalysisLevel.SLS) -> ConcreteSection:
        """Return the cached backend section for the given level, building it on first use."""
        if level not in self._sections:
            self._sections[level] = build_concrete_section(self._cross_section, level)
        return self._sections[level]

    def calculate_stress(self, forces: SectionForces) -> StressStrainResult:
        """Compute the stress/strain state, deciding between the uncracked and cracked regime.

        Runs the (cheap) uncracked analysis first; if the maximum concrete tensile stress exceeds the
        flexural tensile strength f_ctm,fl the section is considered cracked and the cracked result is
        returned. This handles combined N + M naturally (compression raises the threshold, tension lowers
        the demand margin).

        Parameters
        ----------
        forces : SectionForces
            The section forces in Blueprints conventions.

        Returns
        -------
        StressStrainResult
            The uncracked or cracked stress/strain result, whichever regime applies.
        """
        uncracked = self.uncracked_stress(forces)
        if uncracked.concrete_stress_max > flexural_tensile_strength(self._cross_section):
            return self.cracked_stress(forces)
        return uncracked

    def uncracked_stress(self, forces: SectionForces) -> StressStrainResult:
        """Compute the uncracked (gross transformed section) stress/strain state.

        Parameters
        ----------
        forces : SectionForces
            The section forces in Blueprints conventions.

        Returns
        -------
        StressStrainResult
            The uncracked stress/strain result, compression negative.
        """
        return analyse_uncracked(
            self._backend_section(AnalysisLevel.SLS),
            forces,
            self._cross_section.concrete_material.e_cm,
            self._cross_section.profile.polygon,
        )

    def cracked_stress(self, forces: SectionForces) -> StressStrainResult:
        """Compute the cracked stress/strain state.

        Parameters
        ----------
        forces : SectionForces
            The section forces in Blueprints conventions.

        Returns
        -------
        StressStrainResult
            The cracked stress/strain result, carrying the cracked properties.

        Raises
        ------
        ValueError
            If the cross-section has no longitudinal reinforcement.
        """
        self._require_rebars()
        return analyse_cracked(
            self._backend_section(AnalysisLevel.SLS),
            forces,
            self._cross_section.concrete_material.e_cm,
            self._cross_section.profile.polygon,
        )

    def cracked_properties(self, forces: SectionForces) -> CrackedProperties:
        """Compute the cracked-section properties for the given forces.

        Parameters
        ----------
        forces : SectionForces
            The section forces in Blueprints conventions.

        Returns
        -------
        CrackedProperties
            The cracked-section properties (cracking moment, neutral axis, cracked second moment).

        Raises
        ------
        ValueError
            If the cross-section has no longitudinal reinforcement.
        """
        self._require_rebars()
        return _cracked_properties_backend(self._backend_section(AnalysisLevel.SLS), forces, self._cross_section.concrete_material.e_cm)

    def _require_rebars(self) -> None:
        """Raise a clear error when a cracked analysis is requested without longitudinal reinforcement."""
        if not self._cross_section.longitudinal_rebars:
            raise ValueError("Cracked analysis requires at least one longitudinal rebar in the cross-section.")

    def invalidate_cache(self) -> None:
        """Drop the cached backend sections, forcing a rebuild on the next analysis."""
        self._sections.clear()
