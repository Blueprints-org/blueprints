"""Private adapter between Blueprints reinforced cross-sections and the ``concreteproperties`` backend.

This is the **only** module that imports ``concreteproperties``, so a future backend swap touches one file.

Unit and convention handling lives here: Blueprints uses kN/kNm, ‰ strain and a tension-positive sign
convention, while ``concreteproperties`` works in N/mm, absolute strain and compression-positive. The
material mappers below convert strains (‰ → ratio) and densities; force/sign conversion happens at the
analysis call site (added in a later step).
"""

import math
import warnings
from collections import defaultdict
from collections.abc import Callable, Iterator
from contextlib import contextmanager
from enum import Enum

import numpy as np

from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_3_materials.formula_3_23 import Form3Dot23FlexuralTensileStrength
from blueprints.materials.concrete import ConcreteMaterial, DiagramType
from blueprints.materials.reinforcement_steel import ReinforcementSteelMaterial
from blueprints.structural_sections.concrete.rebar import Rebar
from blueprints.structural_sections.concrete.reinforced_concrete_sections.analysis.results import (
    BiaxialInteractionResult,
    CrackedProperties,
    InteractionPoint,
    MomentCurvatureResult,
    MomentInteractionResult,
    RebarStressResult,
    Regime,
    StrainPlane,
    StressStrainResult,
    UltimateCapacityResult,
)
from blueprints.structural_sections.concrete.reinforced_concrete_sections.base import ReinforcedCrossSection
from blueprints.structural_sections.section_forces import SectionForces
from blueprints.type_alias import DEG, DIMENSIONLESS, KN, KNM, MM, MPA
from blueprints.unit_conversion import KN_TO_N, KNM_TO_NMM, MM3_TO_M3, N_TO_KN, NMM_TO_KNM, PER_MILLE_TO_RATIO, RATIO_TO_PER_MILLE

try:
    from concreteproperties import (
        BilinearStressStrain,
        Concrete,
        ConcreteLinear,
        ConcreteSection,
        EurocodeParabolicUltimate,
        SteelBar,
        SteelElasticPlastic,
        SteelHardening,
        add_bar,
    )
    from concreteproperties.results import CrackedResults, MomentCurvatureResults, StressResult, UltimateBendingResults
    from concreteproperties.stress_strain_profile import ConcreteServiceProfile, ConcreteUltimateProfile
    from concreteproperties.utils import AnalysisError
    from scipy.optimize import brentq
except ImportError as exc:  # pragma: no cover
    raise ImportError(
        "Reinforced-concrete section analysis requires the optional 'concreteproperties' backend. "
        "Install it with: pip install blue-prints[rc-analysis]"
    ) from exc

from sectionproperties.pre import CompoundGeometry, Geometry  # core dependency, always available
from shapely import Polygon  # core dependency, always available
from shapely.errors import GEOSException  # core dependency, always available

_CONCRETE_COLOUR = "lightgrey"
_STEEL_COLOUR = "grey"

# Bars closer than this (decimals of a mm) are treated as coincident and merged before analysis.
_COINCIDENT_TOLERANCE = 3

# Curvature (ratio strain per mm) below which the section is treated as having no neutral axis (pure axial).
_CURVATURE_TOL: float = 1e-12

# Tolerances for the strain-plane reconstruction consistency check (against the backend's own stresses).
_RECONSTRUCTION_ABS_TOL: MPA = 1e-3
_RECONSTRUCTION_REL_TOL: float = 1e-6

# Design strain limit factor for the inclined steel branch: eps_ud = 0.9 * eps_uk (EN 1992-1-1 art. 3.2.7(2)).
_EPS_UD_FACTOR: float = 0.9

# Strain range (ratio) of the no-tension cracked service profile. Chosen an order of magnitude beyond any
# linear-elastic SLS strain (~1-2 per mille), so the profile stays exactly linear across every service state.
_SERVICE_STRAIN_RANGE: float = 0.02

# Curvature search for the combined N + M cracked stress (see _solve_service_curvature). The bracket seeds on
# the pure-bending stiffness estimate and expands outward; the tolerances close it to well within round-off.
_CURVATURE_BRACKET_START: float = 1e-3
_CURVATURE_BRACKET_STEPS: int = 60
_CURVATURE_XTOL: float = 1e-12
_CURVATURE_RTOL: float = 1e-8


class AnalysisLevel(Enum):
    """Material model level driving the stress-strain profiles handed to the backend.

    SLS keeps steel elastic at f_yk/E_s (no partial factor) with a linear (tension-carrying) concrete, used
    for the uncracked analysis and the pure-bending cracked stress. SLS_CRACKED swaps the concrete for a
    no-tension linear-compression service profile, so a combined N + M state solves its own cracked neutral
    axis (see :func:`_cracked_stress_with_axial`). ULS uses design materials (f_yd, f_cd). The analyzer
    caches one backend section per configuration, so only the sections needed for the requested analyses are
    ever built.
    """

    SLS = "SLS"
    SLS_CRACKED = "SLS_CRACKED"
    ULS = "ULS"


class SteelBranch(Enum):
    """Plastic branch of the reinforcement design diagram at ULS (EN 1992-1-1 art. 3.2.7(2)).

    ``HORIZONTAL`` is the simplified horizontal top branch at f_yd without a strain limit (option (b) of
    art. 3.2.7(2)); ``INCLINED`` is the inclined branch rising to k*f_yd at eps_uk, cut off at the design
    strain limit eps_ud = 0.9 * eps_uk (option (a)).
    """

    HORIZONTAL = "horizontal"
    INCLINED = "inclined"


def _ultimate_profile(concrete: ConcreteMaterial) -> ConcreteUltimateProfile:
    """Build the backend ultimate stress-strain profile from the concrete's diagram type.

    The ultimate profile is mandatory for ``concreteproperties.Concrete`` but stays unused in the SLS
    (linear-elastic) analyses; it is filled here so the same material can serve a future ULS phase.

    Parameters
    ----------
    concrete : ConcreteMaterial
        The Blueprints concrete material.

    Returns
    -------
    ConcreteUltimateProfile
        Bilinear or Eurocode-parabolic ultimate profile.

    Raises
    ------
    NotImplementedError
        If the concrete uses a USER-defined diagram type, which the backend mapping does not support.
    """
    compressive_strain = concrete.eps_c3 * PER_MILLE_TO_RATIO
    ultimate_strain = concrete.eps_cu3 * PER_MILLE_TO_RATIO
    match concrete.diagram_type:
        case DiagramType.BILINEAR:
            return BilinearStressStrain(
                compressive_strength=concrete.f_cd,
                compressive_strain=compressive_strain,
                ultimate_strain=ultimate_strain,
            )
        case DiagramType.PARABOLIC:
            return EurocodeParabolicUltimate(
                compressive_strength=concrete.f_cd,
                compressive_strain=compressive_strain,
                ultimate_strain=ultimate_strain,
                n=concrete.n_factor,
            )
        case _:
            raise NotImplementedError(f"Concrete diagram type {concrete.diagram_type.value!r} is not supported by the analysis backend.")


def effective_modulus(concrete: ConcreteMaterial, creep_coefficient: DIMENSIONLESS) -> MPA:
    """Effective concrete elastic modulus E_c,eff = E_cm / (1 + phi) for a given creep coefficient.

    With ``creep_coefficient = 0`` (short-term) this is simply the secant modulus e_cm. The creep
    coefficient phi is a user input; Blueprints does not derive it from loading age or notional size.

    Parameters
    ----------
    concrete : ConcreteMaterial
        The Blueprints concrete material.
    creep_coefficient : DIMENSIONLESS
        The creep coefficient phi (>= 0) [-].

    Returns
    -------
    MPA
        The effective elastic modulus [MPa].

    Raises
    ------
    ValueError
        If the creep coefficient is negative.
    """
    if creep_coefficient < 0.0:
        raise ValueError(f"The creep coefficient must be zero or positive, got {creep_coefficient}.")
    return concrete.e_cm / (1.0 + creep_coefficient)


