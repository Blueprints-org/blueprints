"""Resultant internal forces on edge of 2D member used for strength or stability checks.

Internal forces on edge of 2D member. Result in member axis (not in principal axis).
"""

from dataclasses import dataclass
from enum import Enum

from blueprints.saf.results.result_internal_force_1d import ResultFor
from blueprints.type_alias import KN_M, KNM_M, M


class ResultOn2DEdge(str, Enum):
    """Enumeration for where the internal force result is located on 2D member.

    Following SAF standard specification for ResultInternalForce2DEdge.
    """

    ON_EDGE = "On edge"


@dataclass(frozen=True)
class ResultInternalForce2DEdge:
    """Resultant internal forces on edge of 2D member.

    Definition following https://www.saf.guide/en/stable/results/resultinternalforce2dedge.html.

    Internal forces on edge of 2D member. All forces and moments are per unit length.
    Results are expressed in the member's coordinate system.

    Coordinate System:
    The coordinate system is aligned with the 2D member's local axes where forces and
    moments are reported per unit length along the edge.

    Attributes
    ----------
    result_on : ResultOn2DEdge
        Specifies the object type where the result is located.
        - "On edge": Result on a 2D member edge (required, currently only supported option)
    member_2d : str
        Reference to the name of the 2D member (StructuralSurfaceMember).
        Required field.
    edge : int
        Index of the edge on the 2D member, starting at 1 and ordered per member's edges property.
        Required field.
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
        X-coordinate (distance from edge start node) where the result is located [m].
    index : int
        Sequential index of the section on the edge, starting at 1 and proceeding from start to end.
        Helps distinguish values on left versus right side of a section at the same location.
    mx : KNM_M
        Bending moment value [kNm/m].
    my : KNM_M
        Bending moment value [kNm/m].
    mxy : KNM_M
        Torsional moment value [kNm/m].
    vx : KN_M
        Shear force value [kN/m].
    vy : KN_M
        Shear force value [kN/m].
    nx : KN_M
        Membrane force value [kN/m].
    ny : KN_M
        Membrane force value [kN/m].
    nxy : KN_M
        Shear force value [kN/m].

    Raises
    ------
    ValueError
        If result_for = ResultFor.LOAD_CASE but load_case is empty.
        If result_for = ResultFor.LOAD_COMBINATION but load_combination is empty.
        If edge < 1.
        If index < 1.
    """

    result_on: ResultOn2DEdge
    result_for: ResultFor
    member_2d: str = ""
    edge: int = 0
    load_case: str = ""
    load_combination: str = ""
    combination_key: str = ""
    section_at: M = 0
    index: int = 1
    mx: KNM_M = 0
    my: KNM_M = 0
    mxy: KNM_M = 0
    vx: KN_M = 0
    vy: KN_M = 0
    nx: KN_M = 0
    ny: KN_M = 0
    nxy: KN_M = 0

    def __post_init__(self) -> None:
        """Validate conditional requirements based on SAF specification.

        Raises
        ------
        ValueError
            If conditional requirements are not satisfied.
        """
        if not self.member_2d:
            raise ValueError("member_2d must be specified")
        if self.edge < 1:
            raise ValueError("edge must be >= 1 (SAF specification requires edge >= 1)")
        if self.result_for == ResultFor.LOAD_CASE and not self.load_case:
            raise ValueError("load_case must be specified when result_for = ResultFor.LOAD_CASE")
        if self.result_for == ResultFor.LOAD_COMBINATION and not self.load_combination:
            raise ValueError("load_combination must be specified when result_for = ResultFor.LOAD_COMBINATION")
        if self.index < 1:
            raise ValueError("index must be >= 1 (SAF specification requires index >= 1)")
