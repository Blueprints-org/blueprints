"""Private adapter between Blueprints reinforced cross-sections and the ``concreteproperties`` backend.

This is the **only** module that imports ``concreteproperties``, so a future backend swap touches one file.

Unit and convention handling lives here: Blueprints uses kN/kNm, ‰ strain and a tension-positive sign
convention, while ``concreteproperties`` works in N/mm, absolute strain and compression-positive. The
material mappers below convert strains (‰ → ratio) and densities; force/sign conversion happens at the
analysis call site (added in a later step).
"""

import math
import warnings
from collections.abc import Iterator
from contextlib import contextmanager
from enum import Enum

from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_3_materials.formula_3_23 import Form3Dot23FlexuralTensileStrength
from blueprints.materials.concrete import ConcreteMaterial, DiagramType
from blueprints.materials.reinforcement_steel import ReinforcementSteelMaterial
from blueprints.structural_sections.concrete.reinforced_concrete_sections.analysis.results import (
    CrackedProperties,
    RebarStressResult,
    StressStrainResult,
)
from blueprints.structural_sections.concrete.reinforced_concrete_sections.base import ReinforcedCrossSection
from blueprints.structural_sections.section_forces import SectionForces
from blueprints.type_alias import KN, KNM, MPA
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
        add_bar,
    )
    from concreteproperties.results import CrackedResults, StressResult
    from concreteproperties.stress_strain_profile import ConcreteUltimateProfile
except ImportError as exc:  # pragma: no cover
    raise ImportError(
        "Reinforced-concrete section analysis requires the optional 'concreteproperties' backend. "
        "Install it with: pip install blue-prints[rc-analysis]"
    ) from exc

from sectionproperties.pre import Geometry  # core dependency, always available

_CONCRETE_COLOUR = "lightgrey"
_STEEL_COLOUR = "grey"


class AnalysisLevel(Enum):
    """Material model level driving the stress-strain profiles handed to the backend.

    SLS keeps steel elastic at f_yk/E_s (no partial factor); ULS (future) yields at f_yd. The analyzer
    caches one backend section per level, so only the level needed for a given analysis is ever built.
    """

    SLS = "SLS"
    ULS = "ULS"


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