def _service_concrete(concrete: ConcreteMaterial, flexural_tensile_strength: MPA, elastic_modulus: MPA | None = None) -> Concrete:
    """Map a Blueprints concrete material to a backend SLS ``Concrete`` (linear-elastic service profile).

    Parameters
    ----------
    concrete : ConcreteMaterial
        The Blueprints concrete material.
    flexural_tensile_strength : MPA
        The flexural tensile strength f_ctm,fl [MPa] used by the backend's cracked-section logic;
        computed once per section from the member height (see ``build_concrete_section``).
    elastic_modulus : MPA | None
        The elastic modulus for the linear service profile: the effective modulus E_c,eff when
        analyzing with creep, or ``None`` to use the short-term secant modulus e_cm.

    Returns
    -------
    Concrete
        The backend concrete material with a linear service profile and a filled ultimate profile.
    """
    return Concrete(
        name=concrete.name,
        density=concrete.density * MM3_TO_M3,
        stress_strain_profile=ConcreteLinear(elastic_modulus=elastic_modulus if elastic_modulus is not None else concrete.e_cm),
        colour=_CONCRETE_COLOUR,
        ultimate_stress_strain_profile=_ultimate_profile(concrete),
        flexural_tensile_strength=flexural_tensile_strength,
    )


def _notension_service_concrete(concrete: ConcreteMaterial, flexural_tensile_strength: MPA, elastic_modulus: MPA | None = None) -> Concrete:
    """Map a Blueprints concrete to a backend SLS ``Concrete`` with a no-tension linear-compression profile.

    Where :func:`_service_concrete` is linear in both compression and tension (used uncracked, and for the
    pure-bending cracked stress where the neutral axis is known), this profile carries **no tension** and is
    linear in compression at the given modulus. A section built with it is intrinsically cracked, so a
    combined N + M state finds its own neutral axis under axial equilibrium instead of reusing the
    pure-bending crack depth (:func:`_cracked_stress_with_axial`).

    Parameters
    ----------
    concrete : ConcreteMaterial
        The Blueprints concrete material.
    flexural_tensile_strength : MPA
        The flexural tensile strength f_ctm,fl [MPa]; carried for consistency with the other service
        concretes but unused, since this profile is only ever driven by :func:`_cracked_stress_with_axial`.
    elastic_modulus : MPA | None
        The compression modulus of the linear branch: the effective modulus E_c,eff when analyzing with
        creep, or ``None`` to use the short-term secant modulus e_cm.

    Returns
    -------
    Concrete
        The backend concrete with a no-tension linear-compression service profile.
    """
    modulus = elastic_modulus if elastic_modulus is not None else concrete.e_cm
    profile = ConcreteServiceProfile(
        strains=[-_SERVICE_STRAIN_RANGE, 0.0, _SERVICE_STRAIN_RANGE],
        stresses=[0.0, 0.0, modulus * _SERVICE_STRAIN_RANGE],
        ultimate_strain=_SERVICE_STRAIN_RANGE,
    )
    with _suppress_asymmetric_modulus_warning():
        # Concrete.__post_init__ caches the elastic modulus, reading the (asymmetric) no-tension profile once.
        return Concrete(
            name=concrete.name,
            density=concrete.density * MM3_TO_M3,
            stress_strain_profile=profile,
            colour=_CONCRETE_COLOUR,
            ultimate_stress_strain_profile=_ultimate_profile(concrete),
            flexural_tensile_strength=flexural_tensile_strength,
        )


def _service_steel(material: ReinforcementSteelMaterial) -> SteelBar:
    """Map a Blueprints reinforcement material to a backend SLS ``SteelBar`` (elastic-plastic at f_yk).

    Parameters
    ----------
    material : ReinforcementSteelMaterial
        The Blueprints reinforcement steel material.

    Returns
    -------
    SteelBar
        The backend reinforcement bar material with an elastic-plastic profile at f_yk/E_s.
    """
    return SteelBar(
        name=material.name,
        density=material.density * MM3_TO_M3,
        stress_strain_profile=SteelElasticPlastic(
            yield_strength=material.f_yk,
            elastic_modulus=material.e_s,
            fracture_strain=material.eps_uk * PER_MILLE_TO_RATIO,
        ),
        colour=_STEEL_COLOUR,
    )


def _curvature_concrete_profile(concrete: ConcreteMaterial, elastic_modulus: MPA, flexural_tensile_strength: MPA) -> ConcreteServiceProfile:
    """Build the bilinear-horizontal concrete curve for the moment-curvature analysis.

    Compression is linear at the given elastic modulus up to f_cd, then a horizontal plateau to eps_cu3
    (the diagram IDEA StatiCa RCS uses for its N-M-kappa stiffness points, keeping moment-curvature
    results benchmarkable). Tension is linear up to the flexural tensile strength f_ctm,fl, then softens
    to zero at twice the cracking strain — a near-brittle drop that produces the cracking kink in the
    moment-curvature curve while staying numerically stable.

    Parameters
    ----------
    concrete : ConcreteMaterial
        The Blueprints concrete material.
    elastic_modulus : MPA
        The elastic modulus of the linear part: e_cm (short-term) or E_c,eff (with creep) [MPa].
    flexural_tensile_strength : MPA
        The flexural tensile strength f_ctm,fl [MPa] at which the concrete cracks.

    Returns
    -------
    ConcreteServiceProfile
        The backend service profile (compression positive, tension negative).
    """
    strain_elbow = concrete.f_cd / elastic_modulus
    strain_ultimate = concrete.eps_cu3 * PER_MILLE_TO_RATIO
    strain_cracking = flexural_tensile_strength / elastic_modulus
    return ConcreteServiceProfile(
        strains=[-2.2 * strain_cracking, -2.0 * strain_cracking, -strain_cracking, 0.0, strain_elbow, strain_ultimate],
        stresses=[0.0, 0.0, -flexural_tensile_strength, 0.0, concrete.f_cd, concrete.f_cd],
        ultimate_strain=strain_ultimate,
    )


def _ultimate_concrete(concrete: ConcreteMaterial, flexural_tensile_strength: MPA, elastic_modulus: MPA | None = None) -> Concrete:
    """Map a Blueprints concrete material to a backend ULS ``Concrete`` (design materials).

    The material carries two profiles: the design ultimate profile (bilinear or parabola-rectangle at
    f_cd, from the material's diagram type) used by the capacity, interaction and ultimate stress
    analyses, and the bilinear-horizontal curve of :func:`_curvature_concrete_profile` used by the
    moment-curvature analysis.

    Parameters
    ----------
    concrete : ConcreteMaterial
        The Blueprints concrete material.
    flexural_tensile_strength : MPA
        The flexural tensile strength f_ctm,fl [MPa], producing the cracking kink in the
        moment-curvature analysis.
    elastic_modulus : MPA | None
        The elastic modulus for the moment-curvature curve: the effective modulus E_c,eff when
        analyzing with creep, or ``None`` for the short-term secant modulus e_cm. The capacity and
        interaction analyses run on the ultimate profile and are unaffected.

    Returns
    -------
    Concrete
        The backend concrete material with design (ULS) profiles.
    """
    return Concrete(
        name=concrete.name,
        density=concrete.density * MM3_TO_M3,
        stress_strain_profile=_curvature_concrete_profile(
            concrete,
            elastic_modulus if elastic_modulus is not None else concrete.e_cm,
            flexural_tensile_strength,
        ),
        colour=_CONCRETE_COLOUR,
        ultimate_stress_strain_profile=_ultimate_profile(concrete),
        flexural_tensile_strength=flexural_tensile_strength,
    )


