"""Frozen result objects for reinforced-concrete cross-section analysis.

All values are in Blueprints conventions and units: stresses and strains are **compression negative /
tension positive**, consistent with section forces where a positive normal force is tension.
"""

from collections.abc import Sequence
from dataclasses import dataclass
from typing import Any

from matplotlib.axes import Axes
from matplotlib.figure import Figure

from blueprints.structural_sections.concrete.reinforced_concrete_sections.analysis.plotting import plot_stress_strain
from blueprints.structural_sections.section_forces import SectionForces
from blueprints.type_alias import DEG, KN, KNM, MM, MM4, MPA, ONE_OVER_MM, PER_MILLE, RAD
from blueprints.unit_conversion import RATIO_TO_PER_MILLE


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
class StrainPlane:
    """Linear strain field over the cross-section (plane sections remain plane).

    The strain at a point ``(x, y)`` in the cross-section plane follows from ``strain_at`` and is
    expressed compression negative / tension positive. ``x`` is the horizontal and ``y`` the vertical
    cross-section coordinate — the same axes as ``Rebar.x`` / ``Rebar.y`` and the section profile.

    Parameters
    ----------
    eps_0 : PER_MILLE
        Strain at the section origin (``x = y = 0``), compression negative / tension positive [‰].
    kappa_y : ONE_OVER_MM
        Curvature about the y-axis: the strain gradient in the vertical (y) direction, as a ratio strain
        per mm [1/mm]. Driven by ``m_y``.
    kappa_z : ONE_OVER_MM
        Curvature about the z-axis: the strain gradient in the horizontal (x) direction, as a ratio
        strain per mm [1/mm]. Driven by ``m_z``.
    neutral_axis_depth : MM | None
        Perpendicular distance from the extreme compression fibre to the zero-strain (neutral) line
        [mm]. ``None`` when the section has no curvature (pure axial) or no fibre in compression.
    neutral_axis_angle : DEG
        Orientation of the neutral (zero-strain) line, measured counter-clockwise from the x-axis and
        normalized to ``[-90, 90)`` [deg]. ``0`` for a horizontal neutral axis (pure ``m_y`` bending) and
        ``0`` by convention when there is no curvature.
    """

    eps_0: PER_MILLE
    kappa_y: ONE_OVER_MM
    kappa_z: ONE_OVER_MM
    neutral_axis_depth: MM | None
    neutral_axis_angle: DEG

    def strain_at(self, x: MM, y: MM) -> PER_MILLE:
        """Return the strain at cross-section point ``(x, y)``.

        Parameters
        ----------
        x : MM
            Horizontal cross-section coordinate [mm].
        y : MM
            Vertical cross-section coordinate [mm].

        Returns
        -------
        PER_MILLE
            Strain at the point, compression negative / tension positive [‰].
        """
        return self.eps_0 + (self.kappa_z * x + self.kappa_y * y) * RATIO_TO_PER_MILLE


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
    strain_plane : StrainPlane | None
        The reconstructed linear strain field over the section. Always populated by the analyzer; the
        default ``None`` exists only for lightweight construction in tests.
    elastic_modulus : MPA
        The concrete elastic modulus (e_cm) used for the analysis, needed by :meth:`plot` to turn the
        strain profile into a concrete-stress profile [MPa].
    geometry : Any
        The section profile polygon (shapely ``Polygon``), used by :meth:`plot` to draw the section
        panel. Always populated by the analyzer; the default ``None`` exists only for lightweight
        construction in tests.
    """

    forces: SectionForces
    is_cracked: bool
    concrete_stress_min: MPA
    concrete_stress_max: MPA
    rebar_results: Sequence[RebarStressResult]
    raw: Any
    cracked_properties: CrackedProperties | None = None
    strain_plane: StrainPlane | None = None
    elastic_modulus: MPA = 0.0
    geometry: Any = None

    def plot(self, *, figsize: tuple[float, float] = (11.0, 6.0)) -> Figure:
        """Plot the strain and stress diagrams over the section height (IDEA-RCS style).

        Draws three panels sharing the section-height axis: the section with its reinforcement, the
        linear strain profile (‰, compression negative), and the stress profile (MPa, compression
        negative) with the reinforcement stresses marked. The profiles are projected onto the axis
        perpendicular to the neutral axis, so uniaxial and biaxial-uncracked states both render upright.

        Parameters
        ----------
        figsize : tuple[float, float]
            Figure size in inches, forwarded to matplotlib.

        Returns
        -------
        Figure
            The matplotlib figure with the three panels.

        Raises
        ------
        ValueError
            If the result was constructed without a strain plane or section geometry (an analyzer always
            supplies both).
        """
        return plot_stress_strain(self, figsize=figsize)

    def plot_mesh_stress(self, *args: object, **kwargs: object) -> Axes:
        """Plot the backend's 2D mesh stress contour, delegating to the backend's stress plot.

        This is the ``concreteproperties`` mesh-contour view (a colour-mapped cross-section), kept
        available under its own name so :meth:`plot` can produce the strain/stress-over-height figure.

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
