"""Frozen result objects for reinforced-concrete cross-section analysis.

All values are in Blueprints conventions and units: stresses and strains are **compression negative /
tension positive**, consistent with section forces where a positive normal force is tension.
"""

from collections.abc import Sequence
from dataclasses import dataclass
from typing import Any

from matplotlib.axes import Axes

from blueprints.structural_sections.section_forces import SectionForces
from blueprints.type_alias import KN, KNM, MM, MM4, MPA, PER_MILLE, RAD


@dataclass(frozen=True)
class RebarStressResult:
    """Stress and strain state of a single reinforcement bar.

    Parameters
    ----------
    x : MM
        x-coordinate of the bar centroid in the cross-section plane [mm].
    y : MM
        y-coordinate of the bar centroid in the cross-section plane [mm].
    diameter : MM
        Bar diameter [mm].
    stress : MPA
        Axial stress in the bar, compression negative / tension positive [MPa].
    strain : PER_MILLE
        Axial strain in the bar, compression negative / tension positive [‰].
    force : KN
        Axial force in the bar, compression negative / tension positive [kN].
    """

    x: MM
    y: MM
    diameter: MM
    stress: MPA
    strain: PER_MILLE
    force: KN


@dataclass(frozen=True)
class CrackedProperties:
    """Cracked-section properties of a reinforced-concrete cross-section.

    Parameters
    ----------
    m_cr : KNM
        Cracking moment of the section [kNm].
    neutral_axis_depth : MM
        Depth of the cracked neutral axis from the extreme compression fibre [mm].
    theta : RAD
        Angle of the neutral axis used for the cracked analysis [rad].
    i_cracked : MM4
        Second moment of area of the cracked transformed section about the neutral axis [mm⁴].
    raw : Any
        The underlying backend cracked-results object, kept as an escape hatch for advanced use.
    """

    m_cr: KNM
    neutral_axis_depth: MM
    theta: RAD
    i_cracked: MM4
    raw: Any


@dataclass(frozen=True)
class StressStrainResult:
    """Result of a reinforced-concrete cross-section stress/strain analysis.

    Parameters
    ----------
    forces : SectionForces
        The section forces that produced this result (echoed back for traceability).
    is_cracked : bool
        Which regime produced the result: ``True`` if the cracked analysis was used, ``False`` for uncracked.
    concrete_stress_min : MPA
        Most compressive concrete stress (algebraic minimum), compression negative [MPa].
    concrete_stress_max : MPA
        Most tensile concrete stress (algebraic maximum), compression negative [MPa].
    rebar_results : Sequence[RebarStressResult]
        Per-bar stress/strain results.
    raw : Any
        The underlying backend result object, kept as an escape hatch for advanced use.
    cracked_properties : CrackedProperties | None
        The cracked-section properties when ``is_cracked`` is ``True``; ``None`` for an uncracked result.
    """

    forces: SectionForces
    is_cracked: bool
    concrete_stress_min: MPA
    concrete_stress_max: MPA
    rebar_results: Sequence[RebarStressResult]
    raw: Any
    cracked_properties: CrackedProperties | None = None

    def plot(self, *args: object, **kwargs: object) -> Axes:
        """Plot the stress state, delegating to the backend's stress plot.

        Parameters
        ----------
        *args : object
            Positional arguments forwarded to the backend plotter.
        **kwargs : object
            Keyword arguments forwarded to the backend plotter.

        Returns
        -------
        Axes
            The matplotlib axes produced by the backend plotter.
        """
        return self.raw.plot_stress(*args, **kwargs)
