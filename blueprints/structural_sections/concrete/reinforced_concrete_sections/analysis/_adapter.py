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
from blueprints.structural_sections.concrete.reinforced_concrete_sections.analysis.results import RebarStressResult, StressStrainResult
from blueprints.structural_sections.concrete.reinforced_concrete_sections.base import ReinforcedCrossSection
from blueprints.structural_sections.section_forces import SectionForces
from blueprints.type_alias import KN, KNM, MPA
from blueprints.unit_conversion import KN_TO_N, KNM_TO_NMM, MM3_TO_M3, N_TO_KN, PER_MILLE_TO_RATIO, RATIO_TO_PER_MILLE

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
    from concreteproperties.results import StressResult
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
    _, min_y, _, max_y = polygon.bounds
    section_height = max_y - min_y
    flexural_tensile_strength = float(Form3Dot23FlexuralTensileStrength(h=section_height, f_ctm=cross_section.concrete_material.f_ctm))

    concrete = _service_concrete(cross_section.concrete_material, flexural_tensile_strength)
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


def _to_stress_strain_result(forces: SectionForces, raw: StressResult, *, is_cracked: bool) -> StressStrainResult:
    """Map a backend ``StressResult`` to a Blueprints ``StressStrainResult`` (compression negative).

    Parameters
    ----------
    forces : SectionForces
        The section forces that produced the result, echoed back.
    raw : StressResult
        The backend ``StressResult`` (concrete stresses compression-positive).
    is_cracked : bool
        Which regime produced the result.

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
    )