def _ultimate_steel(material: ReinforcementSteelMaterial, branch: SteelBranch = SteelBranch.HORIZONTAL) -> SteelBar:
    """Map a Blueprints reinforcement material to a backend ULS ``SteelBar`` (design diagram at f_yd).

    With the default ``HORIZONTAL`` branch the diagram is elastic-plastic at f_yd/E_s (EN 1992-1-1
    art. 3.2.7(2)(b), no strain limit); the characteristic strain eps_uk is only kept as the numerical
    fracture strain the backend needs, far beyond any realistic flexural state. With the ``INCLINED``
    branch the plastic part rises towards k*f_yd at eps_uk and is cut off at eps_ud = 0.9 * eps_uk
    (art. 3.2.7(2)(a)).

    Parameters
    ----------
    material : ReinforcementSteelMaterial
        The Blueprints reinforcement steel material.
    branch : SteelBranch
        The plastic branch of the design diagram.

    Returns
    -------
    SteelBar
        The backend reinforcement bar material with the design (ULS) stress-strain profile.
    """
    f_yd = material.f_yd
    eps_yd = f_yd / material.e_s
    eps_uk = material.eps_uk * PER_MILLE_TO_RATIO
    if branch is SteelBranch.HORIZONTAL:
        profile = SteelElasticPlastic(yield_strength=f_yd, elastic_modulus=material.e_s, fracture_strain=eps_uk)
    else:
        eps_ud = _EPS_UD_FACTOR * eps_uk
        # design inclined branch: from (eps_yd, f_yd) towards (eps_uk, k * f_yd), evaluated at eps_ud.
        stress_at_eps_ud = f_yd * (1.0 + (material.ductility_factor_k - 1.0) * (eps_ud - eps_yd) / (eps_uk - eps_yd))
        profile = SteelHardening(yield_strength=f_yd, elastic_modulus=material.e_s, fracture_strain=eps_ud, ultimate_strength=stress_at_eps_ud)
    return SteelBar(
        name=material.name,
        density=material.density * MM3_TO_M3,
        stress_strain_profile=profile,
        colour=_STEEL_COLOUR,
    )


def axial_capacities(cross_section: ReinforcedCrossSection) -> tuple[KN, KN]:
    """Design axial capacities of the section: the squash load and the tensile capacity.

    The squash load counts the net concrete area at f_cd plus the reinforcement at f_yd (the strain at
    zero-curvature crushing is far beyond the yield strain); the tensile capacity is the reinforcement
    alone at f_yd (concrete carries no design tension). With the inclined steel branch the true
    capacities are marginally higher; using f_yd is slightly conservative.

    Parameters
    ----------
    cross_section : ReinforcedCrossSection
        The Blueprints reinforced cross-section.

    Returns
    -------
    tuple[KN, KN]
        ``(n_compression, n_tension)``: the squash load (negative) and tensile capacity (positive) [kN].
    """
    reinforcement_force = sum(rebar.area * rebar.material.f_yd for rebar in cross_section.longitudinal_rebars)
    net_concrete_area = cross_section.profile.polygon.area - sum(rebar.area for rebar in cross_section.longitudinal_rebars)
    n_compression: KN = -(cross_section.concrete_material.f_cd * net_concrete_area + reinforcement_force) * N_TO_KN
    n_tension: KN = reinforcement_force * N_TO_KN
    return n_compression, n_tension


def flexural_tensile_strength(cross_section: ReinforcedCrossSection) -> MPA:
    """Mean flexural tensile strength f_ctm,fl of the section (EN 1992-1-1 formula 3.23).

    Uses the profile's bounding-box height as the member depth. Also the cracking threshold for the
    uncracked-vs-cracked decision and the value handed to the backend's ``flexural_tensile_strength``.

    Parameters
    ----------
    cross_section : ReinforcedCrossSection
        The reinforced cross-section.

    Returns
    -------
    MPA
        The mean flexural tensile strength [MPa].
    """
    _, min_y, _, max_y = cross_section.profile.polygon.bounds
    section_height = max_y - min_y
    return float(Form3Dot23FlexuralTensileStrength(h=section_height, f_ctm=cross_section.concrete_material.f_ctm))


def build_concrete_section(
    cross_section: ReinforcedCrossSection,
    level: AnalysisLevel = AnalysisLevel.SLS,
    elastic_modulus: MPA | None = None,
    steel_branch: SteelBranch = SteelBranch.HORIZONTAL,
) -> ConcreteSection:
    """Build a backend ``ConcreteSection`` from a Blueprints reinforced cross-section.

    The section profile becomes the concrete geometry and each longitudinal rebar is added as a lumped
    bar. Reinforcement materials are mapped to distinct ``SteelBar`` instances, reusing one instance per
    distinct Blueprints material. The flexural tensile strength is taken from formula 3.23 using the
    profile's bounding-box height. The ``level`` selects the material models: characteristic/service
    profiles for SLS, design profiles (f_cd, f_yd) for ULS.

    Parameters
    ----------
    cross_section : ReinforcedCrossSection
        The Blueprints reinforced cross-section (geometry + materials + longitudinal rebars).
    level : AnalysisLevel
        The material model level (SLS, SLS_CRACKED or ULS).
    elastic_modulus : MPA | None
        The concrete elastic modulus for the service profile: the effective modulus E_c,eff when
        analyzing with creep, or ``None`` for the short-term secant modulus e_cm. At the ULS level this
        only affects the moment-curvature curve; capacity and interaction run on the ultimate profile.
    steel_branch : SteelBranch
        The plastic branch of the ULS reinforcement design diagram. Ignored for SLS.

    Returns
    -------
    ConcreteSection
        The backend section ready for analysis.
    """
    polygon = cross_section.profile.polygon
    f_ctm_fl = flexural_tensile_strength(cross_section)
    match level:
        case AnalysisLevel.SLS:
            concrete = _service_concrete(cross_section.concrete_material, f_ctm_fl, elastic_modulus)
        case AnalysisLevel.SLS_CRACKED:
            concrete = _notension_service_concrete(cross_section.concrete_material, f_ctm_fl, elastic_modulus)
        case _:
            concrete = _ultimate_concrete(cross_section.concrete_material, f_ctm_fl, elastic_modulus)
    # concreteproperties materials are accepted structurally by sectionproperties' Geometry but are not a
    # nominal subclass of sectionproperties.pre.Material, so the static type does not line up.
    geometry = Geometry(geom=polygon, material=concrete)  # ty: ignore[invalid-argument-type]

    steel_bars: dict[ReinforcementSteelMaterial, SteelBar] = {}
    for x, y, area, material in _merge_coincident_rebars(cross_section.longitudinal_rebars):
        if material not in steel_bars:
            is_service = level in (AnalysisLevel.SLS, AnalysisLevel.SLS_CRACKED)
            steel_bars[material] = _service_steel(material) if is_service else _ultimate_steel(material, steel_branch)
        geometry = add_bar(geometry, area=area, material=steel_bars[material], x=x, y=y)

    # the backend requires a CompoundGeometry; add_bar returns one, but an unreinforced section (no bars
    # added) is still a plain Geometry and must be wrapped explicitly.
    if not isinstance(geometry, CompoundGeometry):
        geometry = CompoundGeometry([geometry])
    return ConcreteSection(geometry)  # ty: ignore[invalid-argument-type]


def _merge_coincident_rebars(rebars: list[Rebar]) -> list[tuple[float, float, float, ReinforcementSteelMaterial]]:
    """Merge bars that share a location into one bar with the combined area.

    Convenience placement on multiple edges puts a bar at each shared corner from both edges, producing
    coincident bars. The backend cannot mesh two bars at the same point, so coincident bars are merged
    into a single bar with the summed area at the shared location. This keeps the analyzed reinforcement
    consistent with the cross-section's own reported reinforcement area.

    Parameters
    ----------
    rebars : list[Rebar]
        The longitudinal rebars of the cross-section.

    Returns
    -------
    list[tuple[float, float, float, ReinforcementSteelMaterial]]
        One ``(x, y, area, material)`` entry per distinct location.

    Raises
    ------
    ValueError
        If coincident bars have different materials, which cannot be merged unambiguously.
    """
    groups: dict[tuple[float, float], list[Rebar]] = defaultdict(list)
    for rebar in rebars:
        groups[round(rebar.x, _COINCIDENT_TOLERANCE), round(rebar.y, _COINCIDENT_TOLERANCE)].append(rebar)

    merged: list[tuple[float, float, float, ReinforcementSteelMaterial]] = []
    for group in groups.values():
        materials = {rebar.material for rebar in group}
        if len(materials) > 1:
            raise ValueError(
                f"Coincident reinforcement bars with different materials at (x={group[0].x}, y={group[0].y}) cannot be merged for analysis."
            )
        total_area = sum(rebar.area for rebar in group)
        merged.append((group[0].x, group[0].y, total_area, group[0].material))
    return merged


