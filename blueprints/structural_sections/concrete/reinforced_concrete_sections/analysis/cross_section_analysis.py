"""Analyzer for reinforced-concrete cross-sections.

Owns a lazily built, cached backend section per configuration so that ``ReinforcedCrossSection`` stays a
pure data object. One backend section is cached per (analysis level, elastic modulus) pair, so SLS
analyses with and without creep live next to each other and a future ULS section slots in without an
API change.
"""

from __future__ import annotations

import math
from dataclasses import replace
from typing import TYPE_CHECKING, Literal

from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_7_serviceability_limit_state.formula_7_18 import Form7Dot18DeformationParameter
from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_7_serviceability_limit_state.formula_7_19 import Form7Dot19DistributionCoefficient
from blueprints.structural_sections.concrete.reinforced_concrete_sections.analysis._adapter import (
    AnalysisLevel,
    SteelBranch,
    analyse_cracked,
    analyse_ultimate,
    analyse_uncracked,
    axial_capacities,
    biaxial_interaction,
    build_concrete_section,
    effective_modulus,
    flexural_tensile_strength,
    moment_curvature,
    moment_interaction,
    ultimate_capacity,
)
from blueprints.structural_sections.concrete.reinforced_concrete_sections.analysis.results import (
    BiaxialInteractionResult,
    InteractionSurface,
    MomentCurvatureResult,
    MomentInteractionEnvelope,
    MomentInteractionResult,
    Regime,
    StressStrainResult,
    UltimateCapacityResult,
    UtilizationResult,
    VerificationDiagram,
)
from blueprints.structural_sections.concrete.reinforced_concrete_sections.base import ReinforcedCrossSection
from blueprints.structural_sections.section_forces import SectionForces

if TYPE_CHECKING:
    from concreteproperties import ConcreteSection

    from blueprints.type_alias import DEG, DIMENSIONLESS, KN, MPA


# EN 1992-1-1 art. 7.19 distribution-coefficient beta: 1.0 for a short-term single load, 0.5 for a
# sustained or cyclic load. A positive creep coefficient marks the sustained case.
_TENSION_STIFFENING_BETA_SHORT_TERM = 1.0
_TENSION_STIFFENING_BETA_SUSTAINED = 0.5

# Below this fraction of the larger component a moment component is treated as zero, so a nominally
# uniaxial trace stays uniaxial when reconstructing its direction.
_UNIAXIAL_TOLERANCE = 1e-3


def _curvature(result: StressStrainResult) -> float:
    """Curvature magnitude [1/mm] of a stress/strain result, from its strain-plane gradients."""
    plane = result.strain_plane
    # every SLS stress result carries a reconstructed strain plane.
    assert plane is not None
    return math.hypot(plane.kappa_y, plane.kappa_z)


def _dominant_moment_direction(result: MomentCurvatureResult) -> tuple[float, float]:
    """Unit ``(m_y, m_z)`` direction of the traced moment, snapping a negligible component to zero."""
    index = max(range(len(result.m)), key=lambda i: result.m[i])
    m_y, m_z = result.m_y[index], result.m_z[index]
    if abs(m_z) < _UNIAXIAL_TOLERANCE * abs(m_y):
        m_z = 0.0
    if abs(m_y) < _UNIAXIAL_TOLERANCE * abs(m_z):
        m_y = 0.0
    magnitude = math.hypot(m_y, m_z)
    return m_y / magnitude, m_z / magnitude