def _service_concrete(concrete: ConcreteMaterial, flexural_tensile_strength: MPA) -> Concrete:
    """Map a Blueprints concrete material to a backend SLS ``Concrete`` (linear-elastic service profile).

    Parameters
    ----------
    concrete : ConcreteMaterial
        The Blueprints concrete material.
    flexural_tensile_strength : MPA
        The flexural tensile strength f_ctm,fl [MPa] used by the backend's cracked-section logic;
        computed once per section from the member height (see ``build_concrete_section``).

    Returns
    -------
    Concrete
        The backend concrete material with a linear service profile and a filled ultimate profile.
    """
    return Concrete(
        name=concrete.name,
        density=concrete.density * MM3_TO_M3,
        stress_strain_profile=ConcreteLinear(elastic_modulus=concrete.e_cm),
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


def build_concrete_section(cross_section: ReinforcedCrossSection, level: AnalysisLevel = AnalysisLevel.SLS) -> ConcreteSection:
    """Build a backend ``ConcreteSection`` from a Blueprints reinforced cross-section.

    The section profile becomes the concrete geometry and each longitudinal rebar is added as a lumped
    bar. Reinforcement materials are mapped to distinct ``SteelBar`` instances, reusing one instance per
    distinct Blueprints material. The flexural tensile strength is taken from formula 3.23 using the
    profile's bounding-box height.

    Parameters
    ----------
    cross_section : ReinforcedCrossSection
        The Blueprints reinforced cross-section (geometry + materials + longitudinal rebars).
    level : AnalysisLevel
        The material model level. Only ``AnalysisLevel.SLS`` is implemented.

    Returns
    -------
    ConcreteSection
        The backend section ready for stress/strain analysis.

    Raises
    ------
    NotImplementedError
        If a level other than SLS is requested.
    """
    if level is not AnalysisLevel.SLS:
        raise NotImplementedError(f"Analysis level {level.value!r} is not implemented yet; only SLS is available.")

    polygon = cross_section.profile.polygon
    concrete = _service_concrete(cross_section.concrete_material, flexural_tensile_strength(cross_section))
    # concreteproperties materials are accepted structurally by sectionproperties' Geometry but are not a
    # nominal subclass of sectionproperties.pre.Material, so the static type does not line up.
    geometry = Geometry(geom=polygon, material=concrete)  # ty: ignore[invalid-argument-type]

    steel_bars: dict[ReinforcementSteelMaterial, SteelBar] = {}
    for rebar in cross_section.longitudinal_rebars:
        material = rebar.material
        if material not in steel_bars:
            steel_bars[material] = _service_steel(material)
        geometry = add_bar(geometry, area=rebar.area, material=steel_bars[material], x=rebar.x, y=rebar.y)

    # add_bar returns a CompoundGeometry at runtime; the union annotation in the backend stub loses that.
    return ConcreteSection(geometry)  # ty: ignore[invalid-argument-type]


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


def analyse_uncracked(section: ConcreteSection, forces: SectionForces) -> StressStrainResult:
    """Run the backend uncracked stress analysis and map the result to Blueprints conventions.

    Parameters
    ----------
    section : ConcreteSection
        The backend section built by :func:`build_concrete_section`.
    forces : SectionForces
        The section forces in Blueprints conventions.

    Returns
    -------
    StressStrainResult
        The uncracked stress/strain result, compression negative.
    """
    n, m_x, m_y = _to_backend_actions(forces)
    with _suppress_pure_axial_warning():
        raw = section.calculate_uncracked_stress(n=n, m_x=m_x, m_y=m_y)
    return _to_stress_strain_result(forces=forces, raw=raw, is_cracked=False)


def _to_stress_strain_result(
    forces: SectionForces,
    raw: StressResult,
    *,
    is_cracked: bool,
    cracked_properties: CrackedProperties | None = None,
) -> StressStrainResult:
    """Map a backend ``StressResult`` to a Blueprints ``StressStrainResult`` (compression negative).

    Parameters
    ----------
    forces : SectionForces
        The section forces that produced the result, echoed back.
    raw : StressResult
        The backend ``StressResult`` (concrete stresses compression-positive).
    is_cracked : bool
        Which regime produced the result.
    cracked_properties : CrackedProperties | None
        The cracked-section properties for a cracked result, or ``None`` for an uncracked result.

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
    for geometry, stress, strain, force in zip(
        raw.lumped_reinforcement_geometries,
        raw.lumped_reinforcement_stresses,
        raw.lumped_reinforcement_strains,
        raw.lumped_reinforcement_forces,
        strict=True,
    ):
        x, y = geometry.calculate_centroid()
        diameter = math.sqrt(4 * geometry.calculate_area() / math.pi)
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

    return StressStrainResult(
        forces=forces,
        is_cracked=is_cracked,
        concrete_stress_min=concrete_stress_min,
        concrete_stress_max=concrete_stress_max,
        rebar_results=rebar_results,
        raw=raw,
        cracked_properties=cracked_properties,
    )


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


def _cracked_results(section: ConcreteSection, forces: SectionForces, elastic_modulus: MPA) -> tuple[CrackedResults, float, float]:
    """Run the backend cracked-properties analysis and populate its transformed properties.

    Parameters
    ----------
    section : ConcreteSection
        The backend section.
    forces : SectionForces
        The section forces in Blueprints conventions.
    elastic_modulus : MPA
        Reference elastic modulus for the transformed cracked properties (the concrete e_cm).

    Returns
    -------
    tuple[CrackedResults, float, float]
        The backend cracked results plus the backend ``(n, m)`` actions for a subsequent stress analysis.

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
    try:
        cracked = section.calculate_cracked_properties(theta=theta)
    except (ValueError, RuntimeError) as exc:
        raise RuntimeError(f"Cracked neutral-axis analysis did not converge for forces {forces}: {exc}") from exc
    cracked.calculate_transformed_properties(elastic_modulus=elastic_modulus)
    return cracked, n, m


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


def cracked_properties(section: ConcreteSection, forces: SectionForces, elastic_modulus: MPA) -> CrackedProperties:
    """Compute the cracked-section properties for the given forces.

    Parameters
    ----------
    section : ConcreteSection
        The backend section.
    forces : SectionForces
        The section forces in Blueprints conventions.
    elastic_modulus : MPA
        Reference elastic modulus (the concrete e_cm).

    Returns
    -------
    CrackedProperties
        The cracked-section properties in Blueprints conventions.
    """
    cracked, _, _ = _cracked_results(section, forces, elastic_modulus)
    return _to_cracked_properties(cracked)


def analyse_cracked(section: ConcreteSection, forces: SectionForces, elastic_modulus: MPA) -> StressStrainResult:
    """Run the backend cracked stress analysis and map the result to Blueprints conventions.

    Parameters
    ----------
    section : ConcreteSection
        The backend section.
    forces : SectionForces
        The section forces in Blueprints conventions.
    elastic_modulus : MPA
        Reference elastic modulus (the concrete e_cm).

    Returns
    -------
    StressStrainResult
        The cracked stress/strain result, compression negative, carrying the cracked properties.
    """
    cracked, n, m = _cracked_results(section, forces, elastic_modulus)
    raw = section.calculate_cracked_stress(cracked_results=cracked, n=n, m=m)
    return _to_stress_strain_result(forces, raw, is_cracked=True, cracked_properties=_to_cracked_properties(cracked))