def _to_backend_actions(forces: SectionForces) -> tuple[float, float, float]:
    """Convert Blueprints section forces to the backend's (n, m_x, m_y) in N and Nmm.

    Blueprints uses kN/kNm, tension-positive and the SAF y/z member axes; the backend uses N/mm,
    compression-positive and geometric x/y axes (cross-section y -> geometric x, z -> geometric y).

    Parameters
    ----------
    forces : SectionForces
        The section forces in Blueprints conventions.

    Returns
    -------
    tuple[float, float, float]
        ``(n, m_x, m_y)`` for the backend: ``n = -forces.n``, ``m_x = forces.m_y``, ``m_y = -forces.m_z``.
    """
    n: KN = -forces.n * KN_TO_N
    m_x: KNM = forces.m_y * KNM_TO_NMM
    m_y: KNM = -forces.m_z * KNM_TO_NMM
    return n, m_x, m_y


def _from_backend_actions(n: float, m_x: float, m_y: float) -> tuple[KN, KNM, KNM]:
    """Convert backend actions ``(n, m_x, m_y)`` in N/Nmm back to Blueprints ``(n, m_y, m_z)`` in kN/kNm.

    The exact inverse of :func:`_to_backend_actions`: the backend is compression-positive on geometric
    x/y axes, Blueprints is tension-positive on the SAF y/z member axes (cross-section y -> geometric x,
    z -> geometric y).

    Parameters
    ----------
    n : float
        Backend axial force [N], compression positive.
    m_x : float
        Backend bending moment about the geometric x-axis [Nmm].
    m_y : float
        Backend bending moment about the geometric y-axis [Nmm].

    Returns
    -------
    tuple[KN, KNM, KNM]
        ``(n, m_y, m_z)`` in Blueprints conventions: ``n = -n``, ``m_y = m_x``, ``m_z = -m_y``.
    """
    return -n * N_TO_KN, m_x * NMM_TO_KNM, -m_y * NMM_TO_KNM


@contextmanager
def _suppress_pure_axial_warning() -> Iterator[None]:
    """Suppress the spurious runtime warnings the backend emits for pure-axial actions.

    With zero bending the neutral-axis gradient is computed as 0/0, which propagates NaN through the
    backend's geometry handling and raises a cluster of ``invalid value encountered in ...`` warnings
    (scalar divide, then shapely linestrings/intersects). The resulting stresses are still correct (not
    NaN), so the whole cluster is suppressed. The shared message prefix is matched as a regex.
    """
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=RuntimeWarning, message="invalid value encountered")
        yield


@contextmanager
def _suppress_asymmetric_modulus_warning() -> Iterator[None]:
    """Suppress the backend warning about unequal tensile/compressive moduli for the no-tension profile.

    The cracked service concrete (:func:`_notension_service_concrete`) deliberately has a zero tensile
    modulus, so the backend's ``get_elastic_modulus`` — called lazily while building the section and running
    the service analysis — warns that the two initial moduli differ. That asymmetry is the whole point here,
    so the (correctly targeted) warning is silenced wherever the profile is exercised.
    """
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=UserWarning, message="Initial compressive and tensile elastic moduli are not equal")
        yield


@contextmanager
def _wrap_backend_convergence_errors(description: str) -> Iterator[None]:
    """Turn a backend solver failure into a clear Blueprints ``ValueError``.

    The backend's iterative solvers (ultimate capacity, interaction diagrams, moment-curvature) raise a
    backend-specific ``AnalysisError`` when the neutral-axis iteration cannot reach equilibrium — most
    commonly because the axial force exceeds the tensile or compressive capacity of the section.

    Parameters
    ----------
    description : str
        Human-readable description of the analysis, echoed in the error message.
    """
    try:
        yield
    except AnalysisError as exc:
        raise ValueError(f"The {description} did not converge: {exc}") from exc


@contextmanager
def _wrap_backend_geometry_errors() -> Iterator[None]:
    """Turn a raw backend geometry failure into a clear, actionable Blueprints error.

    The meshing backend raises a low-level ``shapely GEOSException`` when it cannot process the section
    geometry (for example overlapping reinforcement, or a bar on or outside the section boundary). This
    re-raises it as a ``ValueError`` that tells the user what to check.
    """
    try:
        yield
    except GEOSException as exc:
        raise ValueError(
            "The analysis backend could not process the cross-section geometry. This usually means "
            "reinforcement bars overlap, or a bar lies on or outside the section boundary. Check the "
            "reinforcement layout for overlapping bars and confirm every bar is fully inside the section."
        ) from exc


def analyse_uncracked(section: ConcreteSection, forces: SectionForces, elastic_modulus: MPA, geometry: Polygon) -> StressStrainResult:
    """Run the backend uncracked stress analysis and map the result to Blueprints conventions.

    Parameters
    ----------
    section : ConcreteSection
        The backend section built by :func:`build_concrete_section`.
    forces : SectionForces
        The section forces in Blueprints conventions.
    elastic_modulus : MPA
        The concrete elastic modulus used for the analysis (e_cm or the effective modulus E_c,eff),
        used to reconstruct concrete strains from stresses.
    geometry : Polygon
        The section profile polygon, carried on the result for plotting.

    Returns
    -------
    StressStrainResult
        The uncracked stress/strain result, compression negative.
    """
    n, m_x, m_y = _to_backend_actions(forces)
    with _suppress_pure_axial_warning(), _wrap_backend_geometry_errors():
        raw = section.calculate_uncracked_stress(n=n, m_x=m_x, m_y=m_y)
    return _to_stress_strain_result(forces=forces, raw=raw, elastic_modulus=elastic_modulus, geometry=geometry, regime=Regime.SLS_UNCRACKED)