class CrossSectionAnalysis:
    """Compute strains and stresses of a reinforced cross-section from section forces."""

    def __init__(self, cross_section: ReinforcedCrossSection, *, steel_branch: SteelBranch = SteelBranch.HORIZONTAL) -> None:
        """Initialize the analyzer.

        Parameters
        ----------
        cross_section : ReinforcedCrossSection
            The reinforced cross-section to analyze (geometry + materials + longitudinal rebars).
        steel_branch : SteelBranch
            The plastic branch of the reinforcement design diagram used at ULS (EN 1992-1-1
            art. 3.2.7(2)): the simplified ``HORIZONTAL`` branch at f_yd (default), or the ``INCLINED``
            branch rising towards k*f_yd with the strain limit eps_ud = 0.9 * eps_uk. SLS analyses are
            unaffected.
        """
        self._cross_section = cross_section
        self._steel_branch = steel_branch
        self._sections: dict[tuple[AnalysisLevel, MPA | None], ConcreteSection] = {}

    def _backend_section(self, level: AnalysisLevel, elastic_modulus: MPA | None = None) -> ConcreteSection:
        """Return the cached backend section for the given configuration, building it on first use."""
        key = (level, elastic_modulus)
        if key not in self._sections:
            self._sections[key] = build_concrete_section(self._cross_section, level, elastic_modulus, self._steel_branch)
        return self._sections[key]

    def stress(self, forces: SectionForces, *, regime: Regime = Regime.AUTO, creep_coefficient: DIMENSIONLESS = 0.0) -> StressStrainResult:
        """Compute the stress/strain state of the section for the given forces.

        With ``regime=Regime.AUTO`` (the default) the analyzer decides between the SLS regimes: it runs
        the (cheap) uncracked analysis first and switches to the cracked analysis when the maximum
        concrete tensile stress exceeds the flexural tensile strength f_ctm,fl. This handles combined
        N + M naturally (compression raises the threshold, tension lowers the demand margin). Passing
        ``Regime.SLS_UNCRACKED`` or ``Regime.SLS_CRACKED`` forces that regime instead.

        ``Regime.ULS`` computes the ultimate stress/strain state belonging to the design action: the
        bending direction follows from the moment vector, and the strain plane pivots on the concrete
        crushing strain with the neutral axis iterated to balance the axial force. The reported stresses
        are the design stress blocks of that failure state (at M_Rd), not scaled to the moment
        magnitude. ULS is never selected automatically.

        Creep enters through the effective modulus E_c,eff = E_cm / (1 + phi): a positive creep
        coefficient softens the concrete, which deepens the neutral axis, raises the steel stress and can
        flip the uncracked/cracked decision. The cracking threshold f_ctm,fl itself is unaffected by
        creep. The creep coefficient only applies to the SLS regimes; at ULS it is ignored (design
        materials).

        Parameters
        ----------
        forces : SectionForces
            The section forces in Blueprints conventions (kN/kNm, tension positive).
        regime : Regime
            The analysis regime: ``AUTO`` (decide between the SLS regimes), ``SLS_UNCRACKED``,
            ``SLS_CRACKED`` or ``ULS``.
        creep_coefficient : DIMENSIONLESS
            The creep coefficient phi (>= 0) [-]. ``0.0`` is the short-term analysis with E_cm.

        Returns
        -------
        StressStrainResult
            The stress/strain result; its ``regime`` field states which regime actually produced it.

        Raises
        ------
        ValueError
            If the creep coefficient is negative, if a cracked or ULS analysis is requested (or reached
            via ``AUTO``) without longitudinal reinforcement, or if the ULS state cannot reach
            equilibrium.
        """
        if regime is Regime.SLS_CRACKED:
            self._require_rebars()
        if regime is Regime.ULS:
            self._require_rebars("Ultimate stress analysis")

        elastic_modulus = effective_modulus(self._cross_section.concrete_material, creep_coefficient)
        polygon = self._cross_section.profile.polygon

        if regime is Regime.ULS:
            return analyse_ultimate(self._backend_section(AnalysisLevel.ULS), forces, self._cross_section.concrete_material.e_cm, polygon)

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

    def bending_capacity(self, *, n: KN = 0.0, theta: DEG = 0.0) -> UltimateCapacityResult:
        """Compute the ultimate (ULS) bending capacity at a given axial force and neutral-axis angle.

        Uses the design materials (parabola-rectangle or bilinear concrete at f_cd, reinforcement at
        f_yd with the analyzer's ``steel_branch``). The strain plane pivots on the concrete crushing
        strain eps_cu3 at the extreme compression fibre and the neutral-axis depth is iterated until the
        internal axial force balances ``n``.

        Parameters
        ----------
        n : KN
            The axial force at which to compute the capacity, compression negative / tension positive
            [kN]. Defaults to pure bending.
        theta : DEG
            The neutral-axis angle, measured counter-clockwise from the section x-axis [deg]. ``0``
            gives the sagging capacity about the y-axis (tension at the bottom), ``180`` the hogging
            capacity, ``90`` bending about the z-axis.

        Returns
        -------
        UltimateCapacityResult
            The design bending capacity in Blueprints conventions.

        Raises
        ------
        ValueError
            If the cross-section has no longitudinal reinforcement, or if the neutral-axis iteration
            cannot reach equilibrium (an axial force beyond the squash or tensile capacity).
        """
        self._require_rebars("Ultimate capacity analysis")
        return ultimate_capacity(self._backend_section(AnalysisLevel.ULS), n, theta)

    def interaction(self, *, theta: DEG = 0.0, n_points: int = 24) -> MomentInteractionResult:
        """Generate the uniaxial N-M interaction diagram for a fixed neutral-axis angle.

        The diagram runs from the pure-compression (squash) point to the zero-curvature tension point,
        including the pure-compression, balanced and pure-bending control points. Each point is an
        ultimate capacity (design materials) at a different axial force.

        Parameters
        ----------
        theta : DEG
            The neutral-axis angle, measured counter-clockwise from the section x-axis [deg]. ``0``
            for sagging about the y-axis, ``90`` for bending about the z-axis.
        n_points : int
            Number of points to compute including and between the diagram limits.

        Returns
        -------
        MomentInteractionResult
            The N-M interaction diagram in Blueprints conventions, with a ``plot()`` method.

        Raises
        ------
        ValueError
            If the cross-section has no longitudinal reinforcement, or if a diagram point cannot reach
            equilibrium.
        """
        self._require_rebars("Interaction analysis")
        return moment_interaction(self._backend_section(AnalysisLevel.ULS), theta, n_points)

    def interaction_envelope(self, *, axis: Literal["y", "z"] = "y", n_points: int = 24) -> MomentInteractionEnvelope:
        """Generate the closed uniaxial N-M interaction envelope about a single bending axis.

        Where :meth:`interaction` traces one neutral-axis angle — a single side of the envelope — this
        combines the positive- and negative-moment branches into one closed loop, the familiar closed
        "N-M resultant" interaction envelope. For ``axis="y"`` it runs the sagging
        (``theta=0``) and hogging (``theta=180``) branches; for ``axis="z"`` the ``theta=90`` and
        ``theta=-90`` branches. The plotted moment keeps its sign, so an asymmetrically reinforced
        section shows its two different capacities rather than one branch mirrored.

        Parameters
        ----------
        axis : str
            The bending axis of the envelope: ``"y"`` (sagging/hogging about the y-axis) or ``"z"``
            (about the z-axis).
        n_points : int
            Number of points per branch, forwarded to :meth:`interaction`; the closed loop carries
            roughly twice this number.

        Returns
        -------
        MomentInteractionEnvelope
            The closed N-M interaction envelope in Blueprints conventions, with a ``plot()`` method.

        Raises
        ------
        ValueError
            If ``axis`` is not ``"y"`` or ``"z"``, if the cross-section has no longitudinal
            reinforcement, or if a branch point cannot reach equilibrium.
        """
        if axis not in ("y", "z"):
            raise ValueError(f"The bending axis must be 'y' or 'z', got {axis!r}.")
        positive_theta, negative_theta = (0.0, 180.0) if axis == "y" else (90.0, -90.0)
        positive = self.interaction(theta=positive_theta, n_points=n_points)
        negative = self.interaction(theta=negative_theta, n_points=n_points)
        return MomentInteractionEnvelope.from_branches(positive, negative, axis=axis)

    def interaction_surface(self, *, n_theta: int = 24, n_points: int = 24) -> InteractionSurface:
        """Build the ULS interaction surface in (N, M_y, M_z) by sweeping the neutral-axis angle.

        The surface is sampled as ``n_theta`` meridians over a full revolution, each a uniaxial N-M
        diagram at a fixed neutral-axis angle (:meth:`interaction`). It is the general parent of the
        fixed-angle diagram and the fixed-axial-force envelope: any planar section is sliced from it, such
        as the fixed-axial-force ring (:meth:`~...InteractionSurface.ring`) or the fixed-direction
        N-M resultant section (:meth:`~...InteractionSurface.section_resultant`).

        The build runs one interaction diagram per angle, so it is heavier than a single diagram; its
        slicing uses interpolation, so the surface is a visualization tool. The governing unity check
        stays on the exact routines (:meth:`bending_capacity`, :meth:`biaxial_interaction`).

        Parameters
        ----------
        n_theta : int
            Number of neutral-axis angles sampled over ``[0, 360)``. An even value places meridians
            exactly on the principal directions (0, 90, 180, 270 deg).
        n_points : int
            Number of points per meridian, forwarded to :meth:`interaction`.

        Returns
        -------
        InteractionSurface
            The sampled interaction surface, with ``ring`` and ``section_resultant`` slicing methods.

        Raises
        ------
        ValueError
            If the cross-section has no longitudinal reinforcement, or if a meridian cannot be computed.
        """
        self._require_rebars("Interaction surface analysis")
        thetas = tuple(index * 360.0 / n_theta for index in range(n_theta))
        meridians = tuple(self.interaction(theta=theta, n_points=n_points) for theta in thetas)
        return InteractionSurface(thetas=thetas, meridians=meridians, raw=None)

    def biaxial_interaction(self, *, n: KN = 0.0, n_points: int = 48) -> BiaxialInteractionResult:
        """Generate the biaxial M_y-M_z interaction envelope at a fixed axial force.

        The envelope traverses the neutral-axis angle over a full revolution; each point is the ultimate
        bending capacity (design materials) at that angle for the fixed axial force.

        Parameters
        ----------
        n : KN
            The fixed axial force, compression negative / tension positive [kN]. Defaults to pure
            bending.
        n_points : int
            Number of neutral-axis angles to compute over the full revolution. The envelope cost grows
            linearly with this number.

        Returns
        -------
        BiaxialInteractionResult
            The biaxial envelope in Blueprints conventions, with a ``plot()`` method.

        Raises
        ------
        ValueError
            If the cross-section has no longitudinal reinforcement, or if an envelope point cannot
            reach equilibrium (an axial force beyond the squash or tensile capacity).
        """
        self._require_rebars("Biaxial interaction analysis")
        return biaxial_interaction(self._backend_section(AnalysisLevel.ULS), n, n_points)

    def moment_curvature(
        self, *, theta: DEG = 0.0, n: KN = 0.0, creep_coefficient: DIMENSIONLESS = 0.0, tension_stiffening: bool = False
    ) -> MomentCurvatureResult:
        """Trace the moment-curvature response at a fixed axial force and neutral-axis angle.

        The curve is computed with the design material set: concrete bilinear-horizontal at f_cd with a
        tension branch up to f_ctm,fl (producing the cracking kink), reinforcement at f_yd with the
        analyzer's ``steel_branch``. The trace ends when a material reaches its ultimate strain, so the
        peak moment corresponds to the ultimate capacity.

        Creep follows the same mental model as :meth:`stress`: ``creep_coefficient=0.0`` is the
        short-term curve with E_cm; a positive value softens the elastic branch to
        E_c,eff = E_cm / (1 + phi), producing the long-term curve.

        With ``tension_stiffening=True`` the returned curvatures are the **mean** curvatures of
        EN 1992-1-1 art. 7.4.3: the concrete between cracks keeps carrying tension, so the bare cracked
        curvature is blended with the uncracked one through the distribution coefficient zeta
        (Expression 7.19), giving the stiffer curve used for deflections (Expression 7.18). The
        distribution factor beta is 1.0 for a short-term load and 0.5 when creep marks a sustained load.
        Without it (the default) the curve is the bare section response.

        Parameters
        ----------
        theta : DEG
            The neutral-axis angle, measured counter-clockwise from the section x-axis [deg]. ``0``
            for sagging about the y-axis.
        n : KN
            The fixed axial force, compression negative / tension positive [kN].
        creep_coefficient : DIMENSIONLESS
            The creep coefficient phi (>= 0) [-]. ``0.0`` is the short-term curve.
        tension_stiffening : bool
            Apply the EN 1992-1-1 art. 7.4.3 tension-stiffening interpolation to the curvatures.
            Requires a uniaxial trace (bending about a single axis).

        Returns
        -------
        MomentCurvatureResult
            The moment-curvature response in Blueprints conventions, with a ``plot()`` method. Its
            ``tension_stiffening`` flag records whether the mean-curvature interpolation was applied.

        Raises
        ------
        ValueError
            If the creep coefficient is negative, if the cross-section has no longitudinal
            reinforcement, or if a curvature step cannot reach axial equilibrium.
        NotImplementedError
            If ``tension_stiffening`` is requested for a biaxial trace (the cracked analysis it relies
            on is uniaxial).
        """
        self._require_rebars("Moment-curvature analysis")
        elastic_modulus = effective_modulus(self._cross_section.concrete_material, creep_coefficient)
        section = self._backend_section(AnalysisLevel.ULS, None if creep_coefficient == 0.0 else elastic_modulus)
        result = moment_curvature(section, theta, n)
        if not tension_stiffening:
            return result
        return self._apply_tension_stiffening(result, n=n, creep_coefficient=creep_coefficient)

    def _apply_tension_stiffening(self, result: MomentCurvatureResult, *, n: KN, creep_coefficient: DIMENSIONLESS) -> MomentCurvatureResult:
        """Blend the traced (cracked) curvatures towards the uncracked state per EN 1992-1-1 art. 7.4.3.

        Above the cracking moment the traced curvature is the bare cracked response (1/r_II); the mean
        curvature is ``zeta * (1/r_II) + (1 - zeta) * (1/r_I)`` (Expression 7.18), with
        ``zeta = 1 - beta * (m_cr / M)^2`` (Expression 7.19, using the moment ratio as the stress ratio
        sigma_sr/sigma_s, equal for a linear cracked section). The uncracked curvature 1/r_I is linear in
        the moment, anchored on a single uncracked analysis. Below the cracking moment the section is
        uncracked and the traced curvature is returned unchanged.

        Parameters
        ----------
        result : MomentCurvatureResult
            The bare traced moment-curvature response.
        n : KN
            The fixed axial force of the trace [kN].
        creep_coefficient : DIMENSIONLESS
            The creep coefficient of the trace; a positive value selects the sustained beta = 0.5.

        Returns
        -------
        MomentCurvatureResult
            A copy of ``result`` with mean curvatures and ``tension_stiffening=True``.
        """
        reference_moment = 0.5 * result.m_ultimate
        m_y, m_z = _dominant_moment_direction(result)
        forces = SectionForces(n=n, m_y=m_y * reference_moment, m_z=m_z * reference_moment)
        cracked = self.stress(forces, regime=Regime.SLS_CRACKED, creep_coefficient=creep_coefficient)
        uncracked = self.stress(forces, regime=Regime.SLS_UNCRACKED, creep_coefficient=creep_coefficient)
        # SLS_CRACKED always carries the cracked properties (and thus the cracking moment).
        assert cracked.cracked_properties is not None
        cracking_moment = cracked.cracked_properties.m_cr
        uncracked_curvature = _curvature(uncracked)
        beta = _TENSION_STIFFENING_BETA_SUSTAINED if creep_coefficient > 0.0 else _TENSION_STIFFENING_BETA_SHORT_TERM

        mean_kappa: list[float] = []
        for cracked_kappa, moment in zip(result.kappa, result.m, strict=True):
            if moment <= cracking_moment:
                mean_kappa.append(cracked_kappa)  # uncracked branch: the traced curvature is already 1/r_I
                continue
            zeta = float(Form7Dot19DistributionCoefficient(beta=beta, sigma_sr=cracking_moment, sigma_s=moment))
            uncracked_kappa = uncracked_curvature * moment / reference_moment  # 1/r_I is linear in the moment
            mean_kappa.append(float(Form7Dot18DeformationParameter(zeta=zeta, alpha_ll=cracked_kappa, alpha_l=uncracked_kappa)))
        return replace(result, kappa=tuple(mean_kappa), tension_stiffening=True)

    def verify(self, forces_ed: SectionForces, *, n_points: int = 48) -> UtilizationResult:
        """Run the ULS unity check of a design action against the section's design capacity.

        The check picks its route from the design action: a pure axial force is checked against the
        squash or tensile capacity; a uniaxial moment against the bending capacity at the design axial
        force (N-M interaction included) in the matching direction (sagging, hogging or about the
        z-axis); and a biaxial moment pair against the biaxial envelope at the design axial force,
        intersected along the design moment direction.

        Parameters
        ----------
        forces_ed : SectionForces
            The ULS design action in Blueprints conventions (kN/kNm, tension positive).
        n_points : int
            Number of envelope points for the biaxial route; unused for the axial and uniaxial routes.

        Returns
        -------
        UtilizationResult
            The unity check result, with the governing check and the capacities used.

        Raises
        ------
        ValueError
            If the cross-section has no longitudinal reinforcement.
        """
        self._require_rebars("Verification")
        n_compression, n_tension = axial_capacities(self._cross_section)
        n_ed = forces_ed.n
        n_rd: KN | None = None
        axial_ratio = 0.0
        if n_ed < 0:
            n_rd, axial_ratio = n_compression, n_ed / n_compression
        elif n_ed > 0:
            n_rd, axial_ratio = n_tension, n_ed / n_tension

        m_ed = math.hypot(forces_ed.m_y, forces_ed.m_z)
        if m_ed == 0.0:
            return UtilizationResult(forces=forces_ed, utilization=axial_ratio, governing="axial", n_rd=n_rd, m_ed=0.0, m_rd=None)
        if axial_ratio >= 1.0:
            # beyond the axial capacity no bending equilibrium exists; the axial check governs outright
            return UtilizationResult(forces=forces_ed, utilization=axial_ratio, governing="axial", n_rd=n_rd, m_ed=m_ed, m_rd=None)

        if forces_ed.m_y != 0.0 and forces_ed.m_z != 0.0:
            envelope = self.biaxial_interaction(n=n_ed, n_points=n_points)
            m_rd = envelope.capacity_along(forces_ed.m_y, forces_ed.m_z)
            governing = "biaxial bending"
        else:
            theta: DEG = (0.0 if forces_ed.m_y > 0 else 180.0) if forces_ed.m_y != 0.0 else (90.0 if forces_ed.m_z > 0 else -90.0)
            m_rd = self.bending_capacity(n=n_ed, theta=theta).m_rd
            governing = "uniaxial bending"
        return UtilizationResult(forces=forces_ed, utilization=m_ed / m_rd, governing=governing, n_rd=n_rd, m_ed=m_ed, m_rd=m_rd)

    def verification_diagram(self, forces_ed: SectionForces, *, n_theta: int = 24, n_points: int = 24, n_levels: int = 48) -> VerificationDiagram:
        """Draw the ULS unity check of a design action on the capacity section along its moment direction.

        Runs the exact unity check (:meth:`verify`) and slices the resultant capacity section
        (:meth:`~...InteractionSurface.section_resultant`) along the design moment direction, so the
        returned diagram plots the design action and the capacity as two markers on one N-M axes with the
        utilization. The check needs a bending action: a pure axial design action, or one beyond the axial
        capacity, has no moment section to draw.

        Building the surface runs one interaction diagram per angle, so this is heavier than a single
        capacity call; the capacity marker itself comes from the exact :meth:`verify`, not from the
        interpolated loop.

        Parameters
        ----------
        forces_ed : SectionForces
            The ULS design action in Blueprints conventions (kN/kNm, tension positive).
        n_theta : int
            Number of neutral-axis angles for the surface, forwarded to :meth:`interaction_surface`.
        n_points : int
            Number of points per meridian, forwarded to :meth:`interaction_surface`.
        n_levels : int
            Number of axial levels for the section slice.

        Returns
        -------
        VerificationDiagram
            The verification diagram, with a ``plot()`` method.

        Raises
        ------
        ValueError
            If the cross-section has no longitudinal reinforcement, or if the design action is pure axial
            or beyond the axial capacity (no bending section to draw).
        """
        utilization = self.verify(forces_ed)
        if utilization.m_rd is None:
            raise ValueError(
                "A verification diagram needs a bending design action; the given action is pure axial or beyond the "
                "axial capacity, so there is no moment section to draw. Use verify() for the axial check."
            )
        surface = self.interaction_surface(n_theta=n_theta, n_points=n_points)
        section = surface.section_resultant(m_y=forces_ed.m_y, m_z=forces_ed.m_z, n_levels=n_levels)
        return VerificationDiagram(section=section, utilization=utilization)

    def _require_rebars(self, analysis: str = "Cracked analysis") -> None:
        """Raise a clear error when an analysis needs longitudinal reinforcement and there is none."""
        if not self._cross_section.longitudinal_rebars:
            raise ValueError(f"{analysis} requires at least one longitudinal rebar in the cross-section.")

    def invalidate_cache(self) -> None:
        """Drop the cached backend sections, forcing a rebuild on the next analysis."""
        self._sections.clear()
