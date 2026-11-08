"""Force parameters for torsion analysis."""

from dataclasses import dataclass

from blueprints.type_alias import DEG, MM2, MPA, NMM, N


@dataclass(frozen=True)
class TorsionForces:
    """Contains the force and loading parameters for torsion analysis.

    This class stores all the force parameters needed to perform torsion analysis
    according to structural engineering codes. It includes both applied forces
    and geometric parameters that define the assumed failure mechanism.

    Parameters
    ----------
    sigma_cp : MPA
        Concrete compressive stress due to axial force and prestressing.
        Positive values indicate compression. Used to determine the concrete
        contribution to torsional resistance.
    a_sl : MM2
        Area of the tensile reinforcement, which extends l_bd + d beyond the
        section considered (figure 6.3 EN 1992-1-1:2004).
    v_ed : N
        Design shear force acting on the cross-section.
        Combined with torsion, this affects the concrete strut angle and
        overall member behavior under combined loading.
    t_ed : NMM
        Design torsional moment acting on the cross-section.
        This is the primary torsional force that needs to be resisted by
        the combination of concrete and reinforcement.
    alpha : DEG, default 90
        Angle of the compression struts in the concrete relative to the
        member axis. Typically 90° for pure torsion, but may vary for
        combined shear and torsion. Range typically 45° to 90°.
    theta : DEG, default 45
        Angle of the concrete compression struts relative to the member axis
        in the failure mechanism. Standard assumption is 45° for simplified
        analysis, but may be optimized between 21.8° and 45°.

    Examples
    --------
    >>> # Basic torsion case with standard assumptions
    >>> forces = TorsionForces(
    ...     sigma_cp=2.5,  # MPa compression stress
    ...     a_sl=800.0,  # mm² longitudinal reinforcement
    ...     v_ed=50000,  # N shear force
    ...     t_ed=25000000,  # Nmm torsional moment
    ... )
    >>> print(f"Torsion: {forces.t_ed / 1e6:.1f} kNm")

    >>> # Combined loading with custom strut angles
    >>> forces = TorsionForces(
    ...     sigma_cp=1.8,
    ...     a_sl=1200.0,
    ...     v_ed=75000,
    ...     t_ed=40000000,
    ...     alpha=90,  # Pure torsion assumption
    ...     theta=35,  # Optimized compression strut angle
    ... )

    Notes
    -----
    - The class is frozen (immutable) to ensure force parameters don't change
      during analysis calculations
    - Strut angles (alpha, theta) significantly affect the required reinforcement
    - sigma_cp should account for both axial loads and prestressing effects
    - All forces should be design values (factored) not characteristic values
    """

    sigma_cp: MPA
    a_sl: MM2
    v_ed: N
    t_ed: NMM
    alpha: DEG = 90
    theta: DEG = 45