def _to_stress_strain_result(
    forces: SectionForces,
    raw: StressResult,
    elastic_modulus: MPA,
    geometry: Polygon,
    *,
    regime: Regime,
    cracked_properties: CrackedProperties | None = None,
    strain_plane: StrainPlane | None = None,
    concrete_profile: object | None = None,
) -> StressStrainResult:
    """Map a backend ``StressResult`` to a Blueprints ``StressStrainResult`` (compression negative).

    Parameters
    ----------
    forces : SectionForces
        The section forces that produced the result, echoed back.
    raw : StressResult
        The backend ``StressResult`` (concrete stresses compression-positive).
    elastic_modulus : MPA
        The concrete elastic modulus used for the analysis (e_cm or the effective modulus E_c,eff),
        used to reconstruct concrete strains from stresses in the SLS regimes.
    geometry : Polygon
        The section profile polygon, carried on the result for plotting.
    regime : Regime
        The regime that produced the result.
    cracked_properties : CrackedProperties | None
        The cracked-section properties for a cracked result, or ``None`` otherwise.
    strain_plane : StrainPlane | None
        A pre-built strain plane (the ULS route, where the plane follows from the pivot geometry and
        must not be reconstructed from ``stress / E``). ``None`` reconstructs the plane from the linear
        SLS stresses.
    concrete_profile : object | None
        The backend concrete stress-strain profile used to turn strains into stresses when plotting a
        non-linear (ULS) result; ``None`` for the linear SLS regimes.

    Returns
    -------
    StressStrainResult
        The result in Blueprints conventions.
    """
    concrete_stresses = [stress for section_stresses in raw.concrete_stresses for stress in section_stresses]
    # backend is compression-positive; negate to get Blueprints compression-negative (and swap min/max).
    concrete_stress_min: MPA = -max(concrete_stresses)
    concrete_stress_max: MPA = -min(concrete_stresses)

    rebar_results = []
    for bar_geometry, stress, strain, force in zip(
        raw.lumped_reinforcement_geometries,
        raw.lumped_reinforcement_stresses,
        raw.lumped_reinforcement_strains,
        raw.lumped_reinforcement_forces,
        strict=True,
    ):
        x, y = bar_geometry.calculate_centroid()
        diameter = math.sqrt(4 * bar_geometry.calculate_area() / math.pi)
        rebar_results.append(
            RebarStressResult(
                x=x,
                y=y,
                diameter=diameter,
                stress=-float(stress),
                strain=-float(strain) * RATIO_TO_PER_MILLE,
                force=-float(force[0]) * N_TO_KN,
            )
        )

    if strain_plane is None:
        strain_plane = _reconstruct_strain_plane(
            raw,
            elastic_modulus,
            is_cracked=regime is Regime.SLS_CRACKED,
            concrete_stress_min=concrete_stress_min,
            concrete_stress_max=concrete_stress_max,
        )

    return StressStrainResult(
        forces=forces,
        regime=regime,
        concrete_stress_min=concrete_stress_min,
        concrete_stress_max=concrete_stress_max,
        rebar_results=rebar_results,
        raw=raw,
        cracked_properties=cracked_properties,
        strain_plane=strain_plane,
        elastic_modulus=elastic_modulus,
        geometry=geometry,
        concrete_profile=concrete_profile,
    )


def _concrete_node_data(raw: StressResult) -> tuple[np.ndarray, np.ndarray]:
    """Return the concrete mesh node coordinates and their stresses in the backend convention.

    Parameters
    ----------
    raw : StressResult
        The backend stress result.

    Returns
    -------
    tuple[np.ndarray, np.ndarray]
        ``(coords, stresses)`` with ``coords`` shaped ``(N, 2)`` in cross-section (x, y) [mm] and
        ``stresses`` shaped ``(N,)`` compression-positive [MPa], aligned per node.
    """
    coords = []
    stresses = []
    for section, section_stresses in zip(raw.concrete_analysis_sections, raw.concrete_stresses, strict=True):
        coords.append(np.asarray(section.mesh_nodes, dtype=float))
        stresses.append(np.asarray(section_stresses, dtype=float))
    return np.vstack(coords), np.concatenate(stresses)


def _reconstruct_strain_plane(
    raw: StressResult,
    elastic_modulus: MPA,
    *,
    is_cracked: bool,
    concrete_stress_min: MPA,
    concrete_stress_max: MPA,
) -> StrainPlane:
    """Reconstruct the linear strain plane from the backend result and validate it against its stresses.

    The strain field is exactly affine for a linear SLS analysis, so a least-squares plane through the
    reliable strain samples recovers it exactly (this extracts the plane the backend already used, it
    does not re-solve the section). Samples are the lumped rebar strains (valid in every regime) and the
    concrete node strains ``stress / E`` (all nodes when uncracked; compression nodes only when
    cracked, since cracked concrete carries no tension and its tension nodes read zero stress).

    Parameters
    ----------
    raw : StressResult
        The backend stress result.
    elastic_modulus : MPA
        The concrete elastic modulus used for the analysis (e_cm or the effective modulus E_c,eff).
    is_cracked : bool
        Which regime produced the result.
    concrete_stress_min : MPA
        The backend's minimum concrete stress in Blueprints convention (compression negative), for the
        consistency check.
    concrete_stress_max : MPA
        The backend's maximum concrete stress in Blueprints convention, for the consistency check.

    Returns
    -------
    StrainPlane
        The reconstructed strain plane in Blueprints conventions (compression negative).

    Raises
    ------
    ValueError
        If the strain samples do not span the section plane (for example a single rebar layer with no
        compression zone), leaving the plane under-determined.
    RuntimeError
        If the stresses recomputed from the fitted plane do not match the backend's own stresses.
    """
    node_coords, node_stress = _concrete_node_data(raw)
    # Blueprints strain (compression negative) = -(compression-positive backend stress) / E.
    node_strain = -node_stress / elastic_modulus

    if is_cracked:
        compression = node_stress > 0.0  # backend compression-positive; keep only compressed concrete
        fit_coords = [node_coords[compression]]
        fit_strain = [node_strain[compression]]
    else:
        fit_coords = [node_coords]
        fit_strain = [node_strain]

    for geometry, strain in zip(raw.lumped_reinforcement_geometries, raw.lumped_reinforcement_strains, strict=True):
        centroid_x, centroid_y = geometry.calculate_centroid()
        fit_coords.append(np.array([[centroid_x, centroid_y]]))
        fit_strain.append(np.array([-float(strain)]))

    coords = np.vstack(fit_coords)
    strains = np.concatenate(fit_strain)

    matrix = np.column_stack([np.ones(len(coords)), coords[:, 0], coords[:, 1]])
    if np.linalg.matrix_rank(matrix) < 3:
        raise ValueError(
            "The strain state is under-determined: the reinforcement and compression zone do not span the section "
            "plane (for example a single rebar layer with no concrete in compression). The strain plane cannot be "
            "reconstructed reliably for this case."
        )
    eps_0, kappa_z, kappa_y = (float(c) for c in np.linalg.lstsq(matrix, strains, rcond=None)[0])

    _validate_reconstruction(
        node_coords,
        eps_0=eps_0,
        kappa_z=kappa_z,
        kappa_y=kappa_y,
        elastic_modulus=elastic_modulus,
        is_cracked=is_cracked,
        concrete_stress_min=concrete_stress_min,
        concrete_stress_max=concrete_stress_max,
    )
    neutral_axis_depth, neutral_axis_angle = _neutral_axis(node_coords, eps_0=eps_0, kappa_z=kappa_z, kappa_y=kappa_y)
    return StrainPlane(
        eps_0=eps_0 * RATIO_TO_PER_MILLE,
        kappa_y=kappa_y,
        kappa_z=kappa_z,
        neutral_axis_depth=neutral_axis_depth,
        neutral_axis_angle=neutral_axis_angle,
    )


def _validate_reconstruction(
    node_coords: np.ndarray,
    *,
    eps_0: float,
    kappa_z: float,
    kappa_y: float,
    elastic_modulus: MPA,
    is_cracked: bool,
    concrete_stress_min: MPA,
    concrete_stress_max: MPA,
) -> None:
    """Recompute the concrete stress envelope from the fitted plane and check it matches the backend.

    Parameters
    ----------
    node_coords : np.ndarray
        Concrete mesh node coordinates, shaped ``(N, 2)`` [mm].
    eps_0 : float
        Fitted strain at the origin (ratio, compression negative).
    kappa_z : float
        Fitted strain gradient in x (ratio/mm).
    kappa_y : float
        Fitted strain gradient in y (ratio/mm).
    elastic_modulus : MPA
        The concrete elastic modulus used for the analysis (e_cm or the effective modulus E_c,eff).
    is_cracked : bool
        Which regime produced the result (cracked zeros the concrete tension stress).
    concrete_stress_min : MPA
        The backend's minimum concrete stress (compression negative).
    concrete_stress_max : MPA
        The backend's maximum concrete stress (compression negative).

    Raises
    ------
    RuntimeError
        If the recomputed stress envelope does not match the backend's within tolerance.
    """
    strain = eps_0 + kappa_z * node_coords[:, 0] + kappa_y * node_coords[:, 1]
    stress = elastic_modulus * strain
    if is_cracked:
        stress = np.where(stress < 0.0, stress, 0.0)  # cracked concrete carries no tension
    recon_min = float(stress.min())
    recon_max = float(stress.max())
    if not (
        math.isclose(recon_min, concrete_stress_min, rel_tol=_RECONSTRUCTION_REL_TOL, abs_tol=_RECONSTRUCTION_ABS_TOL)
        and math.isclose(recon_max, concrete_stress_max, rel_tol=_RECONSTRUCTION_REL_TOL, abs_tol=_RECONSTRUCTION_ABS_TOL)
    ):
        raise RuntimeError(
            "Strain-plane reconstruction failed its consistency check: concrete stresses recomputed from the fitted "
            f"plane (min {recon_min:.4g}, max {recon_max:.4g} MPa) do not match the backend result "
            f"(min {concrete_stress_min:.4g}, max {concrete_stress_max:.4g} MPa). This is unexpected for a linear SLS "
            "analysis; please report it."
        )


