"""Resultant internal forces used for strength or stability checks.

Internal forces on line, beam, member. Result in member axis (not in principal axis).
"""

from dataclasses import dataclass

from blueprints.type_alias import KN, KNM, M


@dataclass(frozen=True)
class ResultInternalForce1D:
    """Resultant internal forces used for strength or stability checks.
    definition following https://www.saf.guide/en/stable/results/resultinternalforce1d.html.

    Internal forces on line, beam, member.

                    z (vertical, usually strong axis)
                ↑
                |     x (longitudinal beam direction, into screen)
                |    ↗
                |   /
                |  /
                | /
                |/
      ←---------O
       y (horizontal/side, usually weak axis)

        Sign conventions:
        - Normal force N_x: positive = tension, negative = compression.
        - Shear force V_y: positive = left (see coordinate system above).
        - Shear force V_z: positive = up (see coordinate system above).
        - Torsion M_x: positive = from y to z (twisting around x-axis, see coordinate system above).
        - Bending moment M_y: positive = from z to x (rotation around y-axis, see coordinate system above).
        - Bending moment M_z: positive = from x to y (rotation around z-axis, see coordinate system above).

    Attributes
    ----------
    result_on : str
        Specify object where the result is (e.g., "On beam", "On rib").
    member : str
        Reference to the name of 1D member (required if result_on = "On beam").
    member_rib : str
        Reference to the name of 1D member rib (required if result_on = "On rib").
    result_for : str
        Specifies from where the result is coming from (e.g., "Load case", "Load combination").
    load_case : str
        Reference to the name of the load case (required if result_for = "Load case").
    load_combination : str
        Reference to the name of the load combination (required if result_for = "Combination").
    combination_key : str
        Exact combination string, e.g., "1.35*LC1+1.5*LC2".
    section_at : float
        X coordinate on the beam (distance from the start node) where the result is located [m].
    index : int
        Index of the section on beam (order from start to end).
    N : KN
        Result value of N (Normal force) [kN].
    Vy : KN
        Result value of Vy (Shear force in Y axis direction) [kN].
    Vz : KN
        Result value of Vz (Shear force in Z axis direction) [kN].
    Mx : KNM
        Result value of Mx (Moment around X axis) [kNm].
    My : KNM
        Result value of My (Moment around Y axis) [kNm].
    Mz : KNM
        Result value of Mz (Moment around Z axis) [kNm].
    """

    result_on: str = ""
    member: str = ""
    member_rib: str = ""
    result_for: str = ""
    load_case: str = ""
    load_combination: str = ""
    combination_key: str = ""
    section_at: M = 0
    index: int = 0
    N: KN = 0
    Vy: KN = 0
    Vz: KN = 0
    Mx: KNM = 0
    My: KNM = 0
    Mz: KNM = 0
