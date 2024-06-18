
from dataclasses import dataclass

from blueprints.type_alias import KN, KNM


@dataclass
class ResultNodalReaction():
    """
    Represents Nodal Reaction in 1D structural analysis.

    The x-axis defines the local 1D member axis.
    The y and z-axis are perpendicular with the x-axis according to right-hand rule

    Attributes:
    ----------
    r_x : KN
        Axial force. (negative is compression)
    r_y : KN
        Shear force in the y-direction.
    r_z : KN
        Shear force in the z-direction.
    m_x : KNM
        Bending moment around the x-axis. 
        Positive is from Y to Z
    m_y : KNM
        Bending moment around the y-axis.
        Positive is from Z to X
    m_z : KNM
        Bending moment around the z-axis.
        Positive is from X to Y
    """
    r_x: KN = 0
    r_y: KN = 0
    r_z: KN = 0
    m_x: KNM = 0
    m_y: KNM = 0
    m_z: KNM = 0