def _neutral_axis(node_coords: np.ndarray, *, eps_0: float, kappa_z: float, kappa_y: float) -> tuple[MM | None, DEG]:
    """Locate the neutral (zero-strain) line from the fitted plane.

    Parameters
    ----------
    node_coords : np.ndarray
        Concrete mesh node coordinates, shaped ``(N, 2)`` [mm].
    eps_0 : float
        Fitted strain at the origin (ratio, compression negative).
    kappa_z : float
        Fitted strain gradient in x (ratio/mm).
    kappa_y : float
        Fitted strain gradient in y (ratio/mm).

    Returns
    -------
    tuple[MM | None, DEG]
        ``(neutral_axis_depth, neutral_axis_angle)``. The depth is the perpendicular distance from the
        extreme compression fibre to the neutral line, or ``None`` for pure axial (no curvature) or when
        no fibre is in compression. The angle is the neutral line orientation in ``[-90, 90)`` degrees.
    """
    gradient = math.hypot(kappa_z, kappa_y)
    if gradient <= _CURVATURE_TOL:
        return None, 0.0
    # neutral line is perpendicular to the strain gradient (kappa_z, kappa_y).
    angle = (math.degrees(math.atan2(kappa_y, kappa_z)) + 90.0 + 90.0) % 180.0 - 90.0
    strain = eps_0 + kappa_z * node_coords[:, 0] + kappa_y * node_coords[:, 1]
    most_compressive = float(strain.min())  # most negative Blueprints strain = extreme compression fibre
    if most_compressive >= 0.0:
        return None, angle
    return abs(most_compressive) / gradient, angle


def _to_cracked_actions(forces: SectionForces) -> tuple[float, float, float]:
    """Convert Blueprints section forces to the backend's cracked-analysis actions ``(n, theta, m)``.

    The backend cracked analysis is uniaxial: it takes a neutral-axis angle ``theta`` and a single scalar
    moment ``m`` about that axis. A biaxial moment (m_x, m_y) in backend axes is decomposed to its
    resultant magnitude and direction. For the common uniaxial case (Blueprints ``m_y`` only) this gives
    ``theta = 0`` and ``m = m_x``.

    Parameters
    ----------
    forces : SectionForces
        The section forces in Blueprints conventions.

    Returns
    -------
    tuple[float, float, float]
        ``(n, theta, m)`` for the backend, in N, rad and Nmm.
    """
    n, m_x, m_y = _to_backend_actions(forces)
    theta = math.atan2(m_y, m_x) if (m_x or m_y) else 0.0
    m = math.hypot(m_x, m_y)
    return n, theta, m


def _cracked_results(section: ConcreteSection, forces: SectionForces, elastic_modulus: MPA) -> tuple[CrackedResults, float, float, float]:
    """Run the backend cracked-properties analysis and populate its transformed properties.

    Parameters
    ----------
    section : ConcreteSection
        The backend section.
    forces : SectionForces
        The section forces in Blueprints conventions.
    elastic_modulus : MPA
        Reference elastic modulus for the transformed cracked properties — the same modulus as the
        service profile (e_cm or the effective modulus E_c,eff), so neutral-axis depth and strains stay
        consistent.

    Returns
    -------
    tuple[CrackedResults, float, float, float]
        The backend cracked results plus the backend ``(n, theta, m)`` actions for a subsequent stress
        analysis.

    Raises
    ------
    NotImplementedError
        If both bending components are non-zero: the cracked neutral-axis orientation under biaxial
        bending cannot be derived from the moment vector alone, so no reliable result can be given.
    RuntimeError
        If the cracked neutral-axis iteration fails to converge, re-raised with section/force context.
    """
    if forces.m_y != 0.0 and forces.m_z != 0.0:
        raise NotImplementedError(
            "Cracked analysis under biaxial bending (both m_y and m_z non-zero) is not supported: the "
            "cracked neutral-axis orientation is not perpendicular to the moment vector and requires an "
            "iterative biaxial solution. Use uncracked_stress for biaxial bending, or apply bending about "
            "a single axis."
        )
    n, theta, m = _to_cracked_actions(forces)
    with _wrap_backend_geometry_errors():
        try:
            cracked = section.calculate_cracked_properties(theta=theta)
        except (ValueError, RuntimeError, AnalysisError) as exc:
            raise RuntimeError(f"Cracked neutral-axis analysis did not converge for forces {forces}: {exc}") from exc
        cracked.calculate_transformed_properties(elastic_modulus=elastic_modulus)
    return cracked, n, theta, m


def _to_cracked_properties(cracked: CrackedResults) -> CrackedProperties:
    """Map backend ``CrackedResults`` to a Blueprints ``CrackedProperties``.

    ``m_cr`` is populated by ``calculate_cracked_properties`` and ``iuu_cr`` by
    ``calculate_transformed_properties`` (both run in ``_cracked_results``), so neither is ``None`` here.
    """
    m_cr = cracked.m_cr
    i_cracked = cracked.iuu_cr
    # the uniaxial cracked analysis (single neutral-axis angle) yields a scalar cracking moment, never the
    # biaxial (m_cr_pos, m_cr_neg) tuple form; iuu_cr is populated by calculate_transformed_properties.
    assert not isinstance(m_cr, tuple)
    assert i_cracked is not None
    return CrackedProperties(
        m_cr=m_cr * NMM_TO_KNM,
        neutral_axis_depth=cracked.d_nc,
        theta=cracked.theta,
        i_cracked=i_cracked,
        raw=cracked,
    )


def analyse_cracked(
    section: ConcreteSection,
    forces: SectionForces,
    elastic_modulus: MPA,
    geometry: Polygon,
    notension_section: Callable[[], ConcreteSection],
) -> StressStrainResult:
    """Run the backend cracked stress analysis and map the result to Blueprints conventions.

    Two routes, picked by the axial force. Under **pure bending** (``forces.n == 0``) the cracked neutral
    axis is exactly the pure-bending crack depth, so the cheap ``calculate_cracked_stress`` on the linear
    service section is exact. Under a **combined N + M** state the actual neutral axis is deeper (compression)
    or shallower (tension) than the pure-bending crack depth; reusing the latter would remove a strip of
    concrete that is really in compression and overestimate the stresses. That case is routed through
    :func:`_cracked_stress_with_axial`, which solves the true cracked N + M equilibrium on a no-tension
    section instead. The reported ``cracked_properties`` (m_cr, i_cracked, neutral-axis depth) always describe
    the pure-bending cracked section — load-independent section constants; the actual neutral axis of the
    applied state lives on the result's ``strain_plane``.

    Parameters
    ----------
    section : ConcreteSection
        The linear (tension-carrying) SLS section, for the cracked properties and the pure-bending stress.
    forces : SectionForces
        The section forces in Blueprints conventions.
    elastic_modulus : MPA
        Reference elastic modulus (e_cm or the effective modulus E_c,eff, matching the service profile).
    geometry : Polygon
        The section profile polygon, carried on the result for plotting.
    notension_section : Callable[[], ConcreteSection]
        Factory returning the no-tension SLS_CRACKED section, invoked only for the combined N + M route so
        the extra section is never built for a pure-bending workflow.

    Returns
    -------
    StressStrainResult
        The cracked stress/strain result, compression negative, carrying the cracked properties.
    """
    cracked, n, theta, m = _cracked_results(section, forces, elastic_modulus)
    if forces.n == 0.0:
        with _wrap_backend_geometry_errors():
            raw = section.calculate_cracked_stress(cracked_results=cracked, n=n, m=m)
    else:
        i_cracked = cracked.iuu_cr
        # populated by calculate_transformed_properties in _cracked_results, so never None here.
        assert i_cracked is not None
        raw = _cracked_stress_with_axial(notension_section(), forces, n=n, theta=theta, m=m, i_cracked=i_cracked, elastic_modulus=elastic_modulus)
    return _to_stress_strain_result(
        forces, raw, elastic_modulus, geometry, regime=Regime.SLS_CRACKED, cracked_properties=_to_cracked_properties(cracked)
    )


