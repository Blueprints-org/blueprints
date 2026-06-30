"""Private adapter between Blueprints reinforced cross-sections and the ``concreteproperties`` backend.

This is the **only** module that imports ``concreteproperties``, so a future backend swap touches one file.

Unit and convention handling lives here: Blueprints uses kN/kNm, ‰ strain and a tension-positive sign
convention, while ``concreteproperties`` works in N/mm, absolute strain and compression-positive. The
material mappers below convert strains (‰ → ratio) and densities; force/sign conversion happens at the
analysis call site (added in a later step).
"""

from enum import Enum

from blueprints.codes.eurocode.en_1992_1_1_2004.chapter_3_materials.formula_3_23 import Form3Dot23FlexuralTensileStrength
from blueprints.materials.concrete import ConcreteMaterial, DiagramType
from blueprints.materials.reinforcement_steel import ReinforcementSteelMaterial
from blueprints.structural_sections.concrete.reinforced_concrete_sections.base import ReinforcedCrossSection
from blueprints.type_alias import MPA
from blueprints.unit_conversion import MM3_TO_M3, PER_MILLE_TO_RATIO

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
