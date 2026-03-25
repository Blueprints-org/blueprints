"""Resultant internal forces used for strength or stability checks.

Internal forces on line, beam, member. Result in member axis (not in principal axis).
"""

from dataclasses import dataclass
from enum import Enum

from blueprints.type_alias import KN, KNM, M


class ResultOn(str, Enum):
    """Enumeration for where the internal force result is located.

    Following SAF standard specification for ResultInternalForce1D.
    """

    ON_BEAM = "On beam"
    ON_RIB = "On rib"


class ResultFor(str, Enum):
    """Enumeration for the source type of the internal force result.

    Following SAF standard specification for ResultInternalForce1D.
    """

    LOAD_CASE = "Load case"
    LOAD_COMBINATION = "Load combination"


@dataclass(frozen=True)
class ResultInternalForce1D:
    """Internal forces on line, beam, member. Result in member axis (not in principal axis).

    Definition following https://www.saf.guide/en/stable/results/resultinternalforce1d.html.

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

    Sign Conventions:
    - Normal force N_x: positive = tension, negative = compression.
    - Shear force V_y: positive = left (see coordinate system above).
    - Shear force V_z: positive = up (see coordinate system above).
    - Torsion M_x: positive = from y to z (twisting around x-axis, see coordinate system above).
    - Bending moment M_y: positive = from z to x (rotation around y-axis, see coordinate system above).
    - Bending moment M_z: positive = from x to y (rotation around z-axis, see coordinate system above).

    Attributes
    ----------
    result_on : ResultOn
        Specifies the object type where the result is located.
        - "On beam": Result on a StructuralCurveMember (requires `member` to be set)
        - "On rib": Result on a StructuralCurveMemberRib (requires `member_rib` to be set)
    member : str
        Reference to the name of the 1D member (StructuralCurveMember).
        Required if and only if result_on = ResultOn.ON_BEAM.
    member_rib : str
        Reference to the name of the 1D member rib (StructuralCurveMemberRib).
        Required if and only if result_on = ResultOn.ON_RIB.
    result_for : ResultFor
        Specifies the source type of the internal force result.
        - "Load case": Result from a single load case (requires `load_case` to be set)
        - "Load combination": Result from a load combination (requires `load_combination` to be set)
    load_case : str
        Reference to the name of the load case (StructuralLoadCase).
        Required if and only if result_for = ResultFor.LOAD_CASE.
    load_combination : str
        Reference to the name of the load combination (StructuralLoadCombination).
        Required if and only if result_for = ResultFor.LOAD_COMBINATION.
    combination_key : str, optional
        Exact combination formula string for envelope or code-based combinations.
        Example: "1.35*LC1+1.5*LC2". Only applicable when result_for = ResultFor.LOAD_COMBINATION.
    section_at : M
        X-coordinate on the beam (distance from start node) where the result is located [m].
    index : int
        Sequential index of the section on the beam, starting at 1 and proceeding from start to end.
        Helps distinguish values on left versus right side of a section at the same location.
    n : KN
        Normal force value [kN].
    vy : KN
        Shear force in Y-axis direction [kN].
    vz : KN
        Shear force in Z-axis direction [kN].
    mx : KNM
        Torsional moment around X-axis [kNm].
    my : KNM
        Bending moment around Y-axis [kNm].
    mz : KNM
        Bending moment around Z-axis [kNm].

    Raises
    ------
    ValueError
        If result_on = ResultOn.ON_BEAM but member is empty.
        If result_on = ResultOn.ON_RIB but member_rib is empty.
        If result_for = ResultFor.LOAD_CASE but load_case is empty.
        If result_for = ResultFor.LOAD_COMBINATION but load_combination is empty.
        If index < 1.
    """

    result_on: ResultOn
    result_for: ResultFor
    member: str = ""
    member_rib: str = ""
    load_case: str = ""
    load_combination: str = ""
    combination_key: str = ""
    section_at: M = 0
    index: int = 1
    n: KN = 0
    vy: KN = 0
    vz: KN = 0
    mx: KNM = 0
    my: KNM = 0
    mz: KNM = 0

    def __post_init__(self) -> None:
        """Validate conditional requirements based on SAF specification.

        Raises
        ------
        ValueError
            If conditional requirements are not satisfied.
        """
        if self.result_on == ResultOn.ON_BEAM and not self.member:
            raise ValueError("member must be specified when result_on = ResultOn.ON_BEAM")
        if self.result_on == ResultOn.ON_RIB and not self.member_rib:
            raise ValueError("member_rib must be specified when result_on = ResultOn.ON_RIB")
        if self.result_for == ResultFor.LOAD_CASE and not self.load_case:
            raise ValueError("load_case must be specified when result_for = ResultFor.LOAD_CASE")
        if self.result_for == ResultFor.LOAD_COMBINATION and not self.load_combination:
            raise ValueError("load_combination must be specified when result_for = ResultFor.LOAD_COMBINATION")
        if self.index < 1:
            raise ValueError("index must be >= 1 (SAF specification requires index >= 1)")