def _cracked_stress_with_axial(
    section: ConcreteSection,
    forces: SectionForces,
    *,
    n: float,
    theta: float,
    m: float,
    i_cracked: float,
    elastic_modulus: MPA,
) -> StressResult:
    """Solve the true cracked stress state under a combined axial force and moment.

    The section is built with a no-tension linear-compression concrete (:func:`_notension_service_concrete`),
    so it is intrinsically cracked. For a trial curvature the backend converges the strain at the origin on
    axial equilibrium with the target axial force ``n`` (``calculate_service_stress`` with an explicit
    curvature); the curvature is then solved so the resulting moment equals the target ``m``. This finds the
    neutral axis consistent with N *and* M — unlike the pure-bending crack depth — while reusing the backend
    meshing and stress evaluation, so the returned ``StressResult`` plugs into the usual result pipeline.

    Parameters
    ----------
    section : ConcreteSection
        The no-tension SLS_CRACKED backend section.
    forces : SectionForces
        The section forces in Blueprints conventions, echoed in the error message on failure.
    n : float
        The target axial force in the backend convention (compression positive) [N].
    theta : float
        The neutral-axis angle in the backend convention [rad].
    m : float
        The target bending-moment magnitude about ``theta`` [Nmm].
    i_cracked : float
        The pure-bending cracked second moment of area [mm⁴], used only to seed the curvature search.
    elastic_modulus : MPA
        The concrete compression modulus (e_cm or E_c,eff), used only to seed the curvature search.

    Returns
    -------
    StressResult
        The backend service stress result of the solved cracked N + M state.

    Raises
    ------
    ValueError
        If the equilibrium cannot be reached (for example a tension-dominated state with no compression
        zone), or on a backend geometry failure.
    """

    def stress_at(curvature: float) -> StressResult:
        stub = MomentCurvatureResults(default_units=section.default_units, theta=theta, n_target=n)
        return section.calculate_service_stress(stub, m=0.0, kappa=curvature)

    def moment_error(curvature: float) -> float:
        moments = stress_at(curvature).sum_moments()
        return math.hypot(moments[0], moments[1]) - m

    description = f"cracked stress analysis for forces {forces}"
    with _suppress_pure_axial_warning(), _wrap_backend_geometry_errors(), _wrap_backend_convergence_errors(description):
        curvature = _solve_service_curvature(moment_error, m / (elastic_modulus * i_cracked))
        return stress_at(curvature)


def _solve_service_curvature(moment_error: Callable[[float], float], curvature_guess: float) -> float:
    """Bracket and solve the curvature whose no-tension service state carries the target moment.

    The moment grows monotonically with curvature at a fixed axial force, so the pure-bending estimate
    ``curvature_guess`` seeds a bracket that is expanded outward until it straddles the target, then closed
    with a bracketing root finder.

    Parameters
    ----------
    moment_error : Callable[[float], float]
        Signed difference between the moment carried at a trial curvature and the target moment.
    curvature_guess : float
        Curvature estimate from the pure-bending cracked stiffness (m / (E * I_cracked)) [1/mm].

    Returns
    -------
    float
        The curvature whose service state carries the target moment [1/mm].

    Raises
    ------
    ValueError
        If a straddling bracket cannot be found within the iteration budget.
    """
    low, high = curvature_guess * _CURVATURE_BRACKET_START, curvature_guess
    for _ in range(_CURVATURE_BRACKET_STEPS):
        if moment_error(high) >= 0.0:
            break
        high *= 2.0
    else:
        raise ValueError("Could not bracket the cracked curvature: the moment stays below the target across the search range.")
    for _ in range(_CURVATURE_BRACKET_STEPS):
        if moment_error(low) <= 0.0:
            break
        low *= 0.5
    else:
        raise ValueError("Could not bracket the cracked curvature: the moment stays above the target across the search range.")
    return brentq(moment_error, low, high, xtol=_CURVATURE_XTOL, rtol=_CURVATURE_RTOL)


def ultimate_capacity(section: ConcreteSection, n: KN, theta: DEG) -> UltimateCapacityResult:
    """Compute the ultimate (ULS) bending capacity at a given axial force and neutral-axis angle.

    The backend iterates the neutral-axis depth until the internal axial force balances ``n``, with the
    strain plane pivoting on the concrete crushing strain at the extreme compression fibre. The section
    must be built at ``AnalysisLevel.ULS`` (design materials).

    Parameters
    ----------
    section : ConcreteSection
        The backend section built by :func:`build_concrete_section` at the ULS level.
    n : KN
        The axial force in Blueprints conventions (tension positive) [kN].
    theta : DEG
        The neutral-axis angle, measured counter-clockwise from the section x-axis [deg]. ``0`` gives
        the sagging capacity about the y-axis, ``180`` the hogging capacity.

    Returns
    -------
    UltimateCapacityResult
        The capacity in Blueprints conventions.

    Raises
    ------
    ValueError
        If the neutral-axis iteration cannot reach equilibrium (for example an axial force beyond the
        squash or tensile capacity of the section), or on a backend geometry failure.
    """
    description = f"ultimate bending capacity analysis (n={n} kN, theta={theta} deg)"
    with _suppress_pure_axial_warning(), _wrap_backend_geometry_errors(), _wrap_backend_convergence_errors(description):
        raw = section.ultimate_bending_capacity(theta=math.radians(theta), n=-n * KN_TO_N)
    n_out, m_y, m_z = _from_backend_actions(raw.n, raw.m_x, raw.m_y)
    return UltimateCapacityResult(
        n=n_out,
        m_y_rd=m_y,
        m_z_rd=m_z,
        m_rd=math.hypot(m_y, m_z),
        neutral_axis_depth=raw.d_n,
        neutral_axis_angle=math.degrees(raw.theta),
        k_u=raw.k_u,
        raw=raw,
    )


def moment_interaction(section: ConcreteSection, theta: DEG, n_points: int) -> MomentInteractionResult:
    """Generate the uniaxial N-M interaction diagram for a fixed neutral-axis angle.

    The backend traverses neutral-axis depths from the pure-compression (squash) point to the
    zero-curvature tension point, adding the pure-compression, balanced and pure-bending control points.

    Parameters
    ----------
    section : ConcreteSection
        The backend section built by :func:`build_concrete_section` at the ULS level.
    theta : DEG
        The neutral-axis angle, measured counter-clockwise from the section x-axis [deg].
    n_points : int
        Number of points to compute including and between the diagram limits.

    Returns
    -------
    MomentInteractionResult
        The interaction diagram in Blueprints conventions.

    Raises
    ------
    ValueError
        If a diagram point cannot reach equilibrium, or on a backend geometry failure.
    """
    description = f"moment interaction analysis (theta={theta} deg)"
    with _suppress_pure_axial_warning(), _wrap_backend_geometry_errors(), _wrap_backend_convergence_errors(description):
        raw = section.moment_interaction_diagram(theta=math.radians(theta), n_points=n_points, progress_bar=False)
    return MomentInteractionResult(theta=theta, points=tuple(_to_interaction_point(result) for result in raw.results), raw=raw)


