from dataclasses import dataclass
from blueprints.type_alias import KN, KNM


@dataclass
class ResultInternalForces1D():
    """
    Represents internal forces in 1D structural analysis.

    The x-axis defines the local 1D member axis.
    The y and z-axis are perpendicular with the x-axis according to right-hand rule

    Attributes:
    ----------
    n : KN
        Axial force. (negative is compression)
    v_y : KN
        Shear force in the y-direction.
    v_z : KN
        Shear force in the z-direction.
    m_x : KNM
        Bending moment around the x-axis. 
        Positive is from Y to Z
    m_y : KNM
        Bending moment around the y-axis.
        Positive is from X to Z (positive moment gives compression in Z-positive domain)
        Deviates from right-hand rule
    m_z : KNM
        Bending moment around the z-axis.
        Positive is from X to Y
    """
    n: KN = 0
    v_y: KN = 0
    v_z: KN = 0
    m_x: KNM = 0
    m_y: KNM = 0
    m_z: KNM = 0
