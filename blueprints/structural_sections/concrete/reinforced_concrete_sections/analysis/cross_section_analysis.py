"""Analyzer for reinforced-concrete cross-sections.

Owns a lazily built, cached backend section per configuration so that ``ReinforcedCrossSection`` stays a
pure data object. One backend section is cached per (analysis level, elastic modulus) pair, so SLS
analyses with and without creep live next to each other and a future ULS section slots in without an
API change.

Scope: SLS strain/stress (uncracked and cracked). ULS capacity, interaction diagrams and
moment-curvature are a follow-up on the same analyzer.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from blueprints.structural_sections.concrete.reinforced_concrete_sections.analysis._adapter import (
    AnalysisLevel,
    analyse_cracked,
    analyse_uncracked,
    build_concrete_section,
    effective_modulus,
    flexural_tensile_strength,
)
from blueprints.structural_sections.concrete.reinforced_concrete_sections.analysis.results import (
    Regime,
    StressStrainResult,
)
from blueprints.structural_sections.concrete.reinforced_concrete_sections.base import ReinforcedCrossSection
from blueprints.structural_sections.section_forces import SectionForces

if TYPE_CHECKING:
    from concreteproperties import ConcreteSection

    from blueprints.type_alias import DIMENSIONLESS, MPA


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
        self._sections: dict[tuple[AnalysisLevel, MPA | None], ConcreteSection] = {}

    def _backend_section(self, level: AnalysisLevel, elastic_modulus: MPA | None = None) -> ConcreteSection:
        """Return the cached backend section for the given configuration, building it on first use."""
        key = (level, elastic_modulus)
        if key not in self._sections:
            self._sections[key] = build_concrete_section(self._cross_section, level, elastic_modulus)
        return self._sections[key]

    def stress(self, forces: SectionForces, *, regime: Regime = Regime.AUTO, creep_coefficient: DIMENSIONLESS = 0.0) -> StressStrainResult:
        """Compute the stress/strain state of the section for the given forces.

        With ``regime=Regime.AUTO`` (the default) the analyzer decides between the SLS regimes: it runs
        the (cheap) uncracked analysis first and switches to the cracked analysis when the maximum
        concrete tensile stress exceeds the flexural tensile strength f_ctm,fl. This handles combined
        N + M naturally (compression raises the threshold, tension lowers the demand margin). Passing
        ``Regime.SLS_UNCRACKED`` or ``Regime.SLS_CRACKED`` forces that regime instead.

        Creep enters through the effective modulus E_c,eff = E_cm / (1 + phi): a positive creep
        coefficient softens the concrete, which deepens the neutral axis, raises the steel stress and can
        flip the uncracked/cracked decision. The cracking threshold f_ctm,fl itself is unaffected by
        creep.

        Parameters
        ----------
        forces : SectionForces
            The section forces in Blueprints conventions (kN/kNm, tension positive).
        regime : Regime
            The analysis regime: ``AUTO`` (decide between the SLS regimes), ``SLS_UNCRACKED`` or
            ``SLS_CRACKED``.
        creep_coefficient : DIMENSIONLESS
            The creep coefficient phi (>= 0) [-]. ``0.0`` is the short-term analysis with E_cm.

        Returns
        -------
        StressStrainResult
            The stress/strain result; its ``regime`` field states which regime actually produced it.

        Raises
        ------
        ValueError
            If the creep coefficient is negative, or if a cracked analysis is requested (or reached via
            ``AUTO``) without longitudinal reinforcement.
        """
        if regime is Regime.SLS_CRACKED:
            self._require_rebars()

        elastic_modulus = effective_modulus(self._cross_section.concrete_material, creep_coefficient)
        polygon = self._cross_section.profile.polygon

        section = self._backend_section(AnalysisLevel.SLS, elastic_modulus)

        def notension_section() -> ConcreteSection:
            return self._backend_section(AnalysisLevel.SLS_CRACKED, elastic_modulus)

        if regime is Regime.SLS_CRACKED:
            return analyse_cracked(section, forces, elastic_modulus, polygon, notension_section)

        uncracked = analyse_uncracked(section, forces, elastic_modulus, polygon)
        if regime is Regime.AUTO and uncracked.concrete_stress_max > flexural_tensile_strength(self._cross_section):
            self._require_rebars()
            return analyse_cracked(section, forces, elastic_modulus, polygon, notension_section)
        return uncracked

    def _require_rebars(self, analysis: str = "Cracked analysis") -> None:
        """Raise a clear error when an analysis needs longitudinal reinforcement and there is none."""
        if not self._cross_section.longitudinal_rebars:
            raise ValueError(f"{analysis} requires at least one longitudinal rebar in the cross-section.")

    def invalidate_cache(self) -> None:
        """Drop the cached backend sections, forcing a rebuild on the next analysis."""
        self._sections.clear()