def _to_interaction_point(result: UltimateBendingResults) -> InteractionPoint:
    """Map one backend ultimate bending result to a Blueprints interaction point."""
    n, m_y, m_z = _from_backend_actions(result.n, result.m_x, result.m_y)
    return InteractionPoint(n=n, m_y=m_y, m_z=m_z, m=math.hypot(m_y, m_z), label=result.label)


def biaxial_interaction(section: ConcreteSection, n: KN, n_points: int) -> BiaxialInteractionResult:
    """Generate the biaxial M_y-M_z interaction envelope at a fixed axial force.

    The backend traverses the neutral-axis angle over a full revolution, computing the ultimate bending
    capacity at each angle for the fixed axial force; the envelope is closed (the first point is
    repeated at the end).

    Parameters
    ----------
    section : ConcreteSection
        The backend section built by :func:`build_concrete_section` at the ULS level.
    n : KN
        The fixed axial force in Blueprints conventions (tension positive) [kN].
    n_points : int
        Number of neutral-axis angles to compute over the full revolution.

    Returns
    -------
    BiaxialInteractionResult
        The biaxial envelope in Blueprints conventions.

    Raises
    ------
    ValueError
        If an envelope point cannot reach equilibrium (for example an axial force beyond the squash or
        tensile capacity), or on a backend geometry failure.
    """
    description = f"biaxial interaction analysis (n={n} kN)"
    with _suppress_pure_axial_warning(), _wrap_backend_geometry_errors(), _wrap_backend_convergence_errors(description):
        raw = section.biaxial_bending_diagram(n=-n * KN_TO_N, n_points=n_points, progress_bar=False)
    return BiaxialInteractionResult(n=n, points=tuple(_to_interaction_point(result) for result in raw.results), raw=raw)


def _ultimate_strain_plane(polygon: Polygon, theta: float, neutral_axis_depth: MM, ultimate_strain: float) -> StrainPlane:
    """Build the ULS strain plane directly from the pivot geometry (never from ``stress / E``).

    At ultimate the strain plane is still affine (Bernoulli), but the concrete law is non-linear, so the
    plane cannot be reconstructed from stresses. It follows exactly from the pivot: the concrete
    crushing strain at the extreme compression fibre, zero at the neutral axis a depth ``d_n`` below it.

    Parameters
    ----------
    polygon : Polygon
        The section profile polygon, used to locate the extreme compression fibre.
    theta : float
        The backend neutral-axis angle [rad].
    neutral_axis_depth : MM
        The ultimate neutral-axis depth d_n from the extreme compression fibre [mm].
    ultimate_strain : float
        The concrete crushing strain eps_cu at the pivot (ratio, positive).

    Returns
    -------
    StrainPlane
        The ULS strain plane in Blueprints conventions (compression negative).
    """
    coords = np.asarray(polygon.exterior.coords, dtype=float)
    # distance along the compression direction (the rotated "up" axis): v = -x sin(theta) + y cos(theta)
    v = -coords[:, 0] * math.sin(theta) + coords[:, 1] * math.cos(theta)
    v_neutral_axis = float(v.max()) - neutral_axis_depth
    gradient = ultimate_strain / neutral_axis_depth
    kappa_z = gradient * math.sin(theta)
    kappa_y = -gradient * math.cos(theta)
    angle = (math.degrees(math.atan2(kappa_y, kappa_z)) + 90.0 + 90.0) % 180.0 - 90.0
    return StrainPlane(
        eps_0=gradient * v_neutral_axis * RATIO_TO_PER_MILLE,
        kappa_y=kappa_y,
        kappa_z=kappa_z,
        neutral_axis_depth=neutral_axis_depth,
        neutral_axis_angle=angle,
    )


def analyse_ultimate(section: ConcreteSection, forces: SectionForces, elastic_modulus: MPA, geometry: Polygon) -> StressStrainResult:
    """Run the backend ultimate (ULS) stress analysis for the given design action.

    The ULS state belonging to the design action is the ultimate state at its axial force and moment
    direction: the neutral-axis angle follows from the moment vector, and the neutral-axis depth is
    iterated until the internal axial force balances the design axial force with the strain plane
    pivoting on the concrete crushing strain. The reported stresses are those of that failure state
    (the design stress blocks at M_Rd), not scaled to the moment magnitude.

    Parameters
    ----------
    section : ConcreteSection
        The backend section built by :func:`build_concrete_section` at the ULS level.
    forces : SectionForces
        The design action in Blueprints conventions; the moment components set the bending direction.
    elastic_modulus : MPA
        The concrete secant modulus e_cm, carried on the result for reference (the ULS stresses follow
        the non-linear design profile, not this modulus).
    geometry : Polygon
        The section profile polygon, carried on the result for plotting.

    Returns
    -------
    StressStrainResult
        The ULS stress/strain result, compression negative, with the strain plane taken from the pivot
        geometry.

    Raises
    ------
    ValueError
        If the neutral-axis iteration cannot reach equilibrium, or on a backend geometry failure.
    """
    n, theta, _ = _to_cracked_actions(forces)
    description = f"ultimate stress analysis for forces {forces}"
    with _suppress_pure_axial_warning(), _wrap_backend_geometry_errors(), _wrap_backend_convergence_errors(description):
        ultimate = section.ultimate_bending_capacity(theta=theta, n=n)
        raw = section.calculate_ultimate_stress(ultimate_results=ultimate)
    strain_plane = _ultimate_strain_plane(
        geometry,
        theta=ultimate.theta,
        neutral_axis_depth=ultimate.d_n,
        ultimate_strain=section.gross_properties.conc_ultimate_strain,
    )
    return _to_stress_strain_result(
        forces,
        raw,
        elastic_modulus,
        geometry,
        regime=Regime.ULS,
        strain_plane=strain_plane,
        # the concrete geometry always carries a backend Concrete (built by this adapter), which has the
        # ultimate profile; the backend's static Material type is broader.
        concrete_profile=section.concrete_geometries[0].material.ultimate_stress_strain_profile,  # ty: ignore[unresolved-attribute]
    )


def moment_curvature(section: ConcreteSection, theta: DEG, n: KN) -> MomentCurvatureResult:
    """Trace the moment-curvature response at a fixed axial force and neutral-axis angle.

    The backend increases the curvature adaptively, solving axial equilibrium at each step, until a
    material reaches its ultimate strain (concrete crushing or steel fracture). The section must be
    built at ``AnalysisLevel.ULS``: its service curve (bilinear-horizontal concrete with a tension
    branch, steel at f_yd) drives the response.

    Parameters
    ----------
    section : ConcreteSection
        The backend section built by :func:`build_concrete_section` at the ULS level.
    theta : DEG
        The neutral-axis angle, measured counter-clockwise from the section x-axis [deg].
    n : KN
        The fixed axial force in Blueprints conventions (tension positive) [kN].

    Returns
    -------
    MomentCurvatureResult
        The moment-curvature response in Blueprints conventions.

    Raises
    ------
    ValueError
        If a curvature step cannot reach axial equilibrium, or on a backend geometry failure.
    """
    description = f"moment-curvature analysis (n={n} kN, theta={theta} deg)"
    with _suppress_pure_axial_warning(), _wrap_backend_geometry_errors(), _wrap_backend_convergence_errors(description):
        raw = section.moment_curvature_analysis(theta=math.radians(theta), n=-n * KN_TO_N, progress_bar=False)
    return MomentCurvatureResult(
        theta=theta,
        n=n,
        kappa=tuple(raw.kappa),
        m_y=tuple(m_x * NMM_TO_KNM for m_x in raw.m_x),
        m_z=tuple(-m_y * NMM_TO_KNM for m_y in raw.m_y),
        m=tuple(m_xy * NMM_TO_KNM for m_xy in raw.m_xy),
        raw=raw,
    )
