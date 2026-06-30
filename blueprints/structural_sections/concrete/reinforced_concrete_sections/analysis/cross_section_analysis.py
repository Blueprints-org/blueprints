"""Analyzer for reinforced-concrete cross-sections.

Owns a lazily built, cached backend section per analysis level so that ``ReinforcedCrossSection`` stays a
pure data object. Only the SLS uncracked analysis is available in this phase; cracked and ULS analyses
slot into the same cache without an API change.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from blueprints.structural_sections.concrete.reinforced_concrete_sections.analysis._adapter import (
    AnalysisLevel,
    analyse_uncracked,
    build_concrete_section,
)
from blueprints.structural_sections.concrete.reinforced_concrete_sections.analysis.results import StressStrainResult
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
        return analyse_uncracked(self._backend_section(AnalysisLevel.SLS), forces)

    def invalidate_cache(self) -> None:
        """Drop the cached backend sections, forcing a rebuild on the next analysis."""
        self._sections.clear()
