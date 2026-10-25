"""Material-agnostic section forces acting on a cross-section.

The six force components and their sign conventions mirror the SAF member axis system documented in
:class:`blueprints.saf.results.result_internal_force_1d.ResultInternalForce1D`, so the two never drift.
"""

from dataclasses import dataclass

from blueprints.saf.results.result_internal_force_1d import ResultInternalForce1D
from blueprints.type_alias import KN, KNM


@dataclass(frozen=True)
class SectionForces:
    """Internal forces on a cross-section, in the SAF member axis system.

    This object is pure statics: six force components on a section, with no load-combination classification.
    It is material-agnostic, so concrete, steel and other checks can adopt it.

    Coordinate System:

        z (vertical, usually strong axis)
            ↑
            |     x (longitudinal beam direction, into screen)
            |    ↗
            |   /
            |  /
            | /
            |/
      ←-----O
       y (horizontal/side, usually weak axis)

    Sign Conventions (identical to ResultInternalForce1D):
    - Normal force ``n`` (N_x): positive = tension, negative = compression.
    - Shear force ``v_y`` (V_y): positive = along +y.
    - Shear force ``v_z`` (V_z): positive = along +z.
    - Torsion ``t`` (M_x): positive = from y to z (twisting around x-axis).
    - Bending moment ``m_y`` (M_y): positive = from x to z (rotation around y-axis).
    - Bending moment ``m_z`` (M_z): positive = from x to y (rotation around z-axis).

    Parameters
    ----------
    n : KN
        Axial force, positive = tension [kN]. Default 0.0.
    v_y : KN
        Shear force in y-direction [kN]. Not used by strain-plane analyses. Default 0.0.
    v_z : KN
        Shear force in z-direction [kN]. Not used by strain-plane analyses. Default 0.0.
    t : KNM
        Torsional moment (SAF M_x) [kNm]. Not used by strain-plane analyses. Default 0.0.
    m_y : KNM
        Bending moment about the y-axis [kNm]. Default 0.0.
    m_z : KNM
        Bending moment about the z-axis [kNm]. Default 0.0.
    """

    n: KN = 0.0
    v_y: KN = 0.0
    v_z: KN = 0.0
    t: KNM = 0.0
    m_y: KNM = 0.0
    m_z: KNM = 0.0

    @classmethod
    def from_saf_result(cls, result: ResultInternalForce1D) -> "SectionForces":
        """Create a ``SectionForces`` from a SAF ``ResultInternalForce1D``.

        Both objects use the same SAF member axis system, units (kN/kNm) and sign conventions,
        so no unit or sign conversion is applied. The SAF torsional moment ``mx`` maps to ``t``.

        Parameters
        ----------
        result : ResultInternalForce1D
            The SAF internal force result to convert.

        Returns
        -------
        SectionForces
            The section forces carrying the same six components.
        """
        return cls(
            n=result.n,
            v_y=result.vy,
            v_z=result.vz,
            t=result.mx,
            m_y=result.my,
            m_z=result.mz,
        )
